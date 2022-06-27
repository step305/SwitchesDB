import tkinter
from tkinter import messagebox
from fontTools.ttLib import TTFont
import switch_db
import Switch

import Switch

WINDOW_SIZE = (640, 480)
BUTTON_SIZE = (150, 100)
INPUT_FIELD_SIZE = (250, 50)
INPUT_FIELDS_TITLES = ('Серийный номер',
                       'Сопротивление\nв замкнутом состоянии',
                       'Сопротивление\nв разомкнутом состоянии',
                       'Порог срабатывания'
                       )

window = tkinter.Tk()
add_new_record_button = None
input_fields = None
db = switch_db.SwitchDB()


def center(window_instance):
    window_instance.update_idletasks()

    screen_width = window_instance.winfo_screenwidth()
    screen_height = window_instance.winfo_screenheight()

    size = tuple(int(_) for _ in window_instance.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

    window_instance.geometry("+%d+%d" % (x, y))
    window_instance.title("Centered!")


def add_new_record(entries):
    try:
        not_empty_fields = True
        for field in entries:
            not_empty_fields = not_empty_fields and not not field.get()
        if not_empty_fields:
            switch = Switch.Switch(switch_id=entries[0].get(),
                                   r_on=float(entries[1].get()),
                                   r_off=float(entries[2].get()),
                                   threshold=float(entries[3].get()))
            db.add(switch)
            messagebox.showinfo('Добавление новой записи', 'Добавлен ключ №{}'.format(entries[0].get()))
    except Exception as error:
        messagebox.showerror('Ошибка!', str(error))


def enter_callback(event):
    act_widget = window.focus_get()
    if act_widget == input_fields[0]:
        sw = db.get(input_fields[0].get())
        if sw:
            input_fields[1].delete(0, tkinter.END)
            input_fields[1].insert(0, '{:.2f}'.format(sw.r_on))
            input_fields[2].delete(0, tkinter.END)
            input_fields[2].insert(0, '{:.2f}'.format(sw.r_off))
            input_fields[3].delete(0, tkinter.END)
            input_fields[3].insert(0, '{:.2f}'.format(sw.threshold))
        input_fields[1].focus_set()
    elif act_widget == input_fields[1]:
        input_fields[2].focus_set()
    elif act_widget == input_fields[2]:
        input_fields[3].focus_set()
    elif act_widget == input_fields[3]:
        add_new_record_button.focus_set()
    elif act_widget == add_new_record_button:
        input_fields[0].focus_set()
        add_new_record(input_fields)


def close_callback():
    global db
    del db
    window.destroy()


if __name__ == '__main__':
    gost_font = TTFont('fonts\\GOST2304_TypeB.ttf')
    window.title('Тестирование ключей КМГ-2')
    window.geometry('{}x{}'.format(WINDOW_SIZE[0], WINDOW_SIZE[1]))
    center(window)
    window.resizable = False

    input_fields_labels = []
    input_fields = []

    for i in range(len(INPUT_FIELDS_TITLES)):
        y = 45 + i * INPUT_FIELD_SIZE[1] + 5
        label = tkinter.Label(window, text=INPUT_FIELDS_TITLES[i], font=(gost_font, 10))
        label.place(x=50, y=y, height=INPUT_FIELD_SIZE[1], width=INPUT_FIELD_SIZE[0])
        field = tkinter.Entry(window, bd=5, font=(gost_font, 20))
        field.place(x=WINDOW_SIZE[0] - INPUT_FIELD_SIZE[0] * 1.2, y=y,
                    height=INPUT_FIELD_SIZE[1], width=INPUT_FIELD_SIZE[0])
        input_fields_labels.append(label)
        input_fields.append(field)

    input_fields[0].focus_set()

    sw = db.get_last()
    input_fields[0].delete(0, tkinter.END)
    input_fields[0].insert(0, '{}'.format(sw.id))
    input_fields[1].delete(0, tkinter.END)
    input_fields[1].insert(0, '{:.2f}'.format(sw.r_on))
    input_fields[2].delete(0, tkinter.END)
    input_fields[2].insert(0, '{:.2f}'.format(sw.r_off))
    input_fields[3].delete(0, tkinter.END)
    input_fields[3].insert(0, '{:.2f}'.format(sw.threshold))

    add_new_record_button = tkinter.Button(window, text='Добавить', fg='Black',
                                           command=lambda: add_new_record(input_fields),
                                           bd=5, font=(gost_font, 18))
    add_new_record_button.place(x=(WINDOW_SIZE[0] - BUTTON_SIZE[0]) / 2,
                                y=WINDOW_SIZE[1] - BUTTON_SIZE[1] * 1.5,
                                height=BUTTON_SIZE[1], width=BUTTON_SIZE[0])

    window.bind('<Return>', enter_callback)
    window.protocol("WM_DELETE_WINDOW", close_callback)

    window.mainloop()
