import wx
import networkx as nx
from shapes import *


numHpole=0 #number of h poles in the grapth
numSpole=0
numExpole=0 #num of existing poles added to the graph
numExDisk=0
Graph= nx.Graph() # graph to be traversed

class SketchWindow(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.shapes=[]
        self.shapedict= {}
        self.dragImage = None
        self.dragShape = None
        self.hiliteShape = None
        self.old_shape= None
        self.lines = []
        self.curLine = []
        self.strlines=[]
        self.poles= []
        self.expoles= []
        self.pos = (0, 0)
        self.oldpos = (0, 0)
        self.oldpos_flag= False
        self.firstpos = (0, 0)
        self.firstpos_flag= False
        #self.old_xpos, self.old_ypos= 0, 0
        self.InitBuffer()
##        self.SetCursor()
        
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SIZING, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)


##    def SetCursor(self):
##        if self.GetParent().toolSelect == "imageicons/freehandicon2.png":
##            self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
##        else:
##            self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        self.DrawStrLines(dc)
        self.DrawPoles(dc)
        #self.DrawExPoles(dc)
        self.DrawShapes(dc)
        self.reInitBuffer = False
        print 'init buffer'

    def DrawShapes(self, dc):
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)
                lst=self.shapedict[shape]
                if lst[2]:
                    shl= self.shapedict[lst[3]]
                    dc.DrawLine(lst[0],lst[1],shl[0], shl[1])
        

    def GetLinesData(self):
        return self.lines[:]

    def SetLinesData(self, lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()

    def OnEnter(self, evt):
##        image=wx.Image("imageicons/pencilicon.png", type=wx.BITMAP_TYPE_PNG)
##        cursor = wx.CursorFromImage(image)
##        self.SetCursor(cursor)
        if self.GetParent().toolSelect == "imageicons/freehandicon2.png":
            image=wx.Image("imageicons/pencilicon2.png", type=wx.BITMAP_TYPE_PNG)
            image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 1)
            image.SetOptionInt(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 31)
            #imask= image.ConvertToBitmap()
            #mask= wx.Mask(imask)
            image.SetMask(True)
            image.SetMaskColour(255,255,255)
            cursor = wx.CursorFromImage(image)
            self.SetCursor(cursor)
            #self.SetCursor(wx.StockCursor(wx.CURSOR_PENCIL))
        else:
            self.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))

    def OnLeave(self, evt):
        #self.InitBuffer()
        pass

    def OnLeftDown(self, event):
        self.curLine = []
        self.pos = event.GetPositionTuple()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        tooldict={"imageicons/polexdrawicon.png": self.placeExPole,
                  "imageicons/poledrawicon.png": self.placePole,
                  "imageicons/Hpolexdrawicon.png": self.placeExHPole,
                  "imageicons/Hpoledrawicon.png": self.placeHPole,
                  "imageicons/linedrawicon.png": self.placeStrLine,
                  "imageicons/transformericon.png": self.placeTransformer}
        
        tool= self.GetParent().toolSelect
        if tool== "imageicons/freehandicon2.png":
            if self.HasCapture():
                self.lines.append((self.color,
                                   self.thickness,
                                   self.curLine))
                self.curLine = []
                self.ReleaseMouse()

        else:
           if self.HasCapture():
               try:
                   tooldict[tool](event)
               except KeyError:
                   print 'no tool as such'
                   self.ReleaseMouse()
