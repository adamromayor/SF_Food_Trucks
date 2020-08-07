#!/usr/bin/env python

# pip install requests
# pip install sodapy
# pip install pandas
# to run: python3 -m show_open_food_trucks

import requests
import pandas as pd
from sodapy import Socrata
from datetime import datetime


url = "http://data.sfgov.org/resource/bbb8-hzi6.json?"

# Get the current day of the week e.g. "Wednesday"
# To test a different day, change this variable
# e.g. day = "Monday"
day = datetime.today().strftime('%A')

# Curent time in 24hr format e.g. "15:50"
# To test a different time, change this variable
# e.g. current_time = "18:50"
current_time = datetime.now().strftime('%H:%M')

# format url for day of the week
url = url + "dayofweekstr=" + day

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
else:
    print("Failed to retrieve data from ", url)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(data)

# sorts entries by name, and resets index
results_df = results_df.sort_values(by=["applicant"])
results_df = results_df.reset_index(drop=True)


# Input is a single entry from results_df
# Prints name and address of foodtruck
def print_foodtruck_formatted(row):
    str = row["applicant"] + " " + row["location"]
    print(str)


# returns true if foodtruck is open, false if closed
# if curent time is exactly end time, returns false
def is_open(row):
    start= row["start24"]
    end = row["end24"]

    if(start <= current_time and current_time < end):
        return True
    return False


# prints 10 entries starting at index of results_df
# returns -1 if all rows in results_df have been visited
# returns next index in table once 10 food trucks are printed
def print_page(index):
    total_rows = len(results_df.index)
    max_index = index + 10
    while (True):
        if(is_open(results_df.loc[index])):
            print_foodtruck_formatted(results_df.loc[index])
        else:
            max_index += 1
        
        index += 1
        
        if(index == max_index):
            return index
        elif(index == total_rows):
            return -1


# prints 10 open food trucks at a time
# user can type "Y" to see 10 more
# user can type "N" to terminate program
# invalid input will prompt user to type (Y/N)
# once all open food trucks are printed, function will return
def print_open_food_trucks():
    index = 0
    print("Here is a list of open food trucks:\n")

    while(True):
        index = print_page(index)

        if(index == -1):
            print("\nYou have viewed all open food trucks... goodbye!")
            return
        while (True):
            val = input("\nSee more open food trucks? (Y/N): ") 
            print()
            val = val.upper()

            if(val == "N"):
                return
            elif (val == "Y"):
                break


def main():
    if response.status_code != 200:
        return
    print_open_food_trucks()


if __name__ == "__main__":
    main()
