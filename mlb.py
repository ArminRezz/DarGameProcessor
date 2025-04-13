"""
MLB (Major League Baseball)

162-game season, many games per day, different start times:
  • Monday: Public Day
  • Tuesday: Vegas Day
  • Wednesday: Hybrid (first half public, 5:40 PM CST Vegas ====> aka 6:40 PM EST)
  • Thursday: Vegas Day
  • Friday: Public Day
  • Saturday: Vegas Day
  • Sunday: Vegas Day

Additional Notes:
  • Early games (1 PM - 4 PM) tend to favor Vegas betting trends
  • Public loads up on big-name pitchers & home teams
  • Late games often have sharper movement
"""

import pandas as pd
from datetime import datetime
from convert_date_to_day import date_to_day

def is_public_day(day_of_week):
    """
    Determines if a given day is a Public day.
    Public days are Monday and Friday.
    """
    public_days = ['Monday', 'Friday']
    return day_of_week in public_days

def is_hybrid_day(day_of_week):
    """
    Determines if a given day is a Hybrid day (Wednesday).
    """
    return day_of_week == 'Wednesday'

def get_game_assignment(day_of_week, start_time):
    """
    Determines assignment based on day and start time.
    
    Args:
        day_of_week (str): Day of the week
        start_time (str): Game start time in format 'I:M %p EDT/EST'
    
    Returns:
        str: 'Public' or 'Vegas' assignment
    """
    if is_public_day(day_of_week):
        return 'Public'
    
    if is_hybrid_day(day_of_week):
        # Extract time without timezone for comparison
        time_str = start_time.split(' ')[0] + ' ' + start_time.split(' ')[1]
        time_obj = datetime.strptime(time_str, '%I:%M %p')
        
        # Convert to 24-hour format for comparison
        hour = time_obj.hour
        minute = time_obj.minute
        
        # 6:40 PM cutoff
        if hour < 18 or (hour == 18 and minute < 40):
            return 'Public'
        return 'Vegas'
    
    # All other days are Vegas days
    return 'Vegas'

def assign_public_vegas(games_df):
    """
    Assigns 'Public' or 'Vegas' to MLB games based on these rules:
    - Monday and Friday are Public days
    - Wednesday is hybrid (Public before 6:40 PM EST, Vegas after)
    - All other days are Vegas days
    - Early games (1-4 PM) on any day favor Vegas trends
    """
    # Get the day of the week
    game_date = games_df['day'].iloc[0]
    day_of_week = date_to_day(game_date)
    
    # Create assignments based on day and time
    games_df['assignment'] = games_df['start_time'].apply(
        lambda x: get_game_assignment(day_of_week, x)
    )
    
    # Override for early games (1 PM - 4 PM) to favor Vegas
    # Convert times to datetime for comparison
    time_objects = pd.to_datetime(games_df['start_time'].str.replace(' EDT', '').str.replace(' EST', ''), format='%I:%M %p')
    early_game_mask = (
        (time_objects.dt.hour >= 13) & 
        (time_objects.dt.hour <= 16)
    )
    games_df.loc[early_game_mask, 'assignment'] = 'Vegas'
    
    return games_df

def process_mlb_games(input_file, output_file):
    """
    Process MLB games from input CSV and save results to output CSV.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    
    Returns:
        pd.DataFrame: Processed games dataframe with assignments
    """
    # Read MLB games data
    mlb_games = pd.read_csv(input_file)
    
    # Process assignments
    processed_games = assign_public_vegas(mlb_games)
    
    # Save results
    processed_games.to_csv(output_file, index=False)
    
    return processed_games

def main():
    """
    Main function to:
    1. Read MLB games from CSV
    2. Process assignments
    3. Save results to new CSV
    """
    input_file = 'input_csvs/mlb.csv'
    output_file = 'output_csvs/mlb_labeled.csv'
    
    try:
        # Read MLB games data
        print(f"Reading MLB games from {input_file}...")
        mlb_games = pd.read_csv(input_file)
        
        # Process assignments
        print("Assigning Public/Vegas designations...")
        processed_games = assign_public_vegas(mlb_games)
        
        # Save results
        processed_games.to_csv(output_file, index=False)
        print(f"Successfully saved results to {output_file}")
        
        # Print summary
        print("\nAssignment Summary:")
        summary = processed_games.groupby(['start_time', 'assignment']).size().reset_index(name='count')
        print(summary.to_string(index=False))
        
    except Exception as e:
        print(f"Error processing MLB games: {str(e)}")

if __name__ == "__main__":
    main()
