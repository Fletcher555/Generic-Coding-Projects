
import pandas as pd
from ComparisonFunction import matchScript
from alive_progress import alive_bar

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')


counter = 0
list1 = []
def functionThing():
    global counter
    for guessWord in wordList.words:
        for solutionWord in solutionWordList.words:
            matches = matchScript(guessWord, solutionWord)
            if str(matches) not in list1:
                list1.append(str(matches))
        counter = counter + len(list1)
        yield


with alive_bar(len(wordList.words), force_tty=True) as bar:
    for i in functionThing():
        bar()

print(round(counter / len(wordList.words), 2))