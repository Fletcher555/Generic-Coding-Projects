import pandas as pd
import random as rd
import numpy as np
from Comparison File import matchScript
from ComparisonFunction import isPossible




def solutionPicker(wordList):
    return str(wordList[0])


def guessWordPicker(guessList):
    randInt = rd.randint(0, (len(guessList)-1))
    return guessList[randInt]


def removeWords(guessList, matches, guessWord):
    indexToRemove = []
    for x in range(len(guessList)):
        testWord = guessList[x]
        if not isPossible(testWord, matches, guessWord):
            indexToRemove.append(guessList[x])



    for y in indexToRemove:
        guessList.remove(y)

    return guessList








def run():
    wordList = pd.read_csv(r'C:\Users\Milo\Documents\PythonPandasFiles\word.csv')
    for x in
    solutionWord = solutionPicker(wordList=wordList.words)
    print("Solution Word is: " + solutionWord)
    guessList = list(wordList.words)
    done = False
    while not done:
        guessWord = guessWordPicker(guessList=guessList)
        print(guessWord)
        matches = matchScript(guessWord=guessWord, solutionWord=solutionWord)
        print(matches)
        counter = 0
        for element in matches:
            if element == 2:
                counter += 1
        if counter == 5:
            print("The Solution Word is: " + guessWord)
            done = True
        guessList = removeWords(guessList=guessList, matches=matches, guessWord=guessWord)





run()