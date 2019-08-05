import sys
from NaiveBayes import NaiveBayes
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Naive_Bayes_Clasiffier (root)
    #unknown_support.init(root, top)
    root.mainloop()

w = None
def create_Naive_Bayes_Clasiffier(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Naive_Bayes_Clasiffier (w)
    #unknown_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Naive_Bayes_Clasiffier():
    global w
    w.destroy()
    w = None

class Naive_Bayes_Clasiffier:

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {Segoe UI} -size 30 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("500x280+428+169")
        top.title("Naive Bayes Classifer")
        top.configure(background="#3e5d93")

        self.title_naiveBayes = tk.Label(top)
        self.title_naiveBayes.place(relx=0.08, rely=0.0, height=60, width=416)
        self.title_naiveBayes.configure(activebackground="#f0f0f0")
        self.title_naiveBayes.configure(activeforeground="white")
        self.title_naiveBayes.configure(background="#3e5d93")
        self.title_naiveBayes.configure(disabledforeground="#a3a3a3")
        self.title_naiveBayes.configure(font=font11)
        self.title_naiveBayes.configure(foreground="white")
        self.title_naiveBayes.configure(text='''Naive Bayes Classifier''')

        self.directory_frame = tk.LabelFrame(top)
        self.directory_frame.place(relx=0.06, rely=0.214, relheight=0.232
                , relwidth=0.88)
        self.directory_frame.configure(relief='groove')
        self.directory_frame.configure(foreground="white")
        self.directory_frame.configure(text='''Directory Path''')
        self.directory_frame.configure(background="#3e5d93")
        self.directory_frame.configure(width=440)

        self.Browse_button = ttk.Button(top)
        self.Browse_button.place(relx=0.71, rely=0.304, height=25, width=96)
        self.Browse_button.configure(takefocus="")
        self.Browse_button.configure(text='''Browse''')
        self.Browse_button.configure(width=96)
        self.Browse_button.configure(cursor="fleur")
        self.Browse_button.configure(command=self.folderBrowse)

        self.directory_textField = ttk.Entry(top)
        self.directory_textField.place(relx=0.08, rely=0.304, relheight=0.075
                , relwidth=0.592)
        self.directory_textField.configure(width=296)
        self.directory_textField.configure(takefocus="")
        self.directory_textField.configure(cursor="ibeam")

        self.Build_button = ttk.Button(top)
        self.Build_button.place(relx=0.61, rely=0.5, height=55, width=166)
        self.Build_button.configure(takefocus="")
        self.Build_button.configure(text='''Build''')
        self.Build_button.configure(width=166)
        self.Build_button.configure(state='disable')
        self.Build_button.configure(command=self.startBuild)

        self.Dicritezation_frame = tk.LabelFrame(top)
        self.Dicritezation_frame.place(relx=0.06, rely=0.5, relheight=0.232
                , relwidth=0.32)
        self.Dicritezation_frame.configure(relief='groove')
        self.Dicritezation_frame.configure(foreground="white")
        self.Dicritezation_frame.configure(text='''Discretization Bins''')
        self.Dicritezation_frame.configure(background="#3e5d93")
        self.Dicritezation_frame.configure(width=160)

        self.bins_textField = ttk.Entry(top)
        self.bins_textField.place(relx=0.08, rely=0.589, relheight=0.075, relwidth=0.252)
        self.bins_textField.configure(takefocus="")
        self.bins_textField.configure(cursor="ibeam")
        self.bins_textField.bind("<Key>", self.key)

        self.Classify_button = ttk.Button(top)
        self.Classify_button.place(relx=0.61, rely=0.714, height=55, width=166)
        self.Classify_button.configure(takefocus="")
        self.Classify_button.configure(text='''Classify''')
        self.Classify_button.configure(width=166)
        self.Classify_button.configure(command=self.classify)

        self.inputBindAlret = ttk.Label(top)
        self.inputBindAlret.place(relx=0.05, rely=0.75, height=19, width=202)
        self.inputBindAlret.configure(background="#3e5d93")
        self.inputBindAlret.configure(foreground="#3e5d93")
        self.inputBindAlret.configure(relief='flat')
        self.inputBindAlret.configure(text='''please enter only positive number''')
        self.inputBindAlret.configure(width=202)


        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

    def startBuild(self):
        self.NB = NaiveBayes()
        self.NB.build(self.directory_textField.get(),self.bins_textField.get())
        messagebox.showinfo("Update From Build", "Building classifier using train-set is done!")

    def classify(self):
        self.NB.classify()
        messagebox.showinfo("All Done", "It's Done! a file added to your directory with the answers! ")
        sys.exit()
    def folderBrowse(self):
        dirWind = tk.Tk()
        dirWind.withdraw()
        path = askdirectory()
        if(len(str(self.directory_textField.get())) != 0):
            self.directory_textField.delete(0,'end')
        self.directory_textField.insert(0,str(path))
        dirWind.destroy()
        if(self.word.isdigit):
            # check path!!
            self.Build_button.configure(state='normal')

    def key(self,event):
        #(not str(event.char).isdigit()
        if(event.keycode == 8):
            #print("reves")
            self.word = (str(self.bins_textField.get()))[:-1]
        else:
            self.word = str(self.bins_textField.get()+str(event.char))

        #print("shit:" + self.word)
        #print("shit:" + str(len(self.word)))
        if((self.word.isdigit()) or (len(self.word) == 0)):# and len(str(self.bins_textField.get())) == 0)):
            self.inputBindAlret.configure(foreground="#3e5d93")
            if((self.word.isdigit()) and (len(str(self.directory_textField.get())) != 0)):
                self.Build_button.configure(state='normal')
            else:
                self.Build_button.configure(state='disable')

        else:
            self.inputBindAlret.configure(foreground="#ffffffffffff")
            self.Build_button.configure(state='disable')
        #print ("pressed", repr(event.char))


if __name__ == '__main__':
    vp_start_gui()






