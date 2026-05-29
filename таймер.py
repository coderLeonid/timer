import math
from tkinter import *
import ctypes

from pygame import mixer
import time
mixer.init()
music = mixer.music

key_m = (1, 5, 10, 30, 60)
LY, Y, R, G = 'light yellow', 'yellow', 'red', '#00ff00'

win = Tk()
win.title('таймер')
win.iconbitmap('timer.ico')
win['bg'] = LY

width, height = 422, 140
x, y = (win.winfo_screenwidth() - width) // 2, (win.winfo_screenheight() - height) // 2 - 70
win.geometry(f'{width}x{height}+{x}+{y}')
win.resizable(width=False, height=False)
win.attributes('-topmost', True)

h, m, s = (Entry(win, fg=R, bg=LY, font=('Arial', 70, 'bold'), borderwidth=2) for i in range(3))
t = (h, m, s)
[t[i].place(x=10 + 145 * i, y=10, width=110, height=80) for i in range(3)]
for i in range(2):
    colon = Label(win, fg=R, bg=LY, font=('Arial', 70, 'bold'), text=':')
    colon.place(x=120 + 146 * i, y=4, width=35, height=80)
    
m.focus_set()
state = 'off'


def key(k):
    global state
    focus, key = win.focus_get(), k.keysym.lower()
    if focus not in t:
        return
    
    if k.keysym == '??':
        ru_alph = 'йцукенгшщзфывапролдячсмить'
        if k.char in ru_alph:
            key = k.char.translate(str.maketrans(ru_alph, 'qwertyuiopasdfghjklzxcvbnm'))
        elif k.char in 'бю.жэхъ':
            key = ('comma', 'period', 'slash', 'semicolon', 'apostrophe', 'bracketleft', 'bracketright')['бю.жэхъ'.index(k.char)]

    key_hacks = [''] + list('qwertyuiopasdfghjkl') + ['semicolon'] + list('zxcvbnm') + ['comma', 'period', 'slash']
    # if key in 'backslash':
    if key in key_hacks:
        key_index = key_hacks.index(key)
        key = str(key_index)[-1:]

        focus.delete(focus.index(INSERT) - 1)
        new = t[(key_index - 1) // 10]
        new.icursor(len(new.get()))
        if len(new.get()) == 2:
            new.delete(0, END)
        focus = new
        focus.insert(focus.index(INSERT), key + '0' * (new == s and not new.get()))
    elif key == 'equal' and (s_time := s.get())[-1:] in ('0', ''):
        s.delete(0, END)
        s.insert(END, s_time[:-1] + '5')
    elif key in ('minus', 'space', 'colon', 'period', 'comma', 'left', 'right'):
        new = (t * 3)[t.index(focus) + 3 + (-1, 1)[key != 'left']]
        new.focus_set()
        new.icursor(len(new.get()))
    elif key == 'backspace' and focus.index(INSERT) == 0 or key == 'delete' and focus.index(INSERT) == len(focus.get()):
        new = (t * 3)[(t * 3).index(focus) + 3 + (-1, 1)[key == 'delete' and focus.index(INSERT) == len(focus.get())]]
        if new.get():
            new.focus_set()
            new.icursor((len(new.get()), 0)[key == 'delete'])
    elif key == 'grave':
        if focus.get() in ('', '`'):
            new = (t * 3)[(t * 3).index(focus) + 3 + (-1, 1)[1]]
            new.delete(0, END)
            new.focus_set()
        focus.delete(0, END)
    elif key == 'return' and state in ('on', 'off'):
        (start, stop)[state == 'on']()
    elif focus.get().isdigit() and len(focus.get()) > 2:
        if focus == h and len(m.get()) + len(s.get()) < 4 or focus == m and len(s.get()) < 2:
            new = (m, s)[focus == m]
            new.focus_set()
            new.insert(0, focus.get()[-1:])
            focus.delete(focus.index(END) - 1)
        elif focus == m and len(h.get()) < 2 or focus == s and len(m.get()) < 2:
            new = (m, h)[focus == m]
            new.focus_set()
            new.insert(END, focus.get()[:1])
            focus.delete(0)
        elif focus == s and len(m.get()) + len(h.get()) < 4:
            focus.delete(focus.index(END) - 1)
            (m, h)[len(m.get()) == 2].insert(END, s.get()[0])
        else:
            focus.delete(focus.index(INSERT) - 1)
            
            
    while not focus.get()[-1:].isdigit() and focus.get():
        focus.delete(focus.index(END) - 1)
    if key == 'space' and state in ('pause', 'on'):
        pause()
    # elif key in 'hms':
    #     new = t['hms'.index(key)]
    #     new.focus_set()
    #     new.icursor(len(new.get()))
    if k.keysym == '??':
        return 'break'


def tick():
    global static_num_of_s, progress_bar, time_ding_dong, num_of_s, state, btn, stopper
    if state == 'pause':
        win.after(900, tick)
    elif num_of_s != time_ding_dong - int(time.time()):
        if num_of_s >= 0:
            if static_num_of_s == 0:
                progress_bar.config(width=0)
            else:
                progress_bar.config(width=int(num_of_s / static_num_of_s * 400))
            if static_num_of_s == 0 or num_of_s == 0:
                progress_bar.config(bg=R)
                percent_of_time_left.config(fg=R)
                percent_of_time_left.config(text='0%')
            else:
                percent_of_time_left.config(text=str(int(math.ceil(num_of_s / static_num_of_s * 100))) + '%')
                fraction_multiplied_512 = int(num_of_s / static_num_of_s * 512 - 1)
                if fraction_multiplied_512 > 255:
                    hex_color_code = '#' + '0' * (2 - len(hex(511 - fraction_multiplied_512)[2:])) + hex(511 - fraction_multiplied_512)[2:] + 'ff00'
                elif fraction_multiplied_512 == 255:
                    hex_color_code = Y
                else:
                    hex_color_code = '#' + 'ff' + '0' * (2 - len(hex(int(fraction_multiplied_512))[2:])) + hex(int(fraction_multiplied_512))[2:] + '00'
                progress_bar.config(bg=hex_color_code)
                percent_of_time_left.config(fg=hex_color_code)
            if num_of_s in (60 * i + 2 for i in key_m):
                music.load(f'звук/{num_of_s // 60}m.mp3')
                music.play(1)
            [i.delete(0, END) for i in (h, m, s)]
            [t[i].insert(END, str((num_of_s // 3600, (num_of_s % 3600) // 60, num_of_s % 60)[i]).rjust(2, '0')) for i in range(3)]
            num_of_s = time_ding_dong - int(time.time())
            win.after(900, tick)
        elif num_of_s == -1:
            win.deiconify()
            music.load("звук/LindErebros-CloudsHeaven.mp3")
            music.play(-1)
            btn.config(text='запустить')
            btn.config(command=start)
    else:
        win.after(100, tick)


def pause():
    global state, time_ding_dong, num_of_s, btn
    if state != 'pause':
        btn.config(text='далее')
    else:
        btn.config(text='пауза')
        time_ding_dong = int(time.time()) + num_of_s
    state = ('on', 'pause')[state != 'pause']


def start():
    music.stop()
    global btn, stopper, state, time_ding_dong, num_of_s, static_num_of_s
    stopper = Button(win, text='сбросить', fg=R, bg=LY, font=('Arial', 16, 'bold'), command=stop)
    stopper.place(x=140, y=100, width=120, height=30)
    btn.config(text='пауза')
    btn.config(command=pause)
    state = 'on'
    static_num_of_s = int(f'0{h.get()}') * 3600 + int(f'0{m.get()}') * 60 + int(f'0{s.get()}')
    if static_num_of_s == 0:
        static_num_of_s = 300
    time_ding_dong = int(time.time()) + static_num_of_s
    num_of_s = static_num_of_s
    tick()


def stop():
    global num_of_s, state, btn, stopper
    state = 'off'
    music.stop()
    [i.delete(0, END) for i in (h, m, s)]
    progress_bar.config(width=400, bg=G)
    percent_of_time_left.config(text='100%', fg=G)
    num_of_s = -2
    btn = Button(win, text='запустить', fg=R, bg=LY, font=('Arial', 16, 'bold'), command=start)
    btn.place(x=10, y=100, width=120, height=30)
    stopper.destroy()
    m.focus_set()


win.bind('<Key>', key)
win.bind('<Escape>', lambda x: win.destroy())

canvas = Canvas(win, width=420, height=50, bg=LY)
canvas.place(x=380, y=198)
canvas.create_rectangle(10, 10, 410, 40, outline='gray')

btn = Button(win, text='запустить', fg=R, bg=LY, font=('Arial', 16, 'bold'), command=start)
btn.place(x=10, y=100, width=120, height=30)
progress_bar = Label(win, bg=G, font=('Arial', 1), text='', width=400)
progress_bar.place(x=80, y=250, height=30)

percent_of_time_left = Label(bg='gray', text='100%', font=('Arial', 20, 'bold'), fg=G)
percent_of_time_left.place(x=270, y=100, width=70, height=30)

win.mainloop()
