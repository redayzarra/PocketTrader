import json
import tkinter.messagebox as msgbox

import customtkinter as ctk

from logger import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()

root.geometry("700x600")
root.title("PocketTrader")


def update_config():
    # Read the existing config data
    with open("config.json", "r") as f:
        config_data = json.load(f)

    # Update values based on GUI entries
    try:
        api_key = api_key_entry.get().strip()
        secret_key = secret_key_entry.get().strip()
        stop_loss_margin = float(stop_loss_margin_entry.get())
        take_profit_margin = float(take_profit_margin_entry.get())
        max_spent_equity = float(max_spent_equity_entry.get())
        max_var = float(max_var_entry.get())
        max_attempts = int(max_attempts_entry.get())
        sleep_time = float(sleep_time_entry.get())
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

    config_data["apiKey"] = api_key
    config_data["secretKey"] = secret_key
    config_data["stopLossMargin"] = stop_loss_margin
    config_data["takeProfitMargin"] = take_profit_margin
    config_data["maxSpentEquity"] = max_spent_equity
    config_data["maxVar"] = max_var
    config_data["maxAttempts"] = max_attempts
    config_data["sleepTime"] = sleep_time

    # Write the updated data back to the config file
    try:
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)
        msgbox.showinfo("Success", "Configuration updated successfully!")
    except Exception as e:
        msgbox.showerror("Error", f"Could not write to config file: {e}")


# Frame to hold all inputs
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Label to title the GUI
label = ctk.CTkLabel(master=frame, text="PocketTrader Bot Configuration")
label.pack(pady=12, padx=10)

# Key Entries
api_key_label = ctk.CTkLabel(master=frame, text="API Key")
api_key_label.pack()
api_key_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter API Key", show="*")
api_key_entry.pack()

secret_key_label = ctk.CTkLabel(master=frame, text="Secret Key")
secret_key_label.pack()
secret_key_entry = ctk.CTkEntry(
    master=frame, placeholder_text="Enter Secret Key", show="*"
)
secret_key_entry.pack()

# Margin Entries
stop_loss_margin_label = ctk.CTkLabel(master=frame, text="Stop Loss Margin")
stop_loss_margin_label.pack()
stop_loss_margin_entry = ctk.CTkEntry(
    master=frame, placeholder_text="Enter Stop Loss Margin"
)
stop_loss_margin_entry.pack()

take_profit_margin_label = ctk.CTkLabel(master=frame, text="Take Profit Margin")
take_profit_margin_label.pack()
take_profit_margin_entry = ctk.CTkEntry(
    master=frame, placeholder_text="Enter Take Profit Margin"
)
take_profit_margin_entry.pack()

# Max Equity Entry
max_spent_equity_label = ctk.CTkLabel(master=frame, text="Max Spent Equity")
max_spent_equity_label.pack()
max_spent_equity_entry = ctk.CTkEntry(
    master=frame, placeholder_text="Enter Max Spent Equity"
)
max_spent_equity_entry.pack()

# Max Variation Entry
max_var_label = ctk.CTkLabel(master=frame, text="Max Variation")
max_var_label.pack()
max_var_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter Max Variation")
max_var_entry.pack()

# Max Attempts Entry
max_attempts_label = ctk.CTkLabel(master=frame, text="Max Attempts")
max_attempts_label.pack()
max_attempts_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter Max Attempts")
max_attempts_entry.pack()

# Sleep Time Entry
sleep_time_label = ctk.CTkLabel(master=frame, text="Sleep Time")
sleep_time_label.pack()
sleep_time_entry = ctk.CTkEntry(master=frame, placeholder_text="Enter Sleep Time")
sleep_time_entry.pack()

# Save Config Button
save_button = ctk.CTkButton(master=frame, text="Save Config", command=update_config)
save_button.pack(pady=20)

root.mainloop()
