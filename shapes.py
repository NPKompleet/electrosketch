import wx

class DragDCircle:
    def __init__(self):
        self.bmp = wx.EmptyBitmap(10,20)
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        bg_colour= wx.WHITE
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.BLUE_BRUSH)
        dc.DrawCircle(5,5,5)
        dc.DrawCircle(5,15,5)
        #dc.Clear()
       
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(self.bmp, bg_colour)
        self.bmp.SetMask(mask)
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False        



#----------------------------------------------------------------------


class DragDCircle2:
    def __init__(self):
        self.bmp = wx.EmptyBitmap(10,20)
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        bg_colour= wx.BLUE
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawCircle(5,5,5)
        dc.DrawCircle(5,15,5)
        #dc.Clear()
       
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(self.bmp, bg_colour)
        self.bmp.SetMask(mask)
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False        



#----------------------------------------------------------------------



class DragCircle:
    def __init__(self):
        self.bmp = wx.EmptyBitmap(15,15)
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        bg_colour= wx.WHITE
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.BLUE_BRUSH)
        dc.DrawCircle(8,8,5)
        #dc.Clear()
       
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(self.bmp, bg_colour)
        self.bmp.SetMask(mask)
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False        



#----------------------------------------------------------------------




class DragCircle2:
    def __init__(self):
        self.bmp = wx.EmptyBitmap(15,15)
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        bg_colour= wx.BLUE
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.DrawCircle(8,8,5)
        #dc.Clear()
       
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(self.bmp, bg_colour)
        self.bmp.SetMask(mask)
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False        



#----------------------------------------------------------------------

class DragICircle:
    def __init__(self):
        self.bmp = wx.EmptyBitmap(40,20)
        dc = wx.MemoryDC()
        dc.SelectObject(self.bmp)
        bg_colour= wx.WHITE
        dc.SetBackground(wx.Brush(bg_colour, wx.SOLID))
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        dc.SetBrush(wx.BLUE_BRUSH)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawCircle(10,10,10)
        dc.DrawCircle(25,10,10)
        #dc.Clear()
       
        dc.SelectObject(wx.NullBitmap)
        mask = wx.Mask(self.bmp, bg_colour)
        self.bmp.SetMask(mask)
        self.pos = (0,0)
        self.shown = True
        self.text = None
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)

            return True
        else:
            return False        


