#!/usr/bin/python
import wx
import os
import time
from ObjectListView import ObjectListView, ColumnDefn
import classification

ID_EXIT = 200
working_data = 'working_data/3topics/'


class FileManager(wx.App):
    def OnInit(self):
        myFrame = MainFrame(None, -1, 'Machine Learning File Manager')
        myFrame.Show(True)
        return True


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        """Constructor method. This will set up the components of the main window, and their sizes and positions."""
        wx.Frame.__init__(self, parent, -1, title)
        self.Maximize(True)

        # Create a panel to make sure it looks right on all systems
        self.panel = wx.Panel(self, wx.ID_ANY)

        # create the Menubar items
        filemenu = wx.Menu()
        filemenu.Append(ID_EXIT, "&Exit", " Terminate the program")
        m_open = filemenu.Append(101, '&Open', 'Open a new directory of Documetns')
        self.Bind(wx.EVT_MENU, self.on_open, m_open)
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
        self.btn_import = wx.Button(self.panel, -1, "Import Files")
        self.btn_import.Bind(wx.EVT_BUTTON, self.onselect_btn_import)
        #self.cb1 = wx.ComboBox(self.panel, -1, 'Choose Classifier',  size=(135, -1))
        #self.display_classifiers()
        #self.cb1.Bind(wx.EVT_COMBOBOX, self.onselect_cb1)

        # Button to classify files.
        self.btn_export = wx.Button(self.panel, -1, "Classify Files")
        # button is greyed out untill classifier is selected.
        self.btn_export.Disable()
        self.btn_export.Bind(wx.EVT_BUTTON, self.onselect_btn_export)
        # Button to create a custom classifier.
        self.btn_classify = wx.Button(self.panel, -1, "Create Classifier")
        self.btn_classify.Bind(wx.EVT_BUTTON, self.onselect_btn_classify)

        # Create top sizer and the two inner sizers to hold the list and header bar
        topSizer = wx.BoxSizer(wx.VERTICAL)
        inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        listSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add components to inner sizers, and add those to the top sizer
        inputSizer.Add(self.btn_import, 0, wx.ALL, 5)
        inputSizer.Add(self.btn_classify, 0, wx.ALL, 5)
        # inputSizer.Add((150, -1), 1, flag = wx.EXPAND | wx.ALIGN_RIGHT)
        inputSizer.Add(self.btn_export, 0, wx.ALL, 5)
        listSizer.Add(self.olv, 1, wx.EXPAND|wx.ALL)
        topSizer.Add(inputSizer, 0, wx.EXPAND|wx.ALL, border=15)
        topSizer.Add(listSizer, 1, wx.EXPAND|wx.ALL, border=15)

        # put top sizer inside the panel and display
        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)
        self.Center()
        self.Show(True)

    def onselect_btn_export(self, event):
        """"""
        # [tk] open up working files

    def onselect_btn_import(self, event):
        """Import Files Button"""
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           # | wx.DD_DIR_MUST_EXIST
                           # | wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            self.olv.directory = dlg.GetPath() +'/'
            self.olv.set_files()
        dlg.Destroy()

    def onselect_btn_classify(self, event):
        """Open window to create and use a classifier"""
        frame = PopupWindow(self)
        frame.Show()

    def on_open(self, event):
        # open working data [tk]
        print "yaa"

    def OnExit(self,e):
        self.Close(True)


