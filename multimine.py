# -*- coding: UTF-8 -*-

from map import *
import re

debug=False
class step:
    def __init__(self,string=''):
        t=string.split(';')
        self.text=t[0]
        self.clicks=t[1:]

    def __repr__(self):
        s=self.text
        for i in self.clicks:
            s+=';'+i
        return s
            
class node:
    def __init__(self,p,string=''):
        self.steps=[step(i) for i in string.split('|')]
        self.pre=p
        self.next=[]

    def __repr__(self):
        s=repr(self.steps[0])
        for i in self.steps[1:]:
            s+='|'+repr(i)
        for i in self.next:
            s+='{'+repr(i)+'}'
        return s
    
    def addstep(self,string):
        self.steps.append(step(string))

        
class multimine(minemap):
    def __init__(self):
        self.filename='Untitled.txt'
        #self.nextnum=0
        minemap.__init__(self)
        #self.readfile()
        
    def read(idir):
        def fee(func):
            def wrap(self):
                self.filename = askopenfilename(initialdir =idir)
                if self.filename=='':
                    return False
                file_object = open(self.filename)
                try:
                    string = file_object.read( )
                finally:
                    file_object.close( )
                    func(self)(string)
            return wrap
        return fee

    @read(idir='replay')
    def readfile(self):
        return self.readstring
    
    def readstring(self,string):
        size=eval(string[:string.index(']')+1])
        string=string[string.index(']')+1:]
        self.newmap(size)
        self.result=None
        q=node(None)
        self.p=q
        i=0
        length=len(string)
        while i<length:
            try:
                l=string.index('{',i)
            except:
                l=len(string)
            try:
                r=string.index('}',i)
            except:
                r=len(string)
                
            j=min(l,r)
            if i!=j:
                self.p.next.append(node(self.p,string[i:j]))
            if j<length:
                if string[j]=='{':
                    self.p=self.p.next[-1]
                elif string[j]=='}':
                    self.p=self.p.pre
            i=j+1
        if q.next==[]:
            self.head=q
        else:
            self.head=q.next[0]
        self.head.pre=None
        self.p=self.head
        self.clicknum=-1
        self.stepnum=-1
        #self.p=self.head
        #self.nextnode(0)
        return True
        
    def writefile(self):
        if self.filename=='':
            return False
        file_object = open(self.filename, 'w')
        try:
            file_object.write(repr([self.width,self.height])+repr(self.head))
        finally:
            file_object.close( )
        return True
    def savefile(self):
        self.filename = asksaveasfilename(initialdir ='replay',defaultextension='.txt')
        self.writefile()

    def newfile(self):
        self.readstring(self.text.get(1.0,END)[:-1])
        self.p.steps[self.stepnum+1].text='开始'
        self.readstep()
        
        
        
    @read(idir='arbitertxt')
    def readmine(self):
        def f(string):
            string=string[string.index('.txt')+4:]
            for i in range(self.height):
                for j in range(self.width):
                    if (string[i*(self.width+1)+j] in ['F','_']):
                        self.addclick('addmine({0},{1})'.format(i,j))
            return True
        return f


    @read(idir='arbitertxt')
    def readopen(self):
        def f(string):
            string=string[string.index('.txt')+4:]
            for i in range(self.height):
                for j in range(self.width):
                    if ('0'<=string[i*(self.width+1)+j]<='8'):
                        self.addclick('lefts({0},{1})'.format(i,j))
                    elif (string[i*(self.width+1)+j] == 'F'):
                        self.addclick('rights({0},{1})'.format(i,j))
            return True
        return f

    @read(idir='rawvf')
    def readrawvf(self):
        def f(string):
            w=int(string[string.index('Width: ')+7:string.index('Height: ')-1])
            h=int(string[string.index('Height: ')+8:string.index('Mines: ')-1])
            self.readstring('[{0},{1}]'.format(w,h))
            self.p.steps[self.stepnum+1].text='布雷中……'
            self.readstep()
            string=string[string.index('Board:\n')+7:]
            for i in range(h):
                for j in range(w):
                    if string[i*(w+1)+j]=='*':
                        self.addclick('addmine({0},{1})'.format(i,j))            
            string=string[string.index('start\n')+6:]
            self.addstep()
            for step in string.split('\n'):
                if step=='':
                    break
                if not step[0].isdigit():
                    continue
                step=re.split(' \(| |\)',step)
                if step[1]=='won':
                    break
                if step[1]=='mv':
                    continue
                #self.addclick('{1}({3},{2})'.format(*step))
                step[2]=int(step[2])/16
                step[3]=int(step[3])/16
                if step[1]=='lc':
                    self.lc(step[3],step[2])
                elif step[1]=='rc':
                    self.rc(step[3],step[2])
                elif step[1]=='lr':
                    self.lr(step[3],step[2])
                elif step[1]=='rr':
                    self.rr(step[3],step[2])
                
                if step[1] in ['lr','rr']:
                    self.addstep()
            self.delstep()
            return True
        return f        

        
    def fastkey(self,event):
        if event.keysym=='Right':
            self.play()
        elif event.keysym=='Left':
            self.backstep()
        elif event.keysym in ['w','s','a','d']:
            self.BigTDirection=event.keysym

    '''
        if event.keysym.isdigit():
            num=int(event.keysym)-1
            if 0<=num<=6:
                self.clickoperate[0]=self.mouseoperate[num]

    '''

    def onclick(self,event):
        x=event.widget['pady']
        y=event.widget['padx']
        c=event.num-1
        if self.clickoperate[c]=='addBigT':
            self.addBigT(x,y)
        else:
            self.addclick(self.clickoperate[c]+'({0},{1})'.format(x,y))
    def addBigT(self,x,y):
        self.addclick('addmine({0},{1})'.format(x,y))
        self.addclick('rights({0},{1})'.format(x,y))
        if self.BigTDirection=='s':
            self.addclick('left({0},{1})'.format(x+1,y))
            self.addclick('double({0},{1})'.format(x+1,y))
            self.addclick('double({0},{1})'.format(x,y-1))
            self.addclick('double({0},{1})'.format(x,y+1))
        elif self.BigTDirection=='w':
            self.addclick('left({0},{1})'.format(x-1,y))
            self.addclick('double({0},{1})'.format(x-1,y))
            self.addclick('double({0},{1})'.format(x,y-1))
            self.addclick('double({0},{1})'.format(x,y+1))
        elif self.BigTDirection=='a':
            self.addclick('left({0},{1})'.format(x,y-1))
            self.addclick('double({0},{1})'.format(x,y-1))
            self.addclick('double({0},{1})'.format(x-1,y))
            self.addclick('double({0},{1})'.format(x+1,y))
        elif self.BigTDirection=='d':
            self.addclick('left({0},{1})'.format(x,y+1))
            self.addclick('double({0},{1})'.format(x,y+1))
            self.addclick('double({0},{1})'.format(x-1,y))
            self.addclick('double({0},{1})'.format(x+1,y))

        
    def addclick(self,operate):
        if self.stepnum==-1:
            self.explaintext.set('请先创建新步骤')#.decode('UTF-8')
            return False
        self.p.steps[self.stepnum].clicks.insert(self.clicknum+1,operate)
        self.readclick()
        return True
        
    def addshow(self):
        self.addclick('show()')

    def fullmine(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].mark!='□' and \
                   self.map[i][j].show ==' ' and \
                   self.map[i][j].answer!=9:
                    self.addclick('addmine({0},{1})'.format(i,j))

    


    def addstep(self):
        self.endclick()
        self.p.steps.insert(self.stepnum+1,step('新步骤'))
        self.nextstep()

    def backstep(self,delete=False):
        if self.back==[]:
            return False
        steps=self.back.pop()
        while steps!=[]:
            if debug:
                print steps[-1]
            exec('self.'+steps.pop())
        if delete:
            del self.p.steps[self.stepnum]
        self.stepnum-=1
        #print self.stepnum
        if self.stepnum==-1:
            if self.p.pre is None:
                #self.stepnum+=1
                return False
            q=self.p.pre
            if self.p.steps==[]:
                t=q.next.index(self.p)
                del q.next[t]
            self.p=self.p.pre
            self.stepnum=len(self.p.steps)-1
            if len(self.p.next)==1:
                self.p.steps+=self.p.next[0].steps
                self.p.next=self.p.next[0].next
        text=self.p.steps[self.stepnum].text
        self.explaintext.set(text)
        self.clicknum=len(self.p.steps[self.stepnum].clicks)-1
        self.branch.delete(0,END)
        return True
    
    def delstep(self):
        self.backstep(True)
            

    def addnode(self):
        self.endstep()
        self.p.next.append(node(self.p))
        self.nextnode(-1)
        self.p.steps[0].text='新分支'
        self.nextstep()

    def setexplain(self):
        text=self.text.get(1.0,END)[:-1]
        self.p.steps[self.stepnum].text=text.encode('UTF-8')
        self.explaintext.set(text)

    def addbranch(self):
        self.endclick()
        if self.stepnum==-1:
            self.backstep()
        #print self.stepnum,len(self.p.steps)
        if self.stepnum+1!=len(self.p.steps):
            q=node(self.p)
            q.steps=self.p.steps[self.stepnum+1:]
            q.next=self.p.next
            self.p.steps=self.p.steps[:self.stepnum+1]
            self.p.next=[q]
        self.addnode()

        
        

    def play(self):
        if not self.readstep():
            if self.branch.size()==0:
                self.shownext()
            else:
                self.nextnode(self.branch.curselection()[0])
                self.branch.delete(0,END)
                self.play()
   
        
    def shownext(self):
        if self.p.next!=[]:
            self.explaintext.set(self.explaintext.get()+'\n请选择分支'.decode('UTF-8'))
            for i in self.p.next:
                self.branch.insert(END,i.steps[0].text)
            self.branch.selection_set(0)

    def reset(self):
        while self.backstep():
            pass
        
    

    def readclick(self):#在当前step内走1click，若已指向最后1click则返回失败
        if self.stepnum==-1:
            return False
        self.clicknum+=1
        if self.clicknum==len(self.p.steps[self.stepnum].clicks):
            self.clicknum-=1
            return False
        #if self.clicknum==0:
        #    text=self.p.steps[self.stepnum].text
        #    self.explaintext.set(text)
        operate=self.p.steps[self.stepnum].clicks[self.clicknum]
        if debug:
            print operate
        exec('self.'+operate)
        return True

    def endclick(self):#在当前step内走完click，若已指向最后1click则返回失败
        if self.readclick():
            while self.readclick():
                pass
            return True
        return False

    def readstep(self):
        if self.nextstep():
            self.endclick()
            return True
        return False
    
    def nextstep(self):#指向当前node内下一step，若已指向最后1step则返回失败
        self.stepnum+=1
        if self.stepnum==len(self.p.steps):
            self.stepnum-=1
            return False
        self.clicknum=-1
        self.back.append([])
        text=self.p.steps[self.stepnum].text
        self.explaintext.set(text)
        return True

    def endstep(self):#在当前node内走完step，若已指向最后1step的最后1click则返回失败
        if not self.endclick():
            if not self.nextstep():
                return False
            self.endclick()
        while self.readstep():
            pass
        return True

    def readnode(self,num):
        if self.nextnode(num):
            self.endstep()
            return True
        return False

    def nextnode(self,num):#指向下表为num的下一node，若最后1node则返回失败
        if self.p.next==[]:
            return False
        self.p=self.p.next[num]
        self.clicknum=-1
        self.stepnum=-1
        #self.back.append([])
        return True

    def endnode(self):#走完雷谱的主线，若已指向若最后1node的最后1step的最后1click则返回失败
        if not self.endstep():
            if not self.nextnode(0):
                return False
            self.endstep()
        while self.nextnode(0):
            self.endstep()

    def goclick(self):
        if not self.readclick():#尝试走click
            if not self.nextstep():#如果走不了click先尝试走step
                if not self.nextnode(0):#如果走不了step再尝试走node
                    return False#都走不了说明已走到底
            self.readclick()#如果走不了click但能先走完step或node则再走click
        return True

    def gostep(self):
        if not self.readstep():
            if not self.nextnode(0):
                return False
            self.endclick()
        return True
    
    def gonode(self):
        return readnode(0)

    def go(self,move,num):
        for i in range(num):
            if not move():
                break

    def showblock(self,i,j):
        t=self.map[i][j].show if self.map[i][j].mark==' ' else self.map[i][j].mark
        r,c=self.skinlist[t]
        self.pic[i][j].place(x = -2-c*16,y = -2-r*16)
        self.window[i][j].grid(row = i,column = j)
        
    def setshow(self,x,y,ch,addback=True):
        minemap.setshow(self,x,y,ch,addback)
        self.showblock(x,y)
        
    def setmark(self,x,y,ch,addback=True):
        minemap.setmark(self,x,y,ch,addback)
        self.showblock(x,y)
        
a=multimine()
