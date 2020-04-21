import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# defining months and days below allows me to call them in the "def get_filters" function below.
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

# Note: was having issues getting the while loops to run correctly inside each user input, asked collegue that knows Python and was shown an easier way to get it by using multiple
# functions and used the "def user_input" and "def return_msg" in that manner.
# To print out the detailed stats from below. 1st item labeled "header" returns the appropriate str for each stat. 2nd item returns the f(x) listed

def return_msg(header, data):
    print(header)
    print(data)


def user_input(response, available_options):
    """ Asks for user input. Use while loop to analzye for incorrect response. """
    while True:
        user_choice = input(response).lower().strip()
        if user_choice in available_options:
            print('You chose ' + user_choice + '!')
            break
        else:
            print('Sorry, you made an incorrect choice. Please try again, type in only an answer from the available options.')
    return user_choice

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """ get user input for city """
    city = user_input('Enter one of the following cities: chicago, new york city, washington ',
                     list(CITY_DATA.keys()))

    """ get user input for month """
    month = user_input('Enter the month you would like data: january, february, march, april, may, june or all: ',
                       months)

    """ get user input for day of week """
    day = user_input('Enter the day of the week for data: monday, tuesday, wednesday, thursday, friday, saturday, sunday, or all ',
                    days)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    start_time = pd.to_datetime(df['Start Time'])
    df['month'] = start_time.dt.strftime("%B")
    df['day'] = start_time.dt.strftime("%A")
    df['hour'] = start_time.dt.strftime("%H")
    df['total_travel'] = pd.to_datetime(df['End Time'])  - start_time

    """ Filter by month """
    if month != 'all':
        df = df[df['month'] == month.title()]

    """ Filter by day """
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ display the most common month """
    most_common_month = df['month'].mode()[0]
    return_msg('The most common month was: ', most_common_month)

    """ display the most common day of week """
    most_common_day = df['day'].mode()[0]
    return_msg('The most common day was: ', most_common_day )

    """ display the most common start hour """
    most_common_hour = df['hour'].mode()[0]
    return_msg('The most common start hour was: ', most_common_hour )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ display most commonly used start station """
    return_msg('The most commonly used start station was: ', df['Start Station'].mode()[0])

    """ display most commonly used end station """
    return_msg('The most commonly used end station was: ', df['End Station'].mode()[0])

    """
     display most frequent combination of start station and end station trip
     Note: I used Stack Overflow to help with this solution.
    """
    return_msg('Top 3 most frequent combinations of start station and end station: ',
                  df.groupby(['Start Station','End Station']).size().nlargest(3))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """ display total travel time """
    return_msg('Total Travel Time: ', df['total_travel'].sum())

    """ display mean travel time """
    return_msg('Average Travel Time: ', df['total_travel'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Display counts of user types """
    #https://www.w3resource.com/pandas/series/series-value_counts.php
    print('User Type Counts: ')
    if 'User Type' in df.keys():
        return_msg('', df['User Type'].value_counts(dropna=True))
        print()
    else:
        return_msg('User Type', 'not available')

    """ Display counts of gender """
    print('Gender Counts: ')
    if 'Gender' in df.keys():
        return_msg('', df['Gender'].value_counts(dropna=True))
    else:
        return_msg('Gender', 'not available')

    """ Display earliest, most recent, and most common year of birth """
    if 'Birth Year' in df.keys():
        return_msg('Earliest birth year: ', int(df['Birth Year'].min()))

        return_msg('Most recent birth year: ', int(df['Birth Year'].max()))

        return_msg('Most common birth year: ', int(df['Birth Year'].mode()[0]))
    else:
        return_msg('Birth year', 'not available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

#        raw_data = user_input('\nWould you like to see table raw data? Enter yes or no.\n', ['yes', 'no'])
#        if raw_data == 'yes':
#            print(df.head())

# https://knowledge.udacity.com/questions/58280 
        lower_bound = 0
        upper_bound = 5
        while True:
          raw_data = input('Would you like to see 5 rows of data data?\nPlease select yes or no.').lower()
          if (raw_data == 'yes'):
            print(df[df.columns[0:]].iloc[lower_bound:upper_bound])
            lower_bound +=5
            upper_bound +=5
            #return
            continue
          elif (raw_data == 'no'):
            break

        restart = user_input('\nWould you like to restart the program? Enter yes or no.\n', ['yes', 'no'])
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
	main()
