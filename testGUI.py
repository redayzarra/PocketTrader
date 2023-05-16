import customtkinter


class ConfigGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Pocket Trader by RDZ")
        self.geometry("800x400")  # Window Size

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)  # Title row
        self.grid_rowconfigure(1, weight=9)  # Main content row
        self.grid_columnconfigure(0, weight=2)  # Explanation textbox
        self.grid_columnconfigure(1, weight=8)  # Settings frame

        # Title label
        self.title_label = customtkinter.CTkLabel(
            self,
            text="PocketTrader",
            font=customtkinter.CTkFont(size=40, weight="bold"),
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Explanation textbox
        self.explanation_textbox = customtkinter.CTkTextbox(self, width=400)
        self.explanation_textbox.grid(
            row=1, column=0, padx=(20, 10), pady=20, sticky="nsew"
        )
        self.explanation_textbox.insert("0.0", "Explanation text goes here...")

        # Settings frame
        self.settings_frame = customtkinter.CTkFrame(self, width=150)
        self.settings_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Entries for API_KEY, SECRET_KEY, maxSpentEquity
        self.api_key_entry = self.create_entry("API string:")
        self.secret_key_entry = self.create_entry("Secret API string:")
        self.max_spent_equity_entry = self.create_entry("Max Spent Equity:")

        # Entries for stopLossMargin, takeProfitMargin, maxVar
        self.stop_loss_margin_entry = self.create_entry("Stop Loss Margin :")
        self.take_profit_margin_entry = self.create_entry("Take Profit Margin:")
        self.max_var_entry = self.create_entry("Max Variation:")

    def create_entry(self, label_text):
        entry_frame = customtkinter.CTkFrame(self.settings_frame)
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.pack(fill="x", padx=(10, 20), pady=10)

        label = customtkinter.CTkLabel(entry_frame, text=label_text)
        label.grid(row=0, column=0, padx=(0, 10))

        entry = customtkinter.CTkEntry(entry_frame, width=20)  # Width for text entries
        entry.grid(row=0, column=1, sticky="ew")

        return entry


if __name__ == "__main__":
    gui = ConfigGUI()
    gui.mainloop()
