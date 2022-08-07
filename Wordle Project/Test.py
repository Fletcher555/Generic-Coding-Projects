
import pandas as pd
from ComparisonFunction import matchScript
from alive_progress import alive_bar

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')



guessWord = 'weary'
counter = 0
for solutionWord in solutionWordList.words:
    if solutionWord.count('s') > 1:
        counter = counter + 1

print(counter)