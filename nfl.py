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

def process_nfl_games(games_df):
    """
    Main processing function for NFL games.
    Takes a DataFrame of games and returns the DataFrame with Public/Vegas assignments.
    
    Args:
        games_df (pandas.DataFrame): DataFrame containing NFL games
            Required columns: ['day', 'start_time']
    
    Returns:
        pandas.DataFrame: Original DataFrame with added 'assignment' column
    """
    if games_df.empty:
        return games_df
        
    # Validate required columns
    required_columns = ['day', 'start_time']
    missing_columns = [col for col in required_columns if col not in games_df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    # Process the games and assign Public/Vegas
    processed_df = assign_public_vegas(games_df.copy())
    
    return processed_df

if __name__ == "__main__":
    # Example usage
    example_data = {
        'day': ['2024-02-08', '2024-02-11', '2024-02-11', '2024-02-11', '2024-02-12'],
        'start_time': ['8:20 PM', '1:00 PM', '4:25 PM', '8:20 PM', '8:15 PM'],
        'home_team': ['Team1', 'Team2', 'Team3', 'Team4', 'Team5'],
        'away_team': ['Team6', 'Team7', 'Team8', 'Team9', 'Team10']
    }
    
    example_df = pd.DataFrame(example_data)
    result_df = process_nfl_games(example_df)
    print("\nProcessed NFL Games:")
    print(result_df[['day', 'start_time', 'assignment']])