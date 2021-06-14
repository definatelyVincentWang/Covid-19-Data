#!/usr/bin/python3
import matplotlib.pyplot as plt
import csv
import sys
import cgi
import matplotlib

matplotlib.use('Agg')

def get_cmd():
  args = cgi.FieldStorage()
  cmd = args['cmd'].value
  return cmd

cmd = get_cmd()
#cmd = "US"

#def find_largest(data):
#    largest = max(data.values())
#    for x,y in data.items():
#        if (y == largest):
#            return x

def line(data, title, x, y):
    # Data is a dictionary with the number of new deaths each day (Ex. Worldwide, USwide, Statewide) _/
    plt.plot(list(data.keys()), list(data.values()))
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.grid()

def bar(data,title,x,y):
    # Data is a dictionary with top 20 States with the most cases
    states = data.keys()
    states = sorted(states, reverse=True, key=lambda k: data[k])
    states = states[:min(20, len(states))]
    values = [data[k] for k in states]
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    #plt.bar(new_data.keys(), new_data.values())
    plt.bar(states, values)

def state_bar(data,title,x,y):
    # Data is a dictionary with top 20 States with the most cases
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.bar(data.keys(), data.values())

"""
def gender(men, women, label, y):
    # sorted dictionary of all number of cases in US based on age _/
    plt.bar(label, men, color = 'r')
    plt.bar(label, women, color = 'b')
    plt.legend(labels=['Men', 'Women'])
    plt.ylabel(y)
"""
    
def unpack_data(csv_file):
    data = {}
    csv_reader = csv.reader(open(csv_file), delimiter=',')
    line = 0
    for row in csv_reader:
        if (line == 0):
            line += 1
        else:
            data[row[0]] = row[1]
    return data

def unpack_multiple_data(csv_file):
    cases = {}
    deaths = {}
    csv_reader = csv.reader(open(csv_file), delimiter=',')
    line = 0
    casesPos = 1
    deathsPos = 2
    for row in csv_reader:
        if (line == 0):
            if (row[0] == deaths):
                casesPos = 2
                deathsPos = 1
            line += 1
        else:
            cases[row[0]] = float(row[casesPos])
            deaths[row[0]] = float(row[deathsPos])
    return cases, deaths

"""
def unpack_genders(file):
    men = csv.reader(open(file), delimiter=',')
    men_cases = []
    men_death = []
    labels = []
    line = 0
    for mens in men:
        if line == 0:
            line += 1
            continue
        labels.append(mens[0])
        men_death.append(int(mens[1]))
        men_cases.append(int(mens[2]))
    return men_cases, men_death, labels
"""


print("Content-Type: image/png\n", flush=True)

# Both deaths and cases
if cmd in ['California', 'Illinois', 'Ohio']:
    N = 2
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(15,13))
    cases, deaths = unpack_multiple_data(f"State_Data/{cmd}.csv")
    plt.subplot(N,1,1)
    state_bar(cases, "Total cases by age", "Age", "Cases")
    plt.subplot(N,1,2)
    state_bar(deaths, "Total deaths by age", "Age", "Deaths")
if cmd == 'Georgia':
    N = 2
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(15,13))
    cases, deaths = unpack_multiple_data(f"State_Data/{cmd}.csv")
    plt.subplot(N,1,1)
    state_bar(cases, "Total cases by age in Bryan, Camden, Chatham, Effingham, Glynn, Liberty, Long, and McIntosh Counties.", "Age", "Cases")
    plt.subplot(N,1,2)
    state_bar(deaths, "Total deaths by age in Bryan, Camden, Chatham, Effingham, Glynn, Liberty, Long, and McIntosh Counties.", "Age", "Deaths")
# only deaths
if cmd in ['Florida', 'New_York', 'Pennsylvania']:
    deaths = unpack_data(f"State_Data/{cmd}.csv")
    state_bar(deaths, "Deaths with confirmed or presumed COVID-19", "Age", "Deaths")
# only cases
if cmd == 'North_Carolina':
    cases = unpack_data("State_Data/North_Carolina.csv")
    state_bar(cases, "Total Cases by age", "Age", "Cases")
# both death and case percentages
if cmd == 'Texas':
    N = 2
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(15,13))
    cases, deaths = unpack_multiple_data("State_Data/Texas.csv")
    plt.subplot(N,1,1)
    state_bar(cases, "Percentage of Total Cases by age", "Age", "Percent Cases")
    plt.subplot(N,1,2)
    state_bar(deaths, "Percentage of TOtal Deaths by age", "Age", "Percent Deaths")
# only death percentage
if cmd == 'New_Jersey':
    data = unpack_data("State_Data/New_Jersey.csv")
    state_bar(data, "Death Percentages by Age", "Age", "Percentage")
# US only
if cmd == 'US':
    # top 20 states deaths and cases
    N = 12
    plt.subplots(N, 1, sharex=False, sharey=False, figsize=(20,63))

    state_cases, state_deaths = unpack_multiple_data("US_Data/Pop_Data.csv")
    plt.subplot(N,1,1)
    bar(state_cases, "Number of cases per 1,000,000 people (Cumulative)", "state", "Cases")

    plt.subplot(N,1,2)
    bar(state_deaths, "Number of deaths per 1,000,000 people (Cumulative)", "state", "Deaths")

    # line graphs for deaths and cases all days
    date_Total_cases, date_New_cases = unpack_multiple_data("US_Data/unused_dates_data.csv")
    date_Total_deaths, date_New_Deaths = unpack_multiple_data("US_Data/unused_dates_Deaths_data.csv")
    date_cases, date_deaths = unpack_multiple_data("US_Data/Dates_Data.csv")

    plt.subplot(N,1,3)
    line(date_cases, "New Cases at the start of every month", "day", "cases")
    
    plt.subplot(N,1,4)
    line(date_deaths, "New Deaths at the start of every month", "day", "deaths") 

    plt.subplot(N,1,5)
    line(date_Total_cases, "Total cases Since 1/22/2020", "day", "cases")
    
    plt.subplot(N,1,6)
    line(date_Total_deaths, "Total deaths Since 1/22/2020", "day", "deaths") 

    plt.subplot(N,1,7)
    line(date_New_cases, "New cases Since 1/22/2020", "day", "cases")
    
    plt.subplot(N,1,8)
    line(date_New_Deaths, "New deaths Since 1/22/2020", "day", "deaths") 

    # gender and age graph
    women_cases, women_deaths = unpack_multiple_data("US_Data/Women_Data.csv")
    men_cases, men_deaths = unpack_multiple_data("US_Data/Men_Data.csv")
    plt.subplot(N,1,9)
    state_bar(women_cases, "Total deaths for Women by age", "age", "cases")
    
    plt.subplot(N,1,10)
    state_bar(men_cases, "Total deaths for Men by age", "age", "cases")
    
    plt.subplot(N,1,11)
    state_bar(women_deaths, "Total cases for Women by age", "age", "Deaths")
    
    plt.subplot(N,1,12)
    state_bar(men_deaths, "Total cases for Men by age", "age", "Deaths")

plt.savefig(sys.stdout.buffer)
sys.stdout.flush()

