from Tkinter import *
from math import sqrt


class UI(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid(padx=20, pady=20)

        self.cordsval = None
        self.points = []
        self.color = 15
        self.type = 0
        self.cbuttons = []
        self.tbuttons = []
        self.temppoints = []
        self.types = ["line", "rect", "circle", "arc", "pieslice", "bezier", "polygon", "random"]
        self.colvs = ["#000000", "#00000F", "#0003E0", "#0703EF", "#007800", "#00780F", "#007BE0", "#00C618",
                      "#007BEF", "#00001F", "#0007E0", "#0007FF", "#00F800", "#00F81F", "#00FFE0", "#00FFFF"]

        self.cs = Canvas(root, width=640, height=480, bg="BLACK")

        self.pal = Frame(root, bg="#5c5c5c", width=200, height=272)
        self.cols = Frame(root, bg="#5c5c5c", width=200, height=200, padx=5, pady=5)

        self.liframe = Frame(root, bg="#5c5c5c", width=200, height=280)
        self.liprop = Frame(root, bg="#5c5c5c", width=200, height=200)

        self.cs.grid(row=0, column=1, rowspan=2, padx=2, pady=2)
        self.pal.grid(row=0, column=2, rowspan=1, padx=2, pady=2)
        self.cols.grid(row=1, column=2, rowspan=1, padx=2, pady=2)
        self.liframe.grid(row=0, column=0, rowspan=1, padx=2, pady=2)
        self.liprop.grid(row=1, column=0, rowspan=1, padx=2, pady=2)

        self.templine = self.cs.create_line(0, 0, 0, 0, fill="#f0f0f0")
        self.tempoval = self.cs.create_oval(0, 0, 0, 0, outline="#f0f0f0")
        self.temprect = self.cs.create_rectangle(0, 0, 0, 0, outline="#f0f0f0")
        self.temparc = self.cs.create_arc(0, 0, 0, 0, outline="#f0f0f0", style=ARC, start=0, extent=270)
        self.temppie = self.cs.create_arc(0, 0, 0, 0, outline="#f0f0f0", style=PIESLICE)
        self.tempbez = self.cs.create_arc(0, 0, 0, 0, outline="#f0f0f0")
        self.temppoly = self.cs.create_polygon(0, 0, 0, 0, outline="#f0f0f0")

        self.initUi()
        self.actions()

    def initUi(self):
        for i in range(4):
            for j in range(2):
                x = i*2+j
                b = Button(self.pal, text=self.types[x], width=6, bg="WHITE",
                           command=lambda y=x: self.typechange(y))
                b.grid(row=i, column=j, padx=2, pady=2)
                b.config(relief=FLAT)
                self.tbuttons.append(b)
        self.tbuttons[0].config(bg="GREY")

        for i in range(4):
            for j in range(4):
                t = (4 * i) + j
                b = Button(self.cols, bg=self.colvs[t], width=1, padx=6,
                           command=lambda x=t: self.colourchange(x))
                b.grid(row=i, column=j, padx=2, pady=2)
                b.config(relief=FLAT)
                self.cbuttons.append(b)
        self.cbuttons[self.color].config(padx=3)



    def actions(self):
        self.cs.bind("<Motion>", self.cords)
        self.cs.bind("<Button-1>", self.getpts)
        self.cs.bind_all("<MouseWheel>", self.mouse_wheel)


    def colourchange(self, c):
        self.cbuttons[self.color].config(padx=6)
        self.color = c
        self.cbuttons[c].config(padx=3)


    def typechange(self, t):
        self.tbuttons[self.type].config(bg="WHITE")
        self.type = t
        self.tbuttons[t].config(bg="GREY")


    def cords(self, e):
        if self.cordsval:
            self.cs.delete(self.cordsval)
        self.cordsval = self.cs.create_text(e.x + 35, e.y + 10, text="(" + str(e.x) + "," + str(e.y) + ")")
        self.cs.itemconfig(self.cordsval, fill="#c4d4ff")

        if len(self.temppoints)>0:
            x1, y1 = self.temppoints[0], self.temppoints[1]
            if self.type == 0:
                self.cs.coords(self.templine, x1, y1, e.x, e.y)
            if self.type == 1:
                self.cs.coords(self.temprect, x1, y1, e.x, e.y)
            if self.type == 2:
                rad = int(sqrt(((x1-e.x) ** 2) + ((y1-e.y) ** 2)))
                self.cs.coords(self.tempoval, x1-rad, y1-rad, x1+rad, y1+rad)
            if self.type == 3:
                rad = int(sqrt(((x1-e.x) ** 2) + ((y1-e.y) ** 2)))
                self.cs.coords(self.temparc,  x1-rad, y1-rad, x1+rad, y1+rad)




    def getpts(self, e):
        if len(self.temppoints)>0:
            self.points.append([self.temppoints[2], self.temppoints[0], self.temppoints[1]])
            self.points.append([self.type, e.x, e.y])
            x1 = self.temppoints.pop(0)
            y1 = self.temppoints.pop(0)
            self.temppoints.pop(0)

            if self.type == 0:
                self.cs.create_line(x1, y1, e.x, e.y, fill=self.colvs[self.color])
            if self.type == 1:
                self.cs.create_rectangle(x1, y1, e.x, e.y, outline=self.colvs[self.color])
            if self.type == 2:
                rad = int(sqrt(((x1-e.x) ** 2) + ((y1-e.y) ** 2)))
                self.cs.create_oval(x1-rad, y1-rad, x1+rad, y1+rad, outline=self.colvs[self.color])


        else:
            self.temppoints.append(e.x)
            self.temppoints.append(e.y)
            self.temppoints.append(self.type)

    def mouse_wheel(self, e):
        print e.delta



root = Tk()
root.title("PyBGI")
app = UI(root)
root.mainloop()
