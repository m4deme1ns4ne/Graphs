import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from scipy.interpolate import make_interp_spline
from my_mistakes import Much_X, Much_Y
import numpy as np

class Speed_boogers:
    def __init__(self, root):
        self.root = root
        self.root.title("Спидозные козявки")


        self.data_x = tk.StringVar()
        self.data_y = tk.StringVar()
        self.plot_title = tk.StringVar(value="")
        self.x_axis_label = tk.StringVar(value="")
        self.y_axis_label = tk.StringVar(value="")


        self.error_message_x = tk.StringVar()
        self.error_message_x.set("")

        self.error_message_y = tk.StringVar()
        self.error_message_y.set("")


        self.smooth_enabled = tk.BooleanVar()
        self.smooth_enabled.set(False)


        self.greed_enabled = tk.BooleanVar()
        self.greed_enabled.set(False)  


        self.create_widgets()

    def create_widgets(self):

        input_frame = ttk.Frame(self.root)
        input_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)


        ttk.Label(input_frame, text="Название графика:").pack(pady=10)
        entry_title = ttk.Entry(input_frame, textvariable=self.plot_title, width=30)
        entry_title.pack(pady=10)


        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Название оси X:").pack(pady=10)
        entry_x_label = ttk.Entry(input_frame, textvariable=self.x_axis_label, width=30)
        entry_x_label.pack(pady=10)

        ttk.Label(input_frame, text="Введите значения X:").pack(pady=10)
        entry_x = ttk.Entry(input_frame, textvariable=self.data_x, width=30)
        entry_x.pack(pady=10)


        error_label_x = ttk.Label(input_frame, textvariable=self.error_message_x, foreground='red')
        error_label_x.pack(pady=10)


        ttk.Separator(input_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=10)

        ttk.Label(input_frame, text="Название оси Y:").pack(pady=10)
        entry_y_label = ttk.Entry(input_frame, textvariable=self.y_axis_label, width=30)
        entry_y_label.pack(pady=10)

        ttk.Label(input_frame, text="Введите значения Y:").pack(pady=10)
        entry_y = ttk.Entry(input_frame, textvariable=self.data_y, width=30)
        entry_y.pack(pady=10)


        error_label_y = ttk.Label(input_frame, textvariable=self.error_message_y, foreground='red')
        error_label_y.pack(pady=10)


        update_button = ttk.Button(input_frame, text="Обновить график", command=self.update_plot)
        update_button.pack(side=tk.BOTTOM)


        smooth_checkbox = ttk.Checkbutton(input_frame, text="Сглаживание", variable=self.smooth_enabled)
        smooth_checkbox.pack(side=tk.BOTTOM)


        greed_checkbox = ttk.Checkbutton(input_frame, text='Сетка', variable=self.greed_enabled)
        greed_checkbox.pack(side=tk.BOTTOM)


        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, padx=10, pady=10, expand=True, fill=tk.BOTH)


        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot_area = self.fig.add_subplot(111)


        canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def update_plot(self):
        try:

            x = list(map(float, self.data_x.get().split()))
            y = list(map(float, self.data_y.get().split()))


            self.error_message_x.set("")
            self.error_message_y.set("")

            if len(x) > len(y):
                raise Much_X
            elif len(y) > len(x):
                raise Much_Y


            self.plot_area.clear()


            try:
                if self.smooth_enabled.get():
                    x_smooth = np.linspace(min(x), max(x), 300)
                    spline = make_interp_spline(x, y, k=3)
                    y_smooth = spline(x_smooth)
                    self.plot_area.plot(x_smooth, y_smooth, label=self.plot_title.get())
                else:
                    self.plot_area.plot(x, y, label=self.plot_title.get(), marker='o')
            except ValueError:
                messagebox.showerror('Ошибка', 'Данный график нельзя сгладить')
            

            if self.greed_enabled.get():
                self.plot_area.grid(True)
            else:
                self.plot_area.grid(False)


            self.plot_area.set_title(self.plot_title.get())
            self.plot_area.set_xlabel(self.x_axis_label.get())
            self.plot_area.set_ylabel(self.y_axis_label.get())


            self.plot_area.legend()


            self.fig.canvas.draw()

        except Much_X:
            self.error_message_x.set(f"Количество значений по X больше на {len(x) - len(y)}")
        except Much_Y:
            self.error_message_y.set(f"Количество значений по Y больше на {len(y) - len(x)}")
        except ValueError:
            messagebox.showerror('Ошибка', '"Пожалуйста, введите корректные числовые значения')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'1336x768')
    app = Speed_boogers(root)
    root.mainloop()
