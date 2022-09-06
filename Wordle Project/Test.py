# This file technically could calculate the average score that the current gen bestWordFinder provides however the speed
# is much too slow, currently after leaving the program running for over two hours I was only able to calculate 50
# different games of the needed 2000. Many changes must be made to the algorithms used to speed up the computations
# This file technically could calculate the average score that the current gen bestWordFinder provides however the speed
# is much too slow, currently after leaving the program running for over two hours I was only able to calculate 50
# different games of the needed 2000. Many changes must be made to the algorithms used to speed up the computations
# current focus is developing an algorithm that can handle the speeds im looking for, as well as optimizing the code
# hopefully in doing this I will also fix the computational problems with the updated wordle clone where the hint
# calculator which is based off of this calculator takes way to long leaving the game frozen for multiple minutes.
# Current ideas are an SQL database storing the certain calculated patterns and the best word for those.
#
# Note as well that this skips the worst of the computation issues by assuming that 'soare' was the first word.
# Interestingly for those first 50 words the average score was 3.86

import pandas as pd
from timeit import default_timer as timer
from finishedUsefullFunctionsV2 import bestWordFinder
from finishedUsefullFunctionsV2 import matchScript

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

