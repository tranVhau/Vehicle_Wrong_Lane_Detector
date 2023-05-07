import cv2
import tkinter as tk
from PIL import Image, ImageTk


#Purpose: draw the detection line by mouse, 
#input: 1st frame of video.
#output: coordinates of the detection line, lane of vehicle.
class LineDrawerGUI:
    def __init__(self, video_source):
        #triger mouse event to draw line
        self.start_x, self.start_y = None, None
        self.end_x, self.end_y = None, None
        self.line_coords = None
        self.root = tk.Tk()
        self.root.title("Draw Detection Line")
        self.video_source = video_source
        self.video = cv2.VideoCapture(video_source)
        ret, frame = self.video.read()
        # Resize the image to a new width and height
        new_width, new_height = 960, 540
        resized_frame = cv2.resize(frame, (new_width, new_height))
        self.image = Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(self.root, width=self.image.width, height=self.image.height)
        self.canvas.pack(expand=True, fill="both")
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.option_val = tk.StringVar(value="")
        tk.Label(self.root, text="Specify the side of lane:").pack()
        tk.Radiobutton(self.root, text="Car-Motobike", variable=self.option_val, value=1).pack()
        tk.Radiobutton(self.root, text="Motobike-Car", variable=self.option_val, value=2).pack()
        
        tk.Button(self.root, text="Confirm", command=self.save_names).pack()
        self.root.mainloop()
            

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_move_press(self, event):
        self.end_x, self.end_y = event.x, event.y
        self.redraw_lines()

    def on_button_release(self, event):
        self.line_coords = self.redraw_lines()
        
    def redraw_lines(self):
        self.canvas.delete("line")
        self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, tags="line", fill="red", width=1)
        line_coords = ((self.start_x,self.start_y),(self.end_x,self.end_y))
        return line_coords
    
    def save_names(self):
        self.option_val =self.option_val.get()
        self.video.release()
        self.root.after(1000, self.root.destroy)

