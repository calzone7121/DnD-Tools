import customtkinter as ctk
import random

class DiceSection(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Initialize dice_entries dictionary to store the text box references for each dice
        self._colors = {"background": "#222831", "foreground": "#31363F", "button": "#76ABAE", "text": "#EEEEEE", "transp": "transparent", "success": "#228B22", "fail": "#880808", "crit_success": "#7CFC00", "crit_fail": "#EE4B2B"}
        self._tab_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
        self._tab_names = ["Custom", "Skill", "Attack"]
        #initialize data to be stored and shared throughout the class
        self._custom_dice_entries = {}
        self._skill_roll_conditions = {"DC": 1, "RollType": 0, "Bonus": 0, "Penalty": 0}
        self._skill_dice_entries = {}
        self._skill_dice_roll_details_text = ""
        #draw/create tabs in the UI
        self._configure_section()
        self._configure_tabview()
        self._configure_customdice_tab()
        self._configure_skill_tab()
#======================================================================================================================================================================================================================
    '''
        Method for setting up the size/structure of the entire section that this class controls
    '''
    def _configure_section(self):
        self.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color=self._colors["background"])
#======================================================================================================================================================================================================================
    '''
        Setup the section to be a tabview containing as many tabs as there are names in the tab_names parameter in the class initialization
    '''
    def _configure_tabview(self):
        #configure tab parameters
        self._section_tabs = ctk.CTkTabview(self, 
                            corner_radius=10, 
                            fg_color=self._colors["background"], 
                            segmented_button_fg_color=self._colors["background"],
                            segmented_button_selected_color=self._colors["button"],
                            text_color=self._colors["text"],
                            anchor='w')
        self._section_tabs._segmented_button.configure(font=self._tab_font)
        self._section_tabs.pack(side="left", fill="both", expand=True)
        #loop through tab names and create each tab
        for i in self._tab_names:
            self._section_tabs.add(i)
            self._section_tabs.tab(i).grid_rowconfigure(0, weight=1)
            self._section_tabs.tab(i).grid_columnconfigure(0, weight=1)
#========================================================================================================================================================================================================================
    '''
        Method to configure the customdice tab (first tab in the tabview)
        method sets grid structure then loops through to create each dice frame
    '''
    def _configure_customdice_tab(self):
        #set size of the content frame within the tab and set up grid structure for internal elements
        self._customdice_content = ctk.CTkFrame(self._section_tabs.tab(self._tab_names[0]), fg_color=self._colors["background"])
        self._customdice_content.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._customdice_content.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self._customdice_content.grid_columnconfigure((0, 1), weight=1)
        #set button font parameter here
        button_font = ("Arial", 20, "bold")
        # loop to create dice frame from another method and assign their grid position
        dice_types = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20']
        for index, dice in enumerate(dice_types):
            row = index // 2
            column = index % 2
            dice_frame = self._create_customdice_frame(dice)
            dice_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        # Create roll and clear button with necessary parameters
        roll_button = ctk.CTkButton(self._customdice_content, text="Roll Dice", font=button_font, fg_color=self._colors["button"], text_color=self._colors["text"], command=self._roll_custom_dice)
        roll_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        clear_button = ctk.CTkButton(self._customdice_content, text = "Clear", font=button_font, fg_color=self._colors["button"], text_color=self._colors["text"], command=self._clear_custom_roll)
        clear_button.grid(row=4, column=0, columnspan=2, padx=10, sticky="nsew")
#=======================================================================================================================================================================================================================
    '''
        Method to create dice frame containing all components necessary before being returned into the customdice content frame
    '''
    def _create_customdice_frame(self, dice):
        #create frame for the dice components
        dice_frame = ctk.CTkFrame(self._customdice_content, fg_color=self._colors["foreground"], corner_radius=10)
        dice_frame.grid_columnconfigure(0, weight=1)
        dice_frame.grid_rowconfigure(2, weight=1)
        # create dice label
        label = ctk.CTkLabel(dice_frame, text=dice, text_color=self._colors["text"], font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, pady=5)
        # create dice Entry box
        vcmd = self.register(self._entry_input_validation)
        dice_entry = ctk.CTkEntry(dice_frame, width=80, height=40, font=("Arial", 20))
        dice_entry.grid(row=1, column=0, pady=5)
        dice_entry.insert(0, "0")
        dice_entry.configure(validate='all', validatecommand=(vcmd, '%P'))
        self._custom_dice_entries[dice] = dice_entry
        # create Increment and decrement buttons
        button_frame = ctk.CTkFrame(dice_frame, fg_color=self._colors["transp"])
        button_frame.grid(row=2, column=0, pady=5)
        value_button = ctk.CTkSegmentedButton(button_frame, width=80, height=40, values=["-", "+"], font=("Arial", 18, "bold"), fg_color=self._colors["button"], unselected_color=self._colors["button"])
        value_button.grid(row=0, column=0, columnspan=2)
        value_button.configure(command=lambda selected, e=dice_entry, v=value_button: self._adjust_entry_values(selected, e, v))
        return dice_frame
