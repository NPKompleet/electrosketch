import wx
import wx.lib.sheet as Sheet
import os, os.path
#import pystache
#import jinja2


#env = jinja2.Environment(autoescape=False,loader=jinja2.FileSystemLoader('templates'))

class mysheets(Sheet.CSheet):
    def __init__(self, parent):
        #wx.grid.Grid.__init__(self, parent)
        Sheet.CSheet.__init__(self, parent)
        self.SetLabelBackgroundColour('#ffaa00')
        self.SetGridLineColour('#ffffff')
        self.SetDefaultCellBackgroundColour('#ffaa00')
        #wx.ScrolledWindow.__init__(self, parent)
        #wx.ScrolledWindow.SetBackgroundColour(wx.RED)
        #self.AppendRows(8)

        data= ['Number of Poles', 'Lenght of Conductor',
               'Number of Pot Insulators', 'Number of Spindles',
               'Number of Fibre Crossarms', 'Number of Tiestraps',
               '5/8 X 6 Bolts and nuts', '5/8 X 8 Bolts and nuts',
               '5/8 X 11 Bolts and nuts', 'Number of Disk insulators',
               'Number of J-hooks', 'Number of 6-Bolt Clamp',
               'Number of Socket Adapter', 'Number of Channel Iron',
               'Lenght of Stay wire', 'Number of Stay Block',
               'Number of Stay Insulator', 'Number of Stay Rods',
               '11/.415kV Transformer', 'D-fuse assembly',
               'Ligthening Arresters', 'Galvanized Earth Rod',
               '70mm2 Copper Wire', '4-Way Feeder Pillar',
               '500mm2 X 1C XLPE cable', '35mm2 X 1C XLPE cable',
               '150mm2 X 4C PVC cable', 'Universal Line Tap',
               'Bimetallic Line Tap', 'Raychem Kit (150mm2 - 185mm2) XLPE I/D',
               'Raychem term. Kit for XLPE O/D','70mm2 cable socket',
               '150mm2 cable socket', '500mm2 cable socket']
        
        self.SetNumberCols(3)
        self.SetNumberRows(len(data))
        self.EnableEditing(False)
        self.SetColSize(0, 170)
        label= ['Item', 'Quantity', 'Unit']
        
        for n in range(3):
            self.SetColLabelValue(n, label[n])

        

        datadict= {'Number of Poles': ['0', 'number'],
               'Lenght of Conductor': ['0', 'meters'],
               'Number of Pot Insulators': ['0', 'number'],
               'Number of Spindles': ['0', 'number'],
               'Number of Fibre Crossarms': ['0', 'number'],
               'Number of Tiestraps': ['0', 'pairs'],
               '5/8 X 6 Bolts and nuts': ['0', 'number'],
               '5/8 X 8 Bolts and nuts': ['0', 'number'],
                '5/8 X 11 Bolts and nuts': ['0', 'number'],
                'Number of Disk insulators': ['0', 'number'],
                'Number of J-hooks': ['0', 'number'],
                'Number of 6-Bolt Clamp': ['0', 'number'],
                'Number of Socket Adapter': ['0', 'number'],
                'Number of Channel Iron': ['0', 'number'],
                'Lenght of Stay wire': ['0', 'meters'],
                'Number of Stay Block': ['0', 'number'],
                'Number of Stay Insulator': ['0', 'number'],
                'Number of Stay Rods': ['0', 'number'],
                '11/.415kV Transformer': ['0', 'number'],
                'D-fuse assembly': ['0', 'set'],
                'Ligthening Arresters': ['0', 'set'],
                'Galvanized Earth Rod': ['0', 'number'],
                '70mm2 Copper Wire': ['0', 'meters'],
                '4-Way Feeder Pillar': ['0', 'number'],
                '500mm2 X 1C XLPE cable': ['0', 'meters'],
                '35mm2 X 1C XLPE cable': ['0', 'meters'],
                '150mm2 X 4C PVC cable': ['0', 'meters'],
                'Universal Line Tap': ['0', 'number'],
                'Bimetallic Line Tap': ['0', 'number'],
                'Raychem Kit (150mm2 - 185mm2) XLPE I/D': ['0', 'kit'],
                'Raychem term. Kit for XLPE O/D': ['0', 'kit'],
                '70mm2 cable socket': ['0', 'number'],
                '150mm2 cable socket': ['0', 'number'],
                '500mm2 cable socket': ['0', 'number']
            }
        
        
        for i in range(len(data)):
            self.SetCellValue(i,0,data[i])
##            self.SetCellValue(i,1,datadict[data[i]][0])
            self.SetCellValue(i,1,'0')
            self.SetCellValue(i,2,datadict[data[i]][1])



        


