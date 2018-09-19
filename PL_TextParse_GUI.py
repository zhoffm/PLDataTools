from tkinter import *
from tkinter import filedialog, Menu
from tkinter.ttk import *
from PL_TextParse import *
import os


class App:
    def __init__(self, master):
        self.active_folder = None
        self.meas_type = Measurement()
        self.master = master
        self.master.title("PL-TextParse")
        self.master.iconbitmap('./assets/icons/pl_icon.ico')
        self.master.geometry('500x150')

        self.menubar = Menu(master)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.folder_open)
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.label1 = Label(master, text="Welcome to PL-TextParse!")
        self.label1.pack(padx=10, pady=10)

        self.vcsel_button = Button(master, state=DISABLED, text="VCSEL Parse", command=self.vcsel_data_parse)
        self.vcsel_button.pack(side=LEFT, padx=50, pady=10)

        self.spectral_button = Button(master, state=DISABLED, text="Spectral Parse", command=self.spectral_data_parse)
        self.spectral_button.pack(side=RIGHT, padx=50, pady=10)

    def list_active_folder(self):
        print(self.active_folder)

    def folder_open(self):
        try:
            self.active_folder = str(filedialog.askdirectory(initialdir=os.getcwd())) + "/"
            self.meas_type_check()
        except FileNotFoundError:
            pass

    def meas_type_check(self):
        try:
            if self.meas_type.check_meas_type(self.active_folder) == 'Spectral':
                self.label1.config(text='Spectral Data Folder Loaded')
                self.spectral_button.config(state=NORMAL)
                self.vcsel_button.config(state=DISABLED)
            elif self.meas_type.check_meas_type(self.active_folder) == 'VCSEL':
                self.label1.config(text='VCSEL Data Folder Loaded')
                self.spectral_button.config(state=DISABLED)
                self.vcsel_button.config(state=NORMAL)
            else:
                pass
        except ValueError:
            self.label1.config(text='Unknown measurement type loaded. Are you in the right directory?')
            self.vcsel_button.config(state=DISABLED)
            self.spectral_button.config(state=DISABLED)

    # def vcsel_data_parse(self):
    #     vcsel = VCSEL(self.active_folder + '/')
    #     vcsel.write_parsed_data(vcsel)
    #     self.label1.config(text='VCSEL data parsing complete.')
    #     self.spectral_button.config(state=DISABLED)
    #     self.vcsel_button.config(state=DISABLED)
    #
    # def spectral_data_parse(self):
    #     spec = Spectral(self.active_folder + '/')
    #     spec.write_parsed_data(spec)
    #     self.label1.config(text='Spectral data parsing complete.')
    #     self.spectral_button.config(state=DISABLED)
    #     self.vcsel_button.config(state=DISABLED)

    def vcsel_data_parse(self):
        if os.path.isdir('./output_data/'):
            vcsel = VCSEL(self.active_folder)
            vcsel.write_parsed_data()
            self.label1.config(text='VCSEL data parsing complete.')
            self.spectral_button.config(state=DISABLED)
            self.vcsel_button.config(state=DISABLED)
        else:
            os.makedirs('./output_data/')
            vcsel = VCSEL(self.active_folder)
            vcsel.write_parsed_data()
            self.label1.config(text='VCSEL data parsing complete.')
            self.spectral_button.config(state=DISABLED)
            self.vcsel_button.config(state=DISABLED)

    def spectral_data_parse(self):
        if os.path.isdir('./output_data/'):
            spec = Spectral(self.active_folder)
            spec.write_parsed_data()
            self.label1.config(text='Spectral data parsing complete.')
            self.spectral_button.config(state=DISABLED)
            self.vcsel_button.config(state=DISABLED)
        else:
            os.makedirs('./output_data/')
            spec = Spectral(self.active_folder)
            spec.write_parsed_data()
            self.label1.config(text='Spectral data parsing complete.')
            self.spectral_button.config(state=DISABLED)
            self.vcsel_button.config(state=DISABLED)


root = Tk()
my_gui = App(root)
root.config(menu=my_gui.menubar)
root.mainloop()