##               dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
##               dc.DrawCircle(self.pos[0], self.pos[1], 5)
##               self.poles.append((self.pos[0], self.pos[1], self.oldpos_flag))
##               if self.oldpos_flag:
##                   dc.DrawLine(self.oldpos[0], self.oldpos[1], self.pos[0], self.pos[1])
##               self.oldpos= self.pos
##               self.oldpos_flag= True
##               self.ReleaseMouse()

    def OnMotion(self, evt):
        tool= self.GetParent().toolSelect
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        print tool
        othrtools= (tool == "imageicons/polexdrawicon.png" or tool == "imageicons/poledrawicon.png" or tool== "imageicons/linedrawicon.png"
                    or tool=="imageicons/Hpolexdrawicon.png" or tool=="imageicons/Hpoledrawicon.png")
        if evt.Dragging() and evt.LeftIsDown() and (tool == "imageicons/freehandicon2.png"):
            self.drawMotion(dc, evt)

        elif evt.Moving() and othrtools and not evt.RightIsDown():
            self.drawimaglineMotion(dc, evt)
        


        elif evt.Dragging() and othrtools and evt.RightIsDown():
            #print 'should drag!!!'
            # if we have a shape, but haven't started dragging yet
            if self.dragShape and not self.dragImage:
               # print'not yet moving'

                # only start the drag after having moved a couple pixels
                tolerance = 2
                pt = evt.GetPosition()
                dx = abs(pt.x - self.dragStartPos.x)
                dy = abs(pt.y - self.dragStartPos.y)
                if dx <= tolerance and dy <= tolerance:
                    return

                # refresh the area of the window where the shape was so it
                # will get erased.
                self.dragShape.shown = False
                self.RefreshRect(self.dragShape.GetRect(), True)
                self.Update()

                if self.dragShape.text:
                    self.dragImage = wx.DragString(self.dragShape.text,
                                                  wx.StockCursor(wx.CURSOR_HAND))
                else:
                    self.dragImage = wx.DragImage(self.dragShape.bmp,
                                                 wx.StockCursor(wx.CURSOR_HAND))

                hotspot = self.dragStartPos - self.dragShape.pos
                self.dragImage.BeginDrag(hotspot, self, self.dragShape.fullscreen)

                self.dragImage.Move(pt)
                self.dragImage.Show()


            # if we have shape and image then move it, posibly highlighting another shape.
            elif self.dragShape and self.dragImage:
                #print'moving'
                onShape = self.FindShape(evt.GetPosition())
                unhiliteOld = False
                hiliteNew = False

                # figure out what to hilite and what to unhilite
                if self.hiliteShape:
                    if onShape is None or self.hiliteShape is not onShape:
                        unhiliteOld = True

                if onShape and onShape is not self.hiliteShape and onShape.shown:
                    hiliteNew = True

                # if needed, hide the drag image so we can update the window
                if unhiliteOld or hiliteNew:
                    self.dragImage.Hide()

                if unhiliteOld:
                    dc = wx.ClientDC(self)
                    self.hiliteShape.Draw(dc)
                    self.hiliteShape = None

                if hiliteNew:
                    dc = wx.ClientDC(self)
                    self.hiliteShape = onShape
                    self.hiliteShape.Draw(dc, wx.INVERT)

                # now move it and show it again if needed
                pos= evt.GetPositionTuple()
                self.dragImage.Move(pos)
                self.shapedict[self.dragShape][0]= pos[0]
                self.shapedict[self.dragShape][1]= pos[1]
                
                if unhiliteOld or hiliteNew:
                    self.dragImage.Show()
            #self.InitBuffer()
        evt.Skip()
        



    # right mouse button is down.
    def OnRightDown(self, evt):
        # Did the mouse go down on one of our shapes?
        shape = self.FindShape(evt.GetPosition())

        # If a shape was 'hit', then set that as the shape we're going to
        # drag around. Get our start position. Dragging has not yet started.
        # That will happen once the mouse moves, OR the mouse is released.
        if shape:
            self.dragShape = shape
            self.dragStartPos = evt.GetPosition()

    # right mouse button up.
    def OnRightUp(self, evt):
        if not self.dragImage or not self.dragShape:
            self.dragImage = None
            self.dragShape = None
            return

        # Hide the image, end dragging, and nuke out the drag image.
        self.dragImage.Hide()
        self.dragImage.EndDrag()
        self.dragImage = None

        if self.hiliteShape:
            self.RefreshRect(self.hiliteShape.GetRect())
            self.hiliteShape = None

        # reposition and draw the shape

        # Note by jmg 11/28/03 
        # Here's the original:
        #
        # self.dragShape.pos = self.dragShape.pos + evt.GetPosition() - self.dragStartPos
        #
        # So if there are any problems associated with this, use that as
        # a starting place in your investigation. I've tried to simulate the
        # wx.Point __add__ method here -- it won't work for tuples as we
        # have now from the various methods
        #
        # There must be a better way to do this :-)
        #
        
        self.dragShape.pos = (
            self.dragShape.pos[0] + evt.GetPosition()[0] - self.dragStartPos[0],
            self.dragShape.pos[1] + evt.GetPosition()[1] - self.dragStartPos[1]
            )
            
        self.dragShape.shown = True
        self.RefreshRect(self.dragShape.GetRect())
        self.dragShape = None
        self.InitBuffer()




        

    #free hand draw
    def drawMotion(self, dc, event):
        dc.SetPen(self.pen)
        newPos = event.GetPositionTuple()
        coords = self.pos + newPos
        self.curLine.append(coords)
        dc.DrawLine(*coords)
        self.pos = newPos

    #guideline
    def drawimaglineMotion(self, dc, event):
        dc.SetPen(wx.Pen("#ffaa00"))
        newPos = event.GetPositionTuple()
        tool= self.GetParent().toolSelect
        othrtools= (tool == "imageicons/polexdrawicon.png" or tool == "imageicons/poledrawicon.png" or tool=="imageicons/Hpolexdrawicon.png"
                    or tool== "imageicons/Hpoledrawicon.png")
        if self.oldpos_flag and othrtools:
            coords = self.oldpos + newPos
            #self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.InitBuffer()
            #self.pos = newPos

        if self.firstpos_flag and tool == "imageicons/linedrawicon.png":
            coords = self.firstpos + newPos
            #self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.InitBuffer()
            #self.pos = newPos

    #to place straightlines
    def placeStrLine(self, evt):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        #dc.SetBrush(wx.WHITE_BRUSH)
        #dc.DrawCircle(self.pos[0], self.pos[1], 5)
        if self.firstpos_flag:
            dc.DrawLine(self.firstpos[0], self.firstpos[1], self.pos[0], self.pos[1])
        self.strlines.append((self.pos[0], self.pos[1], self.firstpos_flag, self.firstpos[0], self.firstpos[1]))
        self.firstpos_flag= True
        self.firstpos= self.pos
        self.ReleaseMouse()
        #self.old_xpos, self.old_ypos= 0, 0
        

    #to place proposed poles
