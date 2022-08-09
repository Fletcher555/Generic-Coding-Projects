# This is just a list of individual functions that I can call from other files if needed.

import numpy as np
import math


# must input a list of all solution words to find lists against
def getAllMatchLists(guessWord, solutionWords):
    possibleMatchLists = tuple()
    for solutionWord in solutionWords:
        matches = matchScript(guessWord, solutionWord)
        if list(matches) not in possibleMatchLists:
            possibleMatchLists += (list(matches),)
    return possibleMatchLists


# Same Match Script as before, takes a guessWord and solutionWord and outputs what their color combination would be
# according to Wordle's color rules.
def matchScript(guessWord, solutionWord):
    guessWordLetterCount = {x: 0 for x in guessWord}

    matchList = np.empty(5, dtype=object)
    for x in range(5):
        if guessWord[x] == solutionWord[x]:
            matchList[x] = 2
            guessWordLetterCount[guessWord[x]] += 1

    for x in range(5):
        if matchList[x] != 2 and guessWord[x] in solutionWord and \
                guessWordLetterCount[guessWord[x]] < solutionWord.count(guessWord[x]):
            matchList[x] = 1
            guessWordLetterCount[guessWord[x]] += 1
    matchList = [0 if v is None else v for v in matchList]
    return matchList


# This takes a guessWord a testWord and a matchList, it checks to see if with the matchList whether the testWord would
# be a possible word with that matchList
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
            if guessWord[x] == testWord[x]:
                return False
            if testWord.count(guessWord[x]) != 0:
                numLetterGreenYellow = 0
                for y in range(5):
                    if (matches[y] == 1 or matches[y] == 2) and guessWord[y] == guessWord[x]:
                        numLetterGreenYellow += 1
                if testWord.count(guessWord[x]) > numLetterGreenYellow:
                    return False
    return True  # Only occurs if none of the false checks trigger.


# This tallies up the words that are still possible with each of the possible matchLists to get an average amount of
# information provided by the word, taking this we can rank the words based on how many other words they cut out.
# Needs a list of the words that you want to test as well as a list of all solution words
def functionThing(words, solutionWords):
    averageBitsList = []
    for guessWord in words:
        possibleMatchLists = getAllMatchLists(guessWord, solutionWords)
        averageBits = 0
        for possibleMatchList in possibleMatchLists:
            counter = 0
            for solutionWord in solutionWords:
                # noinspection PyTypeChecker
                validWord = isPossibleWord(solutionWord, possibleMatchList, guessWord)
                if validWord:
                    counter += 1
            averageBits = averageBits + (
                    (counter / len(solutionWords)) * (math.log((len(solutionWords) / counter), 2)))
            # Formula for this part above is Sum of ( x / total * log2(total/x)
        print("Current guessWord: {}  Average Bits word provides: {}".format(guessWord, averageBits))
        averageBitsList.append(averageBits)
