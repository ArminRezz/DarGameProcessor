from datetime import datetime

def date_to_day(date_string, date_format = '%Y-%m-%d'):
    """
    Convert a date string to the corresponding day of the week.
    
    Args:
        date_string (str): The date string to convert
        date_format (str): The format of the input date string (default: 'YYYY-MM-DD')
    
    Returns:
        str: The day of the week (e.g., 'Monday', 'Tuesday', etc.)
    
    Example:
        >>> date_to_day('2024-03-19')
        'Tuesday'
        >>> date_to_day('03/19/2024', '%m/%d/%Y')
        'Tuesday'
    """
    try:
        # Parse the date string into a datetime object
        date_obj = datetime.strptime(date_string, date_format)
        
        # Get the day of the week (0 = Monday, 6 = Sunday)
        day_number = date_obj.weekday()
        
        # Convert number to day name
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days[day_number]
    
    except ValueError as e:
        return f"Error: Invalid date format. Please use {date_format} format."

