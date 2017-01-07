import ImageGrab, Image
import time
import threading
#tmp

import Tkinter
import ImageTk

__author__ = 'Yair'
'''
current = ImageGrab.grab()
old = Image.open("img.png")
dif = Image.new(old.mode, old.size, None)
o_pixels = old.load()
c_pixels = current.load()
d_pixels = dif.load()
print time.gmtime()
for i in range(old.size[0]):
    for j in range(old.size[1]):
        d_pixels[i,j] = (255,255,255) if c_pixels[i,j] == o_pixels[i,j] else c_pixels[i, j]
print time.gmtime()
dif.save("dif.png")
current.save("img.png")'''

id = 0

def update(canvas):
    global id
    for i in range(1000):
        current = ImageGrab.grab()
        imagebox = ImageTk.PhotoImage(current)
        canvas.itemconfig(id, image=imagebox)

        time.sleep(0.5)

def main():
    global id
    current = ImageGrab.grab()

    root = Tkinter.Tk()

    imagebox = ImageTk.PhotoImage(current)
    canvas = Tkinter.Canvas(root)
    canvas["width"] = current.size[0]
    canvas["height"] = current.size[1]
    id = canvas.create_image((current.size[0]/2,current.size[1]/2), image=imagebox)
    canvas.pack()

    update_thread = threading.Thread(target = lambda: update(canvas), args=())
    update_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
