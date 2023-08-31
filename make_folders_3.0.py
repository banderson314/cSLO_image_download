#!/usr/bin/env python

#Imports
import os

path = "cSLO images"

#Function for individual mice
def individuals():
    print("Type in each mouse number individually. Type 'exit' when you are done.")
    mouseNumber = input("First mouse: ")
    while mouseNumber != "exit" and mouseNumber != "stop":
        checkIfExists = os.path.isdir(os.path.join(path,str(mouseNumber)))
        if checkIfExists == False:
            os.makedirs(os.path.join(path,str(mouseNumber),"OD"))
            os.makedirs(os.path.join(path,str(mouseNumber),"OS"))
        mouseNumber = input("Next mouse: ")


#Function for range of mice
def rangeNumbers():
    #Getting inputs
    start = input("What is the first mouse number? \n")
    print("")
    end = input("What is the last mouse number? \n")
    print("")

    start = int(start)
    end = int(end)

    #Making the folders
    i = start
    while i <= end:
        os.makedirs(os.path.join(path,str(i),"OD"))
        os.makedirs(os.path.join(path,str(i),"OS"))
        print("Creating folder ", i)
        i += 1


#Choosing input method
print("Do you want to create individual[i] folders or a range [r] of folders?")
initialResponse = input("Please type i or r.\n")
if initialResponse == "i":
    individuals()
elif initialResponse == "r":
    rangeNumbers()
else:
    exit()
