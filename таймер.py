import math
from tkinter import *

import pygame
import time
pygame.mixer.init()

is_limit_of_what = 'hours'
timer_flag_clicked_enter = False
timer_flag_paused = False
flag_of_position_one_hour_entry_cursor = False
flag_of_position_one_minute_entry_cursor = False
flag_of_position_one_second_entry_cursor = False
flag_of_place_of_the_mouse_cursor = 0

timer_window = Tk()
timer_window['bg'] = 'light yellow'
timer_window.geometry('500x250+350+300')
timer_window.title('таймер')
timer_window.iconbitmap('timer.ico')
timer_window.resizable(width=False, height=False)
timer_window.attributes('-topmost', True)

entry_hours = Entry(timer_window, fg='red', bg='light yellow',
                    font=('Arial', 70, 'bold'), borderwidth=2)
entry_hours.place(x=35, y=30, width=120, height=80)
entry_hours.focus_set()
entry_minutes = Entry(timer_window, fg='red', bg='light yellow',
                      font=('Arial', 70, 'bold'), borderwidth=2)
entry_minutes.place(x=190, y=30, width=120, height=80)
entry_seconds = Entry(timer_window, fg='red', bg='light yellow',
                      font=('Arial', 70, 'bold'), borderwidth=2)
entry_seconds.place(x=345, y=30, width=120, height=80)
label_hours = Label(timer_window, fg='red', bg='light yellow',
                    font=('Arial', 20, 'bold'), text='часы')
label_hours.place(x=35, y=110, width=120, height=30)
label_minutes = Label(timer_window, fg='red', bg='light yellow',
                      font=('Arial', 20, 'bold'), text='минуты')
label_minutes.place(x=190, y=110, width=120, height=30)
label_seconds = Label(timer_window, fg='red', bg='light yellow',
                      font=('Arial', 20, 'bold'), text='секунды')
label_seconds.place(x=345, y=110, width=120, height=30)
label_between_hours_and_minutes = Label(timer_window, fg='red', bg='light yellow',
                                        font=('Arial', 70, 'bold'), text=':')
label_between_hours_and_minutes.place(x=155, y=24, width=35, height=80)
label_between_minutes_and_seconds = Label(timer_window, fg='red', bg='light yellow',
                                          font=('Arial', 70, 'bold'), text=':')
label_between_minutes_and_seconds.place(x=310, y=24, width=35, height=80)


def focus_on_hours(self):
    global is_limit_of_what, flag_of_place_of_the_mouse_cursor
    global flag_of_position_one_hour_entry_cursor
    is_limit_of_what = 'hours'
    flag_of_place_of_the_mouse_cursor = 0
    if entry_hours.index('insert') == 1:
        flag_of_position_one_hour_entry_cursor = True


def focus_on_minutes(self):
    global is_limit_of_what, flag_of_place_of_the_mouse_cursor
    global flag_of_position_one_minute_entry_cursor
    is_limit_of_what = 'minutes'
    flag_of_place_of_the_mouse_cursor = 1
    if entry_minutes.index('insert') == 1:
        flag_of_position_one_minute_entry_cursor = True


def focus_on_seconds(self):
    global is_limit_of_what, flag_of_place_of_the_mouse_cursor
    global flag_of_position_one_second_entry_cursor
    is_limit_of_what = 'seconds'
    flag_of_place_of_the_mouse_cursor = 2
    if entry_seconds.index('insert') == 1:
        flag_of_position_one_second_entry_cursor = True


