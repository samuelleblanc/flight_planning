def gui_file_select():
    """
    Simple gui file select program. Uses TKinter for interface, returns full path
    """
    from Tkinter import Tk
    from tkFileDialog import askopenfilename

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return filename
