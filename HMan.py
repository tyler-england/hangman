# fullfilepath = r"/Users/Tyler/Desktop/words_test.txt"
fullfilepath = r"C:\Users\EnglandT\Desktop\scratch\words.txt"
import random as rand
import collections

with open(fullfilepath) as textfile:  # list of all possible words
    wordslist = [line.rstrip() for line in textfile]

mistakeset = ["", "head","body","left arm","right arm","left leg","right leg"]

affirmations = ["Yes", "Y"]
resp = input("Do you want to have a word generated for you to guess? (y/n) ")

drawing=[""]*7
drawing[1]=" O "
drawing[2]=(""" O
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

if any(x == resp.strip().upper() for x in affirmations): #word generated to guess
    i = rand.randrange(len(wordslist))
    word = wordslist[i]
    numlets = len(word)
    nummistakes=0

    wordvis=[0]*((numlets*2)-1) #what the user sees (dashes for each letter)
    wordvis[0]="_"
    for i in range(1,len(wordvis)):
        if i%2==0:
            wordvis[i]="_"
        else:
            wordvis[i] = " "

    letsguessed=""
    while nummistakes<6 and any(let == "_" for let in wordvis): #word isn't found, guesses are left
        singleword=False
        print()
        if letsguessed > "":
            print("Not included: " + letsguessed) #letters that have been guessed incorrectly
        strwordvis=""
        for i in wordvis:
            strwordvis +=str(i)
        print(strwordvis) #dashes & letters so far
        if nummistakes>0:
            print(drawing[nummistakes]) #hangman drawing
        guess=input("Guess a letter: ")

        if not guess.isalpha():
            print("Please enter a valid letter.")
        elif any(let == guess.upper() for let in wordvis):
            print("That letter is in the word, but it's already been guessed.")
        elif any(let == guess for let in word):#replace appropriate dash(es)
            for i in range(numlets):
                if word[i]== guess:
                    if i==0:
                        wordvis[0]=guess.upper()
                    else:
                        wordvis[i+i]=guess.upper()
            print("Correct! " + guess.upper() + " does appear in the word!")
        elif any(let == guess.upper() for let in letsguessed):
            print("That letter has already been guessed.")
        else:
            if letsguessed=="":
                letsguessed=guess.upper()
            else:
                letsguessed=letsguessed + ", " + guess.upper()
            nummistakes=nummistakes+1
            print(guess.upper() + " is not in the word. A " + mistakeset[nummistakes] + " is drawn.")

    print()
    if nummistakes==6:
        print(drawing[nummistakes])
        print("Sorry, you lose. The word is: " + word)
    else:
        print("You win! The word is " + word + "!")

else:  # help user guess a word

    numlets = 0
    vowels = ["A", "E", "I", "O", "U"]

    while numlets == 0:  # get number of letters in the word
        try:
            numlets = int(input("How many letters are in the word? "))
        except NameError:
            numlets = 0
            print("You must enter an integer.")

    i = 0  # reduce list to words with correct num of letters
    while i <= (len(wordslist) - 1):
        if len(wordslist[i]) != numlets:
            del wordslist[i]
        else:
            i = i + 1

    if len(wordslist) == 0: #no words found
        print("Error.")
        quit()
    elif len(wordslist) == 1: #one word found
        print("The word is: " + wordslist[0])
        quit()

    nummistakes = 0
    singleword = False
    letsguessed = []
    spelling = ["-"]*numlets  # array with 'numlets' elements
    while nummistakes < 6 and singleword == False:  # 6 mistakes means you lost
        print(wordslist)
        sugglet=""
        corrint=0 #correcting integer, if most freq letter has been guessed
        while sugglet=="":
            strtemp = "" #figure out most tactful letter to guess
            for i in wordslist: #for each word
                cnt=collections.Counter(i) #count letters
                for j in cnt:
                    strtemp=strtemp+j #string where each word's letters are listed w/o freq

            cnt = collections.Counter(strtemp)
            maxsofar = 0
            for key, value in cnt.items():
                if value > maxsofar:
                    maxsofar = value #get highest frequency (letter in most words)
            maxsofar=maxsofar-corrint

            strtemp = ""
            for key, value in cnt.items():
                if value == maxsofar and not(any(letguessed==key.upper() for letguessed in letsguessed)):
                    strtemp += key #string of most frequent new letter(s)

            if len(strtemp)==0:
                corrint=corrint+1
            elif len(strtemp)==1:
                sugglet=strtemp[0]
            else:
                sugglet="xxx"
                for key in strtemp:
                    if any(vowel == key.upper() for vowel in vowels):
                        sugglet = key

                if sugglet=="xxx":
                    sugglet = strtemp[0]

        print("Suggested letter to guess: " + sugglet)
        guess = input("Enter your letter to guess: ")

        if len(guess)>1:
            print("Please enter only one letter.")
        elif not guess.isalpha():
            print("Entry must be a letter.")
        else:
            if any(x == guess for x in letsguessed):
                print("That letter has already been guessed.")
            else:
                letsguessed.append(guess.upper())
                inword = input("Is " + guess.upper() + " in the word? (y/n) ")
                if inword.strip().upper() in affirmations:  # letter is in the word at least once
                    check1=False
                    check2=False
                    finalword=""
                    for word in wordslist:
                        if guess.upper() in word.upper():
                            if check1==True:
                                check2=True
                            else:
                                finalword=word
                                check1=True
                    if check2==False and finalword!="": #only one word with that letter is left
                        print("The word is: " + finalword)
                        quit()

                    numinst = -1  # allow user to enter 0 if they mistakenly chose "y"
                    while numinst == -1:  # get number of times it appears
                        try:
                            numinst = int(input("How many times is " + guess + " in the word? "))
                        except NameError:
                            numinst = -1
                            print("You must enter an integer.")
                    if numinst > 0:
                        letpos = [0]*numinst
                        if numinst == 1:
                            letpos[0] = input("How many letters from the beginning of the word (starting with 1) is the " +
                                              guess.upper() + "? ")
                        else:
                            for x in range(numinst):
                                letpos[x] = input("How many letters from the beginning of the word (starting with 1) is " +
                                                  guess.upper() + " #" + str(x + 1) + "? ")

                        for x in letpos:  # update spelling
                            spelling[int(x) - 1] = guess.upper()
                        i = 0  # reduce wordslist
                        while i < (len(wordslist)):
                            contender=wordslist[i]
                            delword=False
                            for j in letpos:
                                if contender[int(j)-1].upper()!=guess.upper():
                                    delword=True
                            if delword:
                                del wordslist[i]
                            else:
                                i = i + 1

                    else:
                        letsguessed.remove(guess)
                        numinst=-1
                        print("You indicated that the letter " + guess + "was in the word, with a quantity of 0. Please "
                                                                          "retry entering " + guess + " as a new guess.")
                else:  # letter was a bad guess
                    nummistakes = nummistakes + 1
                    i = 0  # reduce wordslist
                    while i < (len(wordslist)):
                        delword = False
                        for j in wordslist[i]:
                            if any(x == guess for x in wordslist[i]):
                                delword = True
                        if delword:
                            del wordslist[i]
                        else:
                            i = i + 1

                    print("Incorrect guess #" + str(nummistakes) + ": a " + mistakeset[nummistakes] + " is drawn.")
                    print(drawing[nummistakes])
            if len(wordslist)==1:
                singleword=True
            elif len(wordslist)==0:
                print("No possible words match the answers given.")
                quit()

    if singleword == True:  # word was found
        print("The word is: " + wordslist[0])
    else:  # game was lost
        print("Too many mistakes. Hangman was fully drawn.")