import tkinter as tk
from tkinter import ttk
import pandas as pd
from mlb import process_mlb_games
from nba import process_nba_games
from nhl import process_nhl_games
from ncaab import process_ncaab_games
from nfl import process_nfl_games

class SportsProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sports Game Processor")
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.grid(row=0, column=0, pady=10)
        
        # Create process button
        self.process_button = ttk.Button(
            self.buttons_frame, 
            text="Process All Sports", 
            command=self.process_all_sports
        )
        self.process_button.grid(row=0, column=0, padx=5)
        
        # Create status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=1, column=0, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs for each sport
        self.tabs = {}
        for sport in ['MLB', 'NBA', 'NHL', 'NCAAB', 'NFL']:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=sport)
            self.tabs[sport] = frame
            
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

    def create_treeview(self, parent, columns):
        """Create a treeview widget with specified columns"""
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        
        # Configure columns and headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
        
        return tree

    def display_data(self, sport, df):
        """Display DataFrame in the appropriate tab with color coding"""
        # Clear existing widgets in the tab
        for widget in self.tabs[sport].winfo_children():
            widget.destroy()
            
        # Create treeview
        columns = df.columns.tolist()
        tree = self.create_treeview(self.tabs[sport], columns)
        
        # Insert data
        for idx, row in df.iterrows():
            values = row.tolist()
            
            # Determine tag based on assignment
            tag = row['assignment'].lower() if 'assignment' in row else ''
            
            # Insert row with tag
            tree.insert('', 'end', values=values, tags=(tag,))
        
        # Configure tags for colors
        tree.tag_configure('public', background='#90EE90', foreground='black')  # Light green
        tree.tag_configure('vegas', background='#FFB6C1', foreground='black')   # Light red

    def process_all_sports(self):
        """Process all sports data and display results"""
        self.status_label.config(text="Processing sports data...")
        
        try:
            # Process each sport
            sports_processors = {
                'MLB': ('input_csvs/mlb.csv', 'output_csvs/mlb_labeled.csv', process_mlb_games),
                'NBA': ('input_csvs/nba.csv', 'output_csvs/nba_labeled.csv', process_nba_games),
                'NHL': ('input_csvs/nhl.csv', 'output_csvs/nhl_labeled.csv', process_nhl_games),
                'NCAAB': ('input_csvs/ncaab.csv', 'output_csvs/ncaab_labeled.csv', process_ncaab_games),
                'NFL': ('input_csvs/nfl.csv', 'output_csvs/nfl_labeled.csv', process_nfl_games)
            }
            
            for sport, (input_file, output_file, processor) in sports_processors.items():
                try:
                    # Process the sport's data
                    processed_df = processor(input_file, output_file)
                    
                    # Display results in the appropriate tab
                    self.display_data(sport, processed_df)
                    
                except Exception as e:
                    print(f"Error processing {sport}: {str(e)}")
                    self.status_label.config(text=f"Error processing {sport}")
            
            self.status_label.config(text="All sports processed successfully!")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = SportsProcessorGUI(root)
    root.lift()  # Brings window to top
    root.focus_force()  # Forces focus on the window
    root.mainloop()

if __name__ == "__main__":
    main()