#=======================================================================================================================================
    '''
        Method to configure the tab for performing a skill checks
    '''
    def _configure_skill_tab(self):
        #set size of the content frame within the tab and set up grid structure for internal elements
        self._skilltab_content = ctk.CTkFrame(self._section_tabs.tab(self._tab_names[1]), fg_color=self._colors["background"])
        self._skilltab_content.grid(row=0, column=0, sticky="nsew")
        self._skilltab_content.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="equal")
        self._skilltab_content.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        #call methods to configure each frame since they all behave differently
        self._create_skill_dcslider()
        self._create_skill_rolltype_frame()
        self._create_skill_modifier_frame()
        self._create_skill_bonusdice_frame()
        self._create_skill_results_frame()
#=====================================================================================================================================
    '''
        Method to create slider utility for adjusting the skill check difficulty
    '''
    def _create_skill_dcslider(self):
        #create frame
        dc_slider_frame = ctk.CTkFrame(self._skilltab_content, fg_color=self._colors["foreground"], corner_radius=10)
        dc_slider_frame.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")
        dc_slider_frame.grid_rowconfigure((0, 1), weight=1)
        dc_slider_frame.grid_columnconfigure((0, 1, 2), weight=1)
        # create font variable
        slider_font=("Arial", 20, "bold")
        #Create label
        dc_label = ctk.CTkLabel(dc_slider_frame, text="DC (Difficulty)", text_color=self._colors["text"], font=slider_font, corner_radius=10)
        dc_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #create slider
        dc_slide = ctk.CTkSlider(dc_slider_frame, from_=1, to=30, fg_color=self._colors["button"])
        dc_slide.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        dc_slide.set(1)
        #create entry
        slide_entry = ctk.CTkEntry(dc_slider_frame, width=30, height=20, font=slider_font)
        slide_entry.grid(row=1, column=2, padx=5, sticky="nsew")
        slide_entry.insert(0, "1")
        dc_slide.configure(command=lambda value, e=slide_entry : self._dc_sliding(value, e))
        return dc_slider_frame
#=================================================================================================================================
    '''
        Method to create a radio button for selecting the roll type (normal, advantage, disadvantage)
    '''
    def _create_skill_rolltype_frame(self):
        #create frame
        rolltype_frame = ctk.CTkFrame(self._skilltab_content, fg_color=self._colors["foreground"])
        rolltype_frame.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")
        rolltype_frame.grid_rowconfigure((0, 1), weight=1)
        rolltype_frame.grid_columnconfigure((0, 1, 2), weight=1)
        #create font variable
        rolltype_font = ("Arial", 17, "bold")
        #create label
        rolltype_label = ctk.CTkLabel(rolltype_frame, text="Roll Type", font=("Arial", 20, "bold"))
        rolltype_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self._skill_roll_conditions["RollType"] = ctk.IntVar(value=0)
        #create and configure radio button
        normal_rad = ctk.CTkRadioButton(rolltype_frame, text="Normal", font=rolltype_font, value=0, variable=self._skill_roll_conditions["RollType"])
        normal_rad.grid(row=1, column=0, sticky="nsew")
        adv_rad = ctk.CTkRadioButton(rolltype_frame, text="Adv", font=rolltype_font, value=1, variable=self._skill_roll_conditions["RollType"])
        adv_rad.grid(row=1, column=1, sticky="nsew")
        dis_rad = ctk.CTkRadioButton(rolltype_frame, text="Disadv", font=rolltype_font, value=2, variable=self._skill_roll_conditions["RollType"])
        dis_rad.grid(row=1, column=2, sticky="nsew")
        return rolltype_frame
