# Information bit calculator, this will calculate the # of words eliminated by having each different letter state
# (gray, yellow, and green) in each of the different positions, using this we can then get the percentage of words
# that this removes. Converting this into bits we can then rank every single combination based on its amount of
# information, then by taking the odds of getting different letter states in each position i.e. odds of a gray 'p' in
# position one.
#
#
# After writing the code to do the above it will take aproximately 6 hours to run so in the meantime I am going to
# try to learn how to get this work with multithreading.

import pandas as pd
import math
from alive_progress import alive_bar
import numpy as np

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
averageBitsList = []


# These vars contain the list of all the words that are checked, this list is approximately 13000 words long.
# The empty list declaration allows for the

# This function finds all possible matchLists possible for the guessWord, it does this by iterating through the entire
# wordlist and finding all unique matchLists.
def getAllMatchLists(guessWord):
    possibleMatchLists = []
    counter = 0
    for solutionWord in wordList.words:
        matches = matchScript(guessWord, solutionWord)
        if list(matches) not in possibleMatchLists:
            possibleMatchLists.append(matches.tolist())
            counter += 1
    return possibleMatchLists


# Same Match Script as before, takes a guessWord and solutionWord and outputs what their color combination would be
# according to Wordle's color rules.
def matchScript(guessWord, solutionWord):
    guessWordLetterCount = {}
    for letter in guessWord:
        guessWordLetterCount[letter] = 0

    matchList = np.empty(5, dtype=object)
    for x in range(len(guessWord)):
        if guessWord[x] == solutionWord[x]:
            matchList[x] = 2
            guessWordLetterCount[guessWord[x]] += 1

    for x in range(len(guessWord)):
        if matchList[x] != 2:
            if guessWord[x] in solutionWord:
                if guessWordLetterCount[guessWord[x]] < solutionWord.count(guessWord[x]):
                    matchList[x] = 1
                    guessWordLetterCount[guessWord[x]] += 1
    for x in range(len(guessWord)):
        if matchList[x] != 2 and matchList[x] != 1:
            matchList[x] = 0
    return matchList


# This takes a guessWord a testWord and a matchList, it checks to see if with the matchList whether the testWord would
# be a possible word with that matchList
def isPossibleWord(testWord, matches, guessWord):
    testWordLetterCount = {}
    for letter in testWord:
        testWordLetterCount[letter] = 0

    for x in range(len(testWord)):
        if matches[x] == 2:
            if guessWord[x] != testWord[x]:
                return False

        if matches[x] == 1:
            if guessWord[x] == testWord[x]:
                return False
            elif guessWord[x] not in testWord:
                return False
            else:
                numLetterGreen = 0
                letter = guessWord[x]
                for y in range(len(matches)):
                    if matches[y] == 2 or matches[y] == 1:
                        if guessWord[y] == letter:
                            numLetterGreen += 1
                if testWord.count(guessWord[x]) < numLetterGreen:
                    return False

        if matches[x] == 0:
            numLetterGreenYellow = 0
            letter = guessWord[x]
            for y in range(len(matches)):
                if matches[y] == 1 or matches[y] == 2:
                    if guessWord[y] == letter:
                        numLetterGreenYellow += 1

            if testWord.count(guessWord[x]) > numLetterGreenYellow:
                return False

    return True


# The way this works it tally's up the words that are still possible with each of the possible matchLists to get an
# average amount of information provided by the word, taking this we can rank the words based on how many other words
# they cut out.
def functionThing():
    for guessWord in wordList.words:
        possibleMatchLists = getAllMatchLists(guessWord)
        averageBits = 0
        for possibleMatchList in possibleMatchLists:
            counter = 0
            for solutionWord in wordList.words:
                # noinspection PyTypeChecker
                validWord = isPossibleWord(solutionWord, possibleMatchList, guessWord)
                if validWord:
                    counter += 1
            averageBits = averageBits + (
                        (counter / len(wordList.words)) * (math.log((len(wordList.words) / counter), 2)))
            # Formula for this part above is Sum of ( x / total * log2(total/x)
        averageBitsList.append(averageBits)
        print("Current GuessWord: {} Average number of Bits: {}".format(guessWord, averageBits))
        yield


# Generates the progress bar to keep track of the 6h long program.
with alive_bar(len(wordList.words), force_tty=True) as bar:
    for i in functionThing():
        bar()

# Creates a dataframe with a column of words and the corresponding number of bits of information they remove on average.
dataFrame = pd.DataFrame({'WordList': wordList.words,
                          'AverageBitsFromWord': averageBitsList})

# Writes that dataframe to a CSV file for later use
dataFrame.to_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')

pd.set_option('expand_frame_repr', False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame.sort_values(by=['NumberOfPossibleWords']))
