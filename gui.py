from tkinter import *
from tkinter.ttk import Scale
from tkinter import colorchooser,filedialog,messagebox
import PIL.ImageGrab as ImageGrab
from droneplacer import analyse

class Draw():
    def __init__(self,root):
        self.root =root
        self.root.title("Drone Placer")
        self.root.configure(background="purple")
        self.root.geometry("800x700")
        self.root.resizable(0,0)
   
        self.pointer="black"
        self.erase="white"
        
        self.dronecount=StringVar()
        self.coordinateplane=StringVar()

        text=Text(root)
        text.tag_configure("Head_Label", justify='center', font=('arial',25),background='black',foreground='white')

        text.insert("1.0", "GUI for Drone Placement")
        text.tag_add("Head_Label", "1.0", "end")
        text.pack()
        
        self.pick_color = LabelFrame(self.root,text='Colors',font =('arial',15),relief=RIDGE,bd=5,bg="white")
        self.pick_color.place(x=0,y=550,width=185,height=90)

        colors = ['blue','red','green','orange','black','yellow']
        i=j=0
        for color in colors:
            Button(self.pick_color,bg=color,bd=2,relief=RIDGE,width=3,command=lambda col=color:self.select_color(col)).grid(row=i,column=j)
            j+=1
            if j==3:
                i=1
                j=0

        self.eraser= Button(self.root,text="Eraser",bd=4,bg='white',command=self.eraser,width=9,relief=RIDGE)
        self.eraser.place(x=100,y=650)


        self.clearScreen= Button(self.root,text="Clear Screen",bd=4,bg='white',command= lambda : self.background.delete('all'),width=9,relief=RIDGE)
        self.clearScreen.place(x=250,y=650)


        self.saveImage= Button(self.root,text="Analyse",bd=4,bg='white',command=self.screenshot,width=9,relief=RIDGE)
        self.saveImage.place(x=450,y=650)

        self.quit=Button(self.root,text="Exit",bd=4,bg='white',command= lambda : self.root.destroy(),width=9,relief=RIDGE)
        self.quit.place(x=600,y=650)

        self.pointer_frame= LabelFrame(self.root,text='Size',bd=5,bg='white',font=('arial',15,'bold'),relief=RIDGE)
        self.pointer_frame.place(x=550,y=550,height=70,width=200)

        self.pointer_size =Scale(self.pointer_frame,orient=HORIZONTAL,from_ =0 , to =48, length=168)
        self.pointer_size.set(1)
        self.pointer_size.grid(row=0,column=1,padx=15)


        self.background = Canvas(self.root,bg='white',bd=5,relief=GROOVE,height=470,width=800)
        self.background.place(x=0,y=40)

        self.dronecountLabel=Label(self.root,text="No. Of Drones",bd=5,bg='white',font=('arial',15,'bold'),relief=RIDGE)
        self.dronecountLabel.place(x=200,y=550)
        self.dronecountEntry=Entry(self.root,textvariable=self.dronecount)
        self.dronecountEntry.place(x=350,y=555)

        self.coordinateplaneLabel=Label(self.root,text="Plane",bd=5,bg='white',font=('arial',15,'bold'),relief=RIDGE)
        self.coordinateplaneLabel.place(x=200,y=600)
        self.coordinateplaneEntry=Entry(self.root,textvariable=self.coordinateplane)
        self.coordinateplaneEntry.place(x=350,y=605)

        self.background.bind("<B1-Motion>",self.paint) 

    def paint(self,event):       
        x1,y1 = (event.x-2), (event.y-2)  
        x2,y2 = (event.x+2), (event.y+2)  

        self.background.create_oval(x1,y1,x2,y2,fill=self.pointer,outline=self.pointer,width=self.pointer_size.get())
 
    def select_color(self,col):
        self.pointer = col

    def eraser(self):
        self.pointer= self.erase
   
    def canvas_color(self):
        color=colorchooser.askcolor()
        self.background.configure(background=color[1])
        self.erase= color[1]

    def screenshot(self):
        file_ss =filedialog.asksaveasfilename(defaultextension='jpg')
        x=self.root.winfo_rootx() + self.background.winfo_x()
        y=self.root.winfo_rooty() + self.background.winfo_y()

        x1= x + self.background.winfo_width() 
        y1= y + self.background.winfo_height()
        
        try:
            ImageGrab.grab().crop((x, y, x1, y1)).convert("RGB").save(file_ss)
        except:
            print("Error in saving the screenshot for analysis")
        
        analyse(file_ss, int(self.dronecount.get()), self.coordinateplane.get())

if __name__ =="__main__":
    root=Tk()
    p=Draw(root)
    root.mainloop()