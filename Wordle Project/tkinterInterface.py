import tkinter as tk
from tkinter import *
import pandas as pd
import random
from ComparisonFunction import matchScript
import math

#TempVars
currentGuess = 0 #row
guessList = []
matchList = []



root = tk.Tk()
root.title("Wordle Game")
root.configure(background='Black')
root.geometry('500x500')
canvas = tk.Canvas(root, width=500, height=500, borderwidth=0, highlightthickness=0)


wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(r'C:\Users\fletc\Downloads\valid_solutions.csv')
solutionWord = solutionWordList.words[random.randint(0, len(solutionWordList.words))]
#Just some variables to be manipulated if dimensions change
cellWidth = 60
cellHeight = 60
rows = 6
columns = 5
cellBorderSize = 5
edgeColor = '#FFFFFF'
green = '#6aaa64'
yellow = '#c9b458'
gray = '#787c7e'


canvas.create_rectangle(300, 0, 500, 500, fill="#E1E1E1", outline="#E1E1E1")
canvas.create_text(400, 50, text="Solution Word:", fill='black', font='Helvetica 15')
canvas.create_text(400, 150, text="Average Score:", fill='black', font='Helvetica 15')
canvas.create_rectangle(0, 360, 500, 500, fill="#E1E1E1", outline="#E1E1E1")



#finds the average score from a csv
def averageScoreFinder():
    scoreList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\AverageScore.csv')
    print(scoreList)
    scoreTotal = 0
    for x in scoreList:
        scoreTotal = scoreTotal + float(x)
    averageScore = scoreTotal / len(scoreList.columns)
    canvas.create_text(400, 175, text=str(averageScore), fill='black', font='Helvetica 12 bold')







#Temp function that displays the cursor postion to make placing the boxes easier
def callback(e):
   x= e.x
   y= e.y
   print("Pointer is currently at %d, %d" %(x,y))
#root.bind('<Motion>',callback)


#Draws the Squares
def drawSquares(guessList = [], matches = []):
    for i in range(len(guessList)):
        for j in range(5):
            x1 = j * cellWidth
            y1 = i * cellHeight
            x2 = x1 + cellWidth
            y2 = y1 + cellHeight
            if matches[(i*5)+j] == 0:
                color = gray
            elif matches[(i*5)+j] == 1:
                color = yellow
            else:
                color = green
            canvas.create_rectangle(x1,y1,x2,y2, fill=color, tags="rect", outline='black',)
            canvas.create_text(((x1 + 30),(y1 + 30)), text=guessList[i][j], font='Helvetica 12 bold')
    for i in range(6 - len(guessList)):
        for j in range(5):
            x1 = (j) * cellWidth
            y1 = (i + len(guessList)) * cellHeight
            x2 = x1 + cellWidth
            y2 = y1 + cellHeight
            canvas.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect", outline='white')

drawSquares()

#This reacts with the button that hides and reveals the solution
buttonState = True
def buttonPress(solutionWord):
    global buttonState
    if not buttonState:
        canvas.create_rectangle(390, 70, 460, 90, fill='#E1E1E1', outline='black')
        canvas.create_text(425, 80, text=solutionWord.upper(), fill=green, font='Helvetica 12 bold')
        solutionButton.config(text='Hide:')
        buttonState = True
    else:
        canvas.create_rectangle(390, 70, 460, 90, fill='#737373', outline='black')
        solutionButton.config(text='Reveal:')
        buttonState = False

guessBox = tk.Entry(root, width=10, font='Helvetica 20 bold')
canvas.create_window(210, 430, window=guessBox)

def playAgain(guessList):
    with open(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\AverageScore.csv', 'a') as fd:
        fd.write(',' + str(len(guessList)))
    guessList = []
    solutionWord = solutionWordList.words[random.randint(0, len(solutionWordList.words))]
    matchList = []
    drawSquares()
    buttonState()



def wordGuesser():
    guessWord = guessBox.get().lower()
    for x in wordList.words:
        if guessWord == x:
            if len(guessList) <=5:
                guessList.append(guessWord)
                var = 0
                break
    else:
        var = 1
    if var != 1:
        matches = matchScript(guessWord, solutionWord)
        if set(matches) == set([2,2,2,2,2]):
            endButton = Button(canvas, text='Congrats! Click to Play Again.', command=lambda: [playAgain(guessList), endButton.pack_forget()], font='Helvetica 20 bold', fg='black', highlightcolor='black', highlightthickness=0, bg='Red')
            endButton.pack()
            endButton.place(x=250, y=250)
        for x in matches:
            matchList.append(x)
        print("matches: {}  MatchList: {}".format(matches, matchList))
        drawSquares(guessList, matchList)


guessButton = tk.Button(canvas, text='Guess:', command=lambda: wordGuesser(), font='Helvetica 20 bold', fg='black', highlightcolor='black', highlightthickness=0)
guessButton.place(x=10, y=405)

wordGuesser()
solutionButton = Button(canvas, text='Reveal:', command= lambda: buttonPress(solutionWord), font='Helvetica 12 bold', fg='black', highlightcolor='black', highlightthickness=0)
buttonPress(solutionWord)
solutionButton.place(x=310, y=65)
averageScoreFinder()



canvas.pack(side="top", fill="both", expand="true")
root.mainloop()





