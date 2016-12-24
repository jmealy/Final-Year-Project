#!/usr/bin/python

import wx
import os
import time


ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        dir = os.listdir('.')

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

        #self.InsertStringItem(0, '..')

        for j, file in enumerate(dir):
            (name, ext) = os.path.splitext(file)
            ex = ext[1:]
            size = os.path.getsize(file)
            sec = os.path.getmtime(file)
            self.InsertStringItem(j, name)
            self.SetStringItem(j, 1, ex)
            self.SetStringItem(j, 2, str(size) + ' B')
            self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M', time.localtime(sec)))

            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        p1 = MyListCtrl(self.splitter, -1)
        p2 = MyListCtrl(self.splitter, -1)
        self.splitter.SplitVertically(p1, p2)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=ID_SPLITTER)

        filemenu= wx.Menu()
        filemenu.Append(ID_EXIT,"E&xit"," Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        tb = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        tb.AddSeparator()
        tb.Realize()

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)


        button8 = wx.Button(self, ID_EXIT, "F10 Quit")

        self.sizer2.Add(button8, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnExit, id=ID_EXIT)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter,1,wx.EXPAND)
        #self.sizer.Add(self.sizer2,0,wx.EXPAND)
        self.SetSizer(self.sizer)

        size = wx.DisplaySize()
        self.SetSize(size)

        self.sb = self.CreateStatusBar()
        self.Center()
        self.Show(True)


    def OnExit(self,e):
        self.Close(True)

    def OnSize(self, event):
        size = self.GetSize()
        #self.splitter.SetSashPosition(size.x / 2)
        #self.sb.SetStatusText(os.getcwd())
        event.Skip()


    def OnDoubleClick(self, event):
        size =  self.GetSize()
        #self.splitter.SetSashPosition(size.x / 2)


class FileManager(wx.App):
    def OnInit(self):
        myFrame = MyFrame(None, -1, 'Machine Learning File Manager')
        myFrame.Show(True)
        return True

app = FileManager(0)
app.MainLoop()