##    def placePole(self, evt):
##        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
##        dc.SetBrush(wx.WHITE_BRUSH)
##        dc.DrawCircle(self.pos[0], self.pos[1], 5)
##        if self.oldpos_flag:
##            dc.DrawLine(self.oldpos[0], self.oldpos[1], self.pos[0], self.pos[1])
##        self.poles.append((self.pos[0], self.pos[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
##        self.oldpos_flag= True
##        self.oldpos= self.pos
##        self.ReleaseMouse()
##        #self.old_xpos, self.old_ypos= 0, 0

    #to place existing poles
##    def placeExPole(self):
##        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
##        dc.SetBrush(wx.BLACK_BRUSH)
##        dc.DrawCircle(self.pos[0], self.pos[1], 5)
##        if self.oldpos_flag:
##            dc.DrawLine(self.oldpos[0], self.oldpos[1], self.pos[0], self.pos[1])
##        self.expoles.append((self.pos[0], self.pos[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
##        self.oldpos_flag= True
##        self.oldpos= self.pos
##        self.ReleaseMouse()

    def placeExPole(self, evt):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBrush(wx.BLACK_BRUSH)
        shape = DragCircle()
        t=evt.GetPositionTuple()
        shape.pos = (t[0]-8, t[1]-8)
        if self.oldpos_flag:
            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
        self.shapes.append(shape)
        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
        self.oldpos_flag= True
        self.oldpos= t
        self.old_shape= shape
        self.InitBuffer()
        #self.Refresh()

        self.ReleaseMouse()



