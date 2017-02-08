#!/usr/bin/python

import wx
import os
import time
from ObjectListView import ObjectListView, ColumnDefn
from sentiment import classify

ID_EXIT = 200


class FileManager(wx.App):
    def OnInit(self):
        myFrame = MainFrame(None, -1, 'Machine Learning File Manager')
        myFrame.Show(True)
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        """constructor"""
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
        self.cb1 = wx.ComboBox(self.panel, -1, 'Choose Classifier',  size=(135, -1))
        self.widget_maker(self.cb1)
        self.cb1.Bind(wx.EVT_COMBOBOX, self.onselect_cb1)

        # Button to classify files
        self.btn1 = wx.Button(self.panel, -1, "Classify Files")
        self.btn1.Disable()
        self.btn1.Bind(wx.EVT_BUTTON, self.onselect_btn1)
        self.btn2 = wx.Button(self.panel, -1, "Create Classifier")
        self.btn2.Bind(wx.EVT_BUTTON, self.onselect_btn2)

        # Create top sizer and the two inner sizers to hold the list and header
        topSizer = wx.BoxSizer(wx.VERTICAL)
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add components to inner sizers, and add those to the top sizer
        inputSizer.Add(self.cb1, 0, wx.ALL, 5)
        inputSizer.Add(self.btn2, 0, wx.ALL, 5)
        # inputSizer.Add((150, -1), 1, flag = wx.EXPAND | wx.ALIGN_RIGHT)
        inputSizer.Add(self.btn1, 0, wx.ALL, 5)
        listSizer.Add(self.olv, 1, wx.EXPAND|wx.ALL)
        topSizer.Add(inputSizer, 0, wx.EXPAND|wx.ALL, border=15)
        topSizer.Add(listSizer, 1, wx.EXPAND|wx.ALL, border=15)

        # put top sizer inside the panel and display
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        self.Center()
        self.Show(True)

    def onselect_cb1(self, event):
        # Enable the Classify Button only when a classifier is selected.
        self.btn1.Enable()

    def onselect_btn1(self, event):
        """Classify Files Button"""
        predicted_vals = classify(self.olv.file_contents, self.cb1.GetStringSelection())
        # Update classification column with the predicted classifications.
        self.olv.set_classes(predicted_vals)

    def onselect_btn2(self, event):
        """"""
        frame = PopupWindow()
        frame.Show()

    def widget_maker(self, widget):
        """Get all the existing classifiers and display in the combobox as options"""
        widget.Clear()
        for fil in os.listdir('classifiers/'):
            # adds name of classifier file to combobox
            widget.Append(os.path.splitext(fil)[0])

    def OnExit(self,e):
        self.Close(True)


class ListView(ObjectListView):
    def __init__(self, parent):
        ObjectListView.__init__(self, parent,  wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.files = []  # Files being displayed in the ListView.
        self.file_contents = []
        self.set_files()  # Call method to populate the ListView.

    def set_files(self, data=None):
        direc = 'working_data/txt_sentoken/'
        file_names = os.listdir(direc)
        for fil in file_names:
            (name, ext) = os.path.splitext(fil)
            ex = ext[1:]
            size = os.path.getsize(direc + fil)
            modif = os.path.getmtime(direc + fil)
            with file(direc + fil) as f:
                contents = f.read()
            f = File(name, ex, size, modif)
            self.file_contents.append(contents)
            self.files.append(f)

        self.SetColumns([
            ColumnDefn("Name", "left", 220, "name", isSpaceFilling=True),
            ColumnDefn("Extension", "left", 100, "Extension"),
            ColumnDefn("Size", "left", 100, "size"),
            ColumnDefn("Last Modified", "left", 150, "last_modified"),
            ColumnDefn("Classification", "left", 150, "classification")
        ])
        self.SetObjects(self.files)

    # def filter_files(self, attribute, value):
    #     if value == 'All Files':
    #         self.SetObjects(self.files)
    #     else:
    #         filtered = [f for f in self.files if getattr(f, attribute) == value]
    #         self.SetObjects(filtered)

    def set_classes(self, classes):
        """Assign classifications to files in list and display them."""
        for i, f in enumerate(self.files):
            f.classification = classes[i]
        self.SetObjects(self.files)


class File:
    def __init__(self, name, ext, size, mod):
        self.name = name
        self.Extension = ext
        self.classification = None
        self.size = size
        self.last_modified = mod


class PopupWindow(wx.Frame):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Create Classifier", size= (550, 200),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # define sizers and grid layout of popup
        panel = wx.Panel(self)
        dir_sizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(3, 2, 9, 100)

        # define text and input boxes
        txt1 = wx.StaticText(panel, label="Classifier Name:")
        txt2 = wx.StaticText(panel, label="Training Data Directory:")
        input1 = wx.TextCtrl(panel)
        # make this input a class variable so it can be modified from the button handler
        self.input2 = wx.TextCtrl(panel, size=(255, 30))
        # define buttons
        dir_btn = wx.Button(panel, label="...", size=(30, 30))
        dir_btn.Bind(wx.EVT_BUTTON, self.on_dir)

        # add directory dialogue and text input to sizer
        dir_sizer.Add(self.input2, 1, flag = wx.EXPAND | wx.ALIGN_RIGHT)
        dir_sizer.Add(dir_btn)

        # add all elements to the grid layout
        grid.AddMany([txt1, (input1, 1, wx.EXPAND), txt2,
                      dir_sizer])

        grid.AddGrowableCol(1, 2)

        # sizer to hold "close" & "ok" buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(panel, label='Ok', size=(70, 30))
        ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        close_btn = wx.Button(panel, label='Close', size=(70, 30))
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        hbox.Add(ok_btn, flag=wx.LEFT | wx.BOTTOM, border=5)
        hbox.Add(close_btn, flag=wx.LEFT | wx.BOTTOM, border=5)

        topSizer.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        topSizer.Add(hbox, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        panel.SetSizer(topSizer)

    def on_dir(self, event):
        """
        Show the DirDialog and print the user's choice to input box
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.input2.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_close(self, event):
        """"""
        self.Close(True)

    def on_ok(self, event):
        """"""
        self.Close(True)



app = FileManager(0)
app.MainLoop()