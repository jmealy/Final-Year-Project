#!/usr/bin/python

import wx
import os
import time
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
from ObjectListView import ObjectListView, ColumnDefn


ID_EXIT = 200


class FileManager(wx.App):
    def OnInit(self):
        myFrame = MainFrame(None, -1, 'Machine Learning File Manager')
        myFrame.Show(True)
        return True


class MainFrame(wx.Frame):
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

        # create object list view to display files, and an input field
        self.olv = ListView(self.panel)

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
        listSizer.Add(self.olv, 1, wx.EXPAND|wx.ALL)
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


class ListView(ObjectListView):
    def __init__(self, parent):
        ObjectListView.__init__(self, parent,  wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.files = []
        direc = os.listdir('.')
        for j, fil in enumerate(direc):
            (name, ext) = os.path.splitext(fil)
            ex = ext[1:]
            size = os.path.getsize(fil)
            modif = os.path.getmtime(fil)
            f = File(name, ex, size, modif)
            self.files.append(f)

        self.setFiles()

    def setFiles(self, data=None):
        self.SetColumns([
            ColumnDefn("Name", "left", 220, "name", isSpaceFilling=True),
            ColumnDefn("Extension", "left", 100, "extension"),
            ColumnDefn("Size", "left", 100, "size"),
            ColumnDefn("Last Modified", "left", 150, "last_modified"),
            ColumnDefn("Classification", "left", 150, "classification")
        ])
        self.SetObjects(self.files)


class File:
    def __init__(self, name, ext, size, mod):
        self.name = name
        self.extension = ext
        self.classification = None
        self.size = size
        self.last_modified = mod



app = FileManager(0)
app.MainLoop()