import tkinter.filedialog
from tkinter.filedialog import askopenfile
from tkinter import *
from tkinter.ttk import *
import pathlib


root = Tk()
canvas2 = Canvas(root, width=400, height=400)
canvas2.pack()


boi = Tk()
boi.withdraw()
def file_open():
    global filename, tmfile
    #filename = askopenfile(mode = 'r', filetypes = (("treemaker files","*.tmd5"),("all files","*.*")))
    #print (filename)
    file = askopenfile(mode = 'r', filetypes = (("treemaker files","*.tmd5"),("all files","*.*")))
    if file is not None: # asksaveasfile return `None` if dialog closed with "cancel".
        filename = pathlib.Path(file.name).name
        def load_words(filename):
            with open(filename) as word_file:
                valid_words = list(word_file.read().split())
            return valid_words
        tmfile = load_words(filename)

vertices = ['buffer item'] #because treemaker counts from 1 rather than 0, so the buffer item lines everything up
creases = ['buffer item']
def findvertices():
    global vertices
    for x in range(0,len(tmfile)):
        if tmfile[x] == 'vrtx':
            vertices.append((tmfile[x+2],tmfile[x+3]))        
def findcreases():
    findvertices()
    global creases
    for x in range(0,len(tmfile)):
        if tmfile[x] == 'crse':
            mv = int(tmfile[x+8])+0
            if mv==1:  #tm's mountains should be valley
                mv = 3
            elif mv ==3: #edges, like when you cut off the corner
                mv = 1  
            creases.append((vertices[int(tmfile[x+4])],vertices[int(tmfile[x+5])],mv))
            #also need to extract the m/v, or at least axial vs hinge vs ridge
def cp(tm): #converts tm coordinates to .cp coordinates
    return (float(tm)*400)-200
def makecp():
    global cpfile
    cpfile = ["1 -200 -200 -200 200", "1 -200 200 200 200", "1 200 200 200 -200", "1 200 -200 -200 -200"]
    findcreases()
    for x in range(1, len(creases)):
        cpfile.append(str(creases[x][2])+" "+str(cp(creases[x][0][0]))+" "+str(cp(creases[x][0][1]))+" "+str(cp(creases[x][1][0]))+" "+str(cp(creases[x][1][1])))


def file_save():
    filename = tkinter.filedialog.asksaveasfile(mode='w+', defaultextension=".cp",parent = boi)
    if filename is None: # asksaveasfile return `None` if dialog closed with "cancel".
        boi.withdraw()
        return
    for x in range(0,len(cpfile)):
        #print(cp_file[x])
        filename.write(str(cpfile[x])+"\n")
        
    filename.close()
    boi.withdraw()


enter = Button(canvas2,text="Import .tmd5 file",command=file_open)
enter.place(x=160,y=100)

enter = Button(canvas2,text="extract creases",command=makecp)
enter.place(x=165,y=200)

enter = Button(canvas2,text="export as .cp file",command=file_save)
enter.place(x=165,y=300)

#==============================================================================================================
#============================================================================================================== for adding new features later
'''
gridsize = int(1/tmfile[4])+1

class path():
    #you need a pytha if max(x distance, y distance) > minlength
    def __init__(index,length,minlength):
        pass
'''















