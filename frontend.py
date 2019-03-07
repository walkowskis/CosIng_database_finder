from tkinter import *
from backend import Database

database = Database("testowa.db")

class Window(object):
    def __init__(self,window):
        self.window = window
        self.window.wm_title("CosIng Searcher")

        l1 = Label(window, text="INCI or CAS")
        l1.grid(row=0, column=0)

        self.title_text = StringVar()
        self.e1 = Entry(window, textvariable=self.title_text)
        self.e1.grid(row=0, column=1)

        self.detail_text = ''
        self.detail = Text(window, height=7, width=45, pady=3, padx=2, wrap=WORD)
        # tag configure to easy format some part of text
        self.detail.tag_configure('big', font=('Verdana', 10, 'bold'))
        self.detail.tag_configure('bold', font=('Verdana', 8, 'bold'), foreground='blue')
        self.detail.insert(END, self.detail_text)
        self.detail.grid(row=8, column=0, rowspan=7, columnspan=4)

        self.list1 = Listbox(window, height=6, width=40, font=('Tahoma', 7))
        self.list1.grid(row=1, column=0, rowspan=6, columnspan=2)

        # bind get_selected_row(self,event) function to the listbox
        self.list1.bind('<<ListboxSelect>>', self.get_selected_row)

        # attach a scrollbar to the listbox and the listbox to a scrollbar
        sb1 = Scrollbar(window)
        sb1.grid(row=1, column=2, rowspan=6, sticky=W+N+S)
        self.list1.config(yscrollcommand=sb1.set)
        sb1.config(command=self.list1.yview)

        sb2 = Scrollbar(window, command=self.detail.yview)
        self.detail.configure(yscrollcommand=sb2.set)
        sb2.grid(row=8, column=6, rowspan=7, sticky=W+N+S) #sticky=N+S - rozciągnięcie na wysokość

        b1 = Button(window, text="View all", width=12, command=self.view_command)
        b1.grid(row=1, column=3)

        b2 = Button(window, text="Search", width=12, command=self.search_command)
        b2.grid(row=0, column=3)

        b6 = Button(window, text="Close", width=12, command=window.destroy)
        b6.grid(row=2, column=3)

    def empty(self):
        if len(self) > 0:
            return self
        else:
            return 'N/A'

    # def empty_rest(self):
    #     if len(self) > 0:
    #         return self.detail.insert(END, 'Restriction: ', 'bold')
    #         self.detail.insert(END, Window.empty(self.selected_tuple[5])+'\n')
    #     else:
    #         return ''

    def get_selected_row(self,event):
        try:
            index = self.list1.curselection()[0]
            self.selected_tuple = self.list1.get(index)
            self.detail.delete(1.0,END)
            self.detail.insert(END, self.selected_tuple[1]+'\n', 'big')
            self.detail.insert(END, 'CAS No: ', 'bold')
            self.detail.insert(END, Window.empty(self.selected_tuple[4])+'\n')
            self.detail.insert(END, 'EC No: ', 'bold')
            self.detail.insert(END, Window.empty(self.selected_tuple[5])+'\n')
            self.detail.insert(END, 'Function: ', 'bold')
            self.detail.insert(END, (self.selected_tuple[8]).title()+'\n')
            self.detail.insert(END, 'Description: ', 'bold')
            self.detail.insert(END, (self.selected_tuple[6]).title())
            
        except IndexError:
            # when listbox is empty
            pass

    def view_command(self):
        self.list1.delete(0, END)
        for row in database.view():
            self.list1.insert(END, row)

    def search_command(self):
        # def empty(x):
        #     if len(str(x)) == 0:
        #         return "x"
        #     else:
        #         return x
        self.list1.delete(0, END)
        for row in database.search(self.title_text.get()):
            self.list1.insert(END, row)

window = Tk()
Window(window)

window.mainloop()
