from tkinter import *
import tkinter.tix as tix
import tkinter.ttk as ttk
import tkinter.font as tkinterfont

from resourses.constants import *
import main_window
import db_helper
import db_viewer
import datetime


def ask_date_period():
    window = Toplevel()
    window.title('Выбор периода')
    window.resizable(width=False, height=False)

    toolbar = Frame(window)
    toolbar.pack(side=BOTTOM, expand=NO, fill=BOTH)

    begin_date_frame = Frame(window)
    begin_date_frame.pack(side=LEFT, expand=YES, fill=BOTH)

    end_date_frame = Frame(window)
    end_date_frame.pack(side=RIGHT, expand=YES, fill=BOTH)

    begin_date_label = Label(begin_date_frame, text='Начало', font=ASK_DATE_DIALOG_LABEL_FONT)
    begin_date_label.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=10, pady=5)
    end_date_label = Label(end_date_frame, text='Конец', font=ASK_DATE_DIALOG_LABEL_FONT)
    end_date_label.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=10, pady=5)

    begin_day_label = Label(begin_date_frame, text='День', font=ASK_DATE_DIALOG_LABEL_FONT)
    begin_month_label = Label(begin_date_frame, text='Месяц', font=ASK_DATE_DIALOG_LABEL_FONT)
    begin_year_label = Label(begin_date_frame, text='Год', font=ASK_DATE_DIALOG_LABEL_FONT)
    begin_day_label.grid(row=1, column=0, sticky=NSEW, padx=5, pady=10)
    begin_month_label.grid(row=2, column=0, sticky=NSEW, padx=5, pady=10)
    begin_year_label.grid(row=3, column=0, sticky=NSEW, padx=5, pady=10)

    end_day_label = Label(end_date_frame, text='День', font=ASK_DATE_DIALOG_LABEL_FONT)
    end_month_label = Label(end_date_frame, text='Месяц', font=ASK_DATE_DIALOG_LABEL_FONT)
    end_year_label = Label(end_date_frame, text='Год', font=ASK_DATE_DIALOG_LABEL_FONT)
    end_day_label.grid(row=2, column=0, sticky=NSEW, padx=5, pady=10)
    end_month_label.grid(row=2, column=1, sticky=NSEW, padx=5, pady=10)
    end_year_label.grid(row=2, column=2, sticky=NSEW, padx=5, pady=10)

    begin_day, begin_month, begin_year = IntVar(), IntVar(), IntVar()

    begin_day_control = tix.Control(begin_date_frame)
    begin_month_control = tix.Control(begin_date_frame)
    begin_year_control = tix.Control(begin_date_frame)
    begin_day_control.config(min=1, max=31, value=1, variable=begin_day)
    begin_month_control.config(min=1, max=12, value=1, variable=begin_month)
    begin_year_control.config(min=1999, max=2100, value=2010, variable=begin_year)
    begin_day_control.grid(row=1, column=1, sticky=NSEW, padx=5, pady=5)
    begin_month_control.grid(row=2, column=1, sticky=NSEW, padx=5, pady=5)
    begin_year_control.grid(row=3, column=1, sticky=NSEW, padx=5, pady=5)

    end_day, end_month, end_year = IntVar(), IntVar(), IntVar()

    end_day_control = tix.Control(end_date_frame)
    end_month_control = tix.Control(end_date_frame)
    end_year_control = tix.Control(end_date_frame)
    end_day_control.config(min=1, max=31, value=1, variable=end_day)
    end_month_control.config(min=1, max=12, value=1, variable=end_month)
    end_year_control.config(min=1999, max=2100, value=2010, variable=end_year)
    end_day_control.grid(row=3, column=0, sticky=NSEW, padx=5, pady=5)
    end_month_control.grid(row=3, column=1, sticky=NSEW, padx=5, pady=5)
    end_year_control.grid(row=3, column=2, sticky=NSEW, padx=5, pady=5)

    def validate():
        nonlocal begin_day, begin_month, begin_year, end_day, end_month, end_year
        begin = (begin_day.get(), begin_month.get(), begin_year.get())
        end = (end_day.get(), end_month.get(), end_year.get())
        try:
            print('Good date :')
            print(datetime.date(*reversed(begin)))
            print(datetime.date(*reversed(end)))
        except ValueError:
            print('Date is bad. Begin : ', begin, 'End :', end)
            return False
        return datetime.date(*reversed(begin)) <= datetime.date(*reversed(end))

    confirm_button = main_window.ToolbarButton(toolbar, text='ОК')
    confirm_button.config(width=15)
    confirm_button.config(font=TOOLBAR_BUTTON_FONT)
    confirm_button.config(command=(lambda: validate() and window.destroy()))
    confirm_button.pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)

    cancel_button_pressed = False

    def cancel():
        nonlocal cancel_button_pressed, window
        cancel_button_pressed = True
        window.destroy()

    cancel_button = main_window.ToolbarButton(toolbar, text='Отмена')
    cancel_button.config(width=15)
    cancel_button.config(font=TOOLBAR_BUTTON_FONT)
    cancel_button.config(command=cancel)
    cancel_button.pack(side=LEFT, expand=NO, fill=X, padx=20, pady=10)

    window.protocol('WM_DELETE_WINDOW', lambda: None)
    window.focus_set()
    window.grab_set()
    window.wait_window()

    begin = end = None
    if not cancel_button_pressed:
        begin = (begin_day.get(), begin_month.get(), begin_year.get())
        end = (end_day.get(), end_month.get(), end_year.get())
    print('begin :', begin, 'end :', end)
    return begin, end


def ask_table_row(table_id, root, account):
    window = Toplevel(root)
    window.title('Выбор записи в таблице [' + account.get_rights() + ']')
    window.resizable(width=True, height=True)
    window.state('zoomed')

    toolbar = Frame(window)
    toolbar.pack(side=BOTTOM, expand=NO, fill=X)

    column_names = INTERFACE_COLUMN_NAMES[table_id]
    table_data = db_helper.select_all_from(DATABASE_TABLE_NAMES[table_id])

    grid_viewer = db_viewer.ScrolledGridViewer(window, column_names, table_data)
    grid_viewer.pack(expand=YES, fill=BOTH)

    def cancel():
        nonlocal cancel_button_pressed, window
        cancel_button_pressed = True
        window.destroy()

    cancel_button = main_window.ToolbarButton(toolbar, text='Отмена')
    cancel_button.config(width=20)
    cancel_button.config(font=TOOLBAR_BUTTON_FONT, bg='#F55', fg='#000')
    cancel_button.config(command=cancel)
    cancel_button.pack(side=RIGHT, expand=NO, fill=X, padx=10, pady=10)

    def confirm():
        return not (grid_viewer.selected_item is None) # and len(grid_viewer.selected_item['values']) > 0

    confirm_button = main_window.ToolbarButton(toolbar, text='ОК')
    confirm_button.config(width=20)
    confirm_button.config(font=TOOLBAR_BUTTON_FONT, bg='#0F0', fg='#000')
    confirm_button.config(command=(lambda: confirm() and window.destroy()))
    confirm_button.pack(side=RIGHT, expand=NO, fill=Y, padx=10, pady=10)

    cancel_button_pressed = False

    window.protocol('WM_DELETE_WINDOW', lambda: cancel)
    window.focus_set()
    window.grab_set()
    window.wait_window()

    if not cancel_button_pressed:
        return grid_viewer.selected_item['values']
    return None