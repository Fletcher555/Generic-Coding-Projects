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
from alive_progress import alive_bar
from FunctionSupport import bestWordFinder
from FunctionSupport import matchScript

solutionWordList = pd.read_csv(
    r'wordleSolutionList.csv')

scoreList = []


def myFunction():
    for solutionWord in solutionWordList.words:
        # Since we want to check the average score of all games we
        # iterate through all possible solution words.
        matchList = tuple()
        guessLists = ('soare',)
        # tuple type variables are used to create tuples filled with lists, this makes processing slightly faster.
        while 1:
            matchList += (matchScript(guessLists[-1], solutionWord),)
            if set(matchList[-1]) == {2, 2, 2, 2, 2}:
                print("The word was: {} number of guesses: {}".format(guessLists[-1], len(guessLists)))
                scoreList.append(len(guessLists))
                break
            guessLists += (bestWordFinder(matchList, guessLists)[0][0],)
            # This while loop repeats until the solution word has been solved, then it breaks and adds it to a list of
            # and prints the word and the number of guesses that word took.
        print(scoreList)
        yield


# Generates the progress bar using the yield inside the for loop
with alive_bar(len(solutionWordList.words), force_tty=True) as bar:
    for i in myFunction():
        bar()

# Prints the scores as well as the average score, not sure if this works because the function never completed.
print("1's: {} 2's: {} 3's: {} 4's: {} 5's: {} 6's: {} 7's: {} 8's: {} Average Score: {}".format(scoreList.count(1),
                                                                                                 scoreList.count(2),
                                                                                                 scoreList.count(3),
                                                                                                 scoreList.count(4),
                                                                                                 scoreList.count(5),
                                                                                                 scoreList.count(6),
                                                                                                 scoreList.count(7),
                                                                                                 scoreList.count(8),
                                                                                                 (sum(scoreList) / len(
                                                                                                     scoreList)), ))
