import pandas as pd
from FunctionSupport import bestWordFinder

wordList = pd.read_csv(r'wordleWordList.csv')
wordList = wordList.words.to_numpy()
solutionWordList = pd.read_csv(
    r'wordleSolutionList.csv')
solutionWordList = solutionWordList.words

print("\nThis is a bot that solves Wordle, please be patient as it may take some time for the first few guesses. \n\n")


def solver(words, solutionWords):
    matchList = ()
    guessLists = ('soare',)
    myList = [[1], ]
    print(f"Suggested guess is: {guessLists[0]}.")

    while guessLists[-1] != myList[0][-1]:
        guess = input(f"What is the match list for {guessLists[-1]}? Format is 0 = Gray, 1 = Yellow, and 2 = Green. "
                      f"Please format response as '#####'. :")
        guess = [int(x) for x in list(guess)]

        matchList += (guess,)
        myList = (bestWordFinder(words, solutionWords, matchList=matchList, guessList=guessLists))
        guessLists += ((myList[0][0]),)
        solutionWords = myList[2]
        print(f"Suggested guess is: {guessLists[-1]}\n")


# Runs Solver Code
solver(wordList, solutionWordList)
