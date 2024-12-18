import vgamepad # https://github.com/yannbouteiller/vgamepad/
from pynput import mouse, keyboard # https://pynput.readthedocs.io/en/stable/
import time

# Fixes inconsistent coordinate scaling on Windows
# https://pynput.readthedocs.io/en/stable/mouse.html#ensuring-consistent-coordinates-between-listener-and-controller-on-windows
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)


# Screen width in pixels
# Since indexing starts at 0, this is the usual value minus 1
SCREEN_WIDTH = 2559

# Number of pixels mouse pointer should move to produce a maximum joystick tilt
# Larger values = less sensitive, smaller values = more sensitive
# Shouldn't exceed half of SCREEN_WIDTH, otherwise you won't be able to produce maximum joystick tilts
SENSITIVITY = 500

# (mouse, keyboard) buttons to reset current mouse pointer position to zero joystick tilt
# This will reposition the mouse pointer if any part of its range of positions that produce joystick tilts clips the edge of the screen
RESET_BUTTON = mouse.Button.right, 'r'

# Seconds to wait before registering the RESET_BUTTON
# Only happens when the keyboard RESET_BUTTON is pressed; the mouse RESET_BUTTON registers instantly
# For Trackmania 2020, the start countdown is 1.5 seconds; this setting allows steering to reset to 0 exactly when the countdown ends
RESET_DELAY = 1.5

# Mouse button to toggle pause this script
PAUSE_BUTTON = mouse.Button.middle


neutral = SCREEN_WIDTH // 2
pause = False
gamepad = vgamepad.VX360Gamepad()
mouse_controller = mouse.Controller()

def on_move(x, y):
    if not pause:
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
        
        gamepad.left_joystick(joystick_tilt, 0)
        gamepad.update()

def reset(x, y):
    if not pause:
        global neutral
        neutral = max(SENSITIVITY, min(SCREEN_WIDTH - SENSITIVITY, x))
        mouse_controller.position = (neutral, y)

def on_click(x, y, button, pressed):
    if pressed:
        if button == RESET_BUTTON[0]:
            reset(x, y)
        if button == PAUSE_BUTTON:
            global pause
            pause = not pause
            if pause:
                gamepad.left_joystick(0, 0)
                gamepad.update()
            else:
                reset(x, y)

def on_press(key):
    if str(key) == f"'{RESET_BUTTON[1]}'":
        time.sleep(RESET_DELAY)
        reset(*mouse_controller.position)

mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
mouse_listener.start()
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

mouse_listener.join()
keyboard_listener.join()
