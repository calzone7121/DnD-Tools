import customtkinter as ctk
import random

color1 = "#97572b"
foreground_color = "#b99566"

class DiceSection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Initialize dice_entries dictionary to store the text box references for each dice
        self._dice_entries = {}
        self._colors = {"background": "#222831", "foreground": "#31363F", "button": "#76ABAE", "text": "#EEEEEE", "transp": "transparent"}
        self._tab_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self._tab_names = ["Custom", "Skill", "Attack", "Timer"]
        self._configure_section()
        self._configure_tabview()
        self._configure_customdice_tab()
#===========================================================================================================
    def _configure_section(self):
        self.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color=self._colors["background"])
#===========================================================================================================
    def _configure_tabview(self):
        self._section_tabs = ctk.CTkTabview(self, 
                            corner_radius=10, 
                            fg_color=self._colors["background"], 
                            segmented_button_fg_color=self._colors["background"],
                            segmented_button_selected_color=self._colors["button"],
                            text_color=self._colors["text"],
                            anchor='w')
        self._section_tabs._segmented_button.configure(font=self._tab_font)
        self._section_tabs.pack(side="left", fill="both", expand=True)
        for i in self._tab_names:
            self._section_tabs.add(i)
            self._section_tabs.tab(i).grid_rowconfigure(0, weight=1)
            self._section_tabs.tab(i).grid_columnconfigure(0, weight=1)
#===========================================================================================================
    def _configure_customdice_tab(self):
        #set size of the content frame within the tab and set up grid structure for internal elements
        self._customdice_content = ctk.CTkFrame(self._section_tabs.tab(self._tab_names[0]))
        self._customdice_content.configure(fg_color=self._colors["background"])
        self._customdice_content.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._customdice_content.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self._customdice_content.grid_columnconfigure((0, 1), weight=1)
        # Add dice labels, entry fields, and increment/decrement buttons
        dice_types = ['D-4', 'D-6', 'D-8', 'D-10', 'D-12', 'D-20']
        for index, dice in enumerate(dice_types):
            row = index // 2
            column = index % 2
            dice_frame = self._create_dice_frame(dice)
            dice_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        # Roll dice button spanning both columns in row 4
        roll_button = ctk.CTkButton(self._customdice_content, text="Roll Dice", font=("Arial", 20, "bold"), fg_color=self._colors["button"], text_color=self._colors["text"], command=self._roll_custom_dice)
        roll_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
#===========================================================================================================
    def _create_dice_frame(self, dice):
        frame = ctk.CTkFrame(self._customdice_content, fg_color=self._colors["foreground"], corner_radius=10)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(2, weight=1)
        # Dice label
        label = ctk.CTkLabel(frame, text=dice, text_color=self._colors["text"], font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, pady=5)
        # Entry box
        entry = ctk.CTkEntry(frame, width=80, height=40, font=("Arial", 20))
        entry.grid(row=1, column=0, pady=5)
        entry.insert(0, "0")
        self._dice_entries[dice] = entry
        # Increment and decrement buttons
        button_frame = ctk.CTkFrame(frame, fg_color=self._colors["transp"])
        button_frame.grid(row=2, column=0, pady=5)
        # increment_button = ctk.CTkButton(button_frame, corner_radius=4, fg_color=self._colors["button"], text="+", width=30, command=lambda e=entry: self._adjust_dice_values(e, "+"))
        # increment_button.grid(row=0, column=0)
        # decrement_button = ctk.CTkButton(button_frame, corner_radius=4, fg_color=self._colors["button"], text="-", width=30, command=lambda e=entry: self._adjust_dice_values(e, "-""))
        # decrement_button.grid(row=0, column=1)
        value_button = ctk.CTkSegmentedButton(button_frame, width=80, height=40, values=["-", "+"], font=("Arial", 18, "bold"), fg_color=self._colors["button"], unselected_color=self._colors["button"])
        value_button.grid(row=0, column=0, columnspan=2)
        value_button.configure(command=lambda selected, e=entry, v=value_button: self._adjust_dice_values(e, selected, v))
        return frame
#===========================================================================================================
    # def _increment_dice(self, entry):
    #     current_value = int(entry.get())
    #     entry.delete(0, ctk.END)
    #     entry.insert(0, str(current_value + 1))
#===========================================================================================================
    # def _decrement_dice(self, entry):
    #     current_value = int(entry.get())
    #     entry.delete(0, ctk.END)
    #     if current_value > 0:
    #         entry.insert(0, str(current_value - 1))
#===============================================================================================================
    def _adjust_dice_values(self, entry, selected, value_button):
        current_val = int(entry.get())
        if selected == "+":
            current_val += 1
        elif selected == "-" and current_val > 0:
            current_val -= 1
        entry.delete(0, ctk.END)
        entry.insert(0, str(current_val))
        value_button.set("")
#===========================================================================================================
    def _roll_custom_dice(self):
        dice_types = {'D-4': 4, 'D-6': 6, 'D-8': 8, 'D-10': 10, 'D-12': 12, 'D-20': 20}
        # Create a pop-up window for results
        results_window = ctk.CTkToplevel(self)
        results_window.title("Dice Roll Results")
        results_window.geometry("300x300")
        # Create a scrollable text box for results
        results_frame = ctk.CTkTextbox(results_window, height=350, width=420)
        results_frame.pack(pady=1)
        all_rolls = {}
        total_sum = 0
        totals_by_dice = {}
        for dice, entry in self._dice_entries.items():
            try:
                count = int(entry.get())  # Get value from entry
            except ValueError:
                count = 0  # Default to 0 if input is invalid
            if count > 0:
                rolls = [random.randint(1, dice_types[dice]) for _ in range(count)]
                all_rolls[dice] = rolls
                total_sum += sum(rolls)
                totals_by_dice[dice] = sum(rolls)
                results_frame.insert(ctk.END, f'{dice} results:\n')
                for roll in rolls:
                    results_frame.insert(ctk.END, f'{roll}\n')
                results_frame.insert(ctk.END, '\n')
        results_summary = ""
        for dice, rolls in all_rolls.items():
            highest_roll = max(rolls)
            lowest_roll = min(rolls)
            results_summary += f'{dice}: Highest Roll = {highest_roll}, Lowest Roll = {lowest_roll}, Total = {totals_by_dice[dice]}\n'
        results_frame.insert('1.0', f"Total sum of all dice = {total_sum}\n")
        results_frame.insert('1.0', f"Roll Summary:\n{results_summary}\n{'-'*30}\n")
        results_frame.configure(state="disabled")
