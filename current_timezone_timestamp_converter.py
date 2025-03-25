"""
Global Travel Booking System - Timestamp Management Module

This module provides functionality for retrieving current timestamps and 
performing time zone conversions for a global travel booking system.
It helps manage the display of local and destination times, calculate
time differences, and format timestamps for different regional displays.
"""

from datetime import datetime
import pytz

def get_current_utc_time():
    """
    Get the current UTC time as a datetime object.
    
    Returns:
        datetime: Current UTC time
        
    Example:
        >>> get_current_utc_time()
        datetime.datetime(2025, 3, 19, 14, 30, 15, 234567, tzinfo=<UTC>)
    """
    return datetime.now(pytz.UTC)

def get_current_time_in_timezone(timezone):
    """
    Get the current time in the specified timezone.
    
    Args:
        timezone (str): Valid IANA timezone identifier (e.g., 'America/New_York')
        
    Returns:
        datetime: Current time in the specified timezone
        None: If the timezone is invalid
        
    Example:
        >>> get_current_time_in_timezone('Europe/London')
        datetime.datetime(2025, 3, 19, 14, 30, 15, 234567, tzinfo=<DstTzInfo 'Europe/London' GMT+0:00:00 STD>)
    """
    # Check if timezone is a string
    if not isinstance(timezone, str):
        print(f"Error: Timezone must be a string, got {type(timezone).__name__}")
        return None
        
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Error: Invalid timezone '{timezone}'")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def convert_timezone(dt, target_tz):
    """
    Convert a datetime object to another timezone.
    
    Args:
        dt (datetime): Datetime object with tzinfo
        target_tz (str): Target timezone (IANA identifier)
        
    Returns:
        datetime: Datetime converted to target timezone
        None: If the timezone is invalid or datetime has no tzinfo
        
    Example:
        >>> utc_time = datetime(2025, 3, 19, 14, 30, 0, tzinfo=pytz.UTC)
        >>> convert_timezone(utc_time, 'Asia/Tokyo')
        datetime.datetime(2025, 3, 19, 23, 30, 0, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)
    """
    if dt is None or dt.tzinfo is None:
        print("Error: Input datetime must have timezone information")
        return None
    
    try:
        target_timezone = pytz.timezone(target_tz)
        return dt.astimezone(target_timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        print(f"Error: Invalid timezone '{target_tz}'")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def format_timestamp(dt, format_string):
    """
    Format a datetime object using the specified format string.
    
    Args:
        dt (datetime): Datetime object to format
        format_string (str): Format string following strftime() conventions
        
    Returns:
        str: Formatted timestamp string
        None: If the datetime is invalid or format is incorrect
        
    Example:
        >>> dt = datetime(2025, 3, 19, 14, 30, 0, tzinfo=pytz.timezone('Europe/London'))
        >>> format_timestamp(dt, '%B %d, %Y %H:%M %Z')
        'March 19, 2025 14:30 GMT'
    """
    if dt is None:
        print("Error: Invalid datetime object")
        return None
    
    try:
        return dt.strftime(format_string)
    except Exception as e:
        print(f"Error: Invalid format string - {str(e)}")
        return None

def calculate_time_difference(timezone1, timezone2):
    """
    Calculate the current time difference between two timezones in hours and minutes.
    
    Args:
        timezone1 (str): First timezone (IANA identifier)
        timezone2 (str): Second timezone (IANA identifier)
        
    Returns:
        dict: Dictionary containing hours and minutes difference
            {'hours': int, 'minutes': int}
        None: If either timezone is invalid
        
    Example:
        >>> calculate_time_difference('America/New_York', 'Asia/Tokyo')
        {'hours': 13, 'minutes': 0}
    """
    try:
        # Get current time in both timezones
        tz1 = pytz.timezone(timezone1)
        tz2 = pytz.timezone(timezone2)
        
        # Use a reference time to ensure consistency
        now = datetime.now(pytz.UTC)
        time1 = now.astimezone(tz1)
        time2 = now.astimezone(tz2)
        
        # Calculate difference in minutes
        diff_seconds = (time2.utcoffset().total_seconds() - 
                       time1.utcoffset().total_seconds())
        diff_minutes = int(diff_seconds / 60)
        
        # Convert to hours and minutes
        hours = diff_minutes // 60
        minutes = diff_minutes % 60
        
        return {'hours': hours, 'minutes': minutes}
    except pytz.exceptions.UnknownTimeZoneError as e:
        print(f"Error: Invalid timezone - {str(e)}")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    """
    Demonstrate timestamp operations for a global travel booking system.
    """
    print("\n===== GLOBAL TRAVEL BOOKING SYSTEM - TIME DISPLAY =====\n")
    
    locations = {
        'New York': 'America/New_York',
        'London': 'Europe/London',
        'Tokyo': 'Asia/Tokyo',
        'Sydney': 'Australia/Sydney',
        'Paris': 'Europe/Paris',
        'Dubai': 'Asia/Dubai',
        'Los Angeles': 'America/Los_Angeles',
        'Singapore': 'Asia/Singapore'
    }
    
    while True:
        print("\nSelect an option:")
        print("1. View current UTC time")
        print("2. View times around the world")
        print("3. Plan a flight")
        print("4. Compare home and destination times")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            # 1. Get current UTC time
            utc_now = get_current_utc_time()
            print(f"\nCurrent UTC Time: {format_timestamp(utc_now, '%Y-%m-%d %H:%M:%S %Z')}")
            
        elif choice == '2':
            # 2. Display current times in different locations
            print("\n----- CURRENT TIMES AROUND THE WORLD -----")
            for city, timezone in locations.items():
                local_time = get_current_time_in_timezone(timezone)
                if local_time:
                    # Format times based on regional preferences
                    if city in ['New York', 'Los Angeles']:
                        formatted_time = format_timestamp(local_time, '%B %d, %Y %I:%M %p %Z')
                    else:
                        formatted_time = format_timestamp(local_time, '%d %B %Y %H:%M %Z')
                    print(f"{city}: {formatted_time}")
            
        elif choice == '3':
            # 3. Flight booking scenario
            print("\n----- FLIGHT BOOKING PLANNER -----")
            
            # Show available cities
            print("\nAvailable cities:")
            city_list = list(locations.keys())
            for i, city in enumerate(city_list):
                print(f"{i+1}. {city}")
            
            # Get departure and arrival cities
            try:
                dep_idx = int(input("\nSelect departure city (number): ")) - 1
                arr_idx = int(input("Select arrival city (number): ")) - 1
                
                if 0 <= dep_idx < len(city_list) and 0 <= arr_idx < len(city_list):
                    departure_city = city_list[dep_idx]
                    arrival_city = city_list[arr_idx]
                    departure_tz = locations[departure_city]
                    arrival_tz = locations[arrival_city]
                    
                    # Get departure date and time with clearer instructions
                    print("\nEnter departure date and time:")
                    print("Date format: YYYY-MM-DD (e.g., 2025-03-20)")
                    dep_date = input("Enter date: ")
                    
                    print("\nTime format: HH:MM in 24-hour format (e.g., 14:30)")
                    dep_time = input("Enter time: ")
                    
                    print("\nFlight duration in hours (e.g., 8.5 for 8 hours 30 minutes)")
                    flight_duration = float(input("Enter flight duration: "))
                    
                    # Create departure datetime with better error handling
                    try:
                        departure_time_str = f"{dep_date} {dep_time}:00"
                        departure_time_naive = datetime.strptime(departure_time_str, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        print(f"\nError: Invalid date or time format.")
                        print("Please use YYYY-MM-DD format for date and HH:MM format for time.")
                        continue
                    departure_tz_obj = pytz.timezone(departure_tz)
                    departure_time = departure_tz_obj.localize(departure_time_naive)
                    
                    # Calculate arrival time
                    from datetime import timedelta
                    arrival_time_utc = departure_time.astimezone(pytz.UTC) + timedelta(hours=flight_duration)
                    arrival_time = convert_timezone(arrival_time_utc, arrival_tz)
                    
                    # Display flight information
                    print("\n----- FLIGHT DETAILS -----")
                    print(f"Flight: {departure_city} to {arrival_city}")
                    print(f"Departure: {format_timestamp(departure_time, '%B %d, %Y %I:%M %p %Z')}")
                    print(f"Arrival: {format_timestamp(arrival_time, '%B %d, %Y %I:%M %p %Z')}")
                    
                    # Time difference between cities
                    time_diff = calculate_time_difference(departure_tz, arrival_tz)
                    if time_diff:
                        sign = "+" if time_diff['hours'] >= 0 else ""
                        print(f"Time Difference: {sign}{time_diff['hours']}h {time_diff['minutes']}m")
                else:
                    print("Invalid city selection.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
            except Exception as e:
                print(f"Error in flight planning: {str(e)}")
            
        elif choice == '4':
            # 4. Time comparison between home and destination
            print("\n----- TRAVELER TIME COMPARISON -----")
            
            # Show available cities
            print("\nAvailable cities:")
            city_list = list(locations.keys())
            for i, city in enumerate(city_list):
                print(f"{i+1}. {city}")
            
            try:
                home_idx = int(input("\nSelect your home city (number): ")) - 1
                dest_idx = int(input("Select your destination city (number): ")) - 1
                
                if 0 <= home_idx < len(city_list) and 0 <= dest_idx < len(city_list):
                    home_city = city_list[home_idx]
                    destination_city = city_list[dest_idx]
                    home_tz = locations[home_city]
                    destination_tz = locations[destination_city]
                    
                    home_time = get_current_time_in_timezone(home_tz)
                    destination_time = get_current_time_in_timezone(destination_tz)
                    
                    print(f"\nYour current time ({home_city}): {format_timestamp(home_time, '%d %B %Y %H:%M %Z')}")
                    print(f"Destination time ({destination_city}): {format_timestamp(destination_time, '%d %B %Y %H:%M %Z')}")
                    
                    time_diff = calculate_time_difference(home_tz, destination_tz)
                    if time_diff:
                        sign = "+" if time_diff['hours'] >= 0 else ""
                        print(f"Time Difference: {sign}{time_diff['hours']}h {time_diff['minutes']}m")
                else:
                    print("Invalid city selection.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
            except Exception as e:
                print(f"Error in time comparison: {str(e)}")
            
        elif choice == '5':
            print("\nThank you for using the Global Travel Booking System. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()