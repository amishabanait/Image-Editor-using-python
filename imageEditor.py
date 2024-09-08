import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog
import cv2
import numpy as np

rot = 0
outputImage = None  # Initialize outputImage here
image_history = []  # Maintain a history of image states
undo_limit = 5  # Set the limit for undo steps


def displayImage(displayImage):
    ImagetoDisplay = displayImage.resize((900, 600))
    ImagetoDisplay = ImageTk.PhotoImage(ImagetoDisplay)
    showWindow.config(image=ImagetoDisplay)
    showWindow.photo_ref = ImagetoDisplay
    showWindow.pack()


def importButton_callback():
    global originalImage, outputImage, image_history
    filename = filedialog.askopenfilename()  # asking from user which image
    originalImage = Image.open(filename)  # for data
    outputImage = originalImage
    image_history = [originalImage.copy()]  # Clear history and add initial image state
    displayImage(originalImage)


def saveButton_callback():
    savefile = filedialog.asksaveasfile(defaultextension=".jpg")  # saving file as jpg
    if savefile:
        outputImage.save(savefile)  # what we have to save


def closeButton_callback():
    window.destroy()


def brightness_callback(brightness_pos):
    global outputImage, image_history
    brightness_pos = float(brightness_pos)  # converting string to float
    if outputImage:
        enhancer = ImageEnhance.Brightness(outputImage)
        outputImage = enhancer.enhance(brightness_pos)
        image_history.append(outputImage.copy())  # Add new state to history
        if len(image_history) > undo_limit:  # Limit the size of the history
            del image_history[0]  # Remove oldest state
        displayImage(outputImage)


def contrast_callback(contrast_pos):
    global outputImage, image_history
    contrast_pos = float(contrast_pos)  # converting string to float
    if outputImage:
        enhancer = ImageEnhance.Contrast(outputImage)
        outputImage = enhancer.enhance(contrast_pos)
        image_history.append(outputImage.copy())  # Add new state to history
        if len(image_history) > undo_limit:  # Limit the size of the history
            del image_history[0]  # Remove oldest state
        displayImage(outputImage)


def rotateButton_callback():
    global outputImage, rot, image_history
    rot += 90
    if outputImage:
        outputImage = outputImage.rotate(angle=90)
        image_history.append(outputImage.copy())  # Add new state to history
        if len(image_history) > undo_limit:  # Limit the size of the history
            del image_history[0]  # Remove oldest state
        displayImage(outputImage)


def undoButton_callback():
    global outputImage, image_history
    if len(image_history) > 1:  # Ensure there's a state to undo to
        image_history.pop()  # Remove the current state
        outputImage = image_history[-1]  # Set outputImage to the previous state
        displayImage(outputImage)


def colorButton_callback(color):
    global outputImage, image_history
    if outputImage:
        opencvImage = cv2.cvtColor(np.array(outputImage), cv2.COLOR_RGB2BGR)
        if color == "yellow":
            opencvImage[:, :, 0] = 20
        elif color == "blue":
            opencvImage[:, :, 2] = 100
        elif color == "pink":
            opencvImage[:, :, 1] = 100
        elif color == "orange":
            opencvImage[:, :, 2] = 200
        outputImage = Image.fromarray(cv2.cvtColor(opencvImage, cv2.COLOR_BGR2RGB))
        image_history.append(outputImage.copy())  # Add new state to history
        if len(image_history) > undo_limit:  # Limit the size of the history
            del image_history[0]  # Remove oldest state
        displayImage(outputImage)


window = tk.Tk()  # to create a GUI window
screen_width = window.winfo_screenwidth()  # to return width of the screen
screen_height = window.winfo_screenheight()  # to return height of the screen
window.geometry(f'{screen_width}x{screen_height}')
window.configure(bg='black')

Frame1 = tk.Frame(window)
Frame1.pack(anchor=tk.N)

Frame2 = tk.Frame(window)
Frame2.pack(anchor=tk.N)

Frame3 = tk.Frame(window)
Frame3.pack(anchor=tk.N)

importButton = tk.Button(Frame1, text="Import", padx=10, pady=5,
                         command=importButton_callback)
importButton.grid(row=0, column=0)

saveButton = tk.Button(Frame1, text="Save", padx=10, pady=5,
                       command=saveButton_callback)
saveButton.grid(row=0, column=1)

closeButton = tk.Button(Frame1, text="Close", padx=10, pady=5,
                        command=closeButton_callback)
closeButton.grid(row=0, column=8)

rotateButton = tk.Button(Frame1, text="Rotate", padx=10, pady=5,
                         command=rotateButton_callback)
rotateButton.grid(row=0, column=2)

undoButton = tk.Button(Frame1, text="Undo", padx=10, pady=5,
                       command=undoButton_callback)
undoButton.grid(row=0, column=3)

brightnessSlider = tk.Scale(Frame2, label="Brightness", from_=0, to=2, orient=tk.HORIZONTAL,
                            length=screen_width, resolution=0.1, command=brightness_callback)
brightnessSlider.set(1)
brightnessSlider.pack(anchor=tk.N)

contrastSlider = tk.Scale(Frame2, label="Contrast", from_=0, to=2, orient=tk.HORIZONTAL,
                          length=screen_width, resolution=0.1, command=contrast_callback)
contrastSlider.set(1)
contrastSlider.pack(anchor=tk.N)

yellowButton = tk.Button(Frame3, text="Yellow", padx=10, pady=5,
                         command=lambda: colorButton_callback("yellow"))
yellowButton.grid(row=0, column=0)

blueButton = tk.Button(Frame3, text="Blue", padx=10, pady=5,
                       command=lambda: colorButton_callback("blue"))
blueButton.grid(row=0, column=1)

pinkButton = tk.Button(Frame3, text="Pink", padx=10, pady=5,
                       command=lambda: colorButton_callback("pink"))
pinkButton.grid(row=0, column=2)

orangeButton = tk.Button(Frame3, text="Orange", padx=10, pady=5,
                         command=lambda: colorButton_callback("orange"))
orangeButton.grid(row=0, column=3)

showWindow = tk.Label(window)
showWindow.pack()

tk.mainloop()
