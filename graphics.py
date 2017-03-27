from tkinter import *
from tkinter import filedialog


BACKGROUND_COLOR = "#a1dbcd"


class AlgorithmChooser(object):
    def __init__(self):
        self.background_color = "#a1dbcd"
        self.root = Tk()
        self.root.configure(pady=0)
        self.file_address = None
        self.file_address_str = StringVar()

        self.set_top_picture_frame()
        self.set_q_learning_frame()
        self.set_a_star_frame()
        mainloop()

    def choose_file(self):
        self.file_address = filedialog.askopenfilename(
            initialdir="./",
            title="Select file",
            filetypes=(("text files", "*.txt"), ("all files", "*.*"))
        )
        self.file_address_str.set("File Address: " + self.file_address)

    def set_top_picture_frame(self):
        top_picture_frame = Frame(self.root, height=100)
        top_picture_frame.pack(side=TOP, fill=X, expand=FALSE, pady=0)

        # path_photo = PhotoImage(file='./images/beginning.png').subsample(1, 8)
        path_photo_label = Label(
            top_picture_frame, text="Path Finding Algorithms", font=("Helvetica", 30), bg=BACKGROUND_COLOR
        )
        path_photo_label.pack(fill=X)

        choose_file_button = Button(
            top_picture_frame,
            text="Choose File",
            command=self.choose_file,
            font=("Helvetica", 14)
        )

        file_address_label = Label(top_picture_frame, textvariable=self.file_address_str, font=("Helvetica", 14))
        self.file_address_str.set("File Address: ")

        choose_file_button.pack(pady=(20, 0))
        file_address_label.pack(pady=(20, 0))

    def start_q_learning(self, event):
        print("Q learning started with parameters")

    def start_a_star(self, event):
        print("A star started with parameters")

    def set_q_learning_frame(self):
        q_learning_frame = Frame(self.root)
        q_learning_frame.pack(side=LEFT, fill=Y, expand=FALSE, padx=40, pady=(40, 100))

        q_learning_title = Label(q_learning_frame, text="Q Learning", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
        q_learning_title.pack(pady=20)

        fields = (
            'Number of Iterations',
            'Number of Episode Steps',
        )
        self.create_form(q_learning_frame, fields)
        q_learning_submit = Button(q_learning_frame, text="Start")
        q_learning_submit.bind('<Button-1>', self.start_q_learning)
        q_learning_submit.pack(pady=(40, 0))

    def set_a_star_frame(self):
        a_star_frame = Frame(self.root)
        a_star_frame.pack(side=LEFT, fill=Y, expand=TRUE, padx=40, pady=(40, 100))

        a_star_title = Label(a_star_frame, text="A*", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
        a_star_title.pack(pady=20)

        fields = (
            "Number of Iterations",
            "Number of Episode Steps"
        )

        self.create_form(a_star_frame, fields)
        a_star_submit = Button(a_star_frame, text="Start")
        a_star_submit.bind('<Button-1>', self.start_a_star)
        a_star_submit.pack(pady=(40, 0))

    def create_form(self, root, fields):
        for field in fields:
            row = Frame(root)
            label = Label(
                row,
                text=field,
                bg=BACKGROUND_COLOR,
                font=("Helvetica", 14)
            )
            entry = Entry(row)
            setattr(self, "".join([a[0] for a in field.split()]), entry)

            label.pack(side=LEFT)
            entry.pack(side=RIGHT, fill=X, expand=True)
            row.pack(pady=2)


AlgorithmChooser()
