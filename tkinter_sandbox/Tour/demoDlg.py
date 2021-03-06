# askopenfilename, askcolor, askquestion, showerror, askfloat, askdirectory

"""создает панель с кнопками, которые вызывают диалоги"""

from tkinter import *
from tkinter_sandbox.Tour.dialogTable import demos
from tkinter_sandbox.Tour.quitter import Quitter

def tc(var):
    print('var :', var.get())

class Demo(Frame):
    def __init__(self, parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        Label(self, text='Basic demos').pack()
        for (key, value) in demos.items():
            Button(self, text=key, command=value).pack(side=TOP, fill=BOTH)
        Quitter(self).pack(side=TOP, fill=BOTH)

        var = IntVar()
        c = Checkbutton(self, text='asdfldf', variable=var)
        c.pack()
        c.config(command=(lambda:tc(var)))




if __name__ == '__main__':
    Demo().mainloop()
