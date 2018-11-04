from pynput import mouse, keyboard

start_record = False
delay_sec = 1
filename = 'script.py'
script = ('import time\n'
    'import pynput.keyboard\n'
    'import pynput.mouse\n'
    'from  pynput.keyboard import Key\n'
    'from  pynput.mouse import Button\n'
    'mouse = pynput.mouse.Controller()\n'
    'keyboard = pynput.keyboard.Controller()\n')

def generate_script():
    global script
    open(filename,'a').close()
    with open(filename,'w') as file:
        file.write(script)
        print(filename,'created at current directory')

def on_click(x, y, button, pressed):
    global script
    if pressed:
        print('Mouse','left' if button==mouse.Button.left else 'right','clicked at',(x,y))
        script += 'mouse.position = {}\nmouse.click({})\n'.format((x,y),button)

def on_scroll(x, y, dx, dy):
    global script
    print('Scrolled {}'.format('down' if dy < 0 else 'up'))
    script += 'mouse.scroll(0,{})\n'.format(str(dy*120))
    
mouse_listener = mouse.Listener(on_click=on_click,on_scroll=on_scroll)

def on_press(key):
    global start_record, script
    if start_record:
        if key != keyboard.Key.esc and key != keyboard.Key.num_lock:
            script += "keyboard.press({0})\n".format(key)
            
def on_release(key):
    global start_record, script
    if key == keyboard.Key.esc:
        if not mouse_listener.running:
            mouse_listener.start()
            start_record = True
            print('\nStart recording...\n')
        else:
            mouse_listener.stop()
            print('\nStop recording...')
            generate_script()
            return False
    elif start_record:
        if key == keyboard.Key.num_lock:
            print('Delay',str(delay_sec),'second')
            script += "time.sleep({})\n".format(str(delay_sec))
        else:
            print('Pressed key',key)
            script += "keyboard.release({0})\n".format(key)

print('Start/Stop recorder by pressing Escape key\nDelay',str(delay_sec),'second by pressing Num Lock\n')
keyboard_listener = keyboard.Listener(on_press=on_press,on_release=on_release)
keyboard_listener.start()
