import pandas as pd
from datetime import datetime

def determine_game_type(row, games_at_same_time):
    # Convert date string to datetime object to get day of week
    date = datetime.strptime(row['day'], '%Y-%m-%d')
    day_of_week = date.strftime('%A')
    
    # Get the start time for comparison
    start_time = row['start_time']
    
    # Rules for each day
    day_rules = {
        'Monday': {'is_public_day': True, 'first_is_vegas': True},
        'Tuesday': {'is_public_day': False, 'first_is_public': True},
        'Wednesday': {'is_public_day': True, 'first_is_vegas': True},
        'Thursday': {'is_public_day': False, 'first_is_public': True},
        'Friday': {'is_public_day': True, 'first_is_vegas': True},
        'Saturday': {'is_public_day': False, 'first_is_public': True},
        'Sunday': {'is_public_day': False, 'first_is_public': True}
    }
    
    rules = day_rules[day_of_week]
    
    # If all games at the same time slot (7 PM) are Vegas
    if len(games_at_same_time) > 1 and start_time == '7:00 PM EDT':
        return 'Vegas'
        
    # For the first game of the day
    if games_at_same_time['game_number'].iloc[0] == 1:
        if rules['is_public_day']:
            return 'Vegas' if rules.get('first_is_vegas') else 'Public'
        else:
            return 'Public' if rules.get('first_is_public') else 'Vegas'
            
    # For subsequent games, alternate between Vegas and Public
    prev_game = games_at_same_time['game_number'].iloc[0] - 1
    if prev_game % 2 == 0:
        return 'Vegas'
    return 'Public'

def process_nba_games(input_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Convert to datetime for sorting
    df['start_time'] = pd.to_datetime(df['day'] + ' ' + df['start_time'], format='%Y-%m-%d %I:%M %p EDT')
    
    # Sort by date and start time
    df = df.sort_values('start_time')
    
    # Add game number for each day
    df['game_number'] = df.groupby(df['day']).cumcount() + 1
    
    # Group by same start time
    df['games_at_same_time'] = df.groupby(['day', 'start_time'])['game_number'].transform('count')
    
    # Apply the rules to determine game type
    df['game_type'] = df.apply(lambda row: determine_game_type(row, 
        df[df['start_time'] == row['start_time']]), axis=1)
    
    # Format the output
    df['start_time'] = df['start_time'].dt.strftime('%I:%M %p')
    result_df = df[['sport', 'day', 'start_time', 'teams', 'game_type']]
    result_df.columns = ['Sport', 'Date', 'Start Time', 'Matchup', 'Game Type']
    
    # Save to Excel
    result_df.to_excel('processed_nba_games.xlsx', index=False)
    return result_df

if __name__ == '__main__':
    processed_games = process_nba_games('data_csvs/nba.csv')
    print("Processing complete. Results saved to 'processed_nba_games.xlsx'")
