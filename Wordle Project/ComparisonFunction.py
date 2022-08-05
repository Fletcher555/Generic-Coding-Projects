import numpy as np

def matchScript(guessWord, solutionWord):
    guessWordLetterCount = {}
    for letter in guessWord:
        guessWordLetterCount[letter] = 0

    matchList = np.empty(5, dtype=object)
    for x in range(len(guessWord)):
        if guessWord[x] == solutionWord[x]:
            matchList[x] = 2
            guessWordLetterCount[guessWord[x]] += 1

    for x in range(len(guessWord)):
        if matchList[x] != 2:
            if guessWord[x] in solutionWord:
                if guessWordLetterCount[guessWord[x]] < solutionWord.count(guessWord[x]):
                    matchList[x] = 1
                    guessWordLetterCount[guessWord[x]] += 1
    for x in range(len(guessWord)):
        if matchList[x] != 2 and matchList[x] != 1:
            matchList[x] = 0
    return matchList