##    def placePole(self, evt):
##        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
##        dc.SetBrush(wx.BLACK_BRUSH)
##        shape = DragCircle2()
##        t=evt.GetPositionTuple()
##        shape.pos = (t[0]-8, t[1]-8)
##        if self.oldpos_flag:
##            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
##        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
##        self.shapes.append(shape)
##        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
##        self.oldpos_flag= True
##        self.oldpos= t
##        self.old_shape= shape
##        self.InitBuffer()
##        #self.Refresh()
##
##        self.ReleaseMouse()    

    def placePole(self, evt):
        lsheet= self.GetParent().listing.sheet
        global numHpole, numExpole, numExDisk, numSpole, Graph
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBrush(wx.BLACK_BRUSH)
        shape = DragCircle2()
        t=evt.GetPositionTuple()
        shape.pos = (t[0]-8, t[1]-8)
        if self.oldpos_flag:
            #could also place this on another thread
            if isinstance(self.old_shape, DragCircle) or isinstance(self.old_shape, DragDCircle):
                Graph.add_node(self.old_shape)
                numExpole +=1
            if isinstance(self.old_shape, DragDCircle2) or isinstance(self.old_shape, DragDCircle):
                numExDisk+=3
                lsheet.SetCellValue(9,1,str(numExDisk))
                lsheet.SetCellValue(10,1,str(numExDisk)) # number of jhooks
                lsheet.SetCellValue(11,1,str(numExDisk)) # number of bolt clamps
                lsheet.SetCellValue(12,1,str(numExDisk)) # number of socket adapters
                lsheet.SetCellValue(13,1,str(numExDisk/3)) # number of channel irons
            Graph.add_edge(self.old_shape, shape, wire= 'overhead')
            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
        self.shapes.append(shape)
        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
        self.oldpos_flag= True
        self.oldpos= t
        self.old_shape= shape
        self.InitBuffer()
        #self.Refresh()

        self.ReleaseMouse()

        #could put this on another thread of execution
        #SHOULD REALLY REALLY PUT THIS ON ANOTHER THREAD OF EXECUTION!!!!!
        numSpole +=1
        lsheet.SetCellValue(0,1,str(Graph.number_of_nodes() + numHpole - numExpole))
        lsheet.SetCellValue(1,1,str(Graph.number_of_edges() * 135)) #using 45m here
        lsheet.SetCellValue(2,1,str(numSpole * 3))
        lsheet.SetCellValue(3,1,str(numSpole * 3))
        lsheet.SetCellValue(4,1,str(numSpole))
        lsheet.SetCellValue(5,1,str(numSpole)) #tie straps uses pairs
        lsheet.SetCellValue(6,1,str(numSpole * 2))
        lsheet.SetCellValue(7,1,str(numSpole))
        lsheet.SetCellValue(8,1,str(numSpole))
        lsheet.Refresh()
        print Graph.nodes()
        


    def placeExHPole(self, evt):
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBrush(wx.BLACK_BRUSH)
        shape = DragDCircle()
        t=evt.GetPositionTuple()
        shape.pos = (t[0]-8, t[1]-8)
        if self.oldpos_flag:
            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
        self.shapes.append(shape)
        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
        self.oldpos_flag= True
        self.oldpos= t
        self.old_shape= shape
        self.InitBuffer()
        #self.Refresh()

        self.ReleaseMouse()



    def placeHPole(self, evt):
        lsheet= self.GetParent().listing.sheet
        global numHpole, numExpole, numExDisk, Graph
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBrush(wx.BLACK_BRUSH)
        shape = DragDCircle2()
        t=evt.GetPositionTuple()
        shape.pos = (t[0]-8, t[1]-8)
        Graph.add_node(shape)
        if self.oldpos_flag:
            #could also place this on another thread
            if isinstance(self.old_shape, DragCircle) or isinstance(self.old_shape, DragDCircle):
                Graph.add_node(self.old_shape)
                numExpole +=1
            if isinstance(self.old_shape, DragDCircle2) or isinstance(self.old_shape, DragDCircle):
                numExDisk+=3
            Graph.add_edge(self.old_shape, shape, wire= 'overhead')
            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
        self.shapes.append(shape)
        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
        self.oldpos_flag= True
        self.oldpos= t
        self.old_shape= shape
        self.InitBuffer()
        #self.Refresh()

        self.ReleaseMouse()

        #could put this on another thread of execution
        #SHOULD REALLY REALLY PUT THIS ON ANOTHER THREAD OF EXECUTION!!!!!
        numHpole +=1
        numExDisk+=3
        
        lsheet.SetCellValue(0,1,str(Graph.number_of_nodes() + numHpole - numExpole))
        lsheet.SetCellValue(1,1,str(Graph.number_of_edges() * 135)) #using 45m here
        lsheet.SetCellValue(9,1,str(numExDisk))
        lsheet.SetCellValue(10,1,str(numExDisk)) # number of jhooks
        lsheet.SetCellValue(11,1,str(numExDisk)) # number of bolt clamps
        lsheet.SetCellValue(12,1,str(numExDisk)) # number of socket adapters
        lsheet.SetCellValue(13,1,str(numExDisk/3)) # number of channel irons
        lsheet.Refresh()
        print'hpole is', numHpole
        print Graph.nodes()


    def placeTransformer(self, evt):
        if isinstance(self.old_shape, DragICircle):
            self.ReleaseMouse()
            return
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        dc.SetBrush(wx.BLACK_BRUSH)
        shape = DragICircle()
        t=evt.GetPositionTuple()
        shape.pos = (t[0]-18, t[1]-8)
        if self.oldpos_flag:
            dc.DrawLine(self.oldpos[0], self.oldpos[1], t[0], t[1])
        self.expoles.append((t[0], t[1], self.oldpos_flag, self.oldpos[0], self.oldpos[1]))
        self.shapes.append(shape)
        self.shapedict[shape]=[t[0], t[1], self.oldpos_flag, self.old_shape]
        self.oldpos_flag= True
        self.oldpos= t
        self.old_shape= shape
        self.InitBuffer()
        #self.Refresh()

        self.ReleaseMouse()


        

    def OnSize(self, event):
        #self.reInitBuffer = True
        self.InitBuffer()

    def OnIdle(self, event):
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)

    def OnPaint(self, event):
        #dc = wx.BufferedPaintDC(self, self.buffer)
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        self.DrawShapes(dc)

    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def DrawStrLines(self, dc):
        dc.SetBrush(wx.WHITE_BRUSH)
        for xpos, ypos, flag, oldx, oldy in self.strlines:
            #dc.DrawCircle(xpos, ypos, 5)
            if flag:
                dc.DrawLine(xpos, ypos, oldx, oldy)      

    def DrawPoles(self, dc):
        dc.SetBrush(wx.WHITE_BRUSH)
        for xpos, ypos, flag, oldx, oldy in self.poles:
            dc.DrawCircle(xpos, ypos, 5)
            if flag:
                dc.DrawLine(xpos, ypos, oldx, oldy)
            #self.old_xpos, self.old_ypos= xpos, ypos

##    def DrawExPoles(self, dc):
##        dc.SetBrush(wx.BLACK_BRUSH)
##        for xpos, ypos, flag, oldx, oldy in self.expoles:
##            #dc.DrawCircle(xpos, ypos, 5)
##            if flag:
##                dc.DrawLine(xpos, ypos, oldx, oldy)
##            #self.old_xpos, self.old_ypos= xpos, ypos



    # This is actually a sophisticated 'hit test', but in this
    # case we're also determining which shape, if any, was 'hit'.
    def FindShape(self, pt):
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
        return None


    # Clears the background, then redraws it. If the DC is passed, then
    # we only do so in the area so designated. Otherwise, it's the whole thing.
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

    

    def SetColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def SetThickness(self, num):
        self.thickness = num
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)


class SketchFrame(wx.Frame):
    def __init__(self, parent):
##        wx.Frame.__init__(self, parent, -1, "Sketch Frame",
##                size=(800,600))
        wx.Frame.__init__(self, parent, -1, "Sketch Frame")
##        self.Maximize()
        self.sketch = SketchWindow(self, -1)
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = SketchFrame(None)
    frame.Show(True)
    app.MainLoop()
