"""
##### NFL (National Football League)

_Weekly games, different schedule from daily sports like NBA/NHL:_
- **Thursday Night Football (Vegas Day)** – Short prep week, favors Vegas lines.
- **Sunday 1 PM (Public Games)** – Heavy casual bettor action, public sides stronger.
- **Sunday 4 PM (Vegas Games)** – Sharper betting movement, more line shifts.
- **Sunday Night Football (Vegas Game)** – Prime-time, sharp money shapes late action.
- **Monday Night Football (Public Game)** – Standalone, public teams get more money.

✔ Public bets favor favorites, overs, and big-name teams.  
✔ Sharp action usually hits Sunday morning and before prime-time games.

"""

import pandas as pd
from datetime import datetime

def date_to_day(date_str):
    """Convert date string to day of week."""
    date_obj = pd.to_datetime(date_str)
    return date_obj.strftime('%A')

def assign_public_vegas(games_df):
    """
    Assigns 'Public' or 'Vegas' to NFL games based on these rules:
    - Thursday Night Football: Vegas
    - Sunday 1 PM: Public
    - Sunday 4 PM: Vegas  
    - Sunday Night Football: Vegas
    - Monday Night Football: Public
    
    Reference from README:
    - Thursday Night Football (Vegas Day) – Short prep week, favors Vegas lines.
    - Sunday 1 PM (Public Games) – Heavy casual bettor action, public sides stronger.
    - Sunday 4 PM (Vegas Games) – Sharper betting movement, more line shifts.
    - Sunday Night Football (Vegas Game) – Prime-time, sharp money shapes late action.
    - Monday Night Football (Public Game) – Standalone, public teams get more money.
    """
    # Sort games by start time to ensure proper ordering
    games_df = games_df.sort_values('start_time')
    
    # Get the day of the week for each game
    games_df['day_of_week'] = games_df['day'].apply(date_to_day)
    
    # Initialize assignment column
    games_df['assignment'] = None
    
    # Thursday Night Football
    thursday_mask = games_df['day_of_week'] == 'Thursday'
    games_df.loc[thursday_mask, 'assignment'] = 'Vegas'
    
    # Sunday Games
    sunday_mask = games_df['day_of_week'] == 'Sunday'
    sunday_games = games_df[sunday_mask]
    
    # Convert times to 24-hour format for comparison
    for idx in sunday_games.index:
        game_time = sunday_games.loc[idx, 'start_time']
        
        # Sunday 1 PM games
        if '1:' in game_time:
            games_df.loc[idx, 'assignment'] = 'Public'
        # Sunday 4 PM games
        elif '4:' in game_time:
            games_df.loc[idx, 'assignment'] = 'Vegas'
        # Sunday Night Football (typically 8:20 PM)
        elif '8:' in game_time:
            games_df.loc[idx, 'assignment'] = 'Vegas'
    
    # Monday Night Football
    monday_mask = games_df['day_of_week'] == 'Monday'
    games_df.loc[monday_mask, 'assignment'] = 'Public'
    
    return games_df

def process_nfl_games(input_file, output_file):
    """
    Process NFL games from input CSV and save results to output CSV.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    
    Returns:
        pd.DataFrame: Processed games dataframe with assignments
    """
    # Read NFL games data
    nfl_games = pd.read_csv(input_file)
    
    # Process assignments
    processed_games = assign_public_vegas(nfl_games)
    
    # Save results
    processed_games.to_csv(output_file, index=False)
    
    return processed_games

def main():
    """
    Main function to:
    1. Read NFL games from CSV
    2. Process assignments
    3. Save results to new CSV
    """
    input_file = 'input_csvs/nfl.csv'
    output_file = 'output_csvs/nfl_labeled.csv'
    
    try:
        # Read NFL games data
        print(f"Reading NFL games from {input_file}...")
        nfl_games = pd.read_csv(input_file)
        
        # Process assignments
        print("Assigning Public/Vegas designations...")
        processed_games = assign_public_vegas(nfl_games)
        
        # Save results
        processed_games.to_csv(output_file, index=False)
        print(f"Successfully saved results to {output_file}")
        
        # Print summary
        print("\nAssignment Summary:")
        summary = processed_games.groupby(['day_of_week', 'assignment']).size().reset_index(name='count')
        print(summary.to_string(index=False))
        
    except Exception as e:
        print(f"Error processing NFL games: {str(e)}")

if __name__ == "__main__":
    main()