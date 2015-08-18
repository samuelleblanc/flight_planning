def gui_file_select():
    """
    Simple gui file select program. Uses TKinter for interface, returns full path
    """
    from Tkinter import Tk
    from tkFileDialog import askopenfilename

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename

def make_gui():
    """
    make the gui with buttons
    """
    import Tkinter as tk
    def make_text():
        k = tk.Label(root,text='button pressed').pack()
    def make_pressed():
        bpressed.config(relief='sunken')
        
    root = tk.Tk()
    bopenfile = tk.Button(text='Open file',command=gui_file_select).pack()
    bmaketext = tk.Button(text='text',command=make_text).pack()
    bpressed = tk.Button(text='button on',command=make_pressed)
    bpressed.pack()
    root.mainloop()
