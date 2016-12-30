import wx
from ObjectListView import ObjectListView, ColumnDefn


########################################################################
class File(object):
    def __init__(self, name, ext, size, mod):
        self.name = name
        self.extension = ext
        self.size = size
        self.last_modified = mod
        self.classification = None

class OLV(ObjectListView):
    def __init__(self, parent):
        ObjectListView.__init__(self, parent,  wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.files = [File("wxPython in Action", "Robin Dunn",
                                      "1932394621", "Manning"),
                                 File("Hello World", "Warren and Carter Sande",
                                      "1933988495", "Manning")
                                 ]

        self.setBooks()

    def setFiles(self, data=None):
        self.SetColumns([
            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("Extension", "left", 200, "extension"),
            ColumnDefn("Size", "right", 100, "size"),
            ColumnDefn("Last Modified", "left", 180, "last_modified"),
            ColumnDefn("Classification", "left", 180, "classification")
        ])

        self.SetObjects(self.files)




########################################################################
class MainPanel(wx.Panel):
    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.files = [File("wxPython in Action", "Robin Dunn",
                              "1932394621", "Manning"),
                         File("Hello World", "Warren and Carter Sande",
                              "1933988495", "Manning")
                         ]

        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.setBooks()

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(self.dataOlv, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(mainSizer)

    # ----------------------------------------------------------------------
    def updateControl(self, event):
        """

        """

        data = self.files
        self.dataOlv.SetObjects(data)

    # ----------------------------------------------------------------------
    def setBooks(self, data=None):
        self.dataOlv.SetColumns([
            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("Extension", "left", 200, "extension"),
            ColumnDefn("Size", "right", 100, "size"),
            ColumnDefn("Last Modified", "left", 180, "last_modified"),
            ColumnDefn("Classification", "left", 180, "classification")
        ])

        self.dataOlv.SetObjects(self.files)


########################################################################
class MainFrame(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="ObjectListView Demo", size=(800, 600))
        # panel = MainPanel(self)
        panel = wx.Panel(self, wx.ID_ANY)
        olv = OLV(panel)


########################################################################
class GenApp(wx.App):
    # ----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    # ----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True


# ----------------------------------------------------------------------
def main():
    """
    Run the demo
    """
    app = GenApp()
    app.MainLoop()


if __name__ == "__main__":
    main()