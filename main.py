import threading
import time
import queue
import webbrowser
from flask import Flask, request, render_template, jsonify
import drivers
import clock_app
from snake_app import SnakeGame

try:
    from pyPS4Controller.controller import Controller
    _HAS_PS4 = True
except ImportError:
    _HAS_PS4 = False
    Controller = None

app = Flask(__name__)
input_queue = queue.Queue()
current_mode = "CLOCK"
game = SnakeGame()

class PS4Handler(Controller if _HAS_PS4 else object):
    def __init__(self, **kwargs):
        if _HAS_PS4:
            Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self): input_queue.put("UP")
    def on_down_arrow_press(self): input_queue.put("DOWN")
    def on_left_arrow_press(self): input_queue.put("LEFT")
    def on_right_arrow_press(self): input_queue.put("RIGHT")
    def on_x_press(self): input_queue.put("SWITCH_MODE")
    def on_options_press(self): input_queue.put("RESET")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/display')
def api_display():
    """返回当前 LED 矩阵的像素数据，供浏览器预览同步显示。"""
    return jsonify(drivers.get_display())

@app.route('/control', methods=['POST'])
def web_control():
    data = request.json or {}
    btn = data.get('btn')
    if btn:
        input_queue.put(btn)
    return {"status": "ok"}

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def run_ps4():
    if not _HAS_PS4:
        print("PS4 Controller 不可用（需 Linux），可使用 Web 遥控")
        return
    try:
        ps4 = PS4Handler(interface="/dev/input/js0", connecting_using_ds4drv=False)
        ps4.listen()
    except Exception as e:
        print(f"PS4 Controller not found: {e}")

def main_loop():
    global current_mode
    last_tick = 0
    
    while True:
        try:
            cmd = input_queue.get_nowait()
            if cmd == "SWITCH_MODE":
                current_mode = "SNAKE" if current_mode == "CLOCK" else "CLOCK"
                drivers.clear()
            elif cmd == "RESET" and current_mode == "SNAKE":
                game.reset()
            elif current_mode == "SNAKE" and cmd in ["UP", "DOWN", "LEFT", "RIGHT"]:
                mapping = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
                game.set_direction(mapping[cmd])
        except queue.Empty:
            pass

        now = time.time()
        
        if current_mode == "CLOCK":
            if now - last_tick > 1.0:
                clock_app.update()
                last_tick = now
                
        elif current_mode == "SNAKE":
            if now - last_tick > 0.2: 
                game.step() 
                game.draw()
                last_tick = now
                if not game.alive:
                    time.sleep(1)
                    game.reset()
        
        time.sleep(0.01)

if __name__ == "__main__":
    t_web = threading.Thread(target=run_flask, daemon=True)
    t_web.start()
    time.sleep(0.5)
    if drivers.MOCK_MODE:
        current_mode = "SNAKE"
        print("\n" + "="*50)
        print("  模拟模式：正在打开浏览器...")
        print("  若未自动打开，请手动访问 http://localhost:5000")
        print("="*50 + "\n")
        threading.Timer(1.5, lambda: webbrowser.open("http://localhost:5000")).start()
    
    t_ps4 = threading.Thread(target=run_ps4, daemon=True)
    t_ps4.start()
    
    try:
        main_loop()
    except KeyboardInterrupt:
        drivers.clear()
