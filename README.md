# SImulation_Project

ISYE 6644 Simulation Project 

Frances C DePree
Julia Lee

#Game Function for one game
#Pretty sure I did everything according to the rules if it is a bit basic. 

def another_game(): 
    import random
    import math
    player_A = 2  
    player_B = 2
    pot = 4
    turn = 0
    cycle = 0 
    game = True
    while player_A != 0 and player_B != 0 and game == True:
        print("Player A has:", player_A, "Player B has:", player_B, "Pot has:", pot)
        turn += 1
        roll = random.randint(1,6)
        if (turn % 2) == 0:
            print("Player B rolled a", roll)
        else:
            print("Player A rolled a", roll)
        
        if roll == 2: 
            if pot == 0:
                game = False
                print("Pot is empty!")
            elif (turn % 2) == 0:
                player_B += pot
                pot = 0
                print("Player B got the pot!") 
            else:
                player_A += pot
                pot = 0
                print("Player A got the pot!")

        if roll == 3:
            if pot <= 1:
                game = False
                print("Pot is empty!")
            elif (turn % 2) == 0:
                player_B += math.floor(pot/2) 
                pot = math.ceil(pot/2)
                print("Player B got half the pot")
            else:
                player_A += math.floor(pot/2)
                pot = math.ceil(pot/2)
                print("Player A got half the pot")

        if roll == 4 or roll == 5 or roll == 6:
            if (turn % 2) == 0 and player_B >= 1:
                pot += 1
                player_B -= 1
                print("Player B put one in the pot")
            elif player_A >= 1:
                pot += 1
                player_A -= 1
                print("Player A put one in the pot")
            else:
                game = False
                print("Player can't pay up!")
    print("Game over after", turn, "turns.") 
    cycle = math.ceil(turn/2) 
    
#Game counter for x number of games - outputs the average cycle length. 

def game_stats(x):
    import random
    import math
    cycle_count = list()
    def another_game(): #this is one game, next need to make another function to loop it and count
        player_A = 2  #Make these a dictionary? 
        player_B = 2
        pot = 4
        turn = 0
        cycle = 0 #need to define the cycle count
        game = True
        while player_A != 0 and player_B != 0 and game == True:
            #print("Player A has:", player_A, "Player B has:", player_B, "Pot has:", pot)
            turn += 1
            roll = random.randint(1,6)
            #if (turn % 2) == 0:
                #print("Player B rolled a", roll)
            #else:
                #print("Player A rolled a", roll)
        
            if roll == 2: 
                if pot == 0:
                    game = False
                    #print("Pot is empty!")
                elif (turn % 2) == 0:
                    player_B += pot
                    pot = 0
                    #print("Player B got the pot!") 
                else:
                    player_A += pot
                    pot = 0
                    #print("Player A got the pot!")

            if roll == 3:
                if pot <= 1:
                    game = False
                    #print("Pot is empty!")
                elif (turn % 2) == 0:
                    player_B += math.floor(pot/2) #add floor function to round down
                    pot = math.ceil(pot/2)
                    #print("Player B got half the pot")
                else:
                    player_A += math.floor(pot/2)
                    pot = math.ceil(pot/2)
                    #print("Player A got half the pot")

            if roll == 4 or roll == 5 or roll == 6:
                if (turn % 2) == 0 and player_B >= 1:
                    pot += 1
                    player_B -= 1
                    #print("Player B put one in the pot")
                elif player_A >= 1:
                    pot += 1
                    player_A -= 1
                    #print("Player A put one in the pot")
                else:
                    game = False
                    #print("Player can't pay up!")
        print("Game", i, "over after", turn, "turns.") #count statistics of what ends the game
        cycle = math.ceil(turn/2) #This needs to be more precise
        cycle_count.append(cycle)
    i = 1
    while i <= x:
        another_game()
        i += 1
    print("After", len(cycle_count), "games, the average game length was", sum(cycle_count)/len(cycle_count), "cycles.")
