match = False
if guessWord[x] in solutionWord:

    else:
    if solutionWord.count(guessWord[x]) < guessWord[x:5].count(guessWord[x]) and guessWord[x] not in solutionWord[0:x - 1]:
        matchList[x] = 1
        done = True
        match = True
    if done == False:
        if solutionWord.count(guessWord[x]) >= guessWord[x:5].count(guessWord[x]):
            matchList[x] = 1
            match = True

    if match == False:
        matchList[x] = 0
else:
    matchList[x] = 0