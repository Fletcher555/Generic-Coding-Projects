import pandas as pd
from timeit import default_timer as timer
from finishedUsefullFunctionsV2 import bestWordFinder
from finishedUsefullFunctionsV2 import matchScript

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
words = wordList.words.to_numpy()
averageWordScore = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')

matchList = ([0, 2, 0, 0, 1], [0, 1, 0, 1, 0], [1, 0, 2, 2, 1])
guessLists = ('soare', 'meynt', 'navew',)

start = timer()
solutionWordList = solutionWordList.words

myList = (bestWordFinder(words, solutionWordList, matchList=matchList, guessList=guessLists))
guessLists += ((myList[0][0]),)
solutionWordList = myList[2]
print("Current Guess: {} MatchList: {}".format(guessLists, matchList))