#=================================================================================================================================
    '''
        Method for creating the bonus and penalty trackers
    '''
    def _create_skill_modifier_frame(self):
        #create frame
        modifier_frame = ctk.CTkFrame(self._skilltab_content, fg_color=self._colors["foreground"])
        modifier_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        modifier_frame.grid_rowconfigure((0, 1), weight=1)
        modifier_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        #create font variable
        modifier_font = ("Arial", 20, "bold")
        #create labels
        bonus_label = ctk.CTkLabel(modifier_frame, text="Bonus", font=modifier_font)
        bonus_label.grid(row=0, column=0, sticky="nsew")
        penalty_label = ctk.CTkLabel(modifier_frame, text="Penalty", font=modifier_font)
        penalty_label.grid(row=0, column=2, sticky="nsew")
        #Create entries
        vcmd = self.register(self._entry_input_validation)
        bonus_entry = ctk.CTkEntry(modifier_frame, width=40, height=10, font=modifier_font)
        bonus_entry.grid(row=0, column=1, padx=(0, 5), pady=10, sticky="ns")
        bonus_entry.insert(0, "0")
        bonus_entry.configure(validate='all', validatecommand=(vcmd, '%P'))
        penalty_entry = ctk.CTkEntry(modifier_frame, width=40, height=10, font=modifier_font)
        penalty_entry.grid(row=0, column=3, padx=(0, 5), pady=10, sticky="ns")
        penalty_entry.insert(0, "0")
        penalty_entry.configure(validate='all', validatecommand=(vcmd, '%P'))
        self._skill_roll_conditions["Bonus"] = bonus_entry
        self._skill_roll_conditions["Penalty"] = penalty_entry
        #Create buttons
        bonus_button = ctk.CTkSegmentedButton(modifier_frame, width=20, height=15, values=["-", "+"], font=("Arial", 17, "bold"), fg_color=self._colors["button"], unselected_color=self._colors["button"])
        penalty_button = ctk.CTkSegmentedButton(modifier_frame, width=20, height=15, values=["-", "+"], font=("Arial", 17, "bold"), fg_color=self._colors["button"], unselected_color=self._colors["button"])
        bonus_button.grid(row=1, column=0, columnspan=2, padx=5,pady=(0, 5), sticky="nsew")
        penalty_button.grid(row=1, column=2, columnspan=2, padx=5,pady=(0, 5), sticky="nsew")
        bonus_button.configure(command=lambda selected, be=bonus_entry, bb=bonus_button: self._adjust_entry_values(selected, be, bb))
        penalty_button.configure(command=lambda selected, pe=penalty_entry, pb=penalty_button: self._adjust_entry_values(selected, pe, pb))
        return modifier_frame
#==============================================================================================================================
    '''
        Method for created dice frames to additional skill roll die
    '''
    def _create_skill_bonusdice_frame(self):
        #create dice frame to house all 6 die types
        bonus_die_frame = ctk.CTkFrame(self._skilltab_content, fg_color=self._colors["foreground"])
        bonus_die_frame.grid(row=3, rowspan=2, column=0, columnspan=3, pady=10, sticky="nsew")
        bonus_die_frame.grid_rowconfigure((0, 1), weight=1)
        bonus_die_frame.grid_columnconfigure((0, 1, 2), weight=1)
        #loop through and create each individual dice frame
        __dice_types=["d4", "d6", "d8", "d10", "d12", "d20"]
        for index, dice in enumerate(__dice_types):
            column = index // 2
            row = index % 2
            dice_frame = self._create_skilldice_frame(bonus_die_frame, dice)
            dice_frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
#================================================================================================================================
    '''
        Method to create dice frame for each skill dice
    '''
    def _create_skilldice_frame(self, bonus_die_frame, dice):
        #create dice frame with grid structure
        dice_frame = ctk.CTkFrame(bonus_die_frame, fg_color=self._colors["foreground"])
        dice_frame.grid_rowconfigure((0, 1), weight=1)
        dice_frame.grid_columnconfigure((0, 1), weight=1)
        #create font variable
        dice_font = ("Arial", 20, "bold")
        #create dice label
        dice_label = ctk.CTkLabel(dice_frame, text=dice, text_color=self._colors["text"], font=dice_font)
        dice_label.grid(row=0, column=0, sticky="nsew")
        #create dice entries
        vcmd = self.register(self._entry_input_validation)
        dice_entry = ctk.CTkEntry(dice_frame, width=10, height=10, font=dice_font)
        dice_entry.grid(row=0, column=1, sticky="nsew")
        dice_entry.insert(0, "0")
        dice_entry.configure(validate='all', validatecommand=(vcmd, '%P'))
        self._skill_dice_entries[dice] = dice_entry
        #create dice buttons
        dice_button = ctk.CTkSegmentedButton(dice_frame, values=["-", "+"], fg_color=self._colors["button"], unselected_color=self._colors["button"], text_color=self._colors["text"], font=dice_font)
        dice_button.grid(row=1, column=0, columnspan=2, sticky="nsew")
        dice_button.configure(command=lambda selected, e=dice_entry, db=dice_button: self._adjust_entry_values(selected, e, db))
        return dice_frame
