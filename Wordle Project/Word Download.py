# Wordle project for science fair. Medium competitiveness
import english_words as word
import numpy as np
import pandas as pd
alphabetArray = "abcdefghijklmnopqrstuvwxyz"
print(alphabetArray)
wordCSV = pd.DataFrame(columns=np.array(['words']))
wordCSV.to_csv(r'C:\Users\Milo\Documents\PythonPandasFiles\word.csv')

y = 0
err = None
for currentWord in word.english_words_lower_alpha_set:
    if len(currentWord) == 5:
        for letterOfWord in currentWord:
            err = True
            done = False
            for letter in alphabetArray:
                if letterOfWord == letter:
                    done = True
                    break
            if done == False:
                err = False
                break
        if err != False:
            y = y + 1
            print(currentWord)
            wordCSV.loc[y] = np.array(currentWord)
            wordCSV.to_csv(r'C:\Users\Milo\Documents\PythonPandasFiles\word.csv')
print(y)