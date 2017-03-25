from tkinter import *


BACKGROUND_COLOR = "#a1dbcd"
root = Tk()
# root.geometry('640x480')

root.configure(pady=0)

top_picture_frame = Frame(root, height=100)
top_picture_frame.pack(side=TOP, fill=X, expand=FALSE, pady=0)

# path_photo = PhotoImage(file='./images/beginning.png').subsample(1, 8)
path_photo_label = Label(top_picture_frame, text="Path Finding Algorithms", font=("Helvetica", 30), bg=BACKGROUND_COLOR)
path_photo_label.pack(fill=X)

choose_file_button = Button(top_picture_frame, text="Choose File", font=("Helvetica", 14))
choose_file_button.pack(pady=(20, 0))

file_address_label = Label(top_picture_frame, text="File Address Will Be Shown Here", font=("Helvetica", 14))
file_address_label.pack(pady=(20, 0))

q_learning_frame = Frame(root)
q_learning_frame.pack(side=LEFT, fill=Y, expand=FALSE, padx=40, pady=(40, 100))

a_star_frame = Frame(root)
a_star_frame.pack(side=LEFT, fill=Y, expand=TRUE, padx=40, pady=(40, 100))

q_learning_title = Label(q_learning_frame, text="Q Learning", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
q_learning_title.pack(pady=20)

a_star_title = Label(a_star_frame, text="A*", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
a_star_title.pack(pady=20)

mainloop()
