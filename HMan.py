# Hangman!
# Tyler England

# txt file of words
# fullfilepath = r"/Users/Tyler/Desktop/words.txt" #macbook
fullfilepath = r"C:\Users\EnglandT\Desktop\scratch\words.txt" #pc

import random as rand
import collections

with open(fullfilepath) as textfile:  # txt file - list of all possible words
    wordlist = [line.rstrip() for line in textfile]  # array of all words

mistakeset = ["", "head", "body", "left arm", "right arm", "left leg", "right leg"]  # parts of the 'hangman'

affirmations = ["YES", "Y"]  # set of affirmative responses to y/n questions
print("You can have a word generated for you to guess, or you can receive help guessing a word provided externally.")
resp = "-"
while not (resp.isalpha()):
    resp = input("Do you want to have a word generated for you to guess? (y/n) ")

drawing = [""] * 7  # array of "hangman" drawing stages where index = number of incorrect guesses
drawing[1] = " O "
drawing[2] = (""" O
 | 
 | """)
drawing[3] = (""" O 
\| 
 | """)
drawing[4] = (""" O 
\|/
 | """)
drawing[5] = (""" O 
\|/
 | 
/  """)
drawing[6] = (""" O 
\|/
 | 
/ \\""")

if any(x == resp.strip().upper() for x in affirmations):  # word will be generated for user to guess
    i = rand.randrange(len(wordlist))  # random number
    word = wordlist[i].upper()  # random word based on random number
    numlets = len(word)  # number of letters in the word
    nummistakes = 0  # initialize variable representing number of incorrect guesses

    wordvis = [0] * ((numlets * 2) - 1)  # what the user sees (dashes for each letter)
    wordvis[0] = "_"  # first letter is always a letter ("_")
    for i in range(1, len(wordvis)):  # spaces between the letters to distinguish them (avoid "_____")
        if i % 2 == 0:
            wordvis[i] = "_"
        else:
            wordvis[i] = " "

    letsguessed = ""  # list of letters that have been guessed
    while nummistakes < 6 and any(let == "_" for let in wordvis):  # word isn't found, guesses are left
        singleword = False  # if this turns true, only one word is left regardless of letters found
        print()
        if letsguessed > "":
            print("Not included: " + letsguessed)  # letters that have been guessed incorrectly
        strword = ""  # used to convert wordvis into a string
        for i in wordvis:
            strword += str(i)
        print(strword)  # pring wordvis as string
        if nummistakes > 0:
            print(drawing[nummistakes])  # hangman drawing
        guess = input("Guess a letter: ")

        if len(guess) > 1:  # more than one character was entered
            if len(guess) == numlets:  # user attempted to guess the word
                if guess.upper() == word:  # user is correct
                    print("You win! The word is: " + word + "!")
                    quit()
                else:  # user is not correct -- counts as an incorrect guess
                    nummistakes += 1
                    print("Sorry, the word is not " + guess.lower() + ". A " + mistakeset[nummistakes] + " is drawn.")
            else:  # user mistakenly typed more than one letter
                print("Please enter only one letter.")
        elif not guess.isalpha():  # not a letter
            print("Entry must be a letter.")
        else:
            guess = guess.upper()  # uppercase letter to use only
            if any(let == guess for let in wordvis):  # letter already guessed
                print("That letter is in the word, but it's already been guessed.")
            elif any(let == guess for let in letsguessed):  # notification of repeat guess
                print("That letter has already been guessed.")
            elif any(let == guess for let in word):  # letter appears in the word
                for i in range(numlets):
                    if word[i] == guess:  # if letter in the word is the same as the guess, update wordvis
                        if i == 0:
                            wordvis[0] = guess
                        else:
                            wordvis[i + i] = guess
                print("Correct! " + guess + " does appear in the word!")  # congratulatory statement
            else:  # incorrect guess
                if letsguessed == "":  # first incorrect guess
                    letsguessed = guess.upper()  # add to list of guessed letters
                else:  # not first incorrect guess
                    letsguessed = letsguessed + ", " + guess.upper()  # add to list of guessed letters
                nummistakes = nummistakes + 1
                print(
                    guess.upper() + " is not in the word. A " + mistakeset[
                        nummistakes] + " is drawn.")  # failure statement

    print()
    if nummistakes == 6:  # game was lost
        print(drawing[nummistakes])  # hangman drawing
        print("Sorry, you lose. The word is: " + word.upper())  # word reveal
    else:
        print("You win! The word is " + word.upper() + "!")  # you win statement

