import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"


def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"


def convert_date(iso_string):
    """Converts and ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    
    # The fromisoformat method in Python changes a date and time string (like “2023-09-01T10:30:00”)
    # into a datetime object that Python can work with. This string follows a standard format called ISO 8601.
    date_obj = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))

    # Format the date into a readable string (e.g., "Monday 01 September 2023")
    return date_obj.strftime("%A %d %B %Y")


def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    # If the temperature is given as a text string, convert it to a number
    if isinstance(temp_in_fahrenheit, str):
        temp_in_fahrenheit = float(temp_in_fahrenheit)
    
    # Change the temperature from Fahrenheit to Celsius
    temp_in_celsius = (temp_in_fahrenheit - 32) * 5 / 9
    
    # Round the Celsius temperature to one decimal place
    return round(temp_in_celsius, 1)


def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    # Change each item in the weather data list to a decimal number
    float_data = [float(item) for item in weather_data]
    
    # Find the average by adding all the numbers together and dividing by how many there are
    mean_value = sum(float_data) / len(float_data)
    
    return mean_value


def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """

    data = [] # Create an empty list to store the weather data

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row since it usually contains headers like "Date", "Min Temp", "Max Temp"
        for row in reader:
            if row:  # Only process the row if it has data
                date_str = row[0] # Get the date from the first column
                temp_min = int(row[1]) # Get the minimum temperature from the second column and convert it to a number
                temp_max = int(row[2]) # Get the maximum temperature from the third column and convert it to a number
                data.append([date_str, temp_min, temp_max]) # Add the date, min temp, and max temp to our data list

    return data


def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:  # Check if the list is empty
        return ()
    
    # Change all items to decimal numbers
    float_data = [float(item) for item in weather_data]
    
    # Get the smallest number
    min_value = min(float_data)
    
    # Find where the last smallest number appears in the list
    min_index = len(float_data) - 1 - float_data[::-1].index(min_value)
    
    return (min_value, min_index)


def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    if not weather_data:  # Check if the list is empty
        return ()
    
    # Convert all items to decimal numbers
    float_data = [float(item) for item in weather_data]
    
    # Get the largest number
    max_value = max(float_data)
    
    # Find where the last largest number appears in the list
    max_index = len(float_data) - 1 - float_data[::-1].index(max_value)
    
    return (max_value, max_index)


def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    # Extract dates, min and max temperatures
    dates = [datetime.fromisoformat(day[0]) for day in weather_data]
    min_temps = [day[1] for day in weather_data]
    max_temps = [day[2] for day in weather_data]

    # Find the overall min and max temperatures and their corresponding dates
    min_temp, min_position = find_min(min_temps)
    max_temp, max_position = find_max(max_temps)
    min_temp_date = dates[min_position]
    max_temp_date = dates[max_position]

    # Calculate the average min and max temperatures
    avg_min_temp = calculate_mean(min_temps)
    avg_max_temp = calculate_mean(max_temps)
    # Convert degrees f to c
    min_temp_c = convert_f_to_c(min_temp)
    max_temp_c = convert_f_to_c(max_temp)
    avg_min_temp_c = convert_f_to_c(avg_min_temp)
    avg_max_temp_c = convert_f_to_c(avg_max_temp)

    # Format the summary string
    summary = (
        f"{len(weather_data)} Day Overview\n"
        f"  The lowest temperature will be {format_temperature(min_temp_c)}, and will occur on {min_temp_date.strftime('%A %d %B %Y')}.\n"
        f"  The highest temperature will be {format_temperature(max_temp_c)}, and will occur on {max_temp_date.strftime('%A %d %B %Y')}.\n"
        f"  The average low this week is {format_temperature(avg_min_temp_c)}.\n"
        f"  The average high this week is {format_temperature(avg_max_temp_c)}.\n"
    )

    return summary


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    # Initialize an empty string to store the final summary
    summary = ""
    
    # Loop through each day's data in the weather_data list
    for day in weather_data:
        # Extract the date, minimum temperature, and maximum temperature from the current day's data
        date = datetime.fromisoformat(day[0])
        min_temp_c = convert_f_to_c(day[1])
        max_temp_c = convert_f_to_c(day[2])
        
        # Format the summary for each day
        day_summary = (
            f"---- {date.strftime('%A %d %B %Y')} ----\n"
            f"  Minimum Temperature: {format_temperature(min_temp_c)}\n"
            f"  Maximum Temperature: {format_temperature(max_temp_c)}\n\n"
        )
        # Add the formatted summary for the current day to the overall summary
        summary += day_summary
    
    return summary