##        for item in data:
##            t=(item, str(datadict[item][0]), str(datadict[item][1]))
##            #self.Append(t)
##            for u in range(len(data)):
##                for v in range(len(t)):
##                    self.SetCellValue(u,v, t[v])
##            
        #self.SetBackgroundColour(wx.BLUE)
        #self.Refresh()

        


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super(ListPanel, self).__init__(parent, style=wx.RAISED_BORDER)
        # Attributes
        self.sheet = mysheets(self)
        
        button= wx.Button(self, -1, 'Create SpreadSheet')
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.sheet, 1, wx.EXPAND)
        sizer.Add(button, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(sizer)
        # Event Handlers
        #self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

        self.Bind(wx.EVT_BUTTON, self.OnButton)
        
##    def OnItemSelected(self, event):
##        selected_row = event.GetIndex()
##        val = list()
##        for column in range(3):
##            item = self.lst.GetItem(selected_row, column)
##            val.append(item.GetText())
##        # Show what was selected in the frames status bar
##        frame = self.GetTopLevelParent()
##        frame.PushStatusText(",".join(val))


    def Replace(self, strng, dic):
        for(k,v) in dic.items():
            strng= strng.replace(k,str(v))
        return strng


    def OnButton(self, evt):
        subdict={'{{Poles}}': self.sheet.GetCellValue(0,1),
               '{{Conductors}}': self.sheet.GetCellValue(1,1),
               '{{PInsulators}}': self.sheet.GetCellValue(2,1),
               '{{Spindles}}': self.sheet.GetCellValue(3,1),
               '{{FCrossarms}}': self.sheet.GetCellValue(4,1),
               '{{Tiestraps}}': self.sheet.GetCellValue(5,1),
               '{{5/8X6}}': self.sheet.GetCellValue(6,1),
               '{{5/8X8}}': self.sheet.GetCellValue(7,1),
                '{{5/8X11}}': self.sheet.GetCellValue(8,1),
                '{{DInsulators}}': self.sheet.GetCellValue(9,1),
                '{{J-hooks}}': self.sheet.GetCellValue(10,1),
                '{{6BClamps}}': self.sheet.GetCellValue(11,1)
                 }
        

        
        wildcard = "Python source (*.py)|*.py|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "XML files (*.xml)|*.xml|"    \
           "XLS files (*.xls)|*.xls|"    \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"
        
        print "CWD: %s\n" % os.getcwd()

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'save' dialog.
        #
        # Unlike the 'open dialog' example found elsewhere, this example does NOT
        # force the current working directory to change if the user chooses a different
        # directory than the one initially set.
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE|wx.OVERWRITE_PROMPT)

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print'You selected "%s"' % path
            print subdict['{{Poles}}'] + 'is the thing'
            #data= "import wx, os\nprint 'good'"
            f= open('templates/sanctiontemplate.xml', 'r')
            t= f.read()
##            t= t.replace('{{Poles}}', str(subdict['{{Poles}}']))
##            t= t.replace('{{Conductors}}', '600')
##            t= t.replace('{{PInsulators}}', '600')
##            t= t.replace('{{Spindles}}', '600')
##            t= t.replace('{{FCrossarms}}', '600')
##            t= t.replace('{{Tiestraps}}', '600')
##            t= t.replace('{{5/8X6}}', '600')
##            t= t.replace('{{5/8X8}}', '600')
##            t= t.replace('{{5/8X11}}', '600')
##            t= t.replace('{{DInsulators}}', '600')
##            t= t.replace('{{J-hooks}}', '600')
##            t= t.replace('{{6BClamps}}', '600')
            s= self.Replace(t, subdict)
##            data= pystache.render(str(t), {'pole':'550'})
##            print data
            #print t
            f.close()

##            template= env.get_template('sanctiontemplate.xml')
##            data=template.render({'pole':'550'})
##            print data

            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
##            fp = open(path, 'w') # Create file anew
##            fp.write(data)
##            fp.close()

            fp = open(path, 'w')
            fp.write(s)
            fp.close()
            #
            # You might want to add some error checking :-)
            #

        # Note that the current working dir didn't change. This is good since
        # that's the way we set it up.
##        print"CWD: %s\n" % os.getcwd()

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

        



##class myframe(wx.Frame):
##    def __init__(self, parent):
##        wx.Frame.__init__(self, parent)
##        mypanel= ListPanel(self)
##        #mysheet.SetBackgroundColour(wx.BLUE)
##        self.Center()
##        #self.SetBackgroundColour(wx.BLUE)
##        self.Show()
##
##if __name__== '__main__':
##    myapp= wx.App()
##    frame= myframe(None)
##    myapp.MainLoop()


class ListFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(420, 200),
                          style= wx.MINIMIZE_BOX|wx.CAPTION
                          |wx.CLOSE_BOX|wx.CLIP_CHILDREN|wx.SYSTEM_MENU)
        self.panel= ListPanel(self)

        #App Icon
        path = os.path.abspath("./ik_icon2.ico")
        icon= wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        self.Center()
        #self.Show(True)

if __name__ == "__main__":
    app= wx.App()
    L=ListFrame(None, -1, "LISTCTRL")
    L.Show(True)
    app.MainLoop()

