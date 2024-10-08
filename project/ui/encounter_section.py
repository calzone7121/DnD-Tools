import customtkinter

class EncounterSection(customtkinter.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")
            self.label = customtkinter.CTkLabel(self, text="Encounter Management")
            #self.label.grid(row=0, column=0, pady=10)
            self.label.pack(pady=10)