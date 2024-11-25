import vgamepad # https://github.com/yannbouteiller/vgamepad/
from pynput.mouse import Button, Controller, Listener # https://pynput.readthedocs.io/en/stable/

# Fixes inconsistent coordinate scaling on Windows
# https://pynput.readthedocs.io/en/stable/mouse.html#ensuring-consistent-coordinates-between-listener-and-controller-on-windows
import ctypes
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)


# Screen width in pixels
# Since indexing starts at 0, this is the usual value minus 1
SCREEN_WIDTH = 1919

# Number of pixels mouse pointer should move to produce a maximum joystick tilt
# Larger values = less sensitive, smaller values = more sensitive
# Shouldn't exceed half of SCREEN_WIDTH, otherwise you won't be able to produce maximum joystick tilts
SENSITIVITY = 200

# Mouse button to reset current mouse pointer position to zero joystick tilt
# This will reposition the mouse pointer if any part of its range of positions that produce joystick tilts clips the edge of the screen
RESET_BUTTON = Button.right


neutral = round(SCREEN_WIDTH / 2)
gamepad = vgamepad.VX360Gamepad()

def on_move(x, y):
    x = max(0, min(SCREEN_WIDTH, x))

    global neutral
    if abs(x - neutral) < SENSITIVITY:
        joystick_tilt = round(((x - neutral) * 65535) / (SENSITIVITY * 2))
    else:
        if x < neutral:
            neutral = x + SENSITIVITY
            joystick_tilt = -32768
        elif x > neutral:
            neutral = x - SENSITIVITY
            joystick_tilt = 32767
    
    gamepad.right_joystick(joystick_tilt, 0)
    gamepad.update()

def on_click(x, y, button, pressed):
    global neutral
    if button == RESET_BUTTON and pressed == True:
        neutral = max(SENSITIVITY, min(SCREEN_WIDTH - SENSITIVITY, x))
        mouse = Controller()
        mouse.position = (neutral, y)

listener = Listener(
    on_move=on_move,
    on_click=on_click)
listener.start()
listener.join()
