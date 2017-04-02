from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import ttk

from a_star_simulator import AStarSimulator
from q_learning_simulator import QLearningSimulator
from q_learning import QLearning


BACKGROUND_COLOR = "#a1dbcd"


class AlgorithmChooser(object):
    def __init__(self):
        self.q_learning_simulator = None
        self.a_star_simulator = None
        self.background_color = "#a1dbcd"
        self.root = Tk()
        self.root.configure(pady=0)
        self.root.title("Path Finding Algorithm")
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
        if self.file_address:
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
        if not self.q_learning_simulator:
            discount_factor = self.DF.get()
            learning_rate = self.LR.get()
            number_of_episode_steps = self.NoES.get()
            number_of_iterations = self.NoI.get()
            policy = self.P.get()
            environment = self.E.get()
            show_q_table = self.QT.get()
            file_address = self.file_address

            okay = True

            if not file_address:
                messagebox.showerror("Error", "Please enter a valid file address")
                okay = False
            else:
                if not discount_factor:
                    messagebox.showerror("Error", "Please enter a valid discount factor")
                    okay = False
                if not learning_rate:
                    messagebox.showerror("Error", "Please enter a valid learning rate")
                    okay = False
                if not number_of_episode_steps:
                    messagebox.showerror("Error", "Please enter a valid number for episode steps")
                    okay = False
                if not number_of_iterations:
                    messagebox.showerror("Error", "Please enter a valid number for iterations")
                    okay = False
                if not policy:
                    messagebox.showerror("Error", "Please enter a valid option for policy")
                    okay = False
                if not environment:
                    messagebox.showerror("Error", "Please enter a valid option for environment")
                    okay = False

                if not show_q_table:
                    messagebox.showerror("Error", "Please enter a valid option for Q Table")
                    okay = False

            if okay:
                is_stochastic = environment == "Stochastic"
                q_learning = QLearning(file_address, is_stochastic=is_stochastic)
                policy_table = {
                    'Random': 'random',
                    'Greedy': 'greedy',
                    'Epsilon': 'epsilon-policy',
                }
                policy = policy_table[policy]
                self.q_learning_simulator = QLearningSimulator(
                    q_learning,
                    delay_time=100,
                    root_frame=self,
                    action_policy=policy
                )
                self.q_learning_simulator.start_simulation(start_position=(9, 0))

    def start_a_star(self, event):
        if not self.a_star_simulator:
            self.a_star_simulator = AStarSimulator(start_frame=self)
            self.a_star_simulator.start_simulation()

    def set_q_learning_frame(self):
        q_learning_frame = Frame(self.root)
        q_learning_frame.pack(side=LEFT, fill=Y, expand=FALSE, padx=40, pady=(40, 100))

        q_learning_title = Label(q_learning_frame, text="Q Learning", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
        q_learning_title.pack(pady=20)

        fields = {
            'Number of Iterations': 'input',
            'Number of Episode Steps': 'input',
            'Learning Rate': 'input',
            'Discount Factor': 'input',
        }

        combo_box_fields = {
            'Policy': ['Random', 'Greedy', 'Epsilon'],
            'Environment': ['Static', 'Stochastic'],
            'Q Table': ['Show', 'Not Show']
        }

        self.create_form(q_learning_frame, fields)
        self.create_form(q_learning_frame, combo_box_fields)

        q_learning_submit = Button(q_learning_frame, text="Start")
        q_learning_submit.bind('<Button-1>', self.start_q_learning)
        q_learning_submit.pack(pady=(40, 0))

    def set_a_star_frame(self):
        a_star_frame = Frame(self.root)
        a_star_frame.pack(side=LEFT, fill=Y, expand=TRUE, padx=40, pady=(40, 100))

        a_star_title = Label(a_star_frame, text="A*", bg=BACKGROUND_COLOR, font=("Helvetica", 20))
        a_star_title.pack(pady=20)

        a_star_submit = Button(a_star_frame, text="Start")
        a_star_submit.bind('<Button-1>', self.start_a_star)
        a_star_submit.pack(pady=(40, 0))

    def create_form(self, root, fields):
        for field in sorted(fields):
            row = Frame(root)
            label = Label(
                row,
                text=field,
                bg=BACKGROUND_COLOR,
                font=("Helvetica", 14)
            )
            if fields[field] == 'input':
                entry = Entry(row)
                default_value = 0.9 if field == 'Learning Rate' or field == 'Discount Factor' else 100
                entry.insert(END, default_value)
            else:
                entry = ttk.Combobox(row)
                entry['values'] = fields[field]
                entry.current(0)

            setattr(self, "".join([a[0] for a in field.split()]), entry)
            label.pack(side=LEFT)
            entry.pack(side=RIGHT, fill=X, expand=True)
            row.pack(pady=2)


AlgorithmChooser()
