intro = """You decide to go for a walk on a cool fall evening through the neighborhood. 
You will have several encounters along the way. Make the right decisions to enjoy your stroll!
Enter numbers only."""

print (intro)

# execute the game

Kitty = """You come upon a kitty cat who chirps and approaches you, what do you do?
1 - Pssp pssp pssp, greet the kitty and give them some scritches
2 - Don't say hi to the cat, it could be feral\n"""

run = True # game will continue when correct decisions are made, if false, the game ends

# first decision to make

firstChoice = "2" # variable defined so will force code into loop

while (firstChoice != "1"): #first loop used in game
    firstChoice = input(Kitty)
    #conditionals below
    if(firstChoice == "1"):
        print ("The kitty purrs, nuzzles your leg, and trots off happy to have met you. You continue your walk.")
    elif(firstChoice == "2"):
        print("Your loss, the kitty sulks away sad, having not connected with you. You feel bad and go home, your walk is over.")
        run = False
        break
    else: #in case user makes error
        print("Please enter 1 or 2.")


Stranger = """You see a shadow lurking behind a bush. As you get closer, you see someone watching you.
You hear them beginning to shout at you and seem hostile. What do you do?
1 - Ignore them and keep walking confidently away
2 - Engage with the weirdo\n"""

# second decision to make
secondChoice = "2"

if (run == True and secondChoice != "1"): # check point to see if walk should continue
    print("Your stroll continues...")

    while (secondChoice != "1"):
        secondChoice = input(Stranger)

        if(secondChoice == "1"):
            print("You successfully evadeed the weirdo, you relax, and keep walking.")
        elif(secondChoice == "2"):
            print("The creepy person taunts you, making you uncomfortable, you run home. Your walk is over.")
            run = False
            break
        else:
            print("Please enter 1 or 2.")

Stars = """You come upon a grassy open field, it is calm and you feel safe now.
You look up and see the stars are poppin. What do you do?
1 - Lay down in the field and look at the stars
2 - Briefly glance up and keep walking\n"""

# third decision to make
thirdChoice = "2"

if (run == True and thirdChoice != "1"):
    print("Your stroll continues further...")

    while (thirdChoice != "1"):
        thirdChoice = input(Stars)

        if(thirdChoice == "1"):
            print("You take in the beautiful night sky, feeling awe. You see a shooting star. You then continue your walk.")
        elif(thirdChoice == "2"):
            print("You decide to go home, feeling neutral. Your walk is over.")
            break
        else:
            print("Please enter 1 or 2")

# the goal is to not end the walk - just keep walking

# tried a function
def thank_you(message):
    print("Thank you,", message)

thank_you("for playing!")