class ListView(ObjectListView):
    def __init__(self, parent):
        ObjectListView.__init__(self, parent,  wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.directory = ''
        self.files = []  # Files being displayed in the ListView.
        self.file_contents = []
        # self.set_files()  # Call method to populate the ListView.

    def set_files(self, data=None):
        """
        Description needed.[tk]
        """
        #clear old values
        self.files = []
        self.file_contents = []
        classification.remove_incompatible_files(self.directory)
        file_names = os.listdir(self.directory)
        for fil in file_names:
            (name, ext) = os.path.splitext(fil)
            ex = ext[1:]
            size = os.path.getsize(self.directory + fil)
            modif = os.path.getmtime(self.directory + fil)
            with file(self.directory + fil) as f:
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

    def set_classes(self, classes):
        """Assign classifications to files in list and display them."""
        for i, f in enumerate(self.files):
            f.classification = classes[i]
        self.SetObjects(self.files)


class PopupWindow(wx.Frame):
    """"""
    # ----------------------------------------------------------------------
    def __init__(self, parent_window):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Create Classifier", size= (550, 320),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        # get reference to the MainFrame window calling the popup. Allows popup to update the list controll of parent.
        self.parent_window = parent_window

        # define sizers and grid layout of popup
        panel = wx.Panel(self)
        topSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.FlexGridSizer(6, 2, 9, 100)

        # input values for user to enter: classifier name and location of training data
        # make them as class variables so they can be accessed by methods
        self.type_input = wx.ComboBox(panel, -1, '',  size=(135, -1))
        self.type_input.Append('Text Classifier (Supervised)')
        self.type_input.Append('Topic Modelling (Unsupervised)')
        self.type_input.Bind(wx.EVT_COMBOBOX, self.onselect_type)
        self.numtopics_input = wx.TextCtrl(panel)
        self.chk_box = wx.CheckBox(panel)
        self.chk_box.Bind(wx.EVT_CHECKBOX, self.onselect_checkbox)
        self.cls_input = wx.ComboBox(panel, -1, '',  size=(135, -1))
        self.display_classifiers()
        self.cls_input.Bind(wx.EVT_COMBOBOX, self.onselect_cls_input)
        self.name_input = wx.TextCtrl(panel)
        self.dir_input = wx.TextCtrl(panel, size=(255, 30))

        # Disable inputs to start. Need to choose classifier first
        self.chk_box.Disable()
        self.cls_input.Disable()
        self.name_input.Disable()
        self.numtopics_input.Disable()
        self.dir_input.Disable()


        # define text for the input boxes
        type_txt = wx.StaticText(panel, label="Classifier Type:")
        numtopics_txt = wx.StaticText(panel, label="Number of Topics:")
        chk_txt = wx.StaticText(panel, label="Use Existing Classifier?")
        cls_txt = wx.StaticText(panel, label="Select Existing Classifier:")
        name_txt = wx.StaticText(panel, label="Classifier Name:")
        dir_txt = wx.StaticText(panel, label="Training Data Directory:")

        # define button for choosing training data directory
        self.dir_btn = wx.Button(panel, label="...", size=(30, 30))
        self.dir_btn.Bind(wx.EVT_BUTTON, self.on_dir)
        self.dir_btn.Disable()

        # add directory dialogue and text input to sizer
        dir_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dir_sizer.Add(self.dir_input, 1, flag = wx.EXPAND | wx.ALIGN_RIGHT)
        dir_sizer.Add(self.dir_btn)

        # add all elements to the grid layout
        grid.AddMany([type_txt, (self.type_input, 1, wx.EXPAND), numtopics_txt, self.numtopics_input, chk_txt, self.chk_box, cls_txt, (self.cls_input, 1, wx.EXPAND),
                      name_txt, (self.name_input, 1, wx.EXPAND), dir_txt, dir_sizer])

        # Define "close" & "ok" buttons, and wrap in a sizer (bottom sizer).
        bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_btn = wx.Button(panel, label='Ok', size=(70, 30))
        self.ok_btn.Disable()
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok)
        close_btn = wx.Button(panel, label='Close', size=(70, 30))
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)
        bottom_sizer.Add(self.ok_btn, flag=wx.LEFT | wx.BOTTOM, border=5)
        bottom_sizer.Add(close_btn, flag=wx.LEFT | wx.BOTTOM, border=5)

        # put grid and the two buttons withing bottom_sizer into topsizer
        topSizer.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        topSizer.Add(bottom_sizer, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        panel.SetSizer(topSizer)

    def display_classifiers(self):
        """Get all the existing classifiers and display in the combobox as options"""
        self.cls_input.Clear()
        for fil in os.listdir('classifiers/'):
            # adds name of classifier file to combobox
            self.cls_input.SetStringSelection(os.path.splitext(fil)[0])
            self.cls_input.Append(os.path.splitext(fil)[0])

    def onselect_cls_input(self, event):
        self.ok_btn.Enable()

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
            self.dir_input.SetValue(dlg.GetPath())
            self.ok_btn.Enable()
        dlg.Destroy()

    def onselect_type(self, event):
        """"""
        if self.type_input.GetValue() == 'Topic Modelling (Unsupervised)':
            self.ok_btn.Enable()
            # Clear and disable classifier name and trainging data input as they are not needed
            self.numtopics_input.Enable()
            self.dir_input.Clear()
            self.dir_input.Disable()
            self.dir_btn.Disable()
            self.chk_box.Disable()
            self.cls_input.Disable()
            self.name_input.Disable()

        # if supervised text classifier is selected, enable relevant inputs
        if self.type_input.GetValue() == 'Text Classifier (Supervised)':
            self.dir_input.Enable()
            self.dir_btn.Enable()
            self.chk_box.Enable()
            self.name_input.Enable()
            # Disable ok button until required information is input by user
            self.ok_btn.Disable()
            self.numtopics_input.Disable()
            self.chk_box.SetValue(False)

    def onselect_checkbox(self, event):
        if self.chk_box.GetValue():
            self.cls_input.Enable()
            self.name_input.Disable()
            self.dir_input.Disable()
            self.dir_btn.Disable()
        else:
            self.cls_input.Disable()
            self.name_input.Enable()
            self.dir_input.Enable()
            self.dir_btn.Enable()

    def on_ok(self, event):
        """confirm selections. Create and save the new classifier"""

        # if name field is empty, use default name.
        if self.name_input.GetValue() == "":
            self.name_input.SetValue('new_classifier')

        # Create the new classifier using the appropriate function, depending on what classifier type is selected
        if self.type_input.GetValue() == 'Text Classifier (Supervised)':
            # check if you need to create a new classifier, or use a saved one.
            if self.chk_box.GetValue():
                labels = classification.load_supervised_classifier(self.cls_input.GetValue(),
                                                          self.parent_window.olv.file_contents)
            else:
                labels = classification.create_supervised_classifier(self.name_input.GetValue(), self.dir_input.GetValue(),
                                                            self.parent_window.olv.file_contents)
            self.parent_window.olv.set_classes(labels)

        if self.type_input.GetValue() == 'Topic Modelling (Unsupervised)':
            num_topics = self.numtopics_input.GetValue()
            if not num_topics:
                # default value for num_topics
                num_topics = 5
            else:
                # ensure that the value entered for num topics is an integer.
                try:
                    num_topics = int(num_topics)
                except ValueError:
                    wx.MessageDialog(self, "Number of Topics: must be an integer", "Warning!",
                                     wx.OK | wx.ICON_WARNING).ShowModal()
                    return
            # create lda model using working data and number of topics entered by the user.
            topics = classification.classify_unsupervised_lda(working_data, num_topics)
            self.parent_window.olv.set_classes(topics)

        # update parent window's classifier list
        self.Close(True)

    def on_close(self, event):
        """Close Popup window"""
        self.Close(True)


class File:
    def __init__(self, name, ext, size, mod):
        self.name = name
        self.Extension = ext
        self.classification = None
        self.size = size
        self.last_modified = mod



app = FileManager(0)
app.MainLoop()