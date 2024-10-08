#import tkinter
import customtkinter
from project.ui.dice_section import DiceSection
from project.ui.encounter_section import EncounterSection
from project.ui.party_section import PartySection
_colors = {"background": "#222831", "foreground": "#81363F", "button": "#76ABAE", "text": "#EEEEEE"}


class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_mainwindow()


    def _configure_mainwindow(self):
        customtkinter.set_appearance_mode("dark")
        #customtkinter.set_default_color_theme("green")
        self.geometry("1000x650")
        self.title("DM Tools")
        self.configure(fg_color=_colors["background"])
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        self.grid_rowconfigure(0, weight=1, uniform="equal")
        self.dice_frame = DiceSection(self)
        self.encounter_frame = EncounterSection(self)
        self.party_frame = PartySection(self)

        




    def button_callbck(self):
        print("button clicked")
