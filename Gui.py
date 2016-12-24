#!/usr/bin/python

import wx
import os
import time
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin

ID_EXIT = 200


class MyListCtrl(wx.ListCtrl , ListCtrlAutoWidthMixin):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        self.files = []

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size')
        self.InsertColumn(3, 'Modified')
        self.InsertColumn(4, 'Sentiment')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 50)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 150)
        self.SetColumnWidth(3, 150)

        self.InsertStringItem(0, '..')

        direc = os.listdir('.')

        for j, fil in enumerate(direc):
            (name, ext) = os.path.splitext(fil)
            ex = ext[1:]
            size = os.path.getsize(fil)
            modif = os.path.getmtime(fil)
            f = File(name, ex, size, modif)
            self.files.append(f)

        self.display_files()

    def display_files(self):
        for j, f in enumerate(self.files):
            self.InsertStringItem(j, f.name)
            self.SetStringItem(j, 1, f.extension)
            self.SetStringItem(j, 2, str(f.size) + ' B')
            self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M', time.localtime(f.last_modified)))
            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)
        self.Maximize(True)

        # Create a panel to make sure it looks right on all systems
        self.panel = wx.Panel(self, wx.ID_ANY)

        # create the Menubar items
        filemenu = wx.Menu()
        filemenu.Append(ID_EXIT, "E&xit", " Terminate the program")
        editmenu = wx.Menu()
        helpmenu = wx.Menu()

        # Add items to menubar
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        # create list control to display files, and an input field
        self.list_control = MyListCtrl(self.panel, -1)
        self.list_control.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        # Create a drop-down list menu containing filter options
        list_options = ['File Type', 'Sentiment']
        self.cb1 = wx.ComboBox(self.panel, -1, list_options[0],  size=(100,-1), choices=list_options,)
        self.cb1.Bind(wx.EVT_COMBOBOX, self.onselect_cb1)
        self.cb2 = wx.ComboBox(self.panel, size=(100,-1), choices=['.txt', '.py'])

        # Button to filter files
        self.btn = wx.Button(self.panel, -1, "Filter Files")
        self.btn.Bind(wx.EVT_BUTTON, self.onselect_btn)

        # Create top sizer and the two inner sizers to hold the list and header
        topSizer = wx.BoxSizer(wx.VERTICAL)
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.VERTICAL)

        # Add components to inner sizers, and add those to the top sizer
        inputSizer.Add(self.cb1, 0, wx.ALL, 5)
        inputSizer.Add(self.cb2, 0, wx.ALL, 5)
        inputSizer.Add(self.btn, 0, wx.ALL, 5)
        listSizer.Add(self.list_control, 1, wx.EXPAND|wx.ALL)
        topSizer.Add(inputSizer, 0, wx.EXPAND|wx.ALL, border=15)
        topSizer.Add(listSizer, 1, wx.EXPAND|wx.ALL, border=15)

        # put top sizer inside the panel and display
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        self.Center()
        self.Show(True)

    def onselect_cb1(self, event):
        """"""
        list = []
        self.cb2.Clear()
        self.cb2.SetValue('')
        print "You selected: " + self.cb1.GetStringSelection()
        if self.cb1.GetStringSelection() == 'File Type':
            list = ['.txt', '.py']
        else:
            list = ['Positive', 'Negative']
        self.widget_maker(self.cb2, list)

    def onselect_btn(self, event):
        """"""
        if  self.cb1.GetValue() == "File Type":
            if self.cb2.GetValue() == ".txt":
                print "txt"
                # ADD FILTER SHIT HERE
            else:
                print ".py"


    def widget_maker(self, widget, list):
        """"""
        widget.Clear()
        for item in list:
            widget.Append(item)

    def OnExit(self,e):
        self.Close(True)

    # def OnSize(self, event):
    #     size = self.GetSize()
    #     # self.splitter.SetSashPosition(size.x / 2)
    #     # self.sb.SetStatusText(os.getcwd())
    #     event.Skip()
    #
    # def OnDoubleClick(self, event):
    #     size =  self.GetSize()
    #     #self.splitter.SetSashPosition(size.x / 2)


class FileManager(wx.App):
    def OnInit(self):
        myFrame = MyFrame(None, -1, 'Machine Learning File Manager')
        myFrame.Show(True)
        return True


class File:
    def __init__(self, name, ext, size, mod):
        self.name = name
        self.extension = ext
        self.classification = None
        self.size = size
        self.last_modified = mod



app = FileManager(0)
app.MainLoop()