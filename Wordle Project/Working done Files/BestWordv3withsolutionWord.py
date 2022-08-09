# Information bit calculator, this will calculate the # of words eliminated by having each different letter state
# (gray, yellow, and green) in each of the different positions, using this we can then get the percentage of words
# that this removes. Converting this into bits we can then rank every single combination based on its amount of
# information, then by taking the odds of getting different letter states in each position i.e. odds of a gray 'p' in
# position one.
#
#
# After writing the code to do the above it will take aproximately 6 hours to run so in the meantime I am going to
# try to learn how to get this work with multithreading. 0.4 operations per second
#
# This is currently v2 which does the same process nearly twice as fast due to a bunch of optimizations. 0.8 operations
# per second.
#
# This is now v3 which fixed a major bug with the isPossible function that caused words with 2 of the same letters
# to overestimate the number of possible words. This version now also only checks against the solution words instead
# of all words as it nearly 10x's the speed. I also fixed an issue with the dataframes that prevented data from being
# written to the CSV file. 7.8 operations per second.

import pandas as pd
import math
from alive_progress import alive_bar
import numpy as np

# These vars contain the list of all the words that are checked, this list is approximately 13000 words long. The list
# of the solution words contains roughly 3000 words which are the possible solutions, the solutions are all contained
# in the overall word list.
wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')
solutionWords = solutionWordList.words.to_numpy()
words = wordList.words.to_numpy()


# This function finds all possible matchLists possible for the guessWord, it does this by iterating through the entire
# wordlist and finding all unique matchLists.
def getAllMatchLists(guessWord):
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
averageBitsList = []


def functionThing():
    for guessWord in words:
        possibleMatchLists = getAllMatchLists(guessWord)
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
        yield


# Generates the progress bar.
with alive_bar(12972, force_tty=True) as bar:
    for i in functionThing():
        bar()

# Writes that dataframe to a CSV file for later use
dataFrame = pd.DataFrame({'WordList': words, 'AverageBitsFromWord': averageBitsList})
dataFrame.to_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')
pd.set_option('expand_frame_repr', False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame.sort_values(by=['AverageBitsFromWord']))
