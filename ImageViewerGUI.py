#Name :HUNNY CHANDRA
#ROLL NO: 21CS30024
from my_package.model import ImageCaptioningModel
from my_package.model import ImageClassificationModel
from tkinter import *
from functools import partial
from PIL import ImageTk, Image
from tkinter import font
from tkinter import filedialog


def fileClick(clicked):
    def choose_file():
        global file_path
        file_path = filedialog.askopenfilename()
        if file_path:

            image = Image.open(file_path)
            s = file_path
            l = list(s.split("/")).pop()

            # Resize the image to fit the input size of the models
            image = image.resize((400, 550))
            photo = ImageTk.PhotoImage(image)
            input_image_label.configure(image=photo)
            label.configure(text=l)
            frame.pack(side=LEFT, fill=X, expand=True)
            # Keep a reference to the photo to avoid garbage collection
            input_image_label.image = photo
    return choose_file


def process(clicked, captioner, classifier, input_image_label, output_label, option_var):

    if input_image_label.image != NONE:
        # Convert the PhotoImage to PIL image
        pil_image = ImageTk.getimage(input_image_label.image)

        # Resize the image to fit the input size of the models
        pil_image = pil_image.resize((500, 500))

        # Caption the image using the captioner model
        caption = captioner.__call__(file_path)

        # Classify the image using the classifier model
        classification = classifier.__call__(file_path)

        option_value = option_var.get()
        if option_value == "IMAGE CAPTIONING":

            # Show the caption if option value is 0
            output_label.delete(0, END)

            output_label.insert(END, "TOP THREE CAPTIONS")
            for x in caption:

                output_label.insert(END, x)
                # output_label.configure(text=f"Caption: {x}\n")
        else:

            # Show the classification if option value is 1
            output_label.delete(0, END)
            output_label.insert(END, "ALL classification")
            for x in classification:

                output_label.insert(END, x)

        # Update the output label with the caption and classification

        # If no input image is selected, show an error message in the output label
    else:
        output_label.insert(END, "Please first select image")
        print("SELECT IMAGE")


if __name__ == '__main__':
    # Instantiate the root window
    root = Tk()
    # root.geometry("400x400")
    # Provide a title to the root window
    root.title("Image Captioning and Classification")

    # Instantiate the captioner and classifier models
    captioner = ImageCaptioningModel()
    classifier = ImageClassificationModel()

    # Declare the input image label
    frame2 = Frame(root, borderwidth=6, bg="black",
                   relief=SUNKEN)  # declaring frame
    frame2.pack(side=BOTTOM, fill=BOTH, expand=True, anchor="s")
    # declare input_image_label
    input_image_label = Label(frame2)
    input_image_label.image = NONE
    input_image_label.pack(side=LEFT)
    # Declare the file browsing button
    frame = Frame(root, borderwidth=6, bg="black", relief=SUNKEN)
    frame.pack(side=TOP, fill=X, expand=True, anchor="n")
    # frame 2

    l = "NO FILE SELECTED"
    label = Label(frame, text=l)
    label.pack(side=LEFT, anchor="nw", fill=X, expand=True)
    label.configure(text=l)

    label.pack(fill=X, expand=True, padx=20, pady=5, side=LEFT, anchor=N)
    # Button for choosing image
    file_button = Button(frame, padx=30, pady=5, highlightbackground="white", bg="black",
                         fg="white", text="OPEN", font="bold", command=fileClick(clicked="file_button"))

    file_button.pack(side=RIGHT, anchor=N)
    my_font = font.Font(family="Helvetica", size=12, weight="bold")
    # Declare the output label
    output_label = Label(frame2)
    output_label = Listbox(frame2, width=75, height=8, font=my_font)
    output_label.pack()
    output_label.pack()

    option_var = StringVar()
    option_var.set("IMAGE CAPTIONING")
    option_menu = OptionMenu(
        frame, option_var, "IMAGE CAPTIONING", "IMAGE CLASSIFICATION")
    option_menu.configure(background="black", highlightbackground="black",
                          foreground="white", padx="30", pady="5", font="bold")
    option_menu.pack(side=RIGHT, anchor=N)

    # Declare the process button

    process_button = Button(frame, highlightbackground="white", padx=30, pady=5, bg="black", fg="white", text="PROCESS", font="bold", command=partial(
        process, clicked="process_button", captioner=captioner, classifier=classifier, input_image_label=input_image_label, output_label=output_label, option_var=option_var))
    process_button.pack(side=RIGHT, anchor="n")

    # Start the main event loop
    root.mainloop()
