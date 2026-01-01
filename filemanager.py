#Импорт всего чего надо
import tkinter as tk
import time
from os import rename
from time import sleep
from tkinter import ttk, StringVar, Scrollbar
import os
import filetype

from config import *


#Начальную директорию задаем
os.chdir(path='/')
#Начало класса
class FileManager():
    #CONSTRUCTOR--------------------------------------------------------------------------------------------------------
    def __init__(self,root):
        self.main = '' #Pwd for relocate func
        self.maindir = os.getcwd() #Main path to file/dir
        self.y_pos = 0 #y file position
        self.all = os.listdir(path='.') #List all files and dir in main dir
        self.app = ''
        self.root = root #Main Window
        self.root.geometry(GEOMETRYWINDOW)
        self.root.title('Frei Manager') #Tittle Window
        #LABEL----------------------------------------------------------------------------------------------------------
        self.canvas_for_label = tk.Canvas(height=60,width=1910)
        self.canvas_for_label.pack(anchor='nw')

        self.scrollbar_for_label = tk.Scrollbar(self.root,orient="horizontal",command=self.canvas_for_label.xview)
        self.scrollbar_for_label.pack(side='top',fill='x')
        self.canvas_for_label.configure(xscrollcommand=self.scrollbar_for_label.set)

        self.label1 = tk.Label(self.canvas_for_label, text=self.maindir, font=(FONT,20), borderwidth=5, relief='ridge',height=1)

        self.canvas_for_label.create_window((0,0),anchor='nw',window=self.label1)
        self.label1.bind('<Configure>', lambda e: self.canvas_for_label.configure(scrollregion=self.canvas_for_label.bbox('all')))
        #MASTERFRAME----------------------------------------------------------------------------------------------------
        self.canvas = tk.Canvas(width=1450,height=1000)
        self.canvas.pack(side='right')

        self.scrollbar = tk.Scrollbar(self.root,orient='vertical',command=self.canvas.yview)
        self.scrollbar.pack(side='right',fill='y')
        self.scrollbar.pack_forget()
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.masterframe = tk.Frame(self.canvas,borderwidth=5,relief='ridge',height=900,width=1400)

        self.canvas.create_window((0,0),anchor='nw',window=self.masterframe)
        self.masterframe.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        #NEUFRAME AND DOPFRAME------------------------------------------------------------------------------------------
        self.neucanvas = tk.Canvas(width=400,height=1000)
        self.neucanvas.pack(side='left')

        self.dopframe = tk.Frame(self.neucanvas,borderwidth=5,relief='ridge',height=360,width=400)
        self.neuframe = tk.Frame(self.neucanvas,borderwidth=5,relief='ridge',height=600,width=400)

        self.neucanvas.create_window((0,0),anchor='nw',window=self.neuframe)
        self.neucanvas.create_window((200,810),window=self.dopframe)
        #BACKBUTTON-----------------------------------------------------------------------------------------------------
        self.backbut = tk.Button(self.masterframe,text='..',font=(FONT,15),command=self.Go_Up)
        self.backbut.place(x=0)
        #DOP INFORMAITON------------------------------------------------------------------------------------------------
        self.name = tk.Label(self.dopframe,text='Frei File Manager',font=(FONT,15,'underline'))
        self.name.place(y=0)

        self.version = tk.Label(self.dopframe,text='Version:1.1.2 DEMO',font=(FONT,15,'underline'))
        self.version.place(y=35)

        self.me = tk.Label(self.dopframe,text='Developer:_F_R_E_I_',font=(FONT,15,'underline'))
        self.me.place(y=70)

        self.update_dir()
        self.updateRights_p()

    #MAINDIR LABEL WITH SCROLLBAR---------------------------------------------------------------------------------------
    def create_main_label (self):
        text_for_label = tk.Text(self.neuframe,width=45,height=2,background='grey',borderwidth=3,relief='ridge')
        text_for_label.place(x=2)
        text_for_label.tag_add('LBL','1.0')
        scrollbar_for_label = tk.Scrollbar(self.neuframe,orient='horizontal',command=text_for_label.xview)
        scrollbar_for_label.place(y=40,width=380)
        scrollbar_for_label.place_forget()

        text_for_label.configure(xscrollcommand=scrollbar_for_label.set)
        maindir_label = tk.Label(text_for_label,text=self.maindir,font=FONT,background='grey')
        text_for_label.window_create('1.0',window=maindir_label)

        if len(self.maindir) >= 30:
            scrollbar_for_label.place(y=40,width=380)
    #DOPLABEL WITH SCROLLBAR--------------------------------------------------------------------------------------------
    def create_dop_label(self, p):
        if os.path.isdir(p):
            y_pos = 350
            y_pos_for_scrlb = 383
        elif filetype.is_archive(p):
            y_pos = 353
            y_pos_for_scrlb = 386
        else:
            y_pos = 300
            y_pos_for_scrlb = 333
        text_for_doplabel = tk.Text(self.neuframe, width=40, height=2, background='grey', borderwidth=3, relief='ridge')
        text_for_doplabel.place(y=y_pos)
        text_for_doplabel.tag_add('LBL', '1.0')
        scrollbar_for_doplabel = tk.Scrollbar(self.neuframe, orient='horizontal', command=text_for_doplabel.xview)
        scrollbar_for_doplabel.place(y=y_pos_for_scrlb, width=380)
        scrollbar_for_doplabel.place_forget()

        text_for_doplabel.configure(xscrollcommand=scrollbar_for_doplabel.set)
        dopdir_label = tk.Label(text_for_doplabel, text=self.main, font=FONT, background='grey')
        text_for_doplabel.window_create('1.0', window=dopdir_label)

        if len(self.maindir) >= 30:
            scrollbar_for_doplabel.place(y=y_pos_for_scrlb,width=380)

    #FUNC FOR UPDATE DIRS-----------------------------------------------------------------------------------------------
    def update_dir(self):
        self.clear_neuframe()
        height = 1000 #Height for masterframe
        self.maindir = os.getcwd() #Present path
        self.label1.config(text=self.maindir) #Change path in label1
        self.y_pos = 0 #y posision for buttons
        #MOVETO FOR SCROLLBARS------------------------------------------------------------------------------------------
        self.canvas.yview_moveto(0.0)
        self.canvas_for_label.xview_moveto(0.0)
        #SCROOLBAR FOR LABEL--------------------------------------------------------------------------------------------
        width_for_label = 146 #width for label
        self.create_main_label()
        if len(self.maindir) >= 130:
            width_for_label = 0
            for i in self.maindir:
                width_for_label += 1
            self.canvas_for_label.config(height=45)
            self.scrollbar.pack_forget()
        self.label1.config(width=width_for_label)
        #BUTTON FOR MOVES WITH DIRS-------------------------------------------------------------------------------------
        work_with_dir = tk.Button(self.neuframe, text='DirMoves',font=FONT,command=lambda p=self.maindir: (self.clear_neuframe(), self.change_moves_for_dir(p)))
        work_with_dir.place(x=0, y=55)
        #CLEAR MASTERFRAME----------------------------------------------------------------------------------------------
        for wid in self.masterframe.winfo_children(): #Delete all widjets in masterframe
            if wid != self.backbut:
                wid.destroy()
     #CREATE LIST BUTTONS--------------------------------------------------------------------------------------------
        try:
            items = os.listdir(path='.')
        except PermissionError:
            items = []
        #CHANGE WIDTH LABEL1--------------------------------------------------------------------------------------------
        if len(os.listdir(path='.')) > 24:
            height = 45
        #CREATE BUTTONS-------------------------------------------------------------------------------------------------
        for item in items:
            #LENITEMS---------------------------------------------------------------------------------------------------
            self.lenitems = tk.Label(self.masterframe,text=f'Objects:{len(items)}',font=(FONT,20,'underline'))
            self.lenitems.place(x=50)
            #OTHER------------------------------------------------------------------------------------------------------
            self.y_pos += 40
            item_path = os.path.join(self.maindir,item)
            #CHANGE HEIGH MASTERFRAME-----------------------------------------------------------------------------------
            if len(items) > 24:
                height += 40
                self.scrollbar.pack(side='right', fill='y')
                self.masterframe.config(height=height)
                self.canvas.config(height=height)

            #FILE BUTTON------------------------------------------------------------------------------------------------
            try:
                #CREATE DOP INFORMATION FOR FILE------------------------------------------------------------------------
                sectime = os.path.getctime(item_path)
                datatime = time.ctime(sectime)
                filezize = f'{os.path.getsize(item)} B'
                #CREATE FILE BUTTON-------------------------------------------------------------------------------------
                if os.path.isdir(item_path):
                    btn = tk.Button(self.masterframe, text=f'{item}/                   {datatime}                    {filezize}',font=(FONT,15), command=lambda p=item_path:(self.clear_neuframe(),self.change_dir(p)))
                    btn.place(y=self.y_pos)
            #IF FILE NOT FOUND------------------------------------------------------------------------------------------
            except FileNotFoundError:
                self.y_pos -= 40
            #DIR BUTTON-------------------------------------------------------------------------------------------------
            if os.path.isfile(item_path):
                #CREATE DOP INFORMATION FOR DIR-------------------------------------------------------------------------
                sectime = os.path.getctime(item_path)
                datatime = time.ctime(sectime)
                filezize = f'{os.path.getsize(item)} B'
                #CREATE DIR BUTTON--------------------------------------------------------------------------------------
                btn2 = tk.Button(self.masterframe, text=f'{item}                   {datatime}                    {filezize}',font=(FONT,15), command=lambda p=item_path:(self.clear_neuframe(),self.change_move(p)))
                btn2.place(y=self.y_pos)

    #CHANGE MOVE FOR FILES----------------------------------------------------------------------------------------------
    def change_move(self,p):
        #MAINP_LABEL----------------------------------------------------------------------------------------------------
        self.create_main_label()
        #BUTTON FOR DIRS MOVES------------------------------------------------------------------------------------------
        work_with_dir = tk.Button(self.neuframe, text='DirMoves',font=FONT,command=lambda p=self.maindir:(self.clear_neuframe(),self.change_moves_for_dir(p)))
        work_with_dir.place(x=0,y=55)
        #BUTTON FOR OPEN FILES------------------------------------------------------------------------------------------
        open_button = tk.Button(self.neuframe,text='Open',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_move(p),self.open_file(p)))
        open_button.place(x=0,y=95)
        #BUTTON FOR DELETE FILE-----------------------------------------------------------------------------------------
        command = f'rm -r "{p}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
        delete_button = tk.Button(self.neuframe,text='Delete',font=FONT,command=lambda :(self.clear_neuframe(),os.system(command),self.check_rights(p=p,cmd=command), self.update_dir()))
        delete_button.place(x=0,y=130)
        #BUTTON FOR RENAME FILE-----------------------------------------------------------------------------------------
        remame_button = tk.Button(self.neuframe,text='Rename',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_move(p),self.create_new_name(p)))
        remame_button.place(x=0,y=165)
        #BUTTON FOR COPY FILE-------------------------------------------------------------------------------------------
        copy_btn = tk.Button(self.neuframe, text='Copy',font=FONT, command=lambda p=p: (self.clear_neuframe(),self.change_move(p),self.Copy_File_or_Dir(p)))
        copy_btn.place(y=200)
        #BUTTON FOR RELOCATE FILE---------------------------------------------------------------------------------------
        self.main = os.path.split(p)[0]
        relocate_move = tk.Button(self.neuframe,text='Relocate',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_move(p),self.change_path_to_relocate(p)))
        relocate_move.place(y=235)
        #BUTTON FOR UNARCHIVE-------------------------------------------------------------------------------------------
        if filetype.is_archive(p):
            unarch_btn = tk.Button(self.neuframe, text='UnArchive',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_move(p),self.UnArch(p)))
            unarch_btn.place(y=270)
    #FUNCION FOR UNARCHIVE----------------------------------------------------------------------------------------------
    def UnArch(self,p):
        #COMBOBOX-------------------------------------------------------------------------------------------------------
        all = os.listdir(self.main)
        list_for_relocate = []
        for i in all:
            full_path = os.path.join(self.main,i)
            if os.path.isdir(full_path):
                if self.maindir == full_path:
                    pass
                else:
                    list_for_relocate.append(i)
            else:
                pass

        path_var = StringVar()
        listpwd = ttk.Combobox(self.neuframe,values=list_for_relocate,textvariable=path_var)
        listpwd.place(y=318)
        #FUNCTION FOR UP-CHANGE UNARCH PATH-----------------------------------------------------------------------------
        def Change_local_path(path_var):
            pv = path_var.get()
            self.main = os.path.join(self.main,pv)
            self.create_dop_label(p=p)
        #FUNCTION FOR DOWN_CHANGE UNARCH PATH---------------------------------------------------------------------------
        def Change_local_path_down(path_var):
            down_dir = os.path.split(self.main)
            self.main = down_dir[0]
            self.create_dop_label(p=p)
        #UNTAR----------------------------------------------------------------------------------------------------------
        def Untar(p):
            command = f'tar xof "{p}" -C "{self.main}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(p=p)
            os.system(command)
        #LABEL WITH PATH TO UNARCHIVE-----------------------------------------------------------------------------------
        self.create_dop_label(p=p)
        #BUTTON FOR UP-CHANGE UNARCHIVE PATH----------------------------------------------------------------------------
        up_btn = tk.Button(self.neuframe,text='Up',font=FONT,command=lambda p=p:(Change_local_path(path_var),self.UnArch(p)))
        up_btn.place(x=170,y=308)
        #BUTTON FOR DOWN-CHANGE UNARCHIVE PATH--------------------------------------------------------------------------
        down_btn = tk.Button(self.neuframe,text='Down',font=FONT,command=lambda p=p:(Change_local_path_down(path_var),self.UnArch(p)))
        down_btn.place(x=220,y=308)
        #BUTTON FOR UNTAR-----------------------------------------------------------------------------------------------
        tar_btn = tk.Button(self.neuframe,text='Tar',font=FONT,command=lambda p=p:(Untar(p),self.clear_neuframe(),self.update_dir()))
        tar_btn.place(x=290,y=308)
        #FUNCTION FOR UNZIP---------------------------------------------------------------------------------------------
        def UnZip(p):
            command = f'unzip -o "{p}" -d "{self.main} 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(p=p)
            os.system(command)
        #BUTTON FOR UNZIP-----------------------------------------------------------------------------------------------
        zip_btn = tk.Button(self.neuframe,text='Zip',font=FONT,command=lambda p=p:(UnZip(p),self.clear_neuframe(),self.update_dir()))
        zip_btn.place(x=342,y=308)
    #FUNCTION FOR RELOCATE----------------------------------------------------------------------------------------------
    def change_path_to_relocate(self,p):
        #Y POSISION-----------------------------------------------------------------------------------------------------
        y_for_buttons = 268
        y_for_main_label = 299
        if os.path.isfile(p):
            if filetype.is_archive(p):
                y_for_buttons =  308
                y_for_main_label = 353
        elif os.path.isdir(p):
            y_for_buttons = 310
            y_for_main_label = 340
        #COMBOBOX-------------------------------------------------------------------------------------------------------
        all = os.listdir(self.main)
        list_for_relocate = []
        for i in all:
            full_path = os.path.join(self.main,i)
            if os.path.isdir(full_path):
                if self.maindir == full_path:
                    pass
                else:
                    list_for_relocate.append(i)
            else:
                pass

        path_var = StringVar()
        listpdw = ttk.Combobox(self.neuframe,values=list_for_relocate,textvariable=path_var)
        listpdw.place(y=y_for_buttons)
        #FUNCTION FOR UP-CHANGE RELOCATE PATH---------------------------------------------------------------------------
        def Change_local_path(path_var):
            pv = path_var.get()
            self.main = os.path.join(self.main,pv)
            self.create_dop_label(p=p)
        #FUNCTION FOR DOWN-CHANGE RELOCATE PATH-------------------------------------------------------------------------
        def Change_local_path_down(path_var):
            down_dir = os.path.split(self.main)
            self.main = down_dir[0]
            self.create_dop_label(p=p)
        #FUNCTION FOR RELOCATE------------------------------------------------------------------------------------------
        def Relocate(p):
            command = f'mv "{p}" {self.main} 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            os.system(command)
            self.check_rights(p=p,cmd=command)
            if os.path.isdir(p):
                self.Go_Up()
            else:
                self.update_dir()
        #LABEL WITH RELOCATE PATH---------------------------------------------------------------------------------------
        self.create_dop_label(p=p)
        #BUTTON FOR UP-CHANGE RELOCATE PATH-----------------------------------------------------------------------------
        up_btn = tk.Button(self.neuframe,text='Up',font=FONT,command=lambda p=p:(Change_local_path(path_var),self.change_path_to_relocate(p)))
        up_btn.place(x=170,y=y_for_buttons)
        #BUTTON FOR DOWN-CHANGE RELOCATE PATH---------------------------------------------------------------------------
        down_btn = tk.Button(self.neuframe,text='Down',font=FONT,command=lambda p=p:(Change_local_path_down(path_var),self.change_path_to_relocate(p)))
        down_btn.place(x=220,y=y_for_buttons)
        #BUTTON FOR RELOCATE--------------------------------------------------------------------------------------------
        ok_btn = tk.Button(self.neuframe,text='OK',font=FONT,command=lambda p=p:(self.clear_neuframe,Relocate(p)))
        ok_btn.place(x=292,y=y_for_buttons)
    #CHANGE MOVES FOR DIRS----------------------------------------------------------------------------------------------
    def change_moves_for_dir(self,p):
        #LABEL FOR PATH MAIN DIR----------------------------------------------------------------------------------------
        self.create_main_label()
        #BUTTON FOR DELETE MAIN DIR-------------------------------------------------------------------------------------
        command_to_delete = f'rm -r {p} 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
        delete_button = tk.Button(self.neuframe,text='Delete',font=FONT,command=lambda :(os.system(command_to_delete),self.check_rights(p=p,cmd=command_to_delete),self.clear_neuframe(),self.Go_Up(), self.update_dir()))
        delete_button.place(x=0,y=130)
        #BUTTON FOR RENAME MAIN DIR-------------------------------------------------------------------------------------
        remame_button = tk.Button(self.neuframe,text='Rename',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_moves_for_dir(p),self.create_new_name(p)))
        remame_button.place(x=0,y=165)
        #BUTTON FOR COPY MAIN DIR---------------------------------------------------------------------------------------
        copy_btn = tk.Button(self.neuframe,text='Copy',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_moves_for_dir(p),self.Copy_File_or_Dir(p)))
        copy_btn.place(y=200)
        #BUTTON FOR CREATE NEW DIR--------------------------------------------------------------------------------------
        create_dir_btn = tk.Button(self.neuframe,text='NewDir',font=FONT,command=lambda:(self.clear_neuframe(),self.change_moves_for_dir(p),self.create_dir()))
        create_dir_btn.place(y=235)
        #BUTTON FOR RELOCATE MAIN DIR-----------------------------------------------------------------------------------
        if os.path.isdir(p):
            self.main = os.path.split(p)[0]
        self.main = os.path.split(p)[0]
        relocate_move = tk.Button(self.neuframe,text='Relocate',font=FONT,command=lambda p=p:(self.clear_neuframe(),self.change_moves_for_dir(p),self.change_path_to_relocate(p)))
        relocate_move.place(y=270)
    #FUNCTION FOR CREATE DIR--------------------------------------------------------------------------------------------
    def create_dir(self):
        #ENTRY FOR NAME NEW DIR-----------------------------------------------------------------------------------------
        name_entr = tk.Entry(self.neuframe)
        name_entr.place(x=90,y=240)
        #FUNCTION FOR ACCEPT CREATE DIR---------------------------------------------------------------------------------
        def clame_name_dir():
            name = name_entr.get()
            command = f'mkdir "{name}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(None,command)
            os.system(command)

            self.clear_neuframe()
            self.update_dir()
        #BUTTON FOR CREATE DIR------------------------------------------------------------------------------------------
        clame_name = tk.Button(self.neuframe,text='Accept',font=FONT,command=lambda:clame_name_dir())
        clame_name.place(x=240,y=235)


    #FUNCTION FOR COPY--------------------------------------------------------------------------------------------------
    def Copy_File_or_Dir(self,p):
        #ENTRY FOR COPY NAME--------------------------------------------------------------------------------------------
        name_copy = tk.Entry(self.neuframe)
        name_copy.place(x=75,y=205)
        #CREATE COPY----------------------------------------------------------------------------------------------------
        def clame_name_copy(p):
            if os.path.isdir(p):
                Path_dir = os.path.split(p)
                copy_name = Path_dir[0] + '/' + name_copy.get()
            if os.path.isfile(p):
                copy_name = name_copy.get()
            command = f'cp -r "{p}" "{copy_name}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(p=p,cmd=command)
            os.system(command)
            #AFTER COPY MOVE--------------------------------------------------------------------------------------------
            if os.path.isdir(p):
                self.Go_Up()
            if os.path.isfile(p):
                self.clear_neuframe()
                self.update_dir()
        #BUTTON FOR CREATE COPY-----------------------------------------------------------------------------------------
        clame_copy = tk.Button(self.neuframe,text='Accept',font=FONT, command=lambda:clame_name_copy(p))
        clame_copy.place(x=230,y=200)
    #FUNCTION FOR RENAME------------------------------------------------------------------------------------------------
    def create_new_name(self,p):
        #ENTRY FOR NEW NAME---------------------------------------------------------------------------------------------
        new_name = tk.Entry(self.neuframe)
        new_name.place(x=90,y=170)
        #RENAME---------------------------------------------------------------------------------------------------------
        def clame_name(p):
            if os.path.isdir(p):
                Path_dir = os.path.split(p)
                New_name = os.path.join(Path_dir[0],new_name.get())
            else:
                New_name = new_name.get()
            command = f'mv "{p}" "{New_name}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(p=p,cmd=command)
            os.system(command)

            self.clear_neuframe()
            self.update_dir()
        #BUTTON FOR CLAME NEW NAME--------------------------------------------------------------------------------------
        clame_new_name = tk.Button(self.neuframe,text='Accept',font=FONT,command=lambda:clame_name(p))
        clame_new_name.place(x=240,y=165)
    #CLEAR NEUFRAME-----------------------------------------------------------------------------------------------------
    def clear_neuframe(self):
        for wid in self.neuframe.winfo_children():
            wid.destroy()
    #FUNCTION FOR OPEN FILES--------------------------------------------------------------------------------------------
    def open_file(self,p):
        pathapp = p #Varible for path file
        self.app = '' #Varible for open-app
        #ENTRY FOR CHANGE OPEN-APP--------------------------------------------------------------------------------------
        app_entry = tk.Entry(self.neuframe)
        app_entry.place(x=70,y=100)
        #OPEN FILE------------------------------------------------------------------------------------------------------
        def Open(pathapp):
            self.app = app_entry.get()
            command = f'{self.app} "{pathapp}" 2> /home/mark/PycharmProjects/FREImanagr/rights_p &'
            self.check_rights(p=p,cmd=command)
            os.system(command)
        #BUTTON FOR OPEN FILE-------------------------------------------------------------------------------------------
        open_btn = tk.Button(self.neuframe,text='Open',font=FONT,command=lambda pathapp=pathapp:(Open(pathapp),self.clear_neuframe()))
        open_btn.place(x=220,y=95)


    #FUNCTION FOR CHANGE MAIN DIR---------------------------------------------------------------------------------------
    def change_dir(self,path):
        try:
            os.chdir(path)
            self.update_dir()
        except PermissionError:
            pass

    #FUNCRION FOR CHANGE DIR PARENT-------------------------------------------------------------------------------------
    def Go_Up(self):
        parent = os.path.dirname(self.maindir)
        try:
            os.chdir(parent)
            self.clear_neuframe()
            self.update_dir()
        except PermissionError:
            pass
    #UPDATE FILE RIGHTS_P AFTER STARTING FFM----------------------------------------------------------------------------
    def updateRights_p(self):
        command = f'true > /home/mark/PycharmProjects/FREImanagr/rights_p &'
        os.system(command)
    #FUNCTION FOR CHECKING NEED ROOT RIGHT------------------------------------------------------------------------------C
    def check_rights(self,p,cmd):
        l = None
        time.sleep(0.2)
        rights = open('/home/mark/PycharmProjects/FREImanagr/rights_p','r')
        for line in rights:
            l = line
        self.checkLine(l,cmd)
        rights.close()
        #command = 'true > /home/mark/PycharmProjects/FREImanagr/filemanager.py '

    def checkLine(self,l,cmd):
        r = 'Отказано в доступе'
        if l == None:
            pass
        elif r in l:
            app = self.createWindowOfSudo(cmd)
            return True


    def createWindowOfSudo(self,command):
        self.command = command
        self.createWindow()
        self.createOpenLabel()
        self.createOKButton()
        self.createCloseButton()
        self.createEntry()

    def createWindow(self):
        self.SudoWindow = tk.Toplevel(self.root)
        self.SudoWindow.geometry('500x150')
        self.SudoWindow.title('Input Sudo')

    def createOpenLabel(self):
        self.OpenLabel = tk.Label(self.SudoWindow,text='Enter Root Password', font=(FONT,16))
        self.OpenLabel.pack(anchor='center')

    def createOKButton(self):
        self.OKButton = tk.Button(self.SudoWindow,text='OK',font=(FONT,12),command=lambda:(self.recommand(),self.update_dir(),self.closeWindow(),self.updateRights_p()))
        self.OKButton.place(x=320,y=80)

    def createCloseButton(self):
        self.CloseButton = tk.Button(self.SudoWindow, text='Close', font=(FONT, 12), command=lambda:(self.closeWindow()))
        self.CloseButton.place(x=120, y=80)

    def createEntry(self):
        self.Entry = tk.Entry(self.SudoWindow,width=50)
        self.Entry.pack(anchor='center')

    def closeWindow(self):
        self.SudoWindow.destroy()

    def getPassword(self):
        pswd = self.Entry.get()
        return pswd

    def recommand(self):
        command = (f'echo {self.getPassword()} | sudo -S {self.command}')
        os.system(command)






#START -F-F-M-
if __name__ == '__main__':
    FFM = tk.Tk()
    app = FileManager(FFM)
    FFM.mainloop()