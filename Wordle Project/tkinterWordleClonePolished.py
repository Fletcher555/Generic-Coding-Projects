# When ran this program creates a clone of the game Wordle, it is the base so that when Programming I can create visual
# demonstrations of my future solvers.
# Author: Fletcher Dares
# Email: fletcher.dares@gmail.com

import tkinter as tk
from tkinter import *
import pandas as pd
import numpy as np
import random

# These vars are used later and just need to be declared as empty global lists.
guessList = []
matchList = []

# Initializes the tkinter tab with a canvas.
root = tk.Tk()
root.title("Wordle Game")
root.configure(background='Black')
root.geometry('500x500')
canvas = tk.Canvas(root, width=500, height=500, borderwidth=0, highlightthickness=0)

# These pull lists of words that I have stored in the accompanying CSV's also selects the solution word.
wordList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleWordList.csv')
solutionWordList = pd.read_csv(
    r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\wordleSolutionList.csv')
solutionWord = solutionWordList.words[random.randint(0, len(solutionWordList.words))]

# Just defines some colors, these are the official colors Wordle uses
green = '#6aaa64'
yellow = '#c9b458'
gray = '#787c7e'


# Quick Function that finds the average Score from the csv
def averageScoreFinder():
    scoreList = pd.read_csv(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\AverageScore.csv')
    scoreTotal = 0
    for x in scoreList:
        scoreTotal = scoreTotal + float(x).__floor__()

    averageScore = round((scoreTotal / len(scoreList.columns)), 2)
    canvas.itemconfig(averageScoreText, text=averageScore)


# This function is responsible for creating the squares in the grid, the way these are created depends on older guesses
# as well as the match list.
def drawSquares(guesses=None, matches=None):
    # This part draws the squares that are used by the current guessed words.
    if guesses is None:
        guesses = []
    if matches is None:
        matches = []
    for i in range(len(guesses)):
        for j in range(5):
            x1 = j * 60
            y1 = i * 60
            x2 = x1 + 60
            y2 = y1 + 60
            if matches[(i * 5) + j] == 0:
                color = gray
            elif matches[(i * 5) + j] == 1:
                color = yellow
            else:
                color = green
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="rect", outline='black', )
            canvas.create_text(((x1 + 30), (y1 + 30)), text=guesses[i][j], font='Helvetica 12 bold')

    # Second part draws the black squares.
    for i in range(6 - len(guesses)):
        for j in range(5):
            x1 = j * 60
            y1 = (i + len(guesses)) * 60
            x2 = x1 + 60
            y2 = y1 + 60
            canvas.create_rectangle(x1, y1, x2, y2, fill="black", tags="rect", outline='white')


# This sets the state of the solution button to a default hidden
buttonState = True


# This function reveals the solution and hides it behind a canvas
def buttonPress(hiddenWord):
    global buttonState
    if not buttonState:
        canvas.create_rectangle(390, 70, 460, 90, fill='#E1E1E1', outline='black')
        canvas.create_text(425, 80, text=hiddenWord.upper(), fill=green, font='Helvetica 12 bold')
        solutionButton.config(text='Hide:')
        buttonState = True
    else:
        canvas.create_rectangle(390, 70, 460, 90, fill='#737373', outline='black')
        solutionButton.config(text='Reveal:')
        buttonState = False


# This makes it so that we can control whether the game is over
gameOver = False


# This function resets the variables and sets up the game to be played again by picking a new solution word and storing
# that games score in a file
def playAgain():
    global guessList
    with open(r'C:\Users\fletc\Documents\GitHub\Generic-Coding-Projects\Wordle Project\AverageScore.csv', 'a') as fd:
        fd.write(r',' + str(len(guessList)))
    guessList = []
    # Picking new solution word.
    global solutionWord
    solutionWord = solutionWordList.words[random.randint(0, len(solutionWordList.words))]
    # Resets all vars to be played again.
    global matchList
    matchList = []
    drawSquares()
    buttonPress(solutionWord)
    global gameOver
    gameOver = False


# This is the function that returns the match lists.
def matchScript(guessWord, Solution):
    guessWordLetterCount = {}
    # Creates a dict with each letter in the guessWord.
    for letter in guessWord:
        guessWordLetterCount[letter] = 0
    matches = np.empty(5, dtype=object)

    # First we do the easy part of finding the green letters.
    for x in range(len(guessWord)):
        if guessWord[x] == Solution[x]:
            matches[x] = 2
            guessWordLetterCount[guessWord[x]] += 1

    # Uses the dict that was created earlier to solve the yellows.
    for x in range(len(guessWord)):
        if matches[x] != 2:
            if guessWord[x] in Solution:
                if guessWordLetterCount[guessWord[x]] < Solution.count(guessWord[x]):
                    matches[x] = 1
                    guessWordLetterCount[guessWord[x]] += 1
    # Sets all the not already set to gray.
    for x in range(len(guessWord)):
        if matches[x] != 2 and matches[x] != 1:
            matches[x] = 0
    return matches


# This is what takes the word from the selection box, runs checks and passes it to the file that checks the matches.
def wordGuesser():
    # Makes sure that we cannot continue to input new words if the game is currently in the 'play again' state.
    global gameOver
    if not gameOver:

        # the only checks that we need to make are whether it is included in the list of possible guesses.
        guessWord = guessBox.get().lower()
        for x in wordList.words:
            if guessWord == x:
                guessList.append(guessWord)
                var = False
                break

        # Runs this if the loop was not broken i.e. the word was not a valid submission
        else:
            var = True
            guessButton.config(background='red')
            print("h")
            guessButton.after(500, lambda: guessButton.config(background='white'))

        # If the loop was broken the checker code runs.
        if not var:
            # Runs the checker to check the matches
            matches = matchScript(guessWord, solutionWord)

            # This runs if we have won / lost.
            if set(matches) == {2, 2, 2, 2, 2} or len(guessList) == 6:
                endButton = Button(canvas, text='Click to Play Again.', command=lambda: [playAgain(), endButton.destroy(
                ), averageScoreFinder()], font='Helvetica 20 bold', fg='black', highlightcolor='black',
                                   highlightthickness=0, bg='Red')

                endButton.pack()
                gameOver = True
                endButton.place(x=50, y=250)

            # This reformats the way that we write the list before sending it to redraw the grid of squares
            for x in matches:
                matchList.append(x)
            print("matches: {}  MatchList: {}".format(matches, matchList))
            drawSquares(guessList, matchList)


# This is where the initial defining of the all Canvas objects must happen.
canvas.create_rectangle(300, 0, 500, 500, fill="#E1E1E1", outline="#E1E1E1")
canvas.create_text(400, 50, text="Solution Word:", fill='black', font='Helvetica 15')
canvas.create_text(400, 150, text="Average Score:", fill='black', font='Helvetica 15')
canvas.create_rectangle(0, 360, 500, 500, fill="#E1E1E1", outline="#E1E1E1")
guessBox = tk.Entry(root, width=10, font='Helvetica 20 bold')
canvas.create_window(210, 430, window=guessBox)
guessButton = Button(canvas, text='Guess:', command=lambda: [wordGuesser()], font='Helvetica 20 bold', fg='black',
                     highlightbackground='black', highlightthickness=0, bg='white')
guessButton.pack()
guessButton.place(x=10, y=405)
solutionButton = Button(canvas, text='Reveal:', command=lambda: buttonPress(solutionWord), font='Helvetica 12 bold',
                        fg='black', highlightcolor='black', highlightthickness=0)
solutionButton.place(x=310, y=65)
averageScoreText = canvas.create_text(400, 175, fill='black', font='Helvetica 12 bold')

# Runs these functions so they can set their values.
buttonPress(solutionWord)
drawSquares()
averageScoreFinder()

# Packs the canvas and starts the mainloop.
canvas.pack(side="top", fill="both")
root.mainloop()