#====================================================================================================================================
    '''
        Method to create result frame that houses buttons and result status message of the skill roll
    '''
    def _create_skill_results_frame(self):
        #create result frame to house subsequent frames and define grid structure
        results_frame = ctk.CTkFrame(self._skilltab_content, corner_radius=20, fg_color=self._colors["foreground"])
        results_frame.grid(row=5, rowspan=2, column=0, columnspan=3, pady=10, sticky="nsew")
        results_frame.grid_rowconfigure((0, 1), weight=1)
        results_frame.grid_columnconfigure((0, 1, 2), weight=1)
        #create font variables
        button_font = ("Arial", 18, "bold")
        label_font = ("Arial", 20)
        #create result label to display success or failure
        result_label = ctk.CTkLabel(results_frame, text="Results: ", font=label_font, corner_radius=10)
        result_label.grid(row=0, column=0, columnspan=3, sticky="nws")
        #create dice roll button
        skill_roll_button = ctk.CTkButton(results_frame, text="Roll", fg_color=self._colors["button"], font=button_font, command=self._clear_skill_roll)
        skill_roll_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        skill_roll_button.configure(command=lambda rl=result_label : self._skill_roll_results(rl))
        #create section clear button
        skill_clear_button = ctk.CTkButton(results_frame, text="Clear", fg_color=self._colors["button"], font=button_font, command= lambda rl = result_label: self._clear_skill_roll(rl))
        skill_clear_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        #create button to display roll details
        skill_detail_button = ctk.CTkButton(results_frame, text="Roll\nDetails", fg_color=self._colors["button"], font=button_font, command=self._get_skill_roll_details)
        skill_detail_button.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
#===============================================================================================================================================
    '''
        Method to roll the custom dice and display pop up window with dice result details
    '''
    def _roll_custom_dice(self):
        dice_types = {'d4': 4, 'd6': 6, 'd8': 8, 'd10': 10, 'd12': 12, 'd20': 20}
        # Create a pop-up window for results
        results_window = ctk.CTkToplevel(self)
        results_window.title("Custom Roll Results")
        results_window.geometry("300x300")
        # Create a scrollable text box for results
        results_frame = ctk.CTkTextbox(results_window, height=350, width=420)
        results_frame.pack(pady=1)
        all_rolls = {}
        total_sum = 0
        totals_by_dice = {}
        #loop to get results
        for dice, entry in self._custom_dice_entries.items():
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
        #display item in pop out window and disable text box
        for dice, rolls in all_rolls.items():
            highest_roll = max(rolls)
            lowest_roll = min(rolls)
            results_summary += f'{dice}: Highest Roll = {highest_roll}, Lowest Roll = {lowest_roll}, Total = {totals_by_dice[dice]}\n'
        results_frame.insert('1.0', f"Total sum of all dice = {total_sum}\n")
        results_frame.insert('1.0', f"Roll Summary:\n{results_summary}\n{'-'*30}\n")
        results_frame.configure(state="disabled")
#==============================================================================================================================================
    '''
        Method to clear custom roll fields
    '''
    def _clear_custom_roll(self):
        for entry in self._custom_dice_entries.values():
            entry.delete(0, ctk.END)
            entry.insert(0, "0")
#=============================================================================================================================================    
    '''
        Method to get slider variable as integer
    '''
    def _dc_sliding(self, value, entry):
        entry.delete(0, ctk.END)
        entry.insert(0, int(value))
        self._skill_roll_conditions["DC"] = int(value)
