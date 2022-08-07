# Information bit calculator, this will calculate the # of words eliminated by having each different letter state
# (gray, yellow, and green) in each of the different positions, using this we can then get the percentage of words
# that this removes. Converting this into bits we can then rank every single combination based on its amount of
# information, then by taking the odds of getting different letter states in each position i.e. odds of a gray 'p' in
# position one.

import pandas as pd
from ComparisonFunction import matchScript
from alive_progress import alive_bar

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')

grayList = []
yellowList = []
greenList = []


def functionThing():
    for guessWord in wordList.words:
        for solutionWord in solutionWordList.words:
            if guessWord[4] == 'a':
                matchList = matchScript(guessWord, solutionWord)
                if matchList[4] == 0 and solutionWord not in grayList:
                    grayList.append(solutionWord)
                elif matchList[4] == 1 and solutionWord not in yellowList:
                    yellowList.append(solutionWord)
                elif matchList[4] == 2 and solutionWord not in greenList:
                    greenList.append(solutionWord)
        yield


with alive_bar(len(wordList.words), force_tty=True) as bar:
    for i in functionThing():
        bar()

counter2 = 0
for x in solutionWordList.words:
    if x in grayList and x.count('a') > 1:
        counter2+=1
        print(x)

print(counter2)


# Green contains list of all letters with 'a' in first
# gray contains all except for words with 2 'a's' and 'a' in first
# yellow contains all words that have an 'a' not in the first
print(
    "length of Gray list: {}  length of Yellow list: {}  length of Green list: {}  number of possible Words: {}".format(
        len(grayList), len(yellowList), len(greenList), len(solutionWordList.words)))
