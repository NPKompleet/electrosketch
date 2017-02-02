##This app was written to help generate a sanction or BEME for the
##department of Distribution planning and System Integration of the
##Ikeja Electricity Distribution Company IKEDC, a company under
##Sahara Power.
##This just the prototype GUI part of the code that creates the user interface
##I am using Python 2.6 with wxPython GUI toolkit

import wx
import os.path
from ikedcgen import *

#modified textctrl class
class TCtrl(wx.TextCtrl):
    def __init__(self,parent,id):
        wx.TextCtrl.__init__(self,parent,id)
        self.WriteText('0')
        self.Enable(False)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_KILL_FOCUS, self.OffFocus)

##    def GetValue(self):
##        #assessing the static attribute value in the class just because
##        if self.Value == '':
##            self.Value= '0'
##            return self.Value
##        return self.Value

    def OnKeyUp(self,evt):
        t=self.GetValue()
        if not t.isdigit() and t:
            #print 'please insert numbers only'
            wx.Bell()
            #mb=wx.MessageBox('PLEASE INSERT NUMBERS ONLY!!!', 'WARNING')
            #db.ShowModal()
            t=t.rstrip(t[-1])
            self.Clear()
            self.WriteText(t)
        #else: print 'Okeydokey!!!'

    def OffFocus(self, evt):
        if not self.GetValue():
            self.WriteText('0')


#modified static text class
class SText(wx.StaticText):
    def __init__(self, parent, id, label):
        wx.StaticText.__init__(self, parent, id, label)
        myfont= wx.Font(7,wx.FONTFAMILY_UNKNOWN,wx.NORMAL,wx.BOLD, False)
        self.SetFont(myfont)
        self.SetForegroundColour("#660000")

class SText1(wx.StaticText):
    def __init__(self, parent, id, label):
        wx.StaticText.__init__(self, parent, id, label)
        self.SetForegroundColour("#660000")


        
#modified radiobutton class
class RButton(wx.RadioButton):
    def __init__(self,parent,id,label,style=wx.RB_SINGLE):
        wx.RadioButton.__init__(self,parent,id,label,style)
        self.SetForegroundColour("#660000")

        
#modified button class
class NButton(wx.Button):
    def __init__(self,parent,id,label):
        wx.Button.__init__(self, parent, id, label)
        self.SetForegroundColour("#660000")
        

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(400,550),
                          style= wx.MINIMIZE_BOX|wx.CAPTION
                          |wx.CLOSE_BOX|wx.CLIP_CHILDREN|wx.SYSTEM_MENU)
        self.panel= wx.Panel(self)
        #self.panel.SetBackgroundColour("#aaaaaa")
        self.panel.SetBackgroundColour("#ffaa00")

        #IKEDC logo
##        img_path = os.path.abspath("./ik_icon.png")
##        bitmap = wx.Bitmap(img_path, type=wx.BITMAP_TYPE_PNG)
##        self.bitmap = wx.StaticBitmap(self.panel, bitmap=bitmap)

