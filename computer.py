#!/usr/bin/env python
from VariablesAndConstants import *
import pandas as pd
import numpy as np
from ast import literal_eval
import csv
import random
from GenerateAndDistribute import *

class computer(object):
    """
    This Class represents the computer, including all
    functions responsible for AI decisions
    """

    def __init__(self, computer_tiles_list):
        """
        The Constructor takes a list of tuples that
        represents the computer tiles set
        """
        self.startDom = 1
        self.strategyChoice = [1,2]
        self._tiles_list = computer_tiles_list
        self.decisionTable = [[0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0]]
        self.probabilityTable = [[0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0]]

        self.sumProbDominos = [0, 0, 0, 0, 0, 0, 0]


        self.opponentList = []
        self.complete_tiles = generate_tiles()


    def updateTable(self, played_tiles):
        if len(played_tiles) != 0:
            for row in played_tiles:
                x = row[0][0]
                y = row[0][1]
                self.decisionTable[x][y] = 1
                self.decisionTable[y][x] = 1

        if len(self._tiles_list) != 0:
            for row in self._tiles_list:
                x = row[0][0]
                y = row[0][1]
                self.decisionTable[x][y] = 1
                self.decisionTable[y][x] = 1

    def updateProbabilityTable(self, played_tiles, pips):
        if len(played_tiles) != 0:
            left = played_tiles[0][0][0]
            right = played_tiles[-1][0][1]

            if pips != "PASS":
                lengthOpponent = len(self._tiles_list)

                for row in played_tiles:
                    x = row[0][0]
                    y = row[0][1]
                    self.probabilityTable[x][y] = 1
                    self.probabilityTable[y][x] = 1

                if len(self._tiles_list) != 0:
                    for row in self._tiles_list:
                        x = row[0][0]
                        y = row[0][1]
                        self.probabilityTable[x][y] = 1
                        self.probabilityTable[y][x] = 1

                if len(played_tiles) != 0:
                    sumL = len(self.countPlayed_L(played_tiles)) + len(self.countLeft(played_tiles, False))
                    diffLeft = 7 - sumL
                    dominoDivLeft = int(diffLeft / 2)
                    remainderLeft = (diffLeft % 2)
                    numStashLeft = dominoDivLeft + remainderLeft
                    opponentLeft = dominoDivLeft

                    sumR = len(self.countPlayed_R(played_tiles)) + len(self.countRight(played_tiles, False))
                    diffRight = 7 - sumR
                    dominoDivRight = int(diffRight / 2)
                    remainderRight = (diffRight % 2)
                    numStashRight = dominoDivRight + remainderRight
                    opponentRight = dominoDivRight
                    
                    listNotVisibleLeft = []
                    for i in self.complete_tiles:
                        if i[0] == left or i[1] == left:
                            if self.checkPlayedTiles(played_tiles, i) and self.checkInHand(i):
                                listNotVisibleLeft.append(i)

                    listNotVisibleRight = []
                    for i in self.complete_tiles:
                        if i[0] == right or i[1] == right:
                            if self.checkPlayedTiles(played_tiles, i) and self.checkInHand(i):
                                listNotVisibleRight.append(i)

                    for row in listNotVisibleLeft:
                        x = row[0]
                        y = row[1]
                        if diffRight!=0:
                            if self.probabilityTable[x][y] != 1:
                                self.probabilityTable[x][y] = round(opponentLeft / 7, 3)
                            if self.probabilityTable[y][x] != 1:
                                self.probabilityTable[y][x] = round(opponentLeft / 7, 3)
                        # print(opponentLeft , ":" ,diffLeft)
                    
                    for row in listNotVisibleRight:
                        x = row[0]
                        y = row[1]
                        if diffRight!=0:
                            if self.probabilityTable[x][y] != 1:
                                self.probabilityTable[x][y] = round(opponentRight / 7, 3)
                            if self.probabilityTable[y][x] != 1:
                                self.probabilityTable[y][x] = round(opponentRight / 7, 3)
                        # print(opponentRight , ":" ,diffRight)

            elif pips == 'PASS':
                listNotVisible = []
                for i in self.complete_tiles:
                    if i[0] == left or i[1] == left:
                        if self.checkPlayedTiles(played_tiles, i) and self.checkInHand(i):
                            listNotVisible.append(i)

                for row in listNotVisible:
                    x = row[0]
                    y = row[1]
                    if self.probabilityTable[x][y] < 1:
                        self.probabilityTable[x][y] = round(self.probabilityTable[x][y], 3) + 0.1
                    if self.probabilityTable[y][x] < 1:
                        self.probabilityTable[y][x] = round(self.probabilityTable[y][x], 3) + 0.1
            # print(self.probabilityTable)

        for i in range (len(self.probabilityTable)):
            sum = 0
            for j in range (len(self.probabilityTable[0])):
                # print("prob table ", self.probabilityTable[i][j])
                sum = sum + self.probabilityTable[i][j]
                
            self.sumProbDominos[i] = sum

        # print("Player: " , self.sumProbDominos)

        


    def checkPlayedTiles(self, played_tiles, tile):
        for row in played_tiles:
            if row[0][0] == tile[0] or row[0][1] == tile[0]:
                if row[0][0] == tile[1] or row[0][1] == tile[1]:
                    return False
        return True

    def checkInHand(self, tile):
        for row in self._tiles_list:
            if row[0][0] == tile[0] or row[0][1] == tile[0]:
                if row[0][0] == tile[1] or row[0][1] == tile[1]:
                    return False
        return True

    def opponentTile(self, tile):
        self.opponentList.append(tile)

    # Testing
    def displayArr(self, arr):
        for i in arr:
            print(i)
    
    def casebasedreasoning(self, played_tile):

        obtained = [] #List used to retrieved data
        print("")
        print("The chain: " , str([row[0] for row in played_tile]))
        # Retrieve
        # will read data from dataset 
        with open('datasetCaseBased.csv') as csvfile:
            filewriter = csv.reader(csvfile, delimiter=';')
            for row in filewriter:

                info = literal_eval(row[0])
                if len(info)>0:
                    # will check if current case equal to cases in dataset
                    # and then add cases to an array
                    if played_tile[0][0][0] == info[0][0] or played_tile[-1][0][1] == info[0][0]:
                        if played_tile[0][0][0] == info[-1][1] or played_tile[-1][0][1] == info[-1][1]:
                            #The cases are stored as an array but the data in that array are string
                            #Therefore, we will used eval later to convert those string into their respective 
                            #data structure
                            obtained.append(row) 

            #display retrieved cases
            print("Retrieved cases: ")
            self.displayArr(obtained)
            print("")

            # Reuses
            refineObtained = [] #List used to store refined data
            
            # find each cases of each dominoes in the user hands
            # and store them in an array: refineObtained 
            if len(obtained) != 0:

                leftDom = self.countLeft(played_tile, False)
                rightDom = self.countRight(played_tile, False)

                for info in obtained:
                    toTuple = eval(info[3]) # convert domino strings in cases to tuple
                    
                    for dom in leftDom:
                        if toTuple[0] == dom[0]:
                            if toTuple[1] == dom[1]:
                                refineObtained.append(info)
                        
                        if toTuple[0] == dom[1]:
                            if toTuple[1] == dom[0]:
                                refineObtained.append(info)
                    
                    for dom in rightDom:
                        if toTuple[0] == dom[0]:
                            if toTuple[1] == dom[1]:
                                if info not in refineObtained:
                                    refineObtained.append(info)
                    
                        if toTuple[0] == dom[1]:
                            if toTuple[1] ==dom[0]:
                                if info not in refineObtained:
                                    refineObtained.append(info)

                #display refined cases based on player domino
                print("Refine retrieved cases based on the agent domino: ")
                self.displayArr(refineObtained)
                print("")

                # Refine
                secondRefine = [] #List used to store second refined data
                if(len(played_tile)-1)==0:
                    self.updateProbabilityTable(PLAYED_TILES,"")
                for refine in refineObtained:

                    #convert sum of probability in case to array
                    toArray = eval(refine[4]) 
                    dominoL = played_tile[0][0][0]
                    #convert domino of case to array
                    toTuple = eval(refine[3])
                    
                    for i in leftDom:
                        #Player sums
                        psum1 = self.sumProbDominos[i[0]]
                        psum2 = self.sumProbDominos[i[1]]
                        sumPlayer = psum1+psum2

                        #Case sums
                        csum1 = toArray[i[0]]
                        csum2 = toArray[i[1]]
                        sumCase = csum1+csum2
                        
                       
                        if sumCase > sumPlayer-0.1 and  sumCase < sumPlayer+0.1 or sumCase==sumPlayer:
                            print("")
                            print("sumCase: ", sumCase)
                            print("sumPlayer: ", sumPlayer)
                            print("sumCase:",sumCase,">= ", "sumPlayer-0.1: ",sumPlayer-0.1)
                            print("sumCase:",sumCase,"<= ", "sumPlayer+0.1: ",sumPlayer+0.1)
                            print("")
                            secondRefine.append(refine)

                    for i in rightDom:
                        #Player sums
                        psum1 = self.sumProbDominos[i[0]]
                        psum2 = self.sumProbDominos[i[1]]
                        sumPlayer = psum1+psum2

                        #Case sums
                        csum1 = toArray[i[0]]
                        csum2 = toArray[i[1]]
                        sumCase = csum1+csum2
                        
                       
                        if sumCase > sumPlayer-0.3 and  sumCase < sumPlayer+0.3 or sumCase==sumPlayer:
                            print("")
                            print("sumCase: ", sumCase)
                            print("sumPlayer: ", sumPlayer)
                            print("sumCase:",sumCase,">= ", "sumPlayer-0.1: ",sumPlayer-0.1)
                            print("sumCase:",sumCase,"<= ", "sumPlayer+0.1: ",sumPlayer+0.1)
                            print("")
                            secondRefine.append(refine)
                
                #display refined cases based on probability matrix
                print("Refine cases a second time based on the probability matrix: ")
                self.displayArr(secondRefine)
                print("")

                # Revise and Review
                countGreedy = 0
                countMinimax = 0

                for refine2 in secondRefine:
                    if refine2[5] == "Greedy Algorithm":
                        countGreedy+=1
                    elif refine2[5] == "Minimax Algorithm":
                        countMinimax+=1

                print("Finding the ocurrence of the algorithms: ")
                print("Occurence of Minmax algorithm: ", countMinimax)
                print("Occurence of Greedy algorithm: ", countGreedy)
                print("")

                # Retain
                if countMinimax > countGreedy:
                    #----Retain function is called in algorithm returned
                    return 1
                elif countGreedy > countMinimax:
                    #----Retain function is called in algorithm returned
                    return 2
                elif countMinimax==countGreedy:
                    r = random.randint(1, 2)
                    #----Retain function is called in algorithm returned
                    return r
                        

    # for each dominos that can be played
    # we check how many dominos of the 2nd numbers in the pip the player have
    # in their hands
    # for example if the Right of the Played_Tiles: 1 and the left of the Played_Tiles:3
    # this function will calculate how much domino of 1 and 3 the player have in their hands
    # and for each domino of 1 and 3, we calculate how much the 2nd number of the same pip the 
    # player have in their, for example the player have domino of 1: 1-4 and 1-5 
    # the function will calculate how many 5 and 4 the player have. 
    def minmax(self, played_tiles):

        # test
        #self.casebasedreasoning(played_tiles)
        #Testing
        print("")
        print("Current chain: " , str([row[0] for row in played_tiles]))
        print("Minmax Algorithm choosen by algorithm: ", str([row[0] for row in self._tiles_list]))

        countL = []
        countR = []
        possibleDom = []
        if len(self.countLeft(played_tiles, True)) != 0:
            countL = self.countLeft(played_tiles, True)
            for i in countL:
                concatenate = []
                check = self.removeHalfLeft(i[0], played_tiles)
                secondColL = []
                for row in self._tiles_list:
                    if row[0][0] == check or row[0][1] == check:
                        secondColL.append(row)
                concatenate = self.concatenateFunc(i, secondColL)
                possibleDom.append(concatenate)

        if len(self.countRight(played_tiles, True)) != 0:
            countR = self.countRight(played_tiles, True)
            for i in countR:
                concatenate = []
                check = self.removeHalfRight(i[0], played_tiles)
                secondColR = []
                for row in self._tiles_list:
                    if row[0][0] == check or row[0][0] == check:
                        secondColR.append(row)
                concatenate = self.concatenateFunc(i, secondColR)
                possibleDom.append(concatenate)
                
        left = self.countLeft(played_tiles, True)
        right = self.countRight(played_tiles, True)

        # If length of domino number in the right is greater or equal to 3
        # then the player will try to block the enemy if they have the domino right+left
        # for example if right:3 and left:2 in the played tiles
        # and if a player has 4 domino of 3 they will check if they have 3-2 
        # and block the enemy
        # method is the same if length of domino number in the left was greater or equal to 3
        # ---right
        if len(right) >= 3:
            for row in countL:
                if played_tiles[0][0][0] != played_tiles[-1][0][1]:
                    if row[0][0] == played_tiles[0][0][0] or row[0][1] == played_tiles[0][0][0]:
                        if row[0][0] == played_tiles[-1][0][1] or row[0][1] == played_tiles[-1][0][1]:
                            row.append("left")
                            self.retain(played_tiles,row,self.sumProbDominos, 1)
                            return row
        # ---left
        if len(left) >= 3:
            for row in countR:
                if played_tiles[0][0][0] != played_tiles[-1][0][1]:
                    if row[0][0] == played_tiles[0][0][0] or row[0][1] == played_tiles[0][0][0]:
                        if row[0][0] == played_tiles[-1][0][1] or row[0][1] == played_tiles[-1][0][1]:
                            row.append("right")
                            self.retain(played_tiles,row,self.sumProbDominos, 1)
                            return row
        #Testing
        print("Possible domino the player 2 is able to play: ", str([row[0][0] for row in possibleDom]))

        if len(possibleDom)==0:
            self.updateProbabilityTable(PLAYED_TILES,"PASS")
        else:
            self.updateProbabilityTable(PLAYED_TILES,"")

        print("Sum of Probability Table: ", self.sumProbDominos)

        checkOccurrence = self.checkNumOccurrance(possibleDom)
        bestTile1 = self.checkProbability(checkOccurrence)
        bestTile = self.bestDom(bestTile1)
        # bestTile = self.bestDom(checkOccurrence)
        print("BestTile chosen by minmax algorithm: ", bestTile[0][0])
        self.retain(played_tiles,bestTile,self.sumProbDominos, 1)
        return bestTile[0]

    def retain(self,played_tiles,tile,sum, model):
        
        if model ==1:
            print("Stored in dataset...",str([row[0] for row in played_tiles]),str(len(self.countLeft(played_tiles,False))), str(len(self.countRight(played_tiles,False))), str(tile[0][0]), str(sum), "Minimax Algorithm")
        elif model ==0:
            print("Stored in dataset...",str([row[0] for row in played_tiles]),str(len(self.countLeft(played_tiles,False))), str(len(self.countRight(played_tiles,False))), str(tile[0]), str(sum), "Greedy Algorithm")
        with open('datasetCaseBased.csv', 'a', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=';')
            if model == 1:
                filewriter.writerow([str([row[0] for row in played_tiles]),str(len(self.countLeft(played_tiles,False))), str(len(self.countRight(played_tiles,False))), str(tile[0][0]), str(sum), "Minimax Algorithm"])
            elif model == 0:
                filewriter.writerow([str([row[0] for row in played_tiles]),str(len(self.countLeft(played_tiles,False))), str(len(self.countRight(played_tiles,False))), str(tile[0]), str(sum), "Greedy Algorithm"])
    

    def displaySumCheckProb(self, data):
        print("Sum: ")
        for i in range(len(data)):
            x = data[i][0][0][0]
            y = data[i][0][0][1]
            sum1 = self.sumProbDominos[x] + self.sumProbDominos[y]
            print("(",x,",",y,") = ", sum1 )

    def checkProbability(self, checkOccurence):
        possibleDom = []
        # testing
        self.displaySumCheckProb(checkOccurence)
        if len(checkOccurence)>0:
            x = checkOccurence[0][0][0][0]
            y = checkOccurence[0][0][0][1]
            probability = self.probabilityTable[x][y]
            sum1 = self.sumProbDominos[x] + self.sumProbDominos[y]
            possibleDom.append(checkOccurence[0])
            for i in checkOccurence:
                x = i[0][0][0]
                y = i[0][0][1]
                temp = self.sumProbDominos[x] + self.sumProbDominos[y]
                if temp > sum1:
                    possibleDom = []
                    possibleDom.append(i)
                    sum1 = temp
                elif temp == sum1:
                    possibleDom.append(i)
        else:
            possibleDom = ["None"]
            
        return possibleDom

    # This function will remove the half pip having the number in the beginning
    # of the played tiles to facilitate us of data
    def removeHalfLeft(self, tiles, played_tiles):
        dominos = []
        first = played_tiles[0]
        if first[0][0] == tiles[0]:
            return tiles[1]
        elif first[0][0] == tiles[1]:
            return tiles[0]

    # This function will remove the half pip having the number at the end
    # of the played tiles to facilitate use of data
    def removeHalfRight(self, tiles, played_tiles):
        dominos = []
        last = played_tiles[-1]
        if last[0][1] == tiles[0]:
            return tiles[1]
        elif last[0][1] == tiles[1]:
            return tiles[0]

    # Put two arrays in a variable
    def concatenateFunc(self, first, second):
        concat = []
        concat.append(first)
        concat.append(second)
        return concat

    # Get the domino with the highest occurence in the possible domino
    # list found in the minimax function
    def bestDom(self, listT):
        if len(listT) != 0:
            biggest = listT[0]
            for i in listT:
                if i[1] > biggest[1]:
                    biggest = i
            return biggest
        else:
            return ["None"]

    # check occurance of second number for each pip based on
    # the numbers we have at the end or beginning of
    # the played tiles
    def checkNumOccurrance(self, possibleDom):
        occurrences = []
        for i in possibleDom:
            concatenate = self.concatenateFunc(i[0], len(i[1]))
            occurrences.append(concatenate)
        return occurrences

    def countPlayed_L(self, played_tiles):
        dominos = []
        first = played_tiles[0]
        for rows in played_tiles:
            if first[0][0] == rows[0][0] or first[0][0] == rows[0][1]:
                dominos.append(rows[0])
        return dominos

    def countPlayed_R(self, played_tiles):
        dominos = []
        last = played_tiles[-1]
        for rows in played_tiles:
            if last[0][1] == rows[0][0] or last[0][1] == rows[0][1]:
                dominos.append(rows[0])
        return dominos

    # This function will find the domino number the played_tiles have at
    # the beginning of the chain
    # and will calculate how many domino of that number does the user have 
    # in their hand
    # for example, if the domino number at the beginning of the played_tiles is: 3
    # this function find how many domino of number 3 the player have 
    # and store that in a variable
    def countLeft(self, played_tiles, position):
        if position == True:
            if len(played_tiles) != 0:
                dominos = []
                first = played_tiles[0]
                for row in self._tiles_list:
                    if first[0][0] == row[0][0] or first[0][0] == row[0][1]:
                        dominos.append(row)
                return dominos
        else:
            if len(played_tiles) != 0:
                dominos = []
                first = played_tiles[0]
                for row in self._tiles_list:
                    if first[0][0] == row[0][0] or first[0][0] == row[0][1]:
                        dominos.append(row[0])
                return dominos

    # This function will find the domino number the played_tiles have at the end of 
    # the chain
    # and will calculate how many domino of that number does the user have 
    # in their hand
    # for example, if the domino number at the beginning of the played_tiles is: 3
    # this function find how many domino of number 3 the player have 
    # and store that in a variable
    def countRight(self, played_tiles, position):
        if position == True:
            if len(played_tiles) != 0:
                dominos = []
                last = played_tiles[-1]
                for row in self._tiles_list:
                    if last[0][1] == row[0][0] or last[0][1] == row[0][1]:
                        dominos.append(row)
                return dominos
        else:
            if len(played_tiles) != 0:
                dominos = []
                last = played_tiles[-1]
                for row in self._tiles_list:
                    if last[0][1] == row[0][0] or last[0][1] == row[0][1]:
                        dominos.append(row[0])
                return dominos

    # if there is no double-1 domino at the start
    # it is incremented to double 2
    # def increase(self):
    #     self.startDom += 1

    # # Get double-domino to be played at the start
    # def getStart(self):
    #     return self.startDom

    # ---------------------------------------------------

    def play(self, played_tiles):
        """
        play(played_tiles)
            returns the best tile to play. or returns "PASS" if
            there are no suitable tiles.
        """
        
        # if this is the first tile to be played, play the biggest tile
        if len(played_tiles) == 0:
            # print("Startbom: ",self.startDom)
            if self.startDom < 6:
                for row in self._tiles_list:
                    # print(self._tiles_list)
                    if row[0] == (self.startDom, self.startDom):
                        firsttiles = row
                        self._tiles_list.remove(row)
                        return firsttiles
                self.startDom += 1

                if self.startDom==6:
                    self.startDom += 1

                return "next"
            elif self.startDom > 6:
                biggest_tile = self.get_biggest_tile()
                # biggest_tile = self.minmax(played_tiles)
                self._tiles_list.remove(biggest_tile)
                return biggest_tile
        
        
        #if played_tiles[0][0][0]==played_tiles[0][0][1]:


        # if this is NOT the first tile to be played
        else:

            # check for the suitable tiles to be played
            suitable_tiles = self.get_suitable_tiles(played_tiles[0][0][0], played_tiles[-1][0][1])

            # there is no suitable tiles, return "PASS"
            if len(suitable_tiles) == 0:
                return "PASS"

            # there is only one suitable tile, return it
            elif len(suitable_tiles) == 1:
                self._tiles_list.remove(suitable_tiles[0])
                # print("Domino Played by Computer 3 (Only one suitable): ", suitable_tiles[0][0])
                # print("")
                return suitable_tiles[0]

            # there are more than one suitable tile, ask the "get_best_tile" method
            else:
                # best_tile=self.get_best_tile(played_tiles, suitable_tiles)
                choiceNum = self.casebasedreasoning(played_tiles)
                if choiceNum==1:
                    best_tile = self.minmax(played_tiles)
                if choiceNum==2:
                    best_tile = self.get_best_tile(played_tiles, suitable_tiles)
                # print("Domino played by Computer 3  (more than one suitable): ", best_tile[0])
                # print("")
                self._tiles_list.remove(best_tile)
                return best_tile

    # ---------------------------------------------------

    def get_biggest_tile(self):
        """
        get_biggest_tile()
            returns the biggest tile in the computer's tiles list
        """

        biggest_tile = [0, 0]

        for tile in self._tiles_list:
            temp = tile[0][0] + tile[0][1]

            if temp > biggest_tile[0]:
                biggest_tile[0] = temp
                biggest_tile[1] = tile

        return biggest_tile[1]

    # ---------------------------------------------------

    def get_suitable_tiles(self, left_value, right_value):
        """
        get_suitable_tiles(left_value, right_value)
            returns a list of tuples that contains the suitable tiles
            to play.
            if there are no suitable tiles, returns an empty list.
        """
        suitable_tiles = []

        for tile in self._tiles_list:
            if (left_value in tile[0]) or (right_value in tile[0]):
                suitable_tiles.append(tile)
        return suitable_tiles

    # ---------------------------------------------------

    def get_best_tile(self, played_tiles, suitable_tiles):

        #Testing
        print("")
        print("Current chain: " , str([row[0] for row in played_tiles]))
        print("Greedy Algorithm choosen by algorithm: ", str([row[0] for row in self._tiles_list]))
        print("Possible domino the player 2 is able to play: ", str([row[0] for row in suitable_tiles]))
        
        if len(suitable_tiles)==0:
            self.updateProbabilityTable(PLAYED_TILES,"PASS")
        else:
            self.updateProbabilityTable(PLAYED_TILES,"")

        #print("Sum of Probability Table: ", self.sumProbDominos)

        priority_list = []
        left_value = played_tiles[0][0][0]
        right_value = played_tiles[-1][0][1]

        # build the priority_list
        priority_list = [0 for x in suitable_tiles]

        # fill the priority_list
        for j in range(len(suitable_tiles)):

            dot_count = suitable_tiles[j][0][0] + suitable_tiles[j][0][1]
            DUO = 0

            # check for the first condition (Total number is Large)
            if dot_count > 7:
                priority_list[j] += (dot_count - 7) + 3

            # check for the second condition (the tile is DUO
            # and I can play on both sides)
            if suitable_tiles[j][0][0] == suitable_tiles[j][0][1]:

                DUO = 1

                left_value_check = 0
                right_value_check = 0

                for tile in suitable_tiles:
                    if left_value in tile[0]:
                        left_value_check = 1
                    if right_value in tile[0]:
                        right_value_check = 1

                if (left_value_check == 1) and (right_value_check == 1):
                    priority_list[j] += 5
                else:
                    priority_list[j] += 2

            # check for the third condition, "Keep The Game Open"
            # only in the beginning of the game
            # NEEDS TO BE TUNED FOR THE NUMBER OF PLAYERS
            if len(self._tiles_list) > 4:
                x, y = suitable_tiles[j][0]

                x_count = 0
                y_count = 0

                for tile in self._tiles_list:
                    if x in tile[0]:
                        x_count += 1
                    if y in tile[0]:
                        y_count += 1

                if (x_count == 1) or (y_count == 1):
                    priority_list[j] -= 3

            # Check for the fourth condition, Watch out if the
            # tile is played 6 times
            x, y = suitable_tiles[j][0]

            x_count = 0
            y_count = 0

            for tile in played_tiles:
                if x in tile[0]:
                    x_count += 1
                if y in tile[0]:
                    y_count += 1

            if (x_count == 6) or (y_count == 6):
                priority_list[j] -= 10

        # Check for the fifth condition, the Biggest tile
        # gets extra 2 points
        sum_list = []
        for tile, position in suitable_tiles:
            sum_list.append(tile[0] + tile[1])

        max_tile = sum_list.index(max(sum_list))
        priority_list[max_tile] += 2

        # FINALLY, return the best tile
        best_tile_index = priority_list.index(max(priority_list))
        self.retain(played_tiles,suitable_tiles[best_tile_index],self.sumProbDominos,0)
        print("Biggest chosen by Greedy Algorithm: ", suitable_tiles[best_tile_index][0])
        return suitable_tiles[best_tile_index]
