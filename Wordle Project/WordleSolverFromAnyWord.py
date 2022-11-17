# This file can solve Wordle from any word by manipulating the match list and guess list, this was never implemented
# Properly

import pandas as pd
from FunctionSupport import bestWordFinder

wordList = pd.read_csv(r'wordleWordList.csv')
words = wordList.words.to_numpy()
solutionWordList = pd.read_csv(
    r'wordleSolutionList.csv')

matchList = ([0, 0, 0, 0, 1], [0, 2, 1, 0, 0], [0, 1, 0, 2, 2])
guessLists = ('soare', 'denet', 'abrin',)

solutionWordList = solutionWordList.words

myList = (bestWordFinder(words, solutionWordList, matchList=matchList, guessList=guessLists))
guessLists += ((myList[0][0]),)
solutionWordList = myList[2]
print("Current Guess: {} MatchList: {}".format(guessLists, matchList))
