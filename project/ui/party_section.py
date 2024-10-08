import customtkinter

class PartySection(customtkinter.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self.grid(row=0, column=2, padx=10, pady=(10, 10), sticky="nsew")
            self.label = customtkinter.CTkLabel(self, text="Party Management")
            #self.label.grid(row=0, column=0, padx=10, pady=10)
            self.label.pack(pady=10)