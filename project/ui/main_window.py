import tkinter
import customtkinter
from project.ui.dice_section import DiceSection
from project.ui.encounter_section import EncounterSection
from project.ui.party_section import PartySection

background_color = "#97572b"
foreground_color = "#b99566"
        
class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._configure_mainwindow()

    def _configure_mainwindow(self):
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        self.geometry("1000x650")
        self.title("DM Tools")
        self.configure(fg_color=background_color)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        self.grid_rowconfigure(0, weight=1, uniform="equal")
        self.dice_frame = DiceSection(self)
        self.encounter_frame = EncounterSection(self)
        self.party_frame = PartySection(self)

        




    def button_callbck(self):
        print("button clicked")
