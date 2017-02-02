##This module helps to calculate the number of components
##to be generated.
##It will be called by the Generate Components button in
##the GUI part of the application

#from Listing import *
from sheet import *


class GenComp:
    def __init__(self, HTSpans, LTSpans, Hpoles, Transf, line):
        self.nSpans= int(HTSpans)
        self.lSpans= int(LTSpans)
        self.nHpoles= int(Hpoles)
        self.nTf= int(Transf)
        self.line= line

    def gen(self):
        #Span dependent part
        #number of poles
        numOfpol= self.nSpans + self.nHpoles
        #lenght of conductor
        lenOfcon= self.nSpans * 45 * 3
        #number of pot insulators and spindle
        numOfpot= numOfspin= self.nSpans * 3
        #number of fibre crossarm
        numOffib= (self.nSpans - self.nHpoles)
        #number of tiestraps
        numOfts= numOffib * 2
        #bolts and nuts
        fifth8by6= numOfpol*2
        fifth8by8= fifth8by11= numOfpol

        if self.nTf:
            #number of dfuse and ligtening arrester
            numOfD= numOfLA= self.nTf
            #lenght of XLPE cable
            lenOfXLPE= self.nTf* 39
            #number of RayChem kit
            numOfRC= self.nTf
            #sockets
            numOfsock= self.nTf* 8
            #nuber of eathrod
            numOfEarthRod= self.nTf* 10
            #lenght of 70mm bare copper
            lenOf70= self.nTf * 45

        if self.lSpans:
            #lenght of LT conductors
            lenOfLTcon= self.lSpans * 200
            #D Irons
            numOfDIron= self.lSpans * 8
            # shackle Insulator
            numOfShck= self.lSpans * 8
            # adds to the 5/8 X 8 
            fifth8by8+= self.lSpans * 8
            # number of 5X8 washer
            numOfwash= self.lSpans * 16

        
        print 'number of 10.06m poles is ', numOfpol
        print 'length of conductors is ', lenOfcon, 'meters'
        if self.line == '11kV':
            print 'number of pin insulators is ', numOfpot
        else:
            print 'number of pot insulators is ', numOfpot
            
        print 'number of spindles is ', numOfpot
        
        if self.line == '11kV':
            print 'number of 6ft fibre crossarms is ', numOffib
        else:
            print 'number of 9ft fibre crossarms is ', numOffib
            
        print 'number of tiestraps is ', numOfts
        print 'number of 5/8 X 6 bolt is ', fifth8by6
        print 'number of 5/8 X 8 bolt is ', fifth8by8
        print 'number of 5/8 X 11 bolt is ', fifth8by11
        print ''
        print ''

        #Hpole dependent part
        #number of channel iron
        numOfcha= self.nHpoles * 2
        #5/8 X 9 bolt and nut
        fifth8by9= self.nHpoles * 2
        print 'number of channel irons is ', numOfcha
        print 'number of 5/8 X 9 bolt is ', fifth8by9
        #number of stays
        self.staygen(2*self.nHpoles)

        if self.nTf:
            print 'number of %s D-Fuse assembly is %d set' %(self.line, numOfD)
            print 'number of %s Lightening Arrester is %d set' %(self.line, numOfD)
            print 'number of Gang Isolator is %d set' %numOfD
            if self.line == '11kV':
                print 'Lenght of XLPE cable is %s meters' %lenOfXLPE
            print 'number of indoor RayChem kit is %s set'%numOfRC
            print 'number of outdoor RayChem kit is %s set'%numOfRC
            print 'number of 1500mm socket is', numOfsock
            print 'number of 150mm socket is', numOfsock
            print 'number of 70mm socket is', numOfsock
            print 'number of Earth rod is', numOfEarthRod
            print 'length of 70mm bare copper is %s meters'%lenOf70
            print ''
            print ''

        if self.lSpans:
            print 'lenght of LT conductors is %s meters' %lenOfLTcon
            print 'number of D-Iron is ', numOfDIron
            print 'number of Shackle Insulator is ', numOfShck
            print 'number of 5X8 washer is ', numOfwash

        L=ListFrame(None, -1, "LISTCTRL")
        L.panel.sheet.SetCellValue(0,1, str(numOfpol))
        L.panel.sheet.SetCellValue(1,1, str(lenOfcon))
        L.panel.sheet.SetCellValue(2,1, str(numOfpot))
        L.panel.sheet.SetCellValue(3,1, str(numOfpot))
        L.panel.sheet.SetCellValue(4,1, str(numOffib))
        L.panel.sheet.SetCellValue(5,1, str(numOffib))
        L.panel.sheet.SetCellValue(6,1, str(fifth8by6))
        L.panel.sheet.SetCellValue(7,1, str(fifth8by8))
        L.panel.sheet.SetCellValue(8,1, str(fifth8by11))
        L.panel.sheet.SetCellValue(9,1, str(numOfdisk))
        L.panel.sheet.SetCellValue(10,1, str(numOfjhook))
        L.panel.sheet.SetCellValue(11,1, str(numOf6BC))
        L.Show(True)
            

    def staygen(self, staynumber):
        number= staynumber
        print 'generating for %s stays...' %number
        lenOfwire= number* 15
        numOfrod= numOfins= numOfblock= number
        print 'lenght of stay wire needed is ', lenOfwire
        print 'number of stay rods needed is ', numOfrod
        print 'number of stay insulators needed is ', numOfins
        print 'number of stay blocks needed is ', numOfblock
        print ''
        print ''

        

