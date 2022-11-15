# This file technically could calculate the average score that the current gen bestWordFinder provides however the speed
# is much too slow, currently after leaving the program running for over two hours I was only able to calculate 50
# different games of the needed 2000. Many changes must be made to the algorithms used to speed up the computations


import pandas as pd
from timeit import default_timer as timer
from FunctionSupport import bestWordFinder
from FunctionSupport import matchScript

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
words = wordList.words.to_numpy()
averageWordScore = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')



matchList = tuple()
guessLists = ('soare',)


start = timer()
solutionWordList = solutionWordList.words
while matchList == tuple() or set(matchList[-1]) != {2, 2, 2, 2, 2}:
    matchList += (matchScript(guessLists[-1], solutionWord),)
    print(matchList[0])
    myList = (bestWordFinder(words, solutionWordList, matchList=matchList, guessList=guessLists))
    guessLists += ((myList[0][0]),)
    solutionWordList = myList[2]
    print("Current Guess: {} MatchList: {}".format(guessLists, matchList))

print("The word was: {} number of guesses: {}".format(guessLists[-2], len(guessLists) - 1))

end = timer()
print(end - start)

