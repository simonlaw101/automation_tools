import os
from pynput import mouse, keyboard
from pynput.keyboard import Key
from pynput.mouse import Button

#Setting
keys = {'record': Key.esc,
        'delay': Key.num_lock,
        'loop': Key.f2,
        'stop_program': Key.num_lock}

filename = 'script.pyw'
delay_sec = 1
loop_times = 5

#Instruction
def format_key(key):
    return str(key).replace('Key.','').replace('_',' ').title()

descriptions = {'record': 'Start/Stop recording',
               'delay': f'Delay {str(delay_sec)} second',
               'loop': 'Start/End looping'}

instruction = '[Instruction]'.center(32) + '\n\n'
for desc_key, desc_val in descriptions.items():
    instruction += '{0:<12}: {1}\n\n'.format(format_key(keys[desc_key]), desc_val)

#Script
script = ('import os\n'
          'import time\n'
          'import pynput\n'
          'from  pynput.keyboard import Key\n'
          'from  pynput.mouse import Button\n'
          'def on_press(key):\n'
          f'    if key == {keys["stop_program"]}:\n'
          '        os._exit(0)\n'
          'keyboard_listener = pynput.keyboard.Listener(on_press=on_press)\n'
          'keyboard_listener.start()\n'
          'mouse = pynput.mouse.Controller()\n'
          'keyboard = pynput.keyboard.Controller()\n')

scripts = {'click': 'mouse.position = {coord}\n{tab}mouse.click({button})\n',
           'press': 'keyboard.press({key})\n',
           'release': 'keyboard.release({key})\n',
           'scroll': 'mouse.scroll(0,{dy})\n',
           'delay': 'time.sleep({sec})\n',
           'start_loop': 'for i in range({times}):\n'}

printout = {'click': '{left_or_right} click at {coord}',
            'press': 'Press {format_key}',
            'scroll': 'Scroll {up_or_down}',
            'delay': 'Delay {sec} second',
            'start_loop': 'Looping {times} times start...',
            'end_loop': 'Looping end...'}

def write_script(dict_):
    global script, start_loop
    action = dict_['action']
    if action in printout.keys():
        print(('    ' if start_loop else '') + printout[action].format(**dict_))
    if action in scripts.keys():
        script += ('    ' if start_loop else '') + scripts[action].format(**dict_)

def save_script():
    global script
    open(filename,'a').close()
    with open(filename,'w') as file:
        file.write(script)
        dir_name = os.path.dirname(os.path.realpath(__file__))
        print('\nAutomated script generated at',os.path.join(dir_name,filename))
        print('Note that you may terminate the running script by pressing',format_key(keys['stop_program']),':)')

#Mouse and Key event
def on_click(x, y, button, pressed):
    global start_loop
    if pressed:
        left_or_right = 'Left' if button==Button.left else 'Right'
        tab = '    ' if start_loop else ''
        write_script({'action': 'click', 'left_or_right': left_or_right, 'coord': (x,y), 'tab': tab, 'button': button})

def on_scroll(x, y, dx, dy):
    up_or_down = 'down' if dy < 0 else 'up'
    write_script({'action': 'scroll', 'up_or_down': up_or_down, 'dy': str(dy*120)})

def on_press(key):
    global start_record
    if start_record and key not in keys.values():
        write_script({'action': 'press', 'key': key, 'format_key': format_key(key)})
            
def on_release(key):
    global start_record, start_loop
    if key == keys['record']:
        if not mouse_listener.running:
            mouse_listener.start()
            start_record = True
            print('\nStart recording...\n')
        else:
            mouse_listener.stop()
            print('\nStop recording...')
            save_script()
            return False
    elif start_record:
        if key == keys['delay']:
            write_script({'action': 'delay', 'sec': str(delay_sec)})
        elif key == keys['loop']:
            if start_loop:
                start_loop = False
                write_script({'action': 'end_loop'})
            else:
                write_script({'action': 'start_loop', 'times': str(loop_times)})
                start_loop = True
        else:
            write_script({'action': 'release', 'key': key})

#Start recorder
start_record = False
start_loop = False
print(instruction)
mouse_listener = mouse.Listener(on_click=on_click,on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press,on_release=on_release)
keyboard_listener.start()
