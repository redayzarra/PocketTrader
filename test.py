import json
import customtkinter
import tkinter.messagebox as msgbox


class ConfigGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Pocket Trader by RDZ")
        self.geometry("800x475")  # Window Size

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
        self.explanation_textbox.insert(
            "0.0",
            "Welcome to PocketTrader!\n\n"
            "PocketTrader is a trading bot designed to automate your trading strategy. "
            "This GUI allows you to configure the bot according to your needs!\n\n"
            "API string & Secret API string: These are your unique identifiers for your Alpaca account. "
            "Please make sure to copy and paste the API strings in their correct spots. "
            "These fields are hidden for your security.\n\n"
            "Max Spent Equity: The maximum amount of your equity that you're willing to spend on a single trade. "
            "Make sure this value aligns with your trading strategy and risk tolerance.\n\n"
            "Stop Loss Margin & Take Profit Margin: These margins determine when the bot will automatically "
            "sell a security. Stop loss is to prevent further losses, and take profit is to secure profits. "
            "Note: 10% is represented as 0.1, not 10.\n\n"
            "Max Variation: This is the maximum variation in the price that you're willing to tolerate.\n\n"
            "Please make sure to enter valid values in all fields before saving the configuration!",
        )

        # Settings frame
        self.settings_frame = customtkinter.CTkFrame(self, width=150)
        self.settings_frame.grid(row=1, column=1, padx=(10, 20), pady=20, sticky="nsew")
        self.settings_frame.grid_columnconfigure(0, weight=1)

        # Entries for API_KEY, SECRET_KEY, maxSpentEquity
        self.api_key_entry = self.create_entry(
            "API string:", "Paste string here", show="*"
        )
        self.secret_key_entry = self.create_entry(
            "Secret API string:", "Paste string here", show="*"
        )
        self.max_spent_equity_entry = self.create_entry(
            "Max Spent Equity:", "Enter numerical value"
        )

        # Entries for stopLossMargin, takeProfitMargin, maxVar
        self.stop_loss_margin_entry = self.create_entry(
            "Stop Loss Margin :", "Enter numerical value"
        )
        self.take_profit_margin_entry = self.create_entry(
            "Take Profit Margin:", "Enter numerical value"
        )
        self.max_var_entry = self.create_entry(
            "Max Variation:", "Enter numerical value"
        )

        # Save Changes button
        self.save_button = customtkinter.CTkButton(
            self.settings_frame,
            text="Save changes",
            width=20,
            command=self.update_config,
        )
        self.save_button.pack(pady=20)

    def create_entry(self, label_text, placeholder=None, show=None):
        entry_frame = customtkinter.CTkFrame(self.settings_frame)
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.pack(fill="x", padx=(10, 20), pady=10)

        label = customtkinter.CTkLabel(entry_frame, text=label_text)
        label.grid(row=0, column=0, padx=(0, 10))

        entry = customtkinter.CTkEntry(
            entry_frame, width=20, placeholder_text=placeholder, show=show
        )  # Width for text entries
        entry.grid(row=0, column=1, sticky="ew")

        return entry

    def update_config(self):
        # Read the existing config data
        with open("config.json", "r") as f:
            config_data = json.load(f)

        # Update values based on GUI entries
        try:
            api_key = self.api_key_entry.get().strip()
            secret_key = self.secret_key_entry.get().strip()
            stop_loss_margin = float(self.stop_loss_margin_entry.get())
            take_profit_margin = float(self.take_profit_margin_entry.get())
            max_spent_equity = float(self.max_spent_equity_entry.get())
            max_var = float(self.max_var_entry.get())
        except ValueError:
            msgbox.showerror(
                "Invalid Input", "Please ensure all fields are correctly filled."
            )
            return

        # Validate inputs
        if not (0 <= stop_loss_margin <= 1) or not (0 <= take_profit_margin <= 1):
            msgbox.showerror(
                "Invalid Input", "Please ensure both margin fields are between 0 and 1."
            )
            return

        config_data["API_KEY"] = api_key
        config_data["SECRET_KEY"] = secret_key
        config_data["stopLossMargin"] = stop_loss_margin
        config_data["takeProfitMargin"] = take_profit_margin
        config_data["maxSpentEquity"] = max_spent_equity
        config_data["maxVar"] = max_var

        # Write the updated data back to the config file
        try:
            with open("config.json", "w") as f:
                json.dump(config_data, f, indent=4)
            msgbox.showinfo("Success", "Configuration updated successfully!")
        except Exception as e:
            msgbox.showerror("Error", f"Could not write to config file: {e}")


if __name__ == "__main__":
    gui = ConfigGUI()
    gui.mainloop()
