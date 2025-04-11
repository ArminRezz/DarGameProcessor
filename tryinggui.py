import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import filedialog

def load_excel(sport):
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    if file_path:
        try:
            df = pd.read_excel(file_path)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Loaded {sport} data:\n\n")
            output_text.insert(tk.END, df.to_string())
        except Exception as e:
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, f"Error loading file: {str(e)}")

window = tk.Tk()
window.title("Sports Data Viewer")
window.geometry("800x600")

# Create a frame for the buttons
button_frame = ttk.Frame(window)
button_frame.pack(pady=10)

# Create sports buttons
sports = ["MLB", "NBA", "NCAA Basketball", "NFL", "NHL"]
for sport in sports:
    button = ttk.Button(
        button_frame,
        text=sport,
        command=lambda s=sport: load_excel(s)
    )
    button.pack(side=tk.LEFT, padx=5)

# Create output area
output_frame = ttk.Frame(window)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_text = tk.Text(output_frame, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(output_text, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

window.mainloop()