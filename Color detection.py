import tkinter as tk
from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
LARGEFONT =("Arial", 10)
def arrayscolorsUP(text):
    if text=="Red":Upper=np.array([10, 255, 255])
    elif text =="Blue":Upper=np.array([130, 255, 255])
    elif text=="Yellow":Upper=np.array([30, 255, 255])
    elif text=="Pink":Upper=np.array([350, 255, 255])
    elif text=="Green": Upper=np.array([80, 255, 255])
    elif text=="Black":Upper=np.array([179, 255, 30])
    elif text=="White":Upper=np.array([179, 18, 255])
    elif text=="Purple":Upper=np.array([160, 255, 255])
    return Upper
def arrayscolorsDOWN(text):
    if text=="Red":Lower=np.array([0, 100, 100])
    elif text =="Blue":Lower=np.array([100, 50, 50])
    elif text=="Yellow":Lower=np.array([20, 100, 100])
    elif text=="Pink":Lower=np.array([160, 50, 170])
    elif text=="Green": Lower=np.array([40, 40, 40])
    elif text=="Black":Lower=np.array([0, 0, 0])
    elif text=="White":Lower=np.array([0, 0, 231])
    elif text=="Purple":Lower=np.array([130, 50, 50])
    return Lower
def detect(img, clicked, self):
    if img == "":
        return
    # Read the image
    img1 = cv2.imread(img)
    img1 = cv2.resize(img1, (300, 300))
    # Convert to HSV color space
    HSV_im_1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    # Create the mask
    mask = cv2.inRange(HSV_im_1, arrayscolorsDOWN(clicked.get()), arrayscolorsUP(clicked.get()))
    # Convert the mask to a 3-channel image
    mask3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    # Apply the mask to the original image
    im_thresh_color = cv2.bitwise_and(img1, mask3)
    # Display the result
    b,g,r = cv2.split(im_thresh_color)
    im_thresh_color = cv2.merge((r,g,b))
    im = Image.fromarray(im_thresh_color)
    Page2.imgtk = ImageTk.PhotoImage(image=im)
    canvas = Canvas(self, width=300, height=300)
    canvas.create_image(10, 10, anchor=NW, image=Page2.imgtk)
    canvas.grid(row=6, column=1, padx=10, pady=10)
    # label2 = Label(self, image=Page2.imgtk)
    # label2.grid(row=6, column=1, padx=10, pady=10)

def browseFiles():
	filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("images","*.jpg*"),("images","*.png*"),("images","*.jpeg*")))
	return filename

class tkinterApp(tk.Tk):	
	# __init__ function for class tkinterApp 
	def __init__(self, *args, **kwargs): 
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True) 
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {} 

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage,Page2):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page2 respectively with 
			# for loop
			self.frames[F] = frame 

			frame.grid(row = 0, column = 0, sticky ="nsew")
			frame.configure(bg="#5A47A5")

		self.show_frame(StartPage)
	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()    
        
# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller): 
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = Label(self, text ="Welcome to the Color detection App\nChoose an Option", font = LARGEFONT, bg="#5A47A5")
		
		# putting the grid in its place by using
		# grid
		label.grid(row = 1, column = 1) 

		buttonphoto = Button(self, text ="Choose photo",
		command = lambda :controller.show_frame(Page2),
		width=17,bg="#3401FF", activebackground="#3401FF")
	
		# putting the button in its place by
		# using grid
		buttonphoto.grid(row = 3, column = 0, padx = 5)



# third window frame page2
class Page2(tk.Frame):
    imgtk=ImageTk
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = Label(self, text ="Choose a color then a photo", font = LARGEFONT, bg="#5A47A5")
        label.grid(row = 1, column = 1, padx = 10, pady = 10)
        options = [ 
			"Red", 
			"Yellow", 
			"Blue", 
			"Pink", 
			"Green", 
			"Black", 
			"White",
			"Purple"
		];clicked = StringVar();clicked.set( "Red" )
        drop = OptionMenu( self , clicked , *options )
        button1 = Button(self, text ="Choose",bg="#CCA62C",command = lambda :detect(browseFiles(),clicked,self), activebackground="#CCA62C")
        button2 = Button(self, text ="Back",bg="#6D2061",command = lambda :controller.show_frame(StartPage), activebackground="#6D2061")
        drop.grid(row=1,column=2,padx=10,pady=10)
        button1.grid(row =2, column = 1,padx=10,pady=10)
        button2.grid(row = 2, column = 2,padx=10,pady=10)
			

# Driver Code
app = tkinterApp()
app.title('Photo Color detection')
app.geometry('500x700')
app.resizable(width=False, height=False)
app.mainloop()

