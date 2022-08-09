# Information bit calculator, this will calculate the # of words eliminated by having each different letter state
# (gray, yellow, and green) in each of the different positions, using this we can then get the percentage of words
# that this removes. Converting this into bits we can then rank every single combination based on its amount of
# information, then by taking the odds of getting different letter states in each position i.e. odds of a gray 'p' in
# position one.

import pandas as pd
from finishedUsefullFunctionsV2 import getAllMatchLists
from finishedUsefullFunctionsV2 import isPossibleWord
import math
from alive_progress import alive_bar
import collections

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')


guessWord = 'guess'
possibleMatchLists = getAllMatchLists(guessWord)
wordCountList = []
for possibleMatchList in possibleMatchLists:
    counter = 0
    for solutionWord in wordList.words:
        validWord = isPossibleWord(solutionWord, possibleMatchList, guessWord)
        if validWord:
            counter += 1
    wordCountList.append(counter)

probabilityList = []
for possibleWord in wordCountList:
    probabilityList.append(possibleWord / len(wordList.words))

bits = []
for probability in probabilityList:
    bits.append(math.log((1 / probability), (2)))

averageBits = 0
for y in range(len(probabilityList)):
    averageBits = averageBits + (probabilityList[y] * bits[y])

dataFrame = pd.DataFrame({'Matches': possibleMatchLists,
                          'NumberOfPossibleWords': wordCountList,
                          'PercentageOfWordsPossible': probabilityList,
                          'NumberOfBits': bits})

pd.set_option('expand_frame_repr', False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame.sort_values(by=['NumberOfPossibleWords']))

print(averageBits)

