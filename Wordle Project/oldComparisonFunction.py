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


def isPossible(testWord, matches, guessWord):
    testWordLetterCount = {}
    for letter in testWord:
        testWordLetterCount[letter] = 0

    for x in range(len(testWord)):
        if matches[x] == 2:
            if guessWord[x] != testWord[x]:
                return False

        if matches[x] == 1:
            if guessWord[x] == testWord[x]:
                return False
            elif guessWord[x] not in testWord:
                return False
            else:
                numLetterGreen = 0
                letter = guessWord[x]
                for y in range(len(matches)):
                    if matches[y] == 2 or matches[y] == 1:
                        if guessWord[y] == letter:
                            numLetterGreen += 1
                if testWord.count(guessWord[x]) < numLetterGreen:
                    return False

        if matches[x] == 0:
            numLetterGreenYellow = 0
            letter = guessWord[x]
            for y in range(len(matches)):
                if matches[y] == 1 or matches[y] == 2:
                    if guessWord[y] == letter:
                         numLetterGreenYellow += 1

            if testWord.count(guessWord[x]) > numLetterGreenYellow:
                return False

    return True


