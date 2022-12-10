import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

class CltzConj:
    def __init__(self, root):
        self.root = root
        self.root.state("zoomed")
        self.root.title("Collatz Conjucture Graphing")
        self.root.configure(bg="#25282e")
        self.font_tuple = ("consolas", 12, "bold")
        self.root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

        self.CreateFrames()

    def CreateFrames(self):
        self.canvas = tk.Canvas(self.root)
        self.canvas.configure(bg="#25282e")
        self.scrollbarY = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.main_frame = tk.Frame(self.canvas)
        self.main_frame.configure(bg="#25282e")

        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbarY.set, bg="#25282e")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbarY.pack(side="right", fill="y")

        self.MaxNumUsrInpt()

    def MaxNumUsrInpt(self):
        self.frame1 = tk.Frame(self.main_frame)
        self.frame1.configure(bg="#25282e")
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        max_num_input_label = tk.Label(self.frame1, text="Enter Maximum number of numbers to be compared: ", bg="#007abd", fg="white", font=self.font_tuple)
        max_num_input_label.grid(row=1, column=0, padx=(5, 5), pady=(10, 5), sticky="ew")
        self.max_num_input_entry = tk.Entry(self.frame1, font=self.font_tuple, fg="black")
        self.max_num_input_entry.grid(row=1, column=1, padx=(5, 5), pady=(10, 5), sticky="ew")
        self.max_num_input_button = tk.Button(self.frame1, text="Enter", command=self.GetMaxNumInput, bg="#007abd", fg="white", font=self.font_tuple)
        self.max_num_input_button.grid(row=1, column=2, pady=5, padx=(5, 5), sticky="ew")
        self.frame1.bind("<Return>", self.GetMaxNumInput)

    def GetMaxNumInput(self):
        self.max_num_input = int(self.max_num_input_entry.get())
        self.max_num_input_button["state"] = "disabled"
        self.max_num_input_entry["state"] = "disabled"
        self.NumUsrInpt()

    def NumUsrInpt(self):
        self._entries = []
        self.temp_row = 1
        for i in range(1, self.max_num_input+1):
            tk.Label(self.frame1, text="Enter number: ", bg="#1cd464", fg="white", font=self.font_tuple).grid(row=i+1, column=0, pady=5, padx=(5, 5), sticky="ew")
            buffer = tk.Entry(self.frame1, font=self.font_tuple, fg="black")
            buffer.grid(row=i+1, column=1, pady=5, padx=(5, 5), sticky="ew")
            self._entries.append(buffer)
            self.temp_row += i
        self.usr_inpt_button = tk.Button(self.frame1, text="Enter", command=self.UpdateVal, bg="#007abd", fg="white", font=self.font_tuple)
        self.usr_inpt_button.grid(row=self.temp_row, column=1, pady=5, padx=(5, 5), sticky="ew")
        self.frame1.bind("<Return>", self.UpdateVal)

    def UpdateVal(self):
        self.val = []
        self.usr_inpt_button["state"] = "disabled"
        for i in range(len(self._entries)):
            buffer = int(self._entries[i].get())
            self.val.append(buffer)
        for i in range(len(self._entries)):
            self._entries[i]["state"] = "disabled"

        tk.Button(self.frame1, text="Calculate & Plot", command=self.CzcjCompute, bg="#ff0404", fg="white", font=self.font_tuple).grid(row=self.temp_row+1, column=1, pady=5, padx=(5, 5), sticky="ew")
        self.frame1.bind("<Return>", self.CzcjCompute)

    def CzcjCompute(self):
        self.OrgX = []
        self.OrgY = []

        def CalcY(n: int):
            iniN = n
            buffer = []
            while n > 1:
                if n % 2:
                    n = 3*n + 1
                else:
                    n = n // 2
                buffer.append(n)
            buffer.insert(0, iniN)
            self.OrgY.append(buffer)

        def CalcX(arr: list):
            buffer = []
            temp = len(arr)
            for i in range(1, temp+1):
                buffer.append(i)
            self.OrgX.append(buffer)

        for i in range(len(self.val)):
            CalcY(self.val[i])
        for i in range(len(self.OrgY)):
            CalcX(self.OrgY[i])

        self.Graphing()

    def Graphing(self):
        self.frame1.destroy()

        self.frame2 = tk.Frame(self.main_frame)
        self.frame2.configure(bg="#25282e")
        self.frame2.pack(padx=(self.root.winfo_screenwidth()/4, self.root.winfo_screenwidth()/4))

        self.scrollbarY.destroy()
        self.scrollbarY = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)

        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbarY.set, bg="#25282e")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbarY.pack(side="right", fill="y")

        tk.Label(self.frame2, text="", bg="#25282e").pack()
        for p in range(len(self.val)):
            tk.Label(self.frame2, text=f"Collatz Conjesture Sequence for {self.val[p]}: \n{self.OrgY[p]}", bg="#242450", fg="white", font=self.font_tuple, wraplength=900).pack()
            tk.Label(self.frame2, text="_"*175, bg="#25282e", fg="#25282e", wraplength=900).pack()

        figure = plt.figure(figsize=(8, 7), dpi=100)
        fig_subplt = figure.add_subplot(111)

        for i in range(len(self.OrgY)):
            fig_subplt.plot(self.OrgX[i], self.OrgY[i], "o:", markersize=5, linewidth=1, label=f"{self.val[i]}")
            
        for i, j in zip(self.OrgX, self.OrgY):
            for l, m in zip(i, j):
                fig_subplt.text(l, m, f"{m}")

        fig_subplt.set_title(f"Collatz Conjecture Graph")
        fig_subplt.set_ylabel("Numbers")
        fig_subplt.legend()
        fig_subplt.grid()
        figure.tight_layout()

        canv = FigureCanvasTkAgg(figure, master=self.frame2)
        canv.draw()
        get_widz = canv.get_tk_widget()
        get_widz.pack()
        self.LoopAgain()

    def LoopAgain(self):
        tk.Label(self.frame2, text="", bg="#25282e").pack()
        tk.Button(self.frame2, text="Run Program Again", command=self.ActualLoopAgain, bg="#ff0404", fg="white", font=self.font_tuple).pack()
        self.frame2.bind("<Return>", self.ActualLoopAgain)
        tk.Label(self.frame2, text="", bg="#25282e").pack()

    def ActualLoopAgain(self):
        self.root.destroy()
        root = tk.Tk()
        gui = CltzConj(root)
        gui.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    gui = CltzConj(root)
    gui.root.mainloop()