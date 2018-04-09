from tkinter import *
from tkinter import filedialog, Menu
from tkinter.ttk import *
from TextParseFunctions import *


class App:
    def __init__(self, master):
        self.active_folder = None
        self.meas_type = None
        self.master = master
        master.title("PL-TextParse")
        master.geometry('500x500')

        # self.combo = Combobox(master)
        # self.combo['values'] = ("VCSEL", "Spectral")
        # self.combo.current(0)
        # self.combo.grid(column=0, row=0, padx=10, pady=10)

        self.menubar = Menu(master)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.folder_open)
        self.filemenu.add_command(label="Save", command=self.list_active_folder)
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.button1 = Button(master, text="Measurement Type Check", command=self.meas_type_check)
        self.button1.grid(column=0, row=0, padx=10, pady=10)

    def folder_open(self):
        self.active_folder = str(filedialog.askdirectory(initialdir='./'))
        print(self.active_folder)

    def list_active_folder(self):
        print(self.active_folder)

    def meas_type_check(self):
        self.meas_type = Measurement()
        self.meas_type.check_meas_type(self.active_folder)


root = Tk()
my_gui = App(root)
root.config(menu=my_gui.menubar)
root.mainloop()

# window = Tk()
# window.title("PL-TextParse")
# window.geometry('500x500')
#
# lbl1 = Label(text="Please choose your measurement type.")
# lbl1.grid(column=0, row=0, padx=10, pady=10)
#
# combo = Combobox(window)
# combo['values'] = ("VCSEL", "Spectral")
# combo.current(0)
# combo.grid(column=0, row=1, padx=0, pady=0)
#
# file = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
#
# window.mainloop()
