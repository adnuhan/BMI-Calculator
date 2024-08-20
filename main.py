import customtkinter as ctk
from setting import *

try:
    from ctypes import windll, byref, sizeof, c_int
except Exception as e:
    pass


class App(ctk.CTk):

    def __init__(self):
        # Window Setup
        super().__init__(fg_color=BACKGROUND_COLOR)
        self.title('')
        self.iconbitmap("icon.ico")
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')

        # Data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.description = ctk.StringVar()
        self.update_bmi()

        # Tracing
        self.height_int.trace('w', self.update_bmi)
        self.weight_float.trace('w', self.update_bmi)
        self.metric_bool.trace('w', self.change_units)

        # Widgets
        ResultText(self, self.bmi_string)
        UnitSwitcher(self, self.metric_bool)
        Category(self, self.description)
        self.weight_input = WeightInput(self, self.weight_float, self.metric_bool)
        self.height_input = HeightInput(self, self.height_int, self.metric_bool)

        self.mainloop()

    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()

    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2, 2)
        blah = ""

        if bmi_result < 18.5:
            blah = "Underweight"
        elif 18.5 <= bmi_result < 25:
            blah = "Healthy"
        elif 25 <= bmi_result < 30:
            blah = "Overweight"
        elif 30 <= bmi_result < 35:
            blah = "Moderately Obese"
        elif 35 <= bmi_result < 40:
            blah = "Severely Obese"
        elif bmi_result >= 40:
            blah = "Morbidly Obese"

        self.bmi_string.set(str(bmi_result))
        self.description.set(blah)

    def change_title_bar_color(self):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, byref(c_int(TITLE_BAR_COLOR)), sizeof(c_int))
        except:
            pass


class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        super().__init__(master=parent, textvariable=bmi_string, font=ctk.CTkFont(FONT, 150, 'bold'), text_color=WHITE)
        self.grid(column=0, row=0, rowspan=2, sticky="nsew")


class Category(ctk.CTkLabel):
    def __init__(self, parent, result):
        super().__init__(master=parent, textvariable=result, text_color=WHITE, font=ctk.CTkFont(FONT, 18, 'bold'))
        self.place(relx=0.5, rely=0.5, anchor='n')


class WeightInput(ctk.CTkFrame):
    def __init__(self, parent, weight_float, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(column=0, row=2, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float
        self.metric_bool = metric_bool

        # Layout
        self.rowconfigure(0, weight=1, uniform='b')
        self.columnconfigure(0, weight=2, uniform='b')
        self.columnconfigure(1, weight=1, uniform='b')
        self.columnconfigure(2, weight=3, uniform='b')
        self.columnconfigure(3, weight=1, uniform='b')
        self.columnconfigure(4, weight=2, uniform='b')

        # output logic
        self.output_string = ctk.StringVar()
        self.update_weight()

        # Text
        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self, textvariable=self.output_string, font=font, text_color=LIGHT_GRAY)
        label.grid(row=0, column=2)

        # Buttons
        large_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'large')), text='-',
                                           text_color=LIGHT_GRAY, font=font, fg_color=DARK_GRAY,
                                           hover_color=SHADE_OF_MEDIUM_GRAY, corner_radius=RADIUS)
        large_minus_button.grid(row=0, column=0, sticky='ns', padx=8, pady=8)

        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('minus', 'small')), text='-',
                                           text_color=LIGHT_GRAY, font=font, fg_color=DARK_GRAY,
                                           hover_color=SHADE_OF_MEDIUM_GRAY, corner_radius=RADIUS)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

        large_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'large')), text='+',
                                          text_color=LIGHT_GRAY, font=font, fg_color=DARK_GRAY,
                                          hover_color=SHADE_OF_MEDIUM_GRAY, corner_radius=RADIUS)
        large_plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('plus', 'small')), text='+',
                                          text_color=LIGHT_GRAY, font=font, fg_color=DARK_GRAY,
                                          hover_color=SHADE_OF_MEDIUM_GRAY, corner_radius=RADIUS)
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

    def update_weight(self, info=None):
        if info:
            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = 0.453592 if info[1] == 'large' else 0.453592 / 16

            if info[0] == 'plus':
                self.weight_float.set(self.weight_float.get() + amount)
            else:
                self.weight_float.set(self.weight_float.get() - amount)

        if self.metric_bool.get():
            self.output_string.set(f'{round(self.weight_float.get(), 1)}kg')
        else:
            raw_ounces = self.weight_float.get() * 2.20462 * 16
            pounds, ounces = divmod(raw_ounces, 16)
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')


class HeightInput(ctk.CTkFrame):
    def __init__(self, parent, height_int, metric_bool):
        super().__init__(master=parent, fg_color=WHITE)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.metric_bool = metric_bool

        # Widgets
        slider = ctk.CTkSlider(master=self, command=self.update_text, button_color=SHADE_OF_DARK_GRAY,
                               button_hover_color=SHADE_OF_MEDIUM_GRAY, progress_color=SHADE_OF_DARK_GRAY,
                               fg_color=LIGHT_GRAY, variable=height_int, from_=100, to=250)
        slider.pack(side='left', fill='x', expand=True, pady=10, padx=10)

        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        output_text = ctk.CTkLabel(self, textvariable=self.output_string, text_color=LIGHT_GRAY, font=font)
        output_text.pack(side='left', fill='x', expand=True, pady=10, padx=10)

    def update_text(self, amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else:
            feet, inches = divmod(amount / 2.54, 12)
            self.output_string.set(f'{int(feet)}\'{int(inches)}\"')


class UnitSwitcher(ctk.CTkLabel):
    def __init__(self, parent, metric_bool):
        super().__init__(master=parent, text='metric', text_color=SHADE_OF_DARK_GRAY, font=ctk.CTkFont(FONT, 18, 'bold'))
        self.place(relx=0.98, rely=0.01, anchor='ne')

        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text='metric')
        else:
            self.configure(text='imperial')


if __name__ == '__main__':
    App()
