#!/usr/bin/env python

# Make sure to install requests before running:
# > pip install requests
# Documentation for the requests library can be found here: http://docs.python-requests.org/en/master/


# pip install sodapy
# pip install pandas

import requests
import pandas as pd
from sodapy import Socrata
from datetime import datetime


url = "http://data.sfgov.org/resource/bbb8-hzi6.json?"

#Get the current day of the week e.g. "Wednesday"
day = datetime.today().strftime('%A')

#Curent time in 24hr format e.g. "15:50"
current_time = datetime.now().strftime('%H:%M')

#format url for day of the week
url = url + "dayofweekstr=" + day

response = requests.get(url)
if response.status_code == 200:
    data = response.json()

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(data)

#sorts entries by name, and resets index
results_df = results_df.sort_values(by=["applicant"])
results_df = results_df.reset_index(drop=True)


# Input is a single entry from results_df
# Prints name and address of foodtruck
def print_foodtruck_formatted(row):
    str = row["applicant"] + " " + row["location"]
    print(str)


#returns true if foodtruck is open
def isOpen(row):
    start= row["start24"]
    end = row["end24"]

    if(start < current_time and current_time < end):
        return True
    return False


#prints 10 entries starting at index
#returns -1 if all rows in results_df have been visited
def print_page(index):
    total_rows = len(results_df.index)

    max_index = index + 10
    while (True):
        if(isOpen(results_df.loc[index])):
            print_foodtruck_formatted(results_df.loc[index])
        else:
            #print("closed: ",end=" --- ")
            #print_foodtruck_formatted(results_df.loc[index])
            max_index += 1
        index += 1
        if(index == max_index):
            return index
        elif(index == total_rows):
            return -1

def print_open_food_trucks():
    index = 0
    print("Here is a list of open food trucks!")
    while(True):
        index = print_page(index)

        #print("--- --- --- --- --- --- --- --- --- --- --- --- ")
        if(index == -1):
            print("You have viewed all open food trucks... goodbye!")
            return
        while (True):
            val = input("See more open food trucks? (Y/N): ") 
            val = val.upper()

            if(val == "N"):
                return
            elif (val == "Y"):
                break


def main():
    print_open_food_trucks()


if __name__ == "__main__":
    main()
