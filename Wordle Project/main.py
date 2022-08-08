# Notes all ranges are set to 5 or 12972 because that is the length of a 5 letter word and the number of 5 letter words
# in the list i have

import pandas as pd
import math
from alive_progress import alive_bar
import numpy as np
from timeit import default_timer as timer

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
words = wordList.words.to_numpy()
averageBitsList = []


def getAllMatchLists(guessWord):
    possibleMatchLists = tuple()
    for solutionWord in words:
        matches = matchScript(guessWord, solutionWord)
        if list(matches) not in possibleMatchLists:
            possibleMatchLists += (list(matches),)
    return possibleMatchLists


def matchScript(guessWord, solutionWord):
    guessWordLetterCount = {x: 0 for x in guessWord}

    matchList = np.empty(5, dtype=object)
    for x in range(5):
        if guessWord[x] == solutionWord[x]:
            matchList[x] = 2
            guessWordLetterCount[guessWord[x]] += 1

    for x in range(5):
        if matchList[x] != 2 and guessWord[x] in solutionWord and guessWordLetterCount[guessWord[x]] < solutionWord.count(guessWord[x]):
            matchList[x] = 1
            guessWordLetterCount[guessWord[x]] += 1
    matchList = [0 if v is None else v for v in matchList]
    return matchList


def isPossibleWord(testWord, matches, guessWord):
    for x in range(5):
        if matches[x] == 2 and guessWord[x] != testWord[x]:
            return False

        if matches[x] == 1:
            if guessWord[x] == testWord[x] or guessWord[x] not in testWord:
                return False
            else:
                numLetterGreen = 0
                for y in range(5):
                    if (matches[y] == 2 or matches[y] == 1) and guessWord[y] == guessWord[x]:
                        numLetterGreen += 1

                if testWord.count(guessWord[x]) < numLetterGreen:
                    return False

        if matches[x] == 0:
            numLetterGreenYellow = 0
            for y in range(5):
                if (matches[y] == 1 or matches[y] == 2) and guessWord[y] == guessWord[x]:
                    numLetterGreenYellow += 1

            if testWord.count(guessWord[x]) > numLetterGreenYellow:
                return False

    return True



averageBitsList = np.empty([])


def functionThing():
    for guessWord in words:
        possibleMatchLists = getAllMatchLists(guessWord)
        averageBits = 0
        for possibleMatchList in possibleMatchLists:
            counter = 0
            for solutionWord in words:
                # noinspection PyTypeChecker
                validWord = isPossibleWord(solutionWord, possibleMatchList, guessWord)
                if validWord:
                    counter += 1
            averageBits = averageBits + (
                    (counter / 12972) * (math.log((12972 / counter), 2)))
            # Formula for this part above is Sum of ( x / total * log2(total/x)
        print("Current guessWord: {}  Average Bits word provides: {}".format(guessWord, averageBits))
        np.append(averageBitsList, averageBits)
        yield


with alive_bar(12972, force_tty=True) as bar:
    for i in functionThing():
        bar()




dataFrame = pd.DataFrame({'WordList': words,
                          'AverageBitsFromWord': averageBitsList})

# Writes that dataframe to a CSV file for later use
dataFrame.to_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')

pd.set_option('expand_frame_repr', False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame.sort_values(by=['NumberOfPossibleWords']))

