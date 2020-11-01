"""
This is a hangman game. It chooses from a list of random words.
"""

import random
import pygame
from listOfWords import listWords
from pygame_functions import *


# Intitializing game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((852, 480))
screenSize(852,480)

# Background
background = pygame.image.load("hangman.jpg")

#dead image
deadImage = pygame.image.load("dead.png")

# Title
pygame.display.set_caption("Hangman")

def get_valid_word(words):
    word = random.choice(words) #randomly chooses something from the list
    while '-' in word or ' ' in word:
        word = random.choice(words)
    word = word.upper()
    return word

word = get_valid_word(listWords)

#defining starting values
currentWord = "*" * len(word)
numLives = 2+int(1.5*len(word))
livesLeft = numLives
currentAttempt = 0
allGuesses = ""
guess = ""


#Text to be shown on the screen
currentWordLabel = makeLabel(currentWord, 60, 100, 20, "white")
livesLeftLabel = makeLabel("Lives Left: " + str(livesLeft), 50, 100, 80, "white")
allGuessesLabel = makeLabel("Letters used: " + allGuesses, 20, 100, 200, "white")

#feedback to user
wrongLetterLabel = makeLabel("Wrong Letter", 50, 100, 350, "red")
correctLetterLabel = makeLabel("Correct letter", 50, 100, 350, "green")
wrongWordLabel = makeLabel("You Lost!", 50, 100, 350, "red")
correctWordLabel = makeLabel("You Won!", 50, 100, 350, "green")
letterAlreadyUsed = makeLabel("Letter already used!", 40, 100, 350, "red")
wordLabelPos = makeLabel(word, 60, 100, 20, "green")
wordLabelNeg = makeLabel(word, 60, 100, 20, "red")

#instructions
instructionsLabel = makeLabel("This is a classical Hangman Game.", 20, 580, 20, "white")
instructionsLabel2 = makeLabel("It is pretty self-explanatory.", 20, 580, 40, "white")


#prompt
wordBox = makeTextBox(100, 250, 250, 2, "Input a Guess", 0, 40)





######################### GAME LOOP ###########################
running = True
lose = False
win = False
counter = 0
while running:


    # RGB - (MAKING IT WHITE)
    screen.fill((255, 255, 255))

    # Adding background
    screen.blit(background, (0, 0))

    # Lives left
    livesLeft = numLives-currentAttempt
    currentAttempt += 1


    #removing former labels
    hideLabel(currentWordLabel)
    hideLabel(livesLeftLabel)
    hideLabel(wrongWordLabel)
    hideLabel(correctWordLabel)
    hideLabel(allGuessesLabel)

    #updating elements
    currentWordLabel = makeLabel(currentWord, 60, 100, 20, "white")
    livesLeftLabel = makeLabel("Lives Left: " + str(livesLeft), 50, 100, 80, "white")
    allGuessesLabel = makeLabel("Used letters: " + allGuesses, 20, 100, 200, "white")

    #showing elements
    showLabel(currentWordLabel)
    showLabel(livesLeftLabel)
    showLabel(allGuessesLabel)
    showLabel(instructionsLabel)
    showLabel(instructionsLabel2)

    #showing textbox and making guess
    showTextBox(wordBox)
    guess = str(textBoxInput(wordBox))
    allGuesses += guess + ", "

    # If the same letter is written twice: go to top of loop. Otherwise it fucks up.
    allGuessesElements = allGuesses.split(", ")
    for i in allGuessesElements:
        if guess == i:
            break  # go to the top of the loop


    if len(guess) > 1: #if you write a word
        if guess == word:
            win = True
        else:
            lose = True

    elif len(guess) <= 1: # if you write a letter
        if guess in word: # if you write a letter
            # feedback
            hideLabel(wrongLetterLabel)
            hideLabel(correctLetterLabel)
            hideLabel(letterAlreadyUsed)
            showLabel(correctLetterLabel)

            if word.count(guess) == 1:               #if the letter only occurs once in the word
                guessPos: int = word.find(guess) + 1 #get the position of the letter
                currentWord = currentWord[0: guessPos - 1] + guess + currentWord[guessPos: len(currentWord)] #insert the letter in currentword

            elif word.count(guess) > 1:           #if the letter occurs more than once in the word
                timesOccuring = word.count(guess) #the number of times the let er occurs

                for number in range(0,timesOccuring): #make a list containing the multiple positions of letter in word

                    if number == 0:                   #append the first position of guess
                        guessPosList = []
                        guessPosList.append(word.find(guess) + 1)
                    else:                             #for the remaining positions of guess
                        guessPosList.append(word.find(guess, guessPosList[number-1]+len(guess))+1)


                for i in guessPosList:                # update currentWord to contain the letters
                    currentWord = currentWord[0:i-1] + guess + currentWord[i: len(currentWord)]



        else: #if your guess-letter is incorrect
            counter = counter + 1
            hideLabel(wrongLetterLabel)
            hideLabel(correctLetterLabel)
            hideLabel(letterAlreadyUsed)
            showLabel(wrongLetterLabel)


    if livesLeft <= 0:
        lose = True

    if currentWord == word:
        win = True

    if win == True:
        hideLabel(wrongLetterLabel)
        hideLabel(correctLetterLabel)
        hideLabel(currentWordLabel)
        hideLabel(letterAlreadyUsed)

        showLabel(correctWordLabel)
        showLabel(wordLabelPos)
        pause(5000)

        end()
        running = False

    if lose == True:
        hideLabel(wrongLetterLabel)
        hideLabel(correctLetterLabel)
        hideLabel(currentWordLabel)
        hideLabel(letterAlreadyUsed)

        showLabel(wrongWordLabel)
        showLabel(wordLabelNeg)

        screen.blit(deadImage, (300, 300))
        pause(5000)
        end()
        running = False

    pygame.display.update() #update the screen

#from pygame_functions
endWait()