##        sizer = wx.BoxSizer(wx.HORIZONTAL)
##        sizer.Add(self.bitmap, 1, wx.ALIGN_RIGHT)
##        self.SetSizer(sizer)

        sboxm = wx.StaticBox(self.panel, label="Use kilometer values only?")
        sboxszm = wx.StaticBoxSizer(sboxm, wx.VERTICAL)

        gbrb1= wx.GridSizer(2,2,1,1)
        self.rbm1= wx.RadioButton(self.panel,200,'', style= wx.RB_GROUP)
        self.rbm2= wx.RadioButton(self.panel,200,'')

        self.text1= SText1(self.panel,-1,'Yes')
        self.text2= SText1(self.panel,-1,'No')
        gbrb1.AddMany([
                    (self.rbm1,-1),
                    (self.text1,-1),
                    (self.rbm2,-1),
                    (self.text2,-1)])
        

        #self.emp1= SText(self.panel,-1,'     ')
        self.emp2= SText(self.panel,-1,'Insert Number of kilometers:')
        self.emp3= TCtrl(self.panel,-1)
        self.emp3.Enable(True)
        
        gbm= wx.GridSizer(1,2,2,2)
        gbm.AddMany([
                    #(self.emp1,2),
                    (self.emp2,-1),
                    (self.emp3,-1)])

        sboxszm.Add(gbrb1,0)
        sboxszm.Add(gbm,0,wx.EXPAND)

        slm=wx.StaticLine(self.panel, -1, (25, 50), (300,1))
        #slm.SetColour(wx.BLUE)

        #Part to choose type of Feeder
        sbox = wx.StaticBox(self.panel, label="Generate components for 11kV or 33kV?")
        sboxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        #create radiobuttons and populate the static box sizer with them
        self.rb1= wx.RadioButton(self.panel,-1,'11kV Feeder', style= wx.RB_GROUP)
        self.rb2= wx.RadioButton(self.panel,-1,'33kV Feeder')
        sboxsz.Add(self.rb1,1,wx.EXPAND)
        sboxsz.Add(self.rb2,1,wx.EXPAND)

        sl=wx.StaticLine(self.panel, -1, (25, 50), (300,1))
        sl.SetForegroundColour(wx.BLUE)

        #Insert General Variables like spans
        sbox1 = wx.StaticBox(self.panel, label="Insert Variables")
        sboxsz1 = wx.StaticBoxSizer(sbox1, wx.VERTICAL)

        gb= wx.GridSizer(4,2,2,2)
        #statictext part inherited from class SText
        self.txt1= SText(self.panel,-1,'Insert Number of HT Spans:')
        self.txt2= SText(self.panel,-1,'Insert Number of LT Spans:')
        self.txt3= SText(self.panel,-1,'Insert Number of H-Poles:')
        self.txt4= SText(self.panel,-1,'Insert Number of Transformers:')

        #textctrl part inherited from class TCtrl
        self.tc1= TCtrl(self.panel,-1)
        self.tc2= TCtrl(self.panel,-1)
        self.tc3= TCtrl(self.panel,-1)
        self.tc4= TCtrl(self.panel,-1)

        #populate the gridsizer
        gb.AddMany([
                    (self.txt1,-1),
                    (self.tc1,-1),
                    (self.txt2,-1),
                    (self.tc2,-1),
                    (self.txt3,-1),
                    (self.tc3,-1),
                    (self.txt4,-1),
                    (self.tc4,-1)])
        sboxsz1.Add(gb,1,wx.EXPAND)

        #Button to generate the components
        self.genbut= NButton(self.panel,100,label='Generate Components')
        

        msizer = wx.BoxSizer(wx.VERTICAL)
        #msizer.Add(self.bitmap, 0, wx.ALIGN_RIGHT)
        msizer.Add(sboxszm, 0, wx.EXPAND|wx.ALL, 20)
        msizer.Add(slm, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        msizer.Add(sboxsz, 0, wx.EXPAND|wx.ALL, 20)
        msizer.Add(sl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        msizer.Add(sboxsz1, 0, wx.EXPAND|wx.ALL, 20)
        msizer.Add(self.genbut, 0, wx.ALL|wx.ALIGN_RIGHT, 20)
        self.panel.SetSizer(msizer)

        #bind buttons
        self.Bind(wx.EVT_BUTTON, self.OnGenComp, id=100)
        self.Bind(wx.EVT_RADIOBUTTON, self.Onrad1, id=200)

        #App Icon
        path = os.path.abspath("./ik_icon2.ico")
        icon= wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.Center()
        self.Show(True)

    def OnGenComp(self, evt):
        if self.rbm2.GetValue():
            #gets the value in each field and sets the value to 0 if field is empty
            t1= self.tc1.GetValue()
            if not t1: t1='0'
            t2= self.tc2.GetValue()
            if not t2: t2='0'
            t3= self.tc3.GetValue()
            if not t3: t3='0'
            t4= self.tc4.GetValue()
            if not t4: t4='0'

            #check to know the voltage levl of the line
            if self.rb1.GetValue():
                line= self.rb1.GetLabel().split(' ')[0]
                #print self.rb1.GetLabel()
            else:
                line= self.rb2.GetLabel().split(' ')[0]
                #print self.rb2.GetLabel()

    ##        print t1
    ##        print t2
    ##        print t3
                
            #output title heading
            print 'Generating components for %s spans, %s hpoles and %s transformer(s)' %(t1,t3,t4)
            print '============================================='
            print ''

            #from the imported module
            Gen= GenComp(t1, t2, t3, t4, line)
            Gen.gen()


        else:
            t= self.emp3.GetValue()
            if self.rb1.GetValue():
                line= self.rb1.GetLabel().split(' ')[0]
            else:
                line= self.rb2.GetLabel().split(' ')[0]

            print 'Generating components for a %skm, %s feeder' %(t,line)
            print '============================================='
            print ''

            
            #from the imported module
            Gen= GenKmComp(t,line)
            Gen.gen()
            


    def Onrad1(self, evt):
        if self.rbm1.GetValue():
            self.emp3.Enable(True)
            self.tc1.Enable(not self.tc1.IsEnabled())
            self.tc2.Enable(not self.tc2.IsEnabled())
            self.tc3.Enable(not self.tc3.IsEnabled())
            self.tc4.Enable(not self.tc4.IsEnabled())

        else:
            self.emp3.Enable(False)
            self.tc1.Enable(not self.tc1.IsEnabled())
            self.tc2.Enable(not self.tc2.IsEnabled())
            self.tc3.Enable(not self.tc3.IsEnabled())
            self.tc4.Enable(not self.tc4.IsEnabled())



if __name__ == "__main__":
    app= wx.App()
    MyFrame(None, -1, "IKEDC SANCTION APP")
    app.MainLoop()
