from tkinter import *
import math

"""
Shell class for Fourier GUI

"""
try:
    from tkinter import *
    # from tkinter.colorchooser import askcolor
    from tkinter.filedialog import askopenfilename
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


class MatPlotLibGUI:

    def __init__(self):

        print("  initializing the Helper class ...")
        self.root = Tk()
        self.root.title("MatPlotLib Demo GUI")

        self.grid = Frame(self.root)

        self.grid.grid_columnconfigure(4, weight=1)
        self.grid.grid_rowconfigure(2, weight=1)

        self.button = Button(self.grid, text="Plot Demo", command=self.plot_data)
        self.button.grid(row=1, column=2)

        # Create a frame for plot
        self.plot_frame = Frame(self.grid)
        self.plot_frame.grid(row=2, column=1, columnspan=4)

        self.grid.pack()
        print("  done init!")

    def plot_data(self):
        print(30*"=")

        omega = (2*math.pi)/3.0

        time = np.linspace(0., 10., 100)
        signal = np.cos(omega*time)

        try:
            fig = Figure()
            plot1 = fig.add_subplot(111)
            plot1.plot(time, signal, 'r-', label='demo signal')

            plot1.set_title(f"MatPlotLib Demo GUI Plot")
            plot1.set_xlabel("time (seconds)")
            plot1.set_ylabel("data")
            fig.legend()

            # Re-create plot_frame so we only have one plot showing at a time
            self.plot_frame = Frame(self.grid)
            self.plot_frame.grid(row=2, column=1, columnspan=4)
            canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            canvas.get_tk_widget().pack()
            canvas.draw()  # drawing the new plot in frame canvas
            self.grid.pack()

            print(" Done plotting data! ")
        except Exception as e:
            print("Failed to plot data! ", e)

    def run(self):
        print("    Entering the Tk main event loop")
        self.root.mainloop()
        print("    Leaving the Tk main event loop")


if __name__ == '__main__':

    print("Inside main...")
    gui = MatPlotLibGUI()
    gui.run()
    print("done!")
