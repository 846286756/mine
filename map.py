# -*- coding: UTF-8 -*-
from tkFileDialog import *

from Tkinter import *
from PIL import Image, ImageTk
class block:
    def __init__(self,num=0):
        self.show=' '
        self.mark=' '
        self.operate=[]
        self.answer=num
    def __repr__(self):
        return self.show

class minemap:
    def __init__(self):
        self.prex=0
        self.prey=0
        self.delay=True
        self.leftdowm=False
        self.rightdown=False
        self.middledown=False
        self.leftinvalid=False
        self.rightinvalid=False
        self.rightminus=False
        self.lclick=0
        self.rclick=0
        self.dclick=0
        self.wclick=0
        self.safe=0
        self.flag=0
        self.mine=0
        self.backwclick=[0]
        self.width=0
        self.height=0
        self.window=[[]]
        self.pic=[[]]
        self.map=[[]]
        self.skinlist=\
                       {'0':(0,0),'1':(0,1),'2':(0,2),'3':(0,3),'4':(0,4),\
                        '5':(0,5),'6':(0,6),'7':(0,7),'8':(0,8),' ':(1,0),\
                        'b':(1,1),'□':(1,1),'*':(1,2),'!':(1,3),'x':(1,4),'#':(1,5)}
        self.root =Tk()
        self.root.bind('<Key>',self.fastkey)

        self.buttonframe=Frame(self.root)
        self.buttonframe.pack(side=BOTTOM)
        self.branchframe=Frame(self.root)
        self.branchframe.pack(side=RIGHT)
        self.clickframe=Frame(self.root)
        self.clickframe.pack(side=LEFT)
        self.mapframe=Frame(self.root)
        self.mapframe.pack(side=TOP)
        self.mapbuttonframe=Frame(self.root)
        self.mapbuttonframe.pack(side=TOP)
        self.explainframe=Frame(self.root)
        self.explainframe.pack(side=TOP)

        
        self.explaintext = StringVar()
        self.explain=Label(self.explainframe,text = '',\
        textvariable = self.explaintext,wraplength = 140,justify = 'left')
        self.explaintext.set('')
        self.explain.pack(side=TOP)
        self.text=Text(self.explainframe,width = 20,height = 5)
        self.text.pack(side=TOP)
        self.branch = Listbox(self.branchframe)
        self.branch.pack(side=TOP)
        self.setoperate = Listbox(self.clickframe)
        for i in ['1：按下左键','2：点击左键','3：点击右键','4：按下双键',\
                  '5：点击双键','6：设置地雷','7：显示标记']:
            self.setoperate.insert(END,i)
        self.setoperate.pack(side=TOP)
        self.setoperate.selection_set(0)
        self.mouseoperate=['left','lefts','rights','double','doubles','addmine','mark']
        self.clickoperate=['lefts','double','rights']
        self.menu = Menu(self.root)
        self.file=Menu(self.menu)
        self.file.add_command(label = '新建',\
                              command = self.newfile)
        self.file.add_command(label = '打开…',\
                              command = self.readfile)
        self.file.add_command(label = '保存',\
                              command = self.writefile)
        self.file.add_command(label = '另存为…',\
                              command = self.savefile)
        self.file.add_command(label = '读取arbiter文本截图布雷',\
                              command = self.readmine)
        self.file.add_command(label = '读取arbiter文本截图局面',\
                              command = self.readopen)
        self.file.add_command(label = '读取rawvf',\
                              command = self.readrawvf)
        self.menu.add_cascade(label = '文件',menu = self.file)
        self.root['menu']=self.menu
        self.playbutton= Button(self.buttonframe,text = '播放',\
                                width = 6,height = 1,command=self.play)
        self.resetbutton= Button(self.buttonframe,text = '重置',\
                                 width = 6,height = 1,command=self.reset)
        self.backbutton= Button(self.buttonframe,text = '后退',\
                                width = 6,height = 1,command=self.backstep)
        self.addstepbutton= Button(self.buttonframe,text = '新步骤',\
                                width = 6,height = 1,command=self.addstep)
        self.delstepbutton= Button(self.buttonframe,text = '删除步骤',\
                                width = 6,height = 1,command=self.delstep)
        self.addbranchbutton= Button(self.buttonframe,text = '新分支',\
                                width = 6,height = 1,command=self.addbranch)
        self.setmousebutton= Button(self.clickframe,text = '设置鼠标',\
                                width = 6,height = 1)
        self.setmousebutton.bind('<Button>',self.setmouse)
        self.addshowbutton= Button(self.mapbuttonframe,text = 'show',\
                                width = 6,height = 1,command=self.addshow)
        self.setexplainbutton= Button(self.explainframe,text = '更改说明',\
                                width = 6,height = 1,command=self.setexplain)
        self.resetbutton.pack(side=LEFT)
        self.backbutton.pack(side=LEFT)
        self.playbutton.pack(side=LEFT)
        self.addstepbutton.pack(side=LEFT)
        self.delstepbutton.pack(side=LEFT)
        self.addbranchbutton.pack(side=LEFT)
        self.setexplainbutton.pack(side=TOP)
        self.setmousebutton.pack(side=TOP)
        self.addshowbutton.pack(side=TOP)
        skin=Image.open('predatorskin.bmp')
        self.photo = ImageTk.PhotoImage(skin)
        self.newmap([0,0])
        self.root.mainloop()

    def setmouse(self,event):
        self.clickoperate[event.num-1]=self.mouseoperate[self.setoperate.curselection()[0]]
    
    def addmine(self,i,j,addback=True):
        if self.map[i][j].answer!=9:
            self.mine+=1
            self.map[i][j].answer=9
            for y in range(i-1,i+2):
                for x in range(j-1,j+2):
                    if 0<=x<self.width and 0<=y<self.height and \
                    self.map[y][x].answer<=8:
                        self.map[y][x].answer+=1
                        if self.map[y][x].show.isdigit():
                            self.setshow(y,x,str(self.map[y][x].answer))
            if self.map[i][j].show.isdigit():
                self.setshow(i,j,'#')
        else:
            self.mine-=1
            self.map[i][j].answer=1
            for y in range(i-1,i+2):
                for x in range(j-1,j+2):
                    if 0<=x<self.width and 0<=y<self.height:
                        if self.map[y][x].answer<=8:
                            self.map[y][x].answer-=1
                            if self.map[y][x].show.isdigit():
                                self.setshow(y,x,str(self.map[y][x].answer))
                        else:
                            self.map[i][j].answer+=1
            if self.map[i][j].show=='#': 
                self.setshow(i,j,str(self.map[i][j].answer))
        if addback:
            self.back[-1].append('addmine({0},{1},False)'.format(i,j))

    def newmap(self,size):
        for i in range(self.height):
            for j in range(self.width):
                self.pic[i][j].place_forget()
                self.window[i][j].grid_forget()
        self.width=size[0]
        self.height=size[1]
        self.push=[]
        self.operate=[]
        self.back=[]
        #self.root.geometry(str(max(self.width*16+160,240))+'x'+\
        #                   str(self.height*16+160))
        self.block=self.width*self.height
        self.map=[[block() for j in range(self.width)]\
                  for i in range(self.height)]
        self.window=[[Frame(self.mapframe,height = 16,width = 16)\
	      for j in range(self.width)] for i in range(self.height)]
        self.pic=[[Label(self.window[i][j],image=self.photo,anchor='nw')
	   for j in range(self.width)] for i in range(self.height)]
        #self.explain.place(anchor = 'nw',x = 0,y = self.height*16+40)
        #self.resetbutton.place(anchor = 'nw',x = 0,y = self.height*16+4)
        #self.playbutton.place(anchor = 'nw',x = 40,y = self.height*16+4)
        #self.backbutton.place(anchor = 'nw',x = 40,y = self.height*16+44)
        #self.branch.place(anchor = 'nw',x = max(self.width*16,80),y = 0)
        #self.setoperate.place(anchor = 'nw',x = max(self.width*16+80,160),y = 0)
        for i in range(self.height):
            for j in range(self.width):
                self.pic[i][j].place(anchor = 'nw',x = -2,y = -18)
                self.pic[i][j]['padx']=j
                self.pic[i][j]['pady']=i
                self.pic[i][j].bind('<Button>',self.onclick)
                self.window[i][j].grid(row = i,column = j)
            #self.showanswer()
    def __repr__(self):
        p='mine:'+str(self.mine)
        p=p+'\n  '+repr(range(self.width)).replace(', ',' ')[1:-1]+' '
        #p=p+'\n '+' -'*self.width
        for i in range(self.height):
            p=p+'\n'+str(i)+'|'
            for j in range(self.width):
                t=self.map[i][j].show if self.map[i][j].mark==' ' \
                       else self.map[i][j].mark
                p=p+t
                if t!='□':
                    p=p+'|'
                    #p=p+'\n '+' -'*self.width
        return p

    def openblock(self,x,y):
        if self.map[x][y].show==' ':
            #print 'open',x,y
            if self.map[x][y].answer==9:
                self.boom(x,y)
                self.gameover('lose')
            else:
                self.setshow(x,y,str(self.map[x][y].answer))
                self.safe+=1
                if self.safe+self.mine==self.block:
                    self.gameover('win')
            if self.map[x][y].answer==0:
                self.openaround(x,y)

    def gameover(self,result):
        pass

    def boom(self,x,y):
        self.result='lose'
        self.setmark(x,y,'#')
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].answer==9 and self.map[i][j].show==' ':
                    self.setshow(i,j,'*')
                elif self.map[i][j].answer<=8 and self.map[i][j].show=='!':
                    self.setshow(i,j,'x')

    def openaround(self,x,y):
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if 0<=i<self.height and 0<=j<self.width:
                    self.openblock(i,j)



    def mv(self,x,y):
        x/=16
        y/=16
        if not self.leftinvalid:
            self.up(self.prex,self.prey,False)
            self.down(x,y,False)
        elif (self.leftdown and self.rightdown) or self.middledown:
            self.uparound(self.prex,self.prey,False)
            self.downaround(x,y,False)
        self.prex=x
        self.prey=y


    def lc(self,x,y):
        #x/=16
        #y/=16
        self.leftdown=True
        #self.back[-1].append('leftdown=False')
        if self.rightdown:
            self.leftinvalid=True
        #self.back[-1].append('leftinvalid=False')
            #self.downaround(x,y,False)
        #elif self.map[x][y].show==' ':
            #self.down(x,y,False)
        self.prex=x
        self.prey=y

    def rc(self,x,y):
        #x/=16
        #y/=16
        self.rightdown=True
        #self.back[-1].append('rightdown=False')
        if self.leftdown:
            self.leftinvalid=True
            #self.back[-1].append('leftinvaild=False')
            #self.downaround(x,y,False)
        else:
            #self.rights(x,y)
            self.addclick('rights({0},{1})'.format(x,y))
            self.rightinvalid=True
            #self.back[-1].append('rightinvalid=False')
        self.prex=x
        self.prey=y
    
    def lr(self,x,y):
        #x/=16
        #y/=16
        self.leftdown=False
        #self.back[-1].append('leftdown=True')
        if self.rightdown:
            #self.uparound(x,y,False)
            if self.delay:
                #self.double(x,y)
                self.addclick('double({0},{1})'.format(x,y))
            else:
                #self.doubles(x,y)
                self.addclick('double({0},{1})'.format(x,y))
            if self.rightinvalid and self.rightminus:
                self.rclick-=1
                self.rightminus=False
                #self.back[-1].append('rightminus=True')
        elif not self.leftinvalid:
            #self.up(x,y,False)
            #self.lefts(x,y)
            self.addclick('lefts({0},{1})'.format(x,y))
        else:
            #self.show()
            self.addclick('show()')
        self.leftinvalid=False
        #self.back[-1].append('leftinvaild=True')
        self.prex=x
        self.prey=y

    def rr(self,x,y):
        #x/=16
        #y/=16
        self.rightdown=False
        #self.back[-1].append('rightdown=True')
        if self.leftdown:
            if self.rightinvalid:
                self.rclick-=1
            #self.uparound(x,y,False)
            if self.delay:
                #self.double(x,y)
                self.addclick('double({0},{1})'.format(x,y))
            else:
                self.doubles(x,y)
        else:
            #self.show()
            self.addclick('show()')
        self.rightinvalid=False
        #self.back[-1].append('rightinvalid=True')
        self.rightminus=True
        #self.back[-1].append('rightminus=False')
        self.prex=x
        self.prey=y

    def mc(self,x,y):
        x/=16
        y/=16
        self.middledown=True
        self.downaround(x,y,False)
        self.prex=x
        self.prey=y

    def mr(self,x,y):
        x/=16
        y/=16
        self.middledown=False
        if self.delay:
            self.double(x,y)
        else:
            self.doubles(x,y)
        self.prex=x
        self.prey=y

                
        

    def lefts(self,x,y):
        self.lclick+=1
        if self.map[x][y].show==' ':
            self.openblock(x,y)
        else:
            self.wclick+=1
            self.backwclick[-1]+=1

    def rights(self,x,y):
        self.rclick+=1
        if self.map[x][y].show==' ':
            self.setshow(x,y,'!')
            self.flag+=1
        elif self.map[x][y].show=='!':
            self.setshow(x,y,' ')
            self.flag-=1
            self.wclick+=2
            self.backwclick[-1]+=2
        else:
            self.rightinvalid=True
            self.wclick+=1
            self.backwclick[-1]+=1

    def doubles(self,x,y):
        self.dclick+=1
        aroundflag=0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if 0<=i<self.height and 0<=j<self.width and \
                       self.map[i][j].show=='!':
                    aroundflag+=1
        if str(aroundflag)==self.map[x][y].show:
            self.openaround(x,y)
        else:
            self.wclick+=1
            self.backwclick[-1]+=1

    def down(self,x,y,change=True):
        if self.map[x][y].show==' ':
            self.push.append((x,y))
            self.back[-1].append('push.pop()')
            self.setmark(x,y,'□')

    def left(self,x,y,change=True):
        self.operate.append('lefts({0},{1})'.format(x,y))
        self.back[-1].append('operate.pop()')
        #self.map[x][y].mark='l'
        self.down(x,y)

    def right(self,x,y,change=True):
        self.operate.append('rights({0},{1})'.format(x,y))
        self.back[-1].append('operate.pop()')
        #self.map[x][y].mark='r'

    def double(self,x,y,change=True):
        self.operate.append('doubles({0},{1})'.format(x,y))
        self.back[-1].append('operate.pop()')
        #self.map[x][y].mark='d'
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if 0<=i<self.height and 0<=j<self.width:
                    self.down(i,j)

    def show(self):
        for i in self.push:
            self.setmark(i[0],i[1],' ')
        for i in self.operate:
            exec('self.'+i)
        self.back[-1].append('operate='+repr(self.operate))
        self.back[-1].append('push='+repr(self.push))
        self.push=[]
        self.operate=[]
    
    def setmark(self,x,y,ch,addback=True):
        if addback:
            #print 'setmark',x,y,ch
            self.back[-1].append('setmark({0},{1},\'{2}\',False)'\
                                 .format(x,y,self.map[x][y].mark))
        self.map[x][y].mark=ch
        
    def setshow(self,x,y,ch,addback=True):
        if addback:
            #print 'setshow',x,y,ch
            self.back[-1].append('setshow({0},{1},\'{2}\',False)'\
                                 .format(x,y,self.map[x][y].show))
        self.map[x][y].show=ch

    def mark(self,x,y):
        self.operate.insert(0,'setmark({0},{1},\' \')'.format(x,y))
        self.setmark(x,y,str(self.map[x][y].answer) \
                     if self.map[x][y].answer!=9 else '*')

    def showanswer(self):
        for i in range(self.height):
            for j in range(self.width):
                print self.map[i][j].answer,
            print


#a=minemap(s)
#print a
