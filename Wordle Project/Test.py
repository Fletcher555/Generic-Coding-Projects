# Current attempt at speeding up the BestWordFinder code by optimizing data structures.
# One function at a time I will try to optimize the speed at which it runs by optimizing the data structure.

import pandas as pd
import math
from alive_progress import alive_bar
from timeit import default_timer as timer
import numpy as np
import itertools

wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
averageBitsList = []

import pandas as pd
import math
from alive_progress import alive_bar
import numpy as np
import itertools

words = [0, 1, 2]
averageBitsList = [0, 2, 2]

dataFrame = pd.DataFrame({'WordList': words,
                          'AverageBitsFromWord': averageBitsList})

# Writes that dataframe to a CSV file for later use


# Writes that dataframe to a CSV file for later use
dataFrame.to_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\averageWordScores.csv')

pd.set_option('expand_frame_repr', False)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(dataFrame.sort_values(by=['AverageBitsFromWord']))
