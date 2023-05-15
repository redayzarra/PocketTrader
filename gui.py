import json
import tkinter.messagebox as msgbox

import customtkinter

from logger import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("750x650")


def update_config():
    # Read the existing config data
    with open("config.json", "r") as f:
        config_data = json.load(f)

    # Update values based on GUI entries
    try:
        stop_loss_margin = float(entry1.get())
        take_profit_margin = float(entry2.get())
    except ValueError:
        logging.error("Invalid input. Please ensure both fields are numeric.")
        msgbox.showerror("Invalid Input", "Please ensure both fields are numeric.")
        return

    # Validate inputs
    if not (0 <= stop_loss_margin <= 1) or not (0 <= take_profit_margin <= 1):
        logging.error("Invalid input. Please ensure both fields are between 0 and 1.")
        msgbox.showerror(
            "Invalid Input", "Please ensure both fields are between 0 and 1."
        )
        return

    config_data["stopLossMargin"] = stop_loss_margin
    config_data["takeProfitMargin"] = take_profit_margin

    # Write the updated data back to the config file
    try:
        with open("config.json", "w") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        logging.error(f"Could not write to config file: {e}")
        msgbox.showerror("Error", f"Could not write to config file: {e}")


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="Variable System")

label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter value")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter input", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=frame, text="System", command=update_config)
button.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Locked in")
checkbox.pack(pady=12, padx=10)

root.mainloop()
