import customtkinter

color1 = "#97572b"
foreground_color = "#b99566"

class DiceSection(customtkinter.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self._configure_section()
            self._configure_tabs()
            self._configure_customdice_tab()
            self._configure_stopwatch_tab()
            
        def _configure_section(self):
            self.grid(row=0, column=0, padx=10, pady=(0, 0), sticky="nsew")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.configure(fg_color=color1)
            
        def _configure_tabs(self):
            _tab_font = customtkinter.CTkFont(family="Arial", size=14, weight="bold")
            self._tab_names = ["Custom", "Skill", "Attack", "Timer"]
            self._section_tabs = customtkinter.CTkTabview(self, 
                                                         corner_radius=10, 
                                                         fg_color = color1, 
                                                         segmented_button_fg_color=color1,
                                                         segmented_button_selected_color="light green",
                                                         text_color="black",
                                                         anchor='w')
            self._section_tabs._segmented_button.configure(font=_tab_font)
            self._section_tabs.pack(side="left", fill="both", expand=True)
            for i in self._tab_names:
                 self._section_tabs.add(i)
                 self._section_tabs.tab(i).grid_rowconfigure(0, weight=1)
                 self._section_tabs.tab(i).grid_columnconfigure(0, weight=1)


        def _configure_customdice_tab(self):
            self._customdice_content = customtkinter.CTkFrame(self._section_tabs.tab(self._tab_names[0]))
            self._customdice_content.configure(fg_color=foreground_color)
            self._customdice_content.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")



        def _configure_stopwatch_tab(self):
            self.diceroll_label = customtkinter.CTkLabel(self._section_tabs.tab(self._tab_names[3]), text="Stop Watch", font=("Arial", 16))
            self.diceroll_label.pack(pady=5)
            