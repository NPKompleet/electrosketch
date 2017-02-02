import wx
import wx.html
import cPickle
import os

#from Listing import * 
from sheet import *

from wx.lib import buttons

from example1 import SketchWindow


class SketchFrame(wx.Frame):
    def __init__(self, parent):
        self.title = "Sanction Sketch Frame"
        wx.Frame.__init__(self, parent, -1, self.title,
                size=(800,600))
        self.Maximize()
        path = os.path.abspath("./ik_icon2.ico")
        icon= wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.filename = ""
        self.sketch = SketchWindow(self, -1)
        self.listing= ListPanel(self)
        
        #print self.listing.lst.GetTopItem().GetItemText()
        self.toolSelect="imageicons/freehandicon2.png"
        wx.EVT_MOTION(self.sketch, self.OnSketchMotion)
        self.initStatusBar()
        self.createMenuBar()
        self.createToolBar()
        self.createPanel()

    def createPanel(self):
        controlPanel = ControlPanel(self, -1, self.sketch)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(controlPanel, 0, wx.EXPAND)
        box.Add(self.sketch, 3, wx.EXPAND)
        box.Add(self.listing, 1, wx.EXPAND)
        
        self.SetSizer(box)

    def initStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def OnSketchMotion(self, event):
        self.statusbar.SetStatusText("Pos: %s" %
                str(event.GetPositionTuple()), 0)
        self.statusbar.SetStatusText("Current Pts: %s" %
                len(self.sketch.curLine), 1)
        self.statusbar.SetStatusText("Line Count: %s" %
                len(self.sketch.lines), 2)
        event.Skip()

    def menuData(self):
        return [("&File", (
                    ("&New", "New Sketch file", self.OnNew),
                    ("&Open", "Open sketch file", self.OnOpen),
                    ("&Save", "Save sketch file", self.OnSave),
                    ("", "", ""),
                    ("&Color", (
                        ("&Black", "", self.OnColor, wx.ITEM_RADIO),
                        ("&Red", "", self.OnColor, wx.ITEM_RADIO),
                        ("&Green", "", self.OnColor, wx.ITEM_RADIO),
                        ("&Blue", "", self.OnColor, wx.ITEM_RADIO),
                        ("&Other...", "", self.OnOtherColor, wx.ITEM_RADIO))),
                    ("", "", ""),
                    ("About...", "Show about window", self.OnAbout),
                    ("&Quit", "Quit", self.OnCloseWindow)))]

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.AppendMenu(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def createToolBar(self):
        toolbar = self.CreateToolBar()
        for each in self.toolbarData():
            self.createSimpleTool(toolbar, *each)
        toolbar.AddSeparator()
        for each in self.toolbarColorData():
            self.createColorTool(toolbar, each)
        toolbar.Realize()

    def createSimpleTool(self, toolbar, label, filename, help, handler):
        if not label:
            toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        tool = toolbar.AddSimpleTool(-1, bmp, label, help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def toolbarData(self):
        return (("New", "new.bmp", "Create new sketch", self.OnNew),
                ("", "", "", ""),
                ("Open", "open.bmp", "Open existing sketch", self.OnOpen),
                ("Save", "save.bmp", "Save existing sketch", self.OnSave))

    def createColorTool(self, toolbar, color):
        bmp = self.MakeBitmap(color)
        tool = toolbar.AddRadioTool(-1, bmp, shortHelp=color)
        self.Bind(wx.EVT_MENU, self.OnColor, tool)

    def MakeBitmap(self, color):
        bmp = wx.EmptyBitmap(16, 15)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(color))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def toolbarColorData(self):
        return ("Black", "Red", "Green", "Blue")

    def OnNew(self, event): pass

    def OnColor(self, event):
        menubar = self.GetMenuBar()
        itemId = event.GetId()
        item = menubar.FindItemById(itemId)
        if not item:
            toolbar = self.GetToolBar()
            item = toolbar.FindById(itemId)
            color = item.GetShortHelp()
        else:
            color = item.GetLabel()
        self.sketch.SetColor(color)

    def OnCloseWindow(self, event):
        self.Destroy()

    def SaveFile(self):
        if self.filename:
            data = self.sketch.GetLinesData()
            f = open(self.filename, 'w')
            cPickle.dump(data, f)
            f.close()

    def ReadFile(self):
        if self.filename:
            try:
                f = open(self.filename, 'r')
                data = cPickle.load(f)
                f.close()
                self.sketch.SetLinesData(data)
            except cPickle.UnpicklingError:
                wx.MessageBox("%s is not a sketch file." % self.filename,
                             "oops!", style=wx.OK|wx.ICON_EXCLAMATION)

    wildcard = "Sketch files (*.sketch)|*.sketch|All files (*.*)|*.*"

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, "Open sketch file...", os.getcwd(),
                           style=wx.OPEN, wildcard=self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def OnSave(self, event):
        if not self.filename:
            self.OnSaveAs(event)
        else:
            self.SaveFile()

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(self, "Save sketch as...", os.getcwd(),
                           style=wx.SAVE | wx.OVERWRITE_PROMPT,
                           wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.sketch'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def OnOtherColor(self, event):
        dlg = wx.ColourDialog(frame)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            self.sketch.SetColor(dlg.GetColourData().GetColour())
        dlg.Destroy()

    def OnAbout(self, event):
        dlg = SketchAbout(self)
        dlg.ShowModal()
        dlg.Destroy()


class SketchAbout(wx.Dialog):
    text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0"
cellpadding="0" border="1">
<tr>
    <td align="center"><h1>Sketch!</h1></td>
</tr>
</table>
</center>
<p><b>Sketch</b> is a demonstration program for <b>wxPython In Action</b>
Chapter 7.  It is based on the SuperDoodle demo included with wxPython,
available at http://www.wxpython.org/
</p>

<p><b>SuperDoodle</b> and <b>wxPython</b> are brought to you by
<b>Robin Dunn</b> and <b>Total Control Software</b>, Copyright
&copy; 1997-2006.</p>
</body>
</html>
'''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About Sketch',
                          size=(440, 400) )

        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "Okay")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.SetSizer(sizer)
        self.Layout()



class ControlPanel(wx.Panel):

    BMP_SIZE = 16
    BMP_BORDER = 3
    NUM_COLS = 4
    SPACING = 4

    colorList = ('Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple',
              'Brown', 'Aquamarine', 'Forest Green', 'Light Blue',
              'Goldenrod', 'Cyan', 'Orange', 'Navy', 'Dark Grey',
              'Light Grey')
    maxThickness = 16

    maintool= ("imageicons/freehandicon2.png", "imageicons/linedrawicon.png",
               "imageicons/rectdrawicon.png","imageicons/circledrawicon.png",
               "imageicons/polexdrawicon.png", "imageicons/poledrawicon.png",
               "imageicons/Hpolexdrawicon.png", "imageicons/Hpoledrawicon.png",
               "imageicons/transformericon.png", "imageicons/erasericon.png")

    maintoolstatus= {"imageicons/freehandicon2.png":'Freehand Draw....', "imageicons/linedrawicon.png":'Draw a Line....',
               "imageicons/rectdrawicon.png":'Draw a Rectangle....',"imageicons/circledrawicon.png":'Draw a Circle....',
               "imageicons/polexdrawicon.png":'Place an Existing Pole....', "imageicons/poledrawicon.png":'Place a Proposed Pole....',
                "imageicons/Hpolexdrawicon.png":'Place an Existing Hpole', "imageicons/Hpoledrawicon.png":'Place an Hpole',
               "imageicons/transformericon.png":'Place a Tranformer....', "imageicons/erasericon.png":'Erase a Free draw....'}
    

    def __init__(self, parent, ID, sketch):
        wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
        self.sketch = sketch
        buttonSize = (self.BMP_SIZE + 2 * self.BMP_BORDER,
                      self.BMP_SIZE + 2 * self.BMP_BORDER)
        colorGrid = self.createColorGrid(parent, buttonSize)
        thicknessGrid = self.createThicknessGrid(buttonSize)
        maintoolpanel= self.createMainTool()
        self.layout(colorGrid, thicknessGrid, maintoolpanel)

##        bmp = wx.EmptyBitmap(31, 31)
##        dc = wx.MemoryDC()
##        dc.SetBackground(wx.Brush(wx.BLUE))
##        dc.SelectObject(bmp)
##        dc.SetPen(wx.Pen(wx.BLACK, 2))
##        dc.SetBrush(wx.WHITE_BRUSH)
##        dc.DrawRectangle(0,0,31,31)
##        dc.SetBrush(wx.WHITE_BRUSH)
##        dc.DrawCircle(16,16,11)
        
        
        #dc.Clear()
##        dc.SelectObject(wx.NullBitmap)
##        b = buttons.GenBitmapToggleButton(self, -1, bmp, size=(34,34))
        #b.SetForegroundColour(wx.WHITE)
##        b.SetBezelWidth(1)
##        b.SetUseFocusIndicator(False)

        #bmp=wx.Image("imageicons/penciliconbmp.bmp", type=wx.BITMAP_TYPE_BMP).ConvertToBitmap()
       
        
        

        self.SetBackgroundColour("#ffaa00")

    def createColorGrid(self, parent, buttonSize):
        self.colorMap = {}
        self.colorButtons = {}
        colorGrid = wx.GridSizer(cols=self.NUM_COLS, hgap=2, vgap=2)
        for eachColor in self.colorList:
            bmp = parent.MakeBitmap(eachColor)
            b = buttons.GenBitmapToggleButton(self, -1, bmp, size=buttonSize)
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.OnSetColour, b)
            colorGrid.Add(b, 0)
            self.colorMap[b.GetId()] = eachColor
            self.colorButtons[eachColor] = b
        self.colorButtons[self.colorList[0]].SetToggle(True)
        return colorGrid

    def createThicknessGrid(self, buttonSize):
        self.thicknessIdMap = {}
        self.thicknessButtons = {}
        thicknessGrid = wx.GridSizer(cols=self.NUM_COLS, hgap=2, vgap=2)
        for x in range(1, self.maxThickness + 1):
            b = buttons.GenToggleButton(self, -1, str(x), size=buttonSize)
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.OnSetThickness, b)
            thicknessGrid.Add(b, 0)
            self.thicknessIdMap[b.GetId()] = x
            self.thicknessButtons[x] = b
        self.thicknessButtons[1].SetToggle(True)
        return thicknessGrid



    def createMainTool(self):
        self.toolIdMap={}
        self.maintoolButtons={}
        compGrid= wx.GridSizer(cols=2,hgap=0,vgap=0)
        self.panel=wx.Panel(self, style=wx.SUNKEN_BORDER)
        for eachtool in self.maintool:
            bmp= wx.Bitmap(eachtool, type=wx.BITMAP_TYPE_PNG)
            b= buttons.GenBitmapToggleButton(self.panel, -1, bmp, size=(35,35))
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.OnSetTool, b)
            self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter, b)
            compGrid.Add(b,0)
            self.toolIdMap[b.GetId()]= eachtool
            self.maintoolButtons[eachtool]=b
        self.maintoolButtons[self.maintool[0]].SetToggle(True)
        self.toolselected= self.maintoolButtons[self.maintool[0]].GetId()
        self.GetParent().toolSelect= self.maintool[0]
        self.panel.SetSizer(compGrid)
        return self.panel
    

    def layout(self, colorGrid, thicknessGrid, panel):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(colorGrid, 0, wx.ALL, self.SPACING)
        box.Add(thicknessGrid, 0, wx.ALL, self.SPACING)

        #sboxm = wx.StaticBox(self, label="")
        
        #sboxm.SetBackgroundColour("#222222")
        #sboxszm = wx.BoxSizer(wx.VERTICAL)
##        self.panel=wx.Panel(self, style=wx.SUNKEN_BORDER)
##        #self.panel.SetBackgroundColour(wx.BLUE)
##        
##        compGrid= wx.GridSizer(cols=2,hgap=0,vgap=0)
##        
##        bmp0=wx.Bitmap("imageicons/linedrawicon.png", type=wx.BITMAP_TYPE_PNG)
##        b0 = buttons.GenBitmapToggleButton(self.panel, -1, bmp0, size=(35,35))
##        b0.SetBezelWidth(1)
##        b0.SetUseFocusIndicator(False)
##        compGrid.Add(b0,0)
##
##        bmp1=wx.Bitmap("imageicons/rectdrawicon.png", type=wx.BITMAP_TYPE_PNG)
##        b1 = buttons.GenBitmapToggleButton(self.panel, -1, bmp1, size=(35,35))
##        b1.SetBezelWidth(1)
##        b1.SetUseFocusIndicator(False)
##        compGrid.Add(b1,0)
##
##        bmp2=wx.Bitmap("imageicons/circledrawicon.png", type=wx.BITMAP_TYPE_PNG)
##        b2 = buttons.GenBitmapToggleButton(self.panel, -1, bmp2, size=(35,35))
##        b2.SetBezelWidth(1)
##        b2.SetUseFocusIndicator(False)
##        compGrid.Add(b2,0)
##
##        bmp3=wx.Bitmap("imageicons/freehandicon2.png", type=wx.BITMAP_TYPE_PNG)
##        b3 = buttons.GenBitmapToggleButton(self.panel, -1, bmp3, size=(35,35))
##        b3.SetBezelWidth(1)
##        b3.SetUseFocusIndicator(False)
##        compGrid.Add(b3,0)
##
##        bmp4=wx.Bitmap("imageicons/polexdrawicon.png", type=wx.BITMAP_TYPE_PNG)
##        b4 = buttons.GenBitmapToggleButton(self.panel, -1, bmp4, size=(35,35))
##        b4.SetBezelWidth(1)
##        b4.SetUseFocusIndicator(False)
##        compGrid.Add(b4,0)
##
##        bmp5=wx.Bitmap("imageicons/poledrawicon.png", type=wx.BITMAP_TYPE_PNG)
##        b5 = buttons.GenBitmapToggleButton(self.panel, -1, bmp5, size=(35,35))
##        b5.SetBezelWidth(1)
##        b5.SetUseFocusIndicator(False)
##        compGrid.Add(b5,0)
##
##        bmp14=wx.Bitmap("imageicons/erasericon.png", type=wx.BITMAP_TYPE_PNG)
##        b14 = buttons.GenBitmapToggleButton(self.panel, -1, bmp14, size=(35,35))
##        b14.SetBezelWidth(1)
##        b14.SetUseFocusIndicator(False)
##        compGrid.Add(b14,0)
##        
##
##        #sboxszm.Add(compGrid, 0, wx.EXPAND)
##        self.panel.SetSizer(compGrid)
        
        #sboxszm.Add(self.panel, 0, wx.EXPAND)
        #box.Add(sboxszm, 0, wx.ALL|wx.ALIGN_CENTER, self.SPACING)

        box.Add(panel, 0, wx.ALL|wx.ALIGN_CENTER, self.SPACING)
        

        #box.Add(compGrid, 0, wx.ALL|wx.ALIGN_CENTER, self.SPACING)
        
        self.SetSizer(box)
        box.Fit(self)

    def OnSetColour(self, event):
        color = self.colorMap[event.GetId()]
        if color != self.sketch.color:
            self.colorButtons[self.sketch.color].SetToggle(False)
        self.sketch.SetColor(color)

    def OnSetThickness(self, event):
        thickness = self.thicknessIdMap[event.GetId()]
        if thickness != self.sketch.thickness:
            self.thicknessButtons[self.sketch.thickness].SetToggle(False)
        self.sketch.SetThickness(thickness)

    def OnSetTool(self, event):
        toolId = event.GetId()
        if toolId != self.toolselected:
            t=self.toolIdMap[self.toolselected]
            label= self.toolIdMap[toolId]
            self.GetTopLevelParent().statusbar.SetStatusText(self.maintoolstatus[label], 0)
            self.maintoolButtons[t].SetToggle(False)
            self.toolselected= toolId
            self.GetParent().toolSelect= label

        else:
            t=self.toolIdMap[self.toolselected]
            self.maintoolButtons[t].SetToggle(True)
        #event.Skip()
        #self.sketch.SetColor(color)

    def OnEnter(self, event):
        butId = event.GetId()
        label= self.toolIdMap[butId]
        self.GetTopLevelParent().statusbar.SetStatusText(self.maintoolstatus[label], 0)
        


class SketchApp(wx.App):

    def OnInit(self):
##        bmp = wx.Image("splash.png").ConvertToBitmap()
##        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
##                1000, None, -1)
        wx.Yield()

        frame = SketchFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = SketchApp(False)
    app.MainLoop()