#==============================================================================================================================================
    '''
        Method to calculate the outcome of the skill roll given all values in the entered fields
    '''
    def _skill_roll_results(self, result_label):
        self._skill_dice_roll_details_text = (f"Roll Summary:\n")
        rolltype = self._skill_roll_conditions["RollType"].get()
        dc = int(self._skill_roll_conditions["DC"])
        bonus = int(self._skill_roll_conditions["Bonus"].get())
        penalty = int(self._skill_roll_conditions["Penalty"].get())
        roll_one, roll_two = random.randint(1, 20), random.randint(1, 20)
        self._skill_dice_roll_details_text += (f"DC: {dc}\nPrimary d20: {roll_one} (normal roll)\nSecondary d20: {roll_two}\nBonus: +{bonus}\nPenalty: -{penalty}\n{'-'*30}\nBonus Dice:\n\n")
        bonus_dice = self._skill_bonus_roll()
        dice_roll = 0
        print(bonus_dice)
        #check if roll is a normal roll
        if rolltype == 0:
            dice_roll = roll_one
        elif rolltype == 1:
            dice_roll = max(roll_one, roll_two)
        elif rolltype == 2:
            dice_roll = min(roll_one, roll_two)
        #check for critial success or failure
        if dice_roll == 20:
            result_label.configure(text="Critial Success!", text_color=self._colors["crit_success"])
            return
        if dice_roll == 1: 
            result_label.configure(text="Critial Failure!", text_color=self._colors["crit_fail"])
            return
        dice_total = (dice_roll + bonus + bonus_dice - penalty)
        if dice_total >= dc:
            result_label.configure(text="Success!", text_color=self._colors["success"])
            return
        else:
            result_label.configure(text="Failure!", text_color=self._colors["fail"])
            return
#============================================================================================================================================
    '''
        Method to get the results of the bonus dice rolled for a skill check
    '''
    def _skill_bonus_roll(self):
        dice_types = {'d4': 4, 'd6': 6, 'd8': 8, 'd10': 10, 'd12': 12, 'd20': 20}
        total_sum = 0
        all_rolls = {}
        totals_by_dice = {}
        roll_details_text = ""
        roll_summary_text = ""
        for dice, entry in self._skill_dice_entries.items():
            try:
                count = int(entry.get())
            except ValueError:
                count = 0
            if count > 0:
                rolls = [random.randint(1, dice_types[dice]) for _ in range(count)]
                all_rolls[dice] = rolls
                totals_by_dice[dice] = sum(rolls)
                total_sum += sum(rolls)
                roll_details_text += (f"{dice} results:\n")
                for roll in rolls:
                    roll_details_text += (f"{roll}\n")
                roll_details_text += "\n"
        roll_summary_text += (f"Sum of all dice = {total_sum}\n")
        for dice, rolls, in all_rolls.items():
            highest_roll = max(rolls)
            lowest_roll = min(rolls)
            roll_summary_text += (f"{dice}: Highest = {highest_roll}, Lowest: {lowest_roll}, Total = {totals_by_dice[dice]}\n")
        self._skill_dice_roll_details_text += (f"{roll_summary_text}\n")
        self._skill_dice_roll_details_text += roll_details_text
        return total_sum
#=============================================================================================================================================
    '''
        Method to clear fields for the skill check section
    '''
    def _clear_skill_roll(self, result_label):
        for entry in self._skill_dice_entries.values():
            entry.delete(0, ctk.END)
            entry.insert(0, "0")
        self._skill_roll_conditions["Bonus"].delete(0, ctk.END)
        self._skill_roll_conditions["Bonus"].insert(0, "0")
        self._skill_roll_conditions["Penalty"].delete(0, ctk.END)
        self._skill_roll_conditions["Penalty"].insert(0, "0")
        self._skill_dice_roll_details_text = ""
        result_label.configure(text="Results: ")
#=============================================================================================================================================
    '''
        Method to get details of the skill check roll in a pop out window
    '''
    def _get_skill_roll_details(self):
        if self._skill_dice_roll_details_text == "":
            return
        results_window = ctk.CTkToplevel(self)
        results_window.title("Skill Roll Details")
        results_window.geometry("300x300")
        results_frame = ctk.CTkTextbox(results_window, height=350, width=420)
        results_frame.pack(pady=1)
        results_frame.insert('1.0', f"{self._skill_dice_roll_details_text}")
        results_frame.configure(state="disabled")
#===============================================================================================================================
    '''
        Method that prevents anything except for an integer to be entered into the entry boxes
    '''
    def _entry_input_validation(self, value):
        if value == "" or value == "0":
            return True
        return str.isdigit(value)
#===============================================================================================================
    '''
        Method that handles increasing and decreasing entry values that use a segmented button
    '''
    def _adjust_entry_values(self, selected, entry, value_button):
        current_val = int(entry.get())
        if selected == "+":
            current_val += 1
        elif selected == "-" and current_val > 0:
            current_val -= 1
        entry.delete(0, ctk.END)
        entry.insert(0, str(current_val))
        value_button.set("")