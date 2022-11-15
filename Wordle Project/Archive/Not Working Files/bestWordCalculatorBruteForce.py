# This is an attempt at brute forcing the best first word by counting the number of words it removes as possible
# solutions, this is not going to work as in order to get a single word of 3000+ to run it takes upwards of 16 minutes
# Note I use the library alive_progress which allows for the creation of the progress bar.

import pandas as pd
from FunctionSupport import matchScript
from alive_progress import alive_bar


wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')

solutionWord = 'guess'
removedWordsList = []


# We start with our solution word, which in this code is 'guess', then we take each of our guess words, and we check
# which ones are still possible. If the word is no longer a possible it adds to a counter which tracks the total removed
# words. This leaves you with a list of guess words with a number for each corresponding to how many words it removes
# from the total possibilities. If you did this for all possible solution words you would get the best starting word on
# average which would be the one that removes the most total words in all possibilities.
def functionThing():
    for word in wordList.words:
        removedWordsCounter = 0
        matches = matchScript(word, solutionWord)
        for y in range(len(solutionWordList.words)):
            for x in range(len(matches)):
                if matches[x] == 0 and word[x] in solutionWordList.words[y]:
                    removedWordsCounter = removedWordsCounter + 1
                elif matches[x] == 1 and word[x] not in solutionWordList.words[y]:
                    removedWordsCounter = removedWordsCounter + 1
                elif matches[x] == 2 and word[x] != solutionWordList.words[y][x]:
                    removedWordsCounter = removedWordsCounter + 1
        removedWordsList.append(removedWordsCounter)
        yield


# Generates the progress bar that displays the progress of the system.
with alive_bar(len(wordList.words), force_tty=True) as bar:
    for i in functionThing():
        bar()
