"""
DAR (Data Analytics Report) Game Categorizer
------------------------------------------
This module categorizes sports games into different types (Vegas/Public/Mixed) based on specific rules:

NBA/NHL/NCAAB Rules:
- Vegas days (Tue/Thu/Sat/Sun): Alternate Public-Vegas starting with Public
- Other days: Alternate Vegas-Public starting with Vegas

NFL Rules:
- Sunday 1 PM games: Public
- Sunday 4 PM, Sunday Night, Thursday games: Vegas
- Monday Night games: Public

MLB Rules:
- Vegas days (Tue/Thu/Sat/Sun): All Vegas games
- Wednesday games: Split based on start time
  * Before 5:40 PM CST: Public
  * After 5:40 PM CST: Vegas
- Other days: All Public games

NCAAF Rules:
- Saturday Early games: Public
- Saturday Afternoon games: Vegas
- Saturday Night games: Mixed
- Thursday/Friday games: Vegas
"""

from datetime import datetime

def get_day_type(sport, day):
    """
    Determines if a given day is traditionally a Vegas or Public day for a sport.
    
    Args:
        sport (str): Sport identifier (nba, nfl, nhl, etc.)
        day (str): Day of the week or specific timeslot
    
    Returns:
        str: 'vegas', 'public', or 'unknown'
    """
    day = day.lower() 
    vegas_days = {
        'nba': ['tuesday', 'thursday', 'saturday', 'sunday'],
        'nfl': ['thursday', 'sunday 4 pm', 'sunday night', 'monday night'],
        'nhl': ['tuesday', 'thursday', 'saturday', 'sunday'],
        'mlb': ['tuesday', 'thursday', 'saturday', 'sunday'],
        'ncaab': ['tuesday', 'thursday', 'saturday', 'sunday'],
        'ncaaf': ['thursday', 'friday', 'saturday afternoon']
    }

    if sport in vegas_days:
        return 'vegas' if any(day.startswith(d) for d in vegas_days[sport]) else 'public'
    return 'unknown'

def determine_game_type(sport, day, game_index, start_time=None):
    """
    Determines the game type (Vegas/Public/Mixed) based on sport-specific rules.
    
    Args:
        sport (str): Sport identifier
        day (str): Day of the week or specific timeslot
        game_index (int): Game number for the day (used for alternating patterns)
        start_time (float, optional): Game start time in 24-hour format (used for MLB)
    
    Returns:
        str: 'vegas', 'public', 'mixed', or 'unknown'
    """
    # Normalize input
    sport = sport.lower()
    day = day.lower()
    day_type = get_day_type(sport, day)

    # Rules for alternating games (NBA/NHL/NCAAB)
    if sport in ['nba', 'nhl', 'ncaab']:
        if 'public' in day_type:
            return 'vegas' if game_index % 2 == 0 else 'public'
        else:
            return 'public' if game_index % 2 == 0 else 'vegas'

    # NFL special case handling
    if sport == 'nfl':
        if '1 pm' in day:
            return 'public'
        elif '4 pm' in day or 'sunday night' in day or 'thursday' in day:
            return 'vegas'
        elif 'monday' in day:
            return 'public'
        else:
            return 'unknown'

    # MLB hybrid Wednesday
    if sport == 'mlb' and 'wednesday' in day and start_time:
        if start_time < 17.4:  # 5:40 PM CST == 17.4 in 24h
            return 'public'
        else:
            return 'vegas'

    # NCAAF handling
    if sport == 'ncaaf':
        if 'saturday' in day:
            if 'early' in day:
                return 'public'
            elif 'afternoon' in day:
                return 'vegas'
            elif 'night' in day:
                return 'mixed'
        return 'vegas'

    return day_type

# Example usage:
games_today = [
    {'sport': 'NBA', 'day': 'Monday', 'game_index': 0},
    {'sport': 'NBA', 'day': 'Monday', 'game_index': 1},
    {'sport': 'NFL', 'day': 'Sunday 1 PM'},
    {'sport': 'NFL', 'day': 'Sunday 4 PM'},
    {'sport': 'MLB', 'day': 'Wednesday', 'start_time': 16.0},
    {'sport': 'MLB', 'day': 'Wednesday', 'start_time': 18.0},
]

for game in games_today:
    result = determine_game_type(
        game['sport'],
        game['day'],
        game.get('game_index', 0),
        game.get('start_time')
    )
    print(f"{game['sport']} on {game['day']} -> {result.title()} Game")