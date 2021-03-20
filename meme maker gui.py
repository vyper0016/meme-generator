from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError, ImageTk
from textwrap import wrap


# ------ Classes -----

class BottomText:
    def __init__(self):
        self.label = Label(frameLeft, text='Bottom text:')
        self.input = Entry(frameLeft, width=35, textvariable=bottomStr)

    def put(self):
        self.label.grid(row=2, column=0, padx=3, pady=2, sticky=W)
        self.input.grid(row=3, column=0, padx=3, pady=10)

    def remove(self):
        self.label.grid_forget()
        self.input.grid_forget()


# ----- Functions -----

imageDir = ''


def open_file():
    global imageDir
    imageDir = filedialog.askopenfilename(initialdir='D:/Pictures/oc memes', title="Choose A Picture",
                                          filetypes=(('JPEG files', "*.jpg"), ("PNG files", "*.png"),
                                                     ("All files", "*.*")))
    # print(imageDir)
    preview()


def save_file():
    save_dir = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    # print(save_dir)
    if not save_dir:
        return

    if not imageDir:
        status.config(text='Please select an Image first')
        return
    att = add_text()
    if att:
        att.save(save_dir)
        print(save_dir.name())
        status.config(text='Image saved in')
    else:
        status.config(text='An Error has occurred while trying to save the image')


def bottom_check():
    global bottomLabel
    v = bottom.get()
    if v:
        bottomLabel.put()
    else:
        bottomLabel.remove()

    preview()


def preview():
    global img
    if previewVariable.get():

        if imageDir:
            status.config(text='nice meme bro')
            # print(imageDir)
            load = add_text()
            if load:
                img.config(image='')
                render = ImageTk.PhotoImage(load)
                img.config(image=render)
                img.image = render
                img.pack(fill=X)


def size_change():
    if not size.get():
        preview()


def add_margin(pil_img, top=0, bottom_margin=0, right=0, left=0, color='white'):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom_margin
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def add_text():
    if colorsVariable.get() == 1:
        color = 'black'
        bg_color = 'white'
    else:
        bg_color = 'black'
        color = 'white'

    try:
        new_image = Image.open(imageDir)
    except UnidentifiedImageError:
        status.config(text='Please select a valid image file')
        return

    wi, h = new_image.size

    if size.get():
        txt_size = int(h / 14)
    else:
        txt_size = int(sizeStr.get())

    fnt = ImageFont.truetype('arial.ttf', txt_size)
    top_txt = topStr.get()

    cw, ch = fnt.getsize('C')
    cpl = wi // cw
    # txt = txt.upper()
    top_lines = wrap(top_txt, cpl)

    y = 10
    top_mh = 10
    for l in top_lines:
        top_mh += fnt.getsize(l)[1]
    top_mh += 5

    if bottom.get():
        bot_text = bottomStr.get()
        bot_lines = wrap(bot_text, cpl)
        bot_mh = 10
        for l in bot_lines:
            bot_mh += fnt.getsize(l)[1]
        bot_mh += 5
    else:
        bot_mh = 0

    new_image = add_margin(new_image, top_mh, bottom_margin=bot_mh, color=bg_color)

    if new_image.size[1] > 625:
        status.config(text='Too many lines bruh')
        return

    d = ImageDraw.Draw(new_image)

    for l in top_lines:
        lw, lh = fnt.getsize(l)
        x = (wi - lw) / 2
        d.text((x, y), l, fill=color, font=fnt)
        y += lh

    if bottom.get():
        h = new_image.size[1]

        y = h - ch * len(bot_lines) - 12

        for l in bot_lines:
            lw, lh = fnt.getsize(l)
            x = (wi - lw) / 2
            d.text((x, y), l, fill=color, font=fnt)
            y += lh

    return new_image


def reset():
    bottomStr.set('')
    topStr.set('')


w = 300
root = Tk()
# root.geometry(str(w)+'x200')

# -------- Main Menu --------

menu = Menu(root)
root.config(menu=menu)
subMenu1 = Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=subMenu1)
subMenu1.add_command(label='Open', command=open_file)
subMenu1.add_command(label='Save', command=save_file)
subMenu1.add_separator()
subMenu1.add_command(label='Exit', command=root.quit)

# ------ Status Bar ------

status = Label(root, text='Please open a picture', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

# ----- Frames -----

frame1 = Frame(root, width=w, height=200)
frame1.pack(fill=X)
frame2 = Frame(root)
frame2.pack(fill=X, side=BOTTOM)
frame3 = Frame(root)
frame3.pack(fill=X, side=BOTTOM)
frameLeft = Frame(frame3, width=100, height=100)
frameLeft.pack(side=LEFT, fill=X)
frameRight = Frame(frame3)
frameRight.pack(side=RIGHT, fill=X, anchor=N)

frame2.grid_rowconfigure(0, weight=1)
frame2.grid_columnconfigure(0, weight=1)

# ----- Labels -----

bottomStr = StringVar()
topStr = StringVar()

img = Label(frame1)

sizeLabel = Label(frame2, text='Size: ')
topLabel = Label(frameLeft, text='Top text:')
topInput = Entry(frameLeft, width=35, textvariable=topStr)
bottomLabel = BottomText()

# ----- Boxes -----

bottom = BooleanVar()
size = BooleanVar()
previewVariable = BooleanVar()
colorsVariable = IntVar()

bottomCheck = Checkbutton(frameRight, text='Bottom text', command=bottom_check, variable=bottom)
check1 = Radiobutton(frameRight, command=preview, text='Black on White', variable=colorsVariable, value=1)
check2 = Radiobutton(frameRight, command=preview, text='White on Black', variable=colorsVariable, value=2)
recommendedSize = Checkbutton(frameRight, text='Recommended size', command=preview, variable=size)
previewCheck = Checkbutton(frameRight, text='Preview', command=preview, variable=previewVariable, font=('Arial', 7))

# ----- Placing -----

topLabel.grid(row=0, column=0, padx=3, pady=2, sticky=W)
topInput.grid(row=1, column=0, padx=20, pady=10)

bottomCheck.grid(row=0, padx=3, pady=2, sticky="e", columnspan=2)
check1.grid(row=1, padx=3, pady=2, sticky="e", columnspan=2)
check2.grid(row=2, padx=3, pady=2, sticky="e", columnspan=2)
recommendedSize.grid(row=3, padx=3, pady=2, sticky="e", columnspan=2)
previewCheck.grid(row=4, padx=3, pady=2, sticky="e", columnspan=2)
sizeLabel.grid(row=0, column=3, padx=3, pady=2, sticky=E)

# ----- Font -----

lst = []
for i in range(8, 73, 2):
    lst.append(i)

sizeStr = StringVar()

resetButton = Button(frame2, text='Reset', command=reset)
resetButton.grid(row=0, columnspan=2, padx=3, pady=2, sticky=E)

fontSizeCombo = Combobox(frame2, value=lst, width=4, textvariable=sizeStr)
fontSizeCombo.grid(row=0, column=4, padx=3, pady=2, sticky=E)

# ----- Initialization -----

size.set(True)
sizeStr.set(10)
colorsVariable.set(1)
previewVariable.set(True)

# ----- Trace -----
topStr.trace("w", lambda name, index, mode: preview())
bottomStr.trace("w", lambda name, index, mode: preview())
sizeStr.trace("w", lambda name, index, mode: size_change())

root.mainloop()
