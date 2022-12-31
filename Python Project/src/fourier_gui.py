import tkinter
import os
import csv
from given.demo_fft import *

try:
    from tkinter import *
    from tkinter.colorchooser import askcolor
    from tkinter import ttk
    from tkinter import filedialog
except ImportError:
    print("tkinter did not import successfully - check you are running Python 3 and that tkinter is available.")
    exit(1)

try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
except ImportError:
    print("matplotlib did not import successfully - check you are running Python 3 and that matplotlib is available.")
    exit(1)

import numpy as np


class FourierGUI:
    def __init__(self):

        self.root = Tk()
        self.root.geometry('700x500')
        self.root.title("Fourier GUI")

    # menu bar
        self.menu_bar = Menu(self.root, background='#ff8000', foreground='black', activebackground='white',
                             activeforeground='black')
        self.file = Menu(self.menu_bar, tearoff=1, background='#ffcc99', foreground='black')
        self.file.add_command(label="Open", command=self.open_file)
        self.file.add_command(label="Save", command=self.save_fig)
        self.file.add_command(label="Save As...", command=self.save_as)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file)
        self.root.config(menu=self.menu_bar)

    # grid
        self.grid = Frame(self.root)
        self.grid.grid_columnconfigure(5, weight=1)
        self.grid.grid_rowconfigure(15, weight=1)

    # open file button
        self.open_button = Button(self.grid, text="Browse Files", command=self.open_file)
        self.open_button.grid(row=2, column=1)
        self.file_text = Label(self.grid, text="Selected File: No File Selected")
        self.file_text.grid(row=1, column=2)

    # plot button
        self.plot_button = Button(self.grid, text="Plot Data", command=self.plot_data)
        self.plot_button.grid(row=2, column=3)

    # color picker button
        self.color_button1 = Button(self.grid, text="Pick Plot Colors", command=self.pick_color)
        self.color_button1.grid(row=2, column=2)
        self.color1 = None
        self.color2 = None

    # choosing number of terms for fourier transform
        self.box_text = Label(self.grid, text="Num Terms")
        self.box_text.grid(row=3, column=1)
        self.M = tkinter.StringVar(value=6)
        self.spin_box = ttk.Spinbox(self.grid, from_=1, to=64, textvariable=self.M, wrap=True, width=5)
        self.spin_box.grid(row=3, column=2, padx=20, pady=20)

    # initialize frame
        self.plot_frame = Frame(self.grid)
        self.plot_frame.grid(row=5, column=1, columnspan=4)

    # initislize terms list
        self.terms = Label(self.grid)
        self.terms.grid(row=5, column=5)

        self.grid.pack()

    @staticmethod
    def read_csv(file_path):
        """
        reads signal data from csv file
        """
        seconds, nanoseconds, signal = [], [], []
        with open(file_path, "rt") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                seconds.append(int(row[0]))
                nanoseconds.append(int(row[1]))
                signal.append(float(row[2]))
        return np.array(seconds) - seconds[0] + 1.0e-9 * np.array(nanoseconds), np.array(signal)

    def pick_color(self):
        """
        Command when color button is pressed. Selects plot color.
        """
        self.color1 = askcolor(title='Noisy Signal Color')
        self.color2 = askcolor(title='Fourier Plot Color')

    def open_file(self):
        """
        command when browse file or open button is pressed. opens a file.
        """
        try:
            self.file_path = filedialog.askopenfilename()
            self.file_name = str(self.file_path)[-18:]
            if self.file_name[-3:] != "dat" and self.file_name[-3:] != "csv":
                self.file_text = Label(self.grid, text=f"Selected File: {self.file_name} (Invalid File!)")
                self.file_text.grid(row=1, column=2)
                self.grid.pack()
                raise TypeError("Invalid file!")
            self.save_path = os.path.join("figures", f"{self.file_name[:-4]}.png")
            self.file_text = Label(self.grid, text=f"Selected File: {self.file_name}")
            self.file_text.grid(row=1, column=2)
            self.grid.pack()
        except TypeError as e:
            print(str(e))

    def plot_data(self):
        """
        reads file and plots data
        """
        print(30 * "=")

        try:

            fig = Figure()
            plot1 = fig.add_subplot(111)
            if self.file_path[-3:] == "dat":
                time, signal = read_binary(self.file_path)
            elif self.file_path[-3:] == "csv":
                time, signal = self.read_csv(self.file_path)
            else:
                raise TypeError("Invalid file!")
            fft = FFT(time, signal)
            fourier_series_components = fft.get_fourier_components(int(self.M.get()))
            if self.color1:
                plot1.plot(time, signal, str(self.color1[1]), label="signal", linewidth=2)
            else:
                plot1.plot(time, signal, label="signal", linewidth=2)

            fourier_series = np.zeros(fft._time.shape)
            dt = time[1] - time[0]

            for components in fourier_series_components:
                mag, freq, phase = components
                fourier_series += mag * np.cos((freq / dt) * fft._time + phase)
            if self.color2:
                plot1.plot(time, fourier_series, str(self.color2[1]), label="Fourier Series")
            else:
                plot1.plot(time, fourier_series, label="Fourier Series")

            plot1.set_title(str(self.file_path)[-18:])
            plot1.set_xlabel("time (seconds)")
            plot1.set_ylabel("signal")
            fig.legend()

        # Re-create plot_frame so we only have one plot showing at a time
            self.plot_frame = Frame(self.grid)
            self.plot_frame.grid(row=5, column=1, columnspan=4)
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.get_tk_widget().pack()
            canvas.draw()

        # display fourier terms
            self.terms.destroy()

            row = 6
            label_string = 'First 5 Fourier Terms Plotted:\n'
            for components in fourier_series_components:
                if row - 6 < 5:
                    mag, freq, _ = components
                    label_string += f"Mag = {mag:.3f}  Freq = {freq:.3f}\n"
                    row += 1
            self.terms = Label(self.grid, text=label_string)
            self.terms.grid(row=5, column=5)
            self.grid.pack()
            print(" Done plotting data! ")
        except Exception as e:
            print("Failed to plot data! ", e)

    def save_fig(self):
        """
        command when save button is pressed. run at the end of save as
        """
        try:
            fig = Figure()
            plot1 = fig.add_subplot(111)
            if self.file_path[-3:] == "dat":
                time, signal = read_binary(self.file_path)
            elif self.file_path[-3:] == "csv":
                time, signal = self.read_csv(self.file_path)
            else:
                raise TypeError("Invalid file!")
            fft = FFT(time, signal)
            fourier_series_components = fft.get_fourier_components(int(self.M.get()))
            if self.color1:
                plot1.plot(time, signal, str(self.color1[1]), label="signal", linewidth=2)
            else:
                plot1.plot(time, signal, label="signal", linewidth=2)

            fourier_series = np.zeros(fft._time.shape)
            dt = time[1] - time[0]

            for components in fourier_series_components:
                mag, freq, phase = components
                fourier_series += mag * np.cos((freq / dt) * fft._time + phase)
            if self.color2:
                plot1.plot(time, fourier_series, str(self.color2[1]), label="Fourier Series")
            else:
                plot1.plot(time, fourier_series, label="Fourier Series")

            plot1.set_title(str(self.file_path)[-18:])
            plot1.set_xlabel("time (seconds)")
            plot1.set_ylabel("signal")
            fig.legend()
            fig.savefig(self.save_path)
        except Exception as e:
            print("Failed to plot data! ", e)

    def save_as(self):
        """
        command when save as button is pressed. stores save path
        """
        try:
            self.save_path = filedialog.asksaveasfile(initialfile=f"{self.file_name[:-4]}.png")
            self.save_fig()
        except Exception as e:
            print("Failed to save file!", e)

    def run(self):
        print("    Entering the Tk main event loop")
        self.root.mainloop()

        print("    Leaving the Tk main event loop")


if __name__ == '__main__':

    print("Inside main...")
    gui = FourierGUI()
    gui.run()
    print("done!")
