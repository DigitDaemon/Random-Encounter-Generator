import sys
import csv
import random
from array import *


def openTable(url=""):  # opens the specified csv file and provide the contents to the application

    table = [[]]
    columns = ""

    # check to see if a url is passed in
    if (url == ""):
        url = input("Enter file url: ")

    try:  # make sur ethe file path is valid
        with open(url, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')

            num = 0
            for row in filereader:
                # print(', '.join(row))
                table.insert(num, [row[0], row[1], row[2], 0])
                num = num + 1

            # save the names of the columns for saving the table
            columns = table[0]

            # remove the first row which contains the value name for each colomn
            del table[0]

            # remove the last row because it contains the end of file for the csv and will break the program otherwise.
            del table[len(table)-1]
            table = fixWeighting(table)

        return (url, table, columns)
    except:  # if the file path is invalid, recursiveally attempt to get the correct path
        print("provided url is invalid, please enter a valid url")
        return openTable()


def printTable(table):  # Print the encounter table
    print("\nThe current table is:\n")
    for row in table:  # iterate through each row and print the contents, not complicated
        print(str(row[0]) + ', ' + row[1] + ', ' + row[2] + ', ' + str(row[3]))


# Fix the weight values on the table so it becomes a range of rollable values.
def fixWeighting(table):
    table[0][3] = int(table[0][0])
    for i in range(1, len(table)):  # For each row, we sum the total weight of the last row and the individual weight of the current row to get the range limit for rolling the table
        table[i][3] = int(table[i][0]) + table[i-1][3]

    return table


def rollEncounter(table):  # decides which encounter will be selected from the table
    # this is the maximum of the tables range so we use that to limit the roll
    high = table[len(table)-1][3]
    roll = random.randrange(high)
    selection = 0

    for row in table:  # now we iterate through the encounter table until we find an encounter that's maximum range is greater then the roll, that is our encounter.
        if(row[3] >= roll):
            break
        else:
            selection = selection + 1

    print("With a roll of " + str(roll) + ": the encounter is " +
          table[selection][1] + ".\n" + table[selection][2])
    return selection  # just to make is possible to save the previous roll or create a roll history later, not used right now


def addEncounter(url, table, column):  # adds an encounter to the table
    name = input("What is the name of the encounter? ")
    description = input("Please describe the encounter: ")

    control = True

    while(control):  # we want to make sure that the user inputs a valid int for the weight
        try:
            weight = input("What is the weighting of the encounter? ")
            if (int(weight) > 0):
                control = False
            else:
                print("Please enter a value greater than 0.\n")
        except:
            print("invalid integer input\n")

    table.insert(len(table), [weight, name, description, 0])
    table = fixWeighting(table)

    saveTable(url, table, column)

    return table


def removeEncounter(url, table, column):  # removes an encounter from the table

    printTable(table)

    name = input(
        "\nEnter the name of the enocunter you would liek to remove: ")
    removed = False

    for i in range(len(table)):
        if (name.lower() == table[i][1].lower()):
            del table[i]
            print("Encounter removed")
            removed = True
            break

    if(removed):
        saveTable(url, table, column)
        fixWeighting(table)
    else:
        print("No encounter with that name was found")

    return table


def printOptions():  # prints the options for the user input menu
    print("\nEnter \"roll\" to roll an encounter\nEnter \"add\" to add an encounter to the table.\nEnter \"remove\" to remove an encounter\nEnter \"change\" to change to a new encounter table\nEnter \"exit\" to exit the application\n")


# this will save changes to the .csv file when the table is updated in the app
def saveTable(url, table, column):

    with open(url, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        filewriter.writerow(column[0] + "," + column[1] + "," + column[2])

        for row in table:
            filewriter.writerow([row[0], row[1], row[2]])

    print("Changes saved")


filepath = ""
encounterTable = [[]]
column = []

print("Welcome to the Random encounter generator")

if len(sys.argv) > 1:  # check to see if a url was passed into the app at start up
    filepath = sys.argv[1]
    filepath, encounterTable, column = openTable(filepath)
else:
    filepath, encounterTable, column = openTable()

# control the primary appliation loop
mainLoop = True
printTable(encounterTable)
printOptions()

# The main application loop
while (mainLoop):

    choice = input("\nEnter your choice: ")
    choice = choice.lower()

    if (choice == "roll"):
        rollEncounter(encounterTable)
    elif (choice == "add"):
        encounterTable = addEncounter(filepath, encounterTable, column)
        printTable(encounterTable)
    elif (choice == "remove"):
        encounterTable = removeEncounter(filepath, encounterTable, column)
        printTable(encounterTable)
    elif (choice == "change"):
        filepath, encounterTable, column = openTable()
        printTable(encounterTable)
    elif (choice == "exit"):
        mainLoop = False
    else:
        printOptions()