else:  # help user guess a word

    numlets = "-"  # initialize as string for the following while loop
    vowels = ["A", "E", "I", "O", "U"]  # set of vowel characters (slightly prioritized)

    while numlets == "-":  # get number of letters in the word
        numlets = input("How many letters are in the word? ")  # get number
        if not (numlets.isnumeric()) or int(numlets) < 1:  # if user enters strings, 0, negatives
            numlets = "-"
            print("You must enter a positive integer.")

    i = 0  # reduce list to words with correct num of letters
    numlets = int(numlets)  # make sure treated as integer
    wordslist = []  # new list of appropriately long words
    while i <= (len(wordlist) - 1):  # for elements in wordlist array
        if len(wordlist[i]) == numlets:  # if the length of word[i] is the proper length...
            wordslist.append(wordlist[i])  # add to new array
        i = i + 1
    del wordlist  # delete temporary array

    if len(wordslist) == 0:  # no words found
        print("Error. No words found with that length.")
        quit()
    elif len(wordslist) == 1:  # one word found
        print("The word is: " + wordslist[0])
        quit()

    nummistakes = 0  # initializing the number of incorrect guesses as 0
    singleword = False  # boolean indicating whether only one possible word is left
    letsguessed = ""  # string of letters that have been guessed
    wordvis = [0] * ((numlets * 2) - 1)  # what the user sees (dashes for each letter)
    wordvis[0] = "_"  # first position is always a letter
    for i in range(1, len(wordvis)):  # spaces between the letters to distinguish them (avoid "_____")
        if i % 2 == 0:
            wordvis[i] = "_"
        else:
            wordvis[i] = " "

    while nummistakes < 6 and singleword == False:  # 6 mistakes means you lost, singleword means you're done
        sugglet = ""  # suggested letter based on frequency in potential words
        strtemp = ""  # string of letters in the words
        for i in wordslist:  # for each word
            cnt = collections.Counter(i.upper())  # dictionary of unique letters & frequencies
            for j in cnt:
                strtemp += j  # string where each word's letters are listed w/o freq
        cnt = collections.Counter(strtemp)  # dictionary of each letter & the number of words left that use it
        cntbyval = sorted(cnt.values(), reverse=True)  # sort dictionary by letter(s) in the most words
        i = 0  # counter for the while loop
        while sugglet == "":
            maxval = cntbyval[i]  # number of words that the most frequent letter is in
            keylist = []  # empty array for letter(s)
            for key, value in cnt.items():  # for the elements of the dictionary...
                if value == maxval and not (any(letguessed.upper() == key.upper() for letguessed in letsguessed) or
                                            any(let == key for let in
                                                wordvis)):  # letter (max freq, not previously used)
                    keylist.append(key)  # keylist will be the new letters with the top frequency
            if len(keylist) > 0:  # at least one letter was found
                if len(keylist) > 1:  # more than one letter was foundd
                    for i in keylist:
                        if any(vowel == i for vowel in vowels):  # choose a vowel if available
                            sugglet = i
                if sugglet == "":  # if no vowel was found, just take the first result
                    sugglet = keylist[0]
            else:  # no letters were found
                i += 1

        if len(letsguessed) > 0:  # print bank of letters that have been guessed
            print("Not included: " + letsguessed)

        strword = ""  # to represent wordvis as a string
        for i in wordvis:  # for each letter space
            strword += str(i)  # strword converts wordvis to a string
        print(strword)
        print("Suggested letter to guess: " + sugglet)
        guess = input("Enter your letter to guess: ")  # get user's letter choice

        if len(guess) > 1:  # more than one letter was entered
            if len(guess) == numlets:  # user attempted to guess the word
                resp = "-"  # set resp as non alpha char
                while not (resp.isalpha()):  # loop in case response isn't alphabetical
                    resp = input("Did you want to guess the word \"" + guess + "\"? (y/n)")
                if resp.upper() in affirmations:  # user said yes
                    resp = "-"  # set resp as non alpha char
                    while not (resp.isalpha()):  # loop in case response isn't alphabetical
                        resp = input("Is " + guess.upper() + " the correct word?")  # check if correct
                    if resp.upper() in affirmations:  # user guessed correctly
                        print("You win! The word is " + guess.upper() + "!")
                        quit()
                    else:  # user guessed incorrectly
                        nummistakes += 1  # counts as an incorrect guess
                        print("Okay, the word is not " + guess.lower() + ". A " + mistakeset[nummistakes] + " is "
                                                                                                            "drawn.")
                        for i in wordslist:  # delete that word from the collection of possibilities if present
                            if i == guess.upper():
                                del i
                else:  # user mistakenly typed more than one letter
                    print("Please enter only one letter.")
            else:  # user mistakenly typed more than one letter
                print("Please enter only one letter.")
        elif not guess.isalpha():  # input wasn't a letter
            print("Entry must be a letter.")
        else:  # input was one letter
            guess = guess.upper()  # uppercase character
            if any(x == guess for x in letsguessed) or any(x == guess for x in wordvis):  # letter has been used
                print("That letter has already been guessed.")
            else:  # new letter has been guessed
                inword = "-"  # set inword as non alphabetical char
                while not (inword.isalpha()):  # loop in case response is non alphabetical
                    inword = input("Is " + guess.upper() + " in the word? (y/n) ")
                if inword.strip().upper() in affirmations:  # letter is in the word at least once
                    check1 = False  # first of two check booleans
                    check2 = False  # second of two check booleans
                    finalword = ""  # initialize variable
                    for word in wordslist:  # for all words
                        if guess.upper() in word.upper():  # if the guessed word is in the word
                            if check1 == True:  # if there is at least one word already with that letter
                                check2 = True  # there are at least 2 words left with that letter
                            else:  # there hasn't been any word with that letter so far
                                finalword = word  # change value of finalword
                                check1 = True  # mark that there's at least 1 word with that letter
                    if check2 == False and finalword != "":  # only one word with that letter is left
                        print("The word is: " + finalword)
                        quit()

                    numinst = -1  # -1 to allow user to enter 0 if they mistakenly chose "y"
                    while numinst == -1:  # get number of times it appears
                        try:
                            numinst = int(input("How many times is " + guess.upper() + " in the word? "))  # get number
                        except NameError:  # if the user enters a letter, etc
                            numinst = -1
                            print("You must enter an integer.")
                    if numinst > 0:  # a positive number was enetered
                        letpos = [0] * numinst  # array of the positions where that letter appears (0's right now)
                        if numinst == 1:  # only one appearance of that letter
                            letpos[0] = input(  # get the position of that letter
                                "How many letters from the beginning of the word (starting with 1) is the " +
                                guess.upper() + "? ")
                        else:  # multiple appearances of that letter
                            for x in range(numinst):  # get all positions of that letter
                                letpos[x] = input(
                                    "How many letters from the beginning of the word (starting with 1) is " +
                                    guess.upper() + " #" + str(x + 1) + "? ")

                        i = 0  # initialize i to update wordvis
                        for i in letpos:  # for each of the positions in the word where the guessed letter is
                            if i == 0:  # if first letter
                                wordvis[0] = guess.upper()
                            else:  # if any position other than first letter
                                k = 0  # simple counter variable
                                for j in range(0, len(wordvis)):  # for j=the position in wordvis
                                    if wordvis[j] != " ":  # either a letter or underscore (not a space)
                                        k += 1  # increment k (k=kth letter of the word)
                                        if int(k) == int(i):  # position in wordvis = position of guessed letter in word
                                            wordvis[j] = guess.upper()

                        wordlist = wordslist  # temp array (adding back to array faster than deleting)
                        del wordslist  # delete array so it can be reformulated
                        wordslist = []  # redeclare array
                        for i in wordlist:  # for each word in the temporary list
                            delword = False
                            for j in letpos:  # for each position where the letter is...
                                if i[int(j) - 1].upper() != guess.upper():  # if the j-1'th letter is wrong
                                    delword = True  # don't include the word in the new array
                                    break
                            if not delword:  # if the word should be included in the new array
                                wordslist.append(i)  # add to new array
                        del wordlist  # delete temp array

                    else:  # letter is in the word with a quantity of 0
                        letsguessed.remove(guess)  # remove the letter from the pool of used letters
                        print(  # notification of how the 0 is being processed
                            "You indicated that the letter " + guess + "was in the word, with a quantity of 0. Please "
                                                                       "retry entering " + guess + " as a new guess.")
                else:  # letter was a bad guess
                    nummistakes = nummistakes + 1  # increment mistake count
                    if letsguessed == "":  # first incorrect letter
                        letsguessed = guess
                    else:  # add to preexisting incorrect letters
                        letsguessed = letsguessed + ", " + guess
                    i = 0  # initialize i in order to reduce wordslist
                    while i < (len(wordslist)):  # for all the words in the list
                        delword = False  # initial state of delword = false
                        for j in wordslist[i]:  # for all the letters in the list
                            if any(x == guess for x in wordslist[i]):  # if the incorrect letter appears..
                                delword = True  # change delword to true
                        if delword:  # if the word contains the incorrect letter
                            del wordslist[i]  # delete the word from the list
                        else:  # the word doesn't contain the incorrect letter
                            i = i + 1  # next word

                    print("Incorrect guess #" + str(nummistakes) + ": a " + mistakeset[nummistakes] + " is drawn.")
                    print(drawing[nummistakes])  # notify about incorrect guess & how that impacts the drawing
            if len(wordslist) == 1:  # only one valid word is left
                singleword = True  # change singleword boolean to break the while loop
            elif len(wordslist) == 0:  # no valid words are left
                print("No possible words match the answers given.")
                quit()

    if singleword == True:  # word was found
        print()
        print("The word is: " + wordslist[0])
    else:  # game was lost
        print()
        print("Too many mistakes. Hangman was fully drawn.")