class GenKmComp:
    def __init__(self, num, feeder):
        self.numOfkilo= int(num)
        self.feeder= feeder

    def gen(self):
        #number of poles
        if self.numOfkilo == 1:
            numOfpol= 24
        elif self.numOfkilo > 1:
            numOfpol= 24+(22*(self.numOfkilo-1))
        else: numOfpol= 0

        lenOfcon= self.numOfkilo * 3000
        numOffib= self.numOfkilo * 17
        numOfts= numOffib * 2
        numOfpot= numOfspin= (numOffib * 3) + 3

        #number of disk insulators
        if self.feeder == '11kV':
            numOfdisk= self.numOfkilo * 27
        else:
            numOfdisk= self.numOfkilo * 27 * 3    
        #number of Socket Adapter and 6-Bolt Clamp and J-hooks
        #numOfSA= numOf6BC= numOfJHook= numOfDisk
        numOfSA=numOfjhook=numOf6BC= self.numOfkilo * 27
        #bolts and nuts
        fifth8by6= self.numOfkilo * 34
        fifth8by8= fifth8by11= self.numOfkilo * 17

        numOfcha= self.numOfkilo * 6


        print 'number of 10.53m poles is ', numOfpol
        print 'length of conductors is ', lenOfcon, 'meters'
        
        if self.feeder == '11kV':
            print 'number of 6ft fibre crossarms is ', numOffib
        else:
            print 'number of 9ft fibre crossarms is ', numOffib
        print 'number of tiestraps is ', numOfts
        if self.feeder == '11kV':
            print 'number of pin insulators is ', numOfpot
        else:
            print 'number of pot insulators is ', numOfpot

        print 'number of Disk insulators is ', numOfdisk
        print 'number of Socket Adaptors is ', numOfSA
        print 'number of 6-Bolt Clamp is ', numOf6BC
        print 'number of J-Hooks is ', numOfjhook
            
        print 'number of spindles is ', numOfpot
        print 'number of 5/8 X 6 bolt is ', fifth8by6
        print 'number of 5/8 X 8 bolt is ', fifth8by8
        print 'number of 5/8 X 11 bolt is ', fifth8by11

        print 'number of channel irons is ', numOfcha

        L=ListFrame(None, -1, "LISTCTRL")
        L.panel.sheet.SetCellValue(0,1, str(numOfpol))
        L.panel.sheet.SetCellValue(1,1, str(lenOfcon))
        L.panel.sheet.SetCellValue(2,1, str(numOfpot))
        L.panel.sheet.SetCellValue(3,1, str(numOfpot))
        L.panel.sheet.SetCellValue(4,1, str(numOffib))
        L.panel.sheet.SetCellValue(5,1, str(numOffib))
        L.panel.sheet.SetCellValue(6,1, str(fifth8by6))
        L.panel.sheet.SetCellValue(7,1, str(fifth8by8))
        L.panel.sheet.SetCellValue(8,1, str(fifth8by11))
        L.panel.sheet.SetCellValue(9,1, str(numOfdisk))
        L.panel.sheet.SetCellValue(10,1, str(numOfjhook))
        L.panel.sheet.SetCellValue(11,1, str(numOf6BC))
        L.Show(True)

if __name__ == '__main__':
    pass
