"""
NHL (National Hockey League)

Follows a similar structure to NBA due to daily games:
- Monday (Public Day) - First game Vegas, then alternates.
- Tuesday (Vegas Day) - First game Public, then alternates.
- Wednesday (Public Day) - First game Vegas, then alternates.
- Thursday (Vegas Day) - First game Public, then alternates.
- Friday (Public Day) - First game Vegas, then alternates.
- Saturday (Vegas Day) - First game Public, then alternates.
- Sunday (Vegas Day) - First game Public, then alternates.

Notes:
- Low-scoring nature makes puck lines important.
- Public tends to overbet favorites and overs.
"""

import pandas as pd
from convert_date_to_day import date_to_day

def is_public_day(day_of_week):
    """
    Determines if a given day is a Public day or Vegas day.
    Public days are Monday, Wednesday, and Friday.
    """
    public_days = ['Monday', 'Wednesday', 'Friday']
    return day_of_week in public_days

def get_first_game_assignment(day_of_week):
    """
    Determines assignment for the first game of the day.
    On Public days: First game is Vegas
    On Vegas days: First game is Public
    """
    if is_public_day(day_of_week):
        return 'Vegas'  # Public days start with Vegas
    return 'Public'    # Vegas days start with Public

def assign_public_vegas(games_df):
    """
    Assigns 'Public' or 'Vegas' to NHL games based on these rules:
    - All games at the same time get the same assignment
    - Assignments alternate between Public and Vegas
    - First game assignment depends on the day of the week
    """
    # Get the day of the week
    game_date = games_df['day'].iloc[0]
    day_of_week = date_to_day(game_date)
    
    # Sort games by start time to ensure proper alternating pattern
    games_df = games_df.sort_values('start_time')
    
    # Get list of unique game times
    game_times = games_df['start_time'].unique()
    
    # Create assignments for each unique game time
    time_to_assignment = {}
    first_assignment = get_first_game_assignment(day_of_week)
    
    for index, game_time in enumerate(game_times):
        # If index is even (0, 2, 4...), use first_assignment
        if index % 2 == 0:
            time_to_assignment[game_time] = first_assignment
        # If index is odd (1, 3, 5...), use opposite of first_assignment
        else:
            if first_assignment == 'Vegas':
                time_to_assignment[game_time] = 'Public'
            else:
                time_to_assignment[game_time] = 'Vegas'
    
    # Add assignment column based on game time
    games_df['assignment'] = games_df['start_time'].map(time_to_assignment)
    
    return games_df

def process_nhl_games(input_file, output_file):
    """
    Process NHL games from input CSV and save results to output CSV.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    
    Returns:
        pd.DataFrame: Processed games dataframe with assignments
    """
    # Read NHL games data
    nhl_games = pd.read_csv(input_file)
    
    # Process assignments
    processed_games = assign_public_vegas(nhl_games)
    
    # Save results
    processed_games.to_csv(output_file, index=False)
    
    return processed_games

def main():
    """
    Main function to:
    1. Read NHL games from CSV
    2. Process assignments
    3. Save results to new CSV
    """
    input_file = 'input_csvs/nhl.csv'
    output_file = 'output_csvs/nhl_labeled.csv'
    
    try:
        # Read NHL games data
        print(f"Reading NHL games from {input_file}...")
        nhl_games = pd.read_csv(input_file)
        
        # Process assignments
        print("Assigning Public/Vegas designations...")
        processed_games = assign_public_vegas(nhl_games)
        
        # Save results
        processed_games.to_csv(output_file, index=False)
        print(f"Successfully saved results to {output_file}")
        
        # Print summary
        print("\nAssignment Summary:")
        summary = processed_games.groupby(['start_time', 'assignment']).size().reset_index(name='count')
        print(summary.to_string(index=False))
        
    except Exception as e:
        print(f"Error processing NHL games: {str(e)}")

if __name__ == "__main__":
    main()