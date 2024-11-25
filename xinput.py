import vgamepad
from pynput import mouse

SCREEN_X = 1919

g = vgamepad.VX360Gamepad()
def on_move(x, _):
    x = max(0, min(SCREEN_X, x))
    g.right_joystick(int((x*(65535/SCREEN_X))-32768), 0) # -32768 instead of -32767.5 because at x=0, joystick should be at -32768
    g.update()

listener = mouse.Listener(on_move = on_move)
listener.start()
listener.join()