def timer_limit(timer_keyboard):
    global is_limit_of_what, flag_of_place_of_the_mouse_cursor, flag_of_position_one_hour_entry_cursor
    global flag_of_position_one_minute_entry_cursor, flag_of_position_one_second_entry_cursor

    if timer_keyboard.keysym in '0123456789':
        if flag_of_place_of_the_mouse_cursor == 2:
            if entry_seconds.index('insert') == 1:
                flag_of_position_one_second_entry_cursor = True
            else:
                flag_of_position_one_second_entry_cursor = False
        elif flag_of_place_of_the_mouse_cursor == 1:
            if entry_minutes.index('insert') == 1:
                flag_of_position_one_minute_entry_cursor = True
            else:
                flag_of_position_one_minute_entry_cursor = False
        else:
            if entry_hours.index('insert') == 1:
                flag_of_position_one_hour_entry_cursor = True
            else:
                flag_of_position_one_hour_entry_cursor = False
        if is_limit_of_what == 'hours' and (entry_hours.get() == '' or len(entry_hours.get()) > 2):
            entry_hours.delete(entry_hours.index('insert') - 1)
        if is_limit_of_what == 'minutes' and (entry_minutes.get() == '' or int(entry_minutes.get()) > 59 or
                                              len(entry_minutes.get()) > 2):
            entry_minutes.delete(entry_minutes.index('insert') - 1)
        if is_limit_of_what == 'seconds' and (entry_seconds.get() == '' or int(entry_seconds.get()) > 59 or
                                              len(entry_seconds.get()) > 2):
            entry_seconds.delete(entry_seconds.index('insert') - 1)
    elif timer_keyboard.keysym == 'BackSpace':
        pass
    elif timer_keyboard.keysym == 'Return':
        if timer_flag_clicked_enter:
            pass
        else:
            timer_start_tick()
    elif timer_keyboard.keysym == 'Right':
        if flag_of_place_of_the_mouse_cursor == 2:
            if entry_seconds.index('insert') == 1:
                flag_of_position_one_second_entry_cursor = True
        elif flag_of_place_of_the_mouse_cursor == 1:
            if entry_minutes.index('insert') == len(entry_minutes.get()):
                if not flag_of_position_one_minute_entry_cursor:
                    entry_seconds.focus_set()
                    entry_seconds.icursor(0)
                    flag_of_place_of_the_mouse_cursor = 2
                else:
                    flag_of_position_one_minute_entry_cursor = False
            elif entry_minutes.index('insert') == 1:
                flag_of_position_one_minute_entry_cursor = True
            else:
                flag_of_position_one_minute_entry_cursor = False
        elif flag_of_place_of_the_mouse_cursor == 0:
            if entry_hours.index('insert') == len(entry_hours.get()):
                if not flag_of_position_one_hour_entry_cursor:
                    entry_minutes.focus_set()
                    entry_minutes.icursor(0)
                    flag_of_place_of_the_mouse_cursor = 1
                else:
                    flag_of_position_one_hour_entry_cursor = False
            elif entry_hours.index('insert') == 1:
                flag_of_position_one_hour_entry_cursor = True
            else:
                flag_of_position_one_hour_entry_cursor = False
        else:
            pass
    elif timer_keyboard.keysym == 'Left':
        if flag_of_place_of_the_mouse_cursor == 0:
            if entry_hours.index('insert') == 1:
                flag_of_position_one_hour_entry_cursor = True
        elif flag_of_place_of_the_mouse_cursor == 1:
            if entry_minutes.index('insert') == 0:
                if not flag_of_position_one_minute_entry_cursor:
                    entry_hours.focus_set()
                    entry_hours.icursor(2)
                    flag_of_place_of_the_mouse_cursor = 0
                else:
                    flag_of_position_one_minute_entry_cursor = False
            elif entry_minutes.index('insert') == 1:
                flag_of_position_one_minute_entry_cursor = True
            else:
                flag_of_position_one_minute_entry_cursor = False
        elif flag_of_place_of_the_mouse_cursor == 2:
            if entry_seconds.index('insert') == 0:
                if not flag_of_position_one_second_entry_cursor:
                    entry_minutes.focus_set()
                    entry_minutes.icursor(2)
                    flag_of_place_of_the_mouse_cursor = 1
                else:
                    flag_of_position_one_second_entry_cursor = False
            elif entry_seconds.index('insert') == 1:
                flag_of_position_one_second_entry_cursor = True
            else:
                flag_of_position_one_second_entry_cursor = False
        else:
            pass
    elif timer_keyboard.keysym == 'Up':
        pass
    else:
        if is_limit_of_what == 'hours':
            entry_hours.delete(entry_hours.index('insert') - 1)
        if is_limit_of_what == 'minutes':
            entry_minutes.delete(entry_minutes.index('insert') - 1)
        if is_limit_of_what == 'seconds':
            entry_seconds.delete(entry_seconds.index('insert') - 1)


entry_hours.bind('<FocusIn>', focus_on_hours)
entry_minutes.bind('<FocusIn>', focus_on_minutes)
entry_seconds.bind('<FocusIn>', focus_on_seconds)
timer_window.bind('<Key>', timer_limit)


def timer_tick():
    global static_number_of_seconds, progress_bar_of_timer, time_ding_dong, number_of_seconds, timer_flag_paused
    global starter_of_timer_ticking, stopper_of_timer, time_ding_dong
    if timer_flag_paused:
        timer_window.after(900, timer_tick)
    elif number_of_seconds != time_ding_dong - int(time.time()):
        if number_of_seconds >= 0:
            if static_number_of_seconds == 0:
                progress_bar_of_timer.configure(width=0)
            else:
                progress_bar_of_timer.configure(width=int(number_of_seconds / static_number_of_seconds * 400))
            if static_number_of_seconds == 0 or number_of_seconds == 0:
                progress_bar_of_timer.configure(bg='#ff0000')
                percent_of_time_left.configure(fg='#ff0000')
                percent_of_time_left.config(text='0%')
            else:
                percent_of_time_left.config(text=str(int(
                    math.ceil(number_of_seconds / static_number_of_seconds * 100))) + '%')
                fraction_multiplied_512 = int(number_of_seconds / static_number_of_seconds * 512 - 1)
                if fraction_multiplied_512 > 255:
                    hex_color_code = '#' + '0' * (2 - len(hex(511 - fraction_multiplied_512)[2:])) + \
                                     hex(511 - fraction_multiplied_512)[2:] + 'ff00'
                    progress_bar_of_timer.configure(bg=hex_color_code)
                    percent_of_time_left.configure(fg=hex_color_code)
                elif fraction_multiplied_512 == 255:
                    hex_color_code = '#ffff00'
                    progress_bar_of_timer.configure(bg=hex_color_code)
                    percent_of_time_left.configure(fg=hex_color_code)
                else:
                    hex_color_code = '#' + 'ff' + '0' * (2 - len(hex(int(fraction_multiplied_512))[2:])) + \
                                     hex(int(fraction_multiplied_512))[2:] + '00'
                    progress_bar_of_timer.configure(bg=hex_color_code)
                    percent_of_time_left.configure(fg=hex_color_code)
            if number_of_seconds == 3602:
                pygame.mixer.music.load("музыка окончания таймера/Остался 1 час.mp3")
                pygame.mixer.music.play(1)
            if number_of_seconds == 1802:
                pygame.mixer.music.load("музыка окончания таймера/Осталось 30 минут.mp3")
                pygame.mixer.music.play(1)
            if number_of_seconds == 602:
                pygame.mixer.music.load("музыка окончания таймера/Осталось 10 минут.mp3")
                pygame.mixer.music.play(1)
            if number_of_seconds == 302:
                pygame.mixer.music.load("музыка окончания таймера/Осталось 5 минут.mp3")
                pygame.mixer.music.play(1)
            if number_of_seconds == 62:
                pygame.mixer.music.load("музыка окончания таймера/Осталась 1 минута.mp3")
                pygame.mixer.music.play(1)
            entry_hours.delete(0, END)
            entry_minutes.delete(0, END)
            entry_seconds.delete(0, END)
            entry_hours.insert(END, '0' * (2 - len(str(number_of_seconds // 3600))) + str(number_of_seconds // 3600))
            entry_minutes.insert(END, '0' * (2 - len(str((number_of_seconds % 3600) // 60))) +
                                 str((number_of_seconds % 3600) // 60))
            entry_seconds.insert(END, '0' * (2 - len(str(number_of_seconds % 60))) + str(number_of_seconds % 60))
            number_of_seconds = time_ding_dong - int(time.time())
            timer_window.after(900, timer_tick)
        elif number_of_seconds == -1:
            timer_window.deiconify()
            pygame.mixer.music.load("музыка окончания таймера/LindErebros-CloudsHeaven.mp3")
            pygame.mixer.music.play(-1)
            starter_of_timer_ticking = Button(timer_window, text='запустить таймер', fg='red', bg='light yellow',
                                              font=('Arial', 16, 'bold'), command=timer_start_tick)
            starter_of_timer_ticking.place(x=20, y=150, width=220, height=30)
        else:
            pass
    else:
        timer_window.after(100, timer_tick)


def pause_click():
    global timer_flag_paused, pause_button_of_timer, unpause_button_of_timer, time_ding_dong, number_of_seconds
    if not timer_flag_paused:
        pause_button_of_timer.destroy()
        unpause_button_of_timer = Button(timer_window, text='продолжить отсчёт', fg='red', bg='light yellow',
                                         font=('Arial', 16, 'bold'), command=pause_click)
        unpause_button_of_timer.place(x=20, y=150, width=220, height=30)
    else:
        pause_button_of_timer = Button(timer_window, text='остановить таймер', fg='red', bg='light yellow',
                                       font=('Arial', 16, 'bold'), command=pause_click)
        pause_button_of_timer.place(x=20, y=150, width=220, height=30)
        unpause_button_of_timer.destroy()
        time_ding_dong = int(time.time()) + number_of_seconds
    timer_flag_paused = not timer_flag_paused



def timer_start_tick():
    pygame.mixer.music.stop()
    global entry_hours, entry_minutes, entry_seconds, starter_of_timer_ticking, stopper_of_timer
    global time_ding_dong, number_of_seconds, static_number_of_seconds, pause_button_of_timer
    global timer_flag_clicked_enter
    stopper_of_timer = Button(timer_window, text='выключить таймер', fg='red', bg='light yellow',
                              font=('Arial', 16, 'bold'), command=timer_stop_tick)
    stopper_of_timer.place(x=260, y=150, width=220, height=30)
    starter_of_timer_ticking.destroy()
    pause_button_of_timer = Button(timer_window, text='остановить таймер', fg='red', bg='light yellow',
                                   font=('Arial', 16, 'bold'), command=pause_click)
    pause_button_of_timer.place(x=20, y=150, width=220, height=30)
    timer_flag_clicked_enter = True
    if entry_seconds.get() == '':
        entry_seconds.insert(END, '0')
    if entry_minutes.get() == '':
        entry_minutes.insert(END, '0')
    if entry_hours.get() == '':
        entry_hours.insert(END, '0')
    static_number_of_seconds = int(entry_hours.get()) * 3600 + int(entry_minutes.get()) * 60 + int(entry_seconds.get())
    time_ding_dong = int(time.time()) + static_number_of_seconds
    number_of_seconds = static_number_of_seconds
    timer_tick()


def timer_stop_tick():
    global number_of_seconds, timer_flag_clicked_enter, starter_of_timer_ticking, stopper_of_timer
    global pause_button_of_timer, unpause_button_of_timer
    timer_flag_clicked_enter = False
    pygame.mixer.music.stop()
    entry_seconds.delete(0, END)
    entry_minutes.delete(0, END)
    entry_hours.delete(0, END)
    progress_bar_of_timer.configure(width=400, bg='#00ff00')
    percent_of_time_left.config(text='100%', fg='#00ff00')
    number_of_seconds = -2
    starter_of_timer_ticking = Button(timer_window, text='запустить таймер', fg='red', bg='light yellow',
                                      font=('Arial', 16, 'bold'), command=timer_start_tick)
    starter_of_timer_ticking.place(x=20, y=150, width=220, height=30)
    stopper_of_timer.destroy()


starter_of_timer_ticking = Button(timer_window, text='запустить таймер', fg='red', bg='light yellow',
                                  font=('Arial', 16, 'bold'), command=timer_start_tick)
starter_of_timer_ticking.place(x=20, y=150, width=220, height=30)
progress_bar_of_timer = Label(timer_window, bg='#00ff00', font=('Arial', 1), text='', width=400)
progress_bar_of_timer.place(x=80, y=200, height=30)
left_border_of_progress_bar_of_timer = Label(bg='gray')
left_border_of_progress_bar_of_timer.place(x=80, y=198, width=6, height=34)
right_border_of_progress_bar_of_timer = Label(bg='gray')
right_border_of_progress_bar_of_timer.place(x=480, y=198, width=6, height=34)
up_border_of_progress_bar_of_timer = Label(bg='gray')
up_border_of_progress_bar_of_timer.place(x=80, y=198, width=404, height=2)
down_border_of_progress_bar_of_timer = Label(bg='gray')
down_border_of_progress_bar_of_timer.place(x=80, y=230, width=404, height=2)
percent_of_time_left = Label(bg='gray', text='100%', font=('Arial', 20, 'bold'), fg='#00ff00')
percent_of_time_left.place(x=14, y=198, width=70, height=34)

timer_window.mainloop()
