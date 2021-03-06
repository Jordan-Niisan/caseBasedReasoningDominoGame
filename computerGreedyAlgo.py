#!/usr/bin/env python
import numpy as np

class computerGreedyAlgo(object):
    '''
    This Class represents the computer, including all
    functions responsible for AI decisions
    '''


    def __init__(self, computer_tiles_list):
        '''
        The Constructor takes a list of tuples that
        represents the computer tiles set
        '''
        self._tiles_list=computer_tiles_list

#---------------------------------------------------

    def play(self, played_tiles):
        """
        play(played_tiles)
            returns the best tile to play. or returns "PASS" if
            there are no suitable tiles.
        """
        """
        #Testing
        print("")
        print("")
        print("Current chain: " , str([row[0] for row in played_tiles]))
        print("Computer 1 (Greedy Algorithm - Player on the top): ", str([row[0] for row in self._tiles_list]))
        
        """
        #if this is the first tile to be played, play the biggest tile
        if len(played_tiles) == 0 :
            biggest_tile = self.get_biggest_tile()
            self._tiles_list.remove(biggest_tile)
            #Testing
            # print("Domino Played by Computer 1 (Greedy Algorithm): ", biggest_tile)
            # print("")
            return biggest_tile

        #if this is NOT the first tile to be played
        else :

            #check for the suitable tiles to be played
            suitable_tiles=self.get_suitable_tiles(played_tiles[0][0][0], played_tiles[-1][0][1])

            #there is no suitable tiles, return "PASS"
            if len(suitable_tiles) == 0 :
                return "PASS"

            #there is only one suitable tile, return it
            elif len(suitable_tiles) == 1 :
                self._tiles_list.remove(suitable_tiles[0])
                #Testing
                # print("Domino Played by Computer 1 (Only one suitable): ", suitable_tiles[0][0])
                # print("")
                return suitable_tiles[0]

            #there are more than one suitable tile, ask the "get_best_tile" method
            else :
                best_tile=self.get_biggest_tile(played_tiles)
                #best_tile=self.get_best_tile(played_tiles, suitable_tiles)
                self._tiles_list.remove(best_tile)
                #Testing
                # print("Domino played by Computer 1 (more than one suitable): ", best_tile[0])
                # print("")
                return best_tile

#---------------------------------------------------

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

#---------------------------------------------------

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

#---------------------------------------------------

    def get_biggest_tile(self,played_tiles):
        """
        get_biggest_tile()
            returns the biggest tile in the computer's tiles list
        """
        dominos=[]
        
        if played_tiles[0][0][0] == played_tiles[-1][0][1] or played_tiles[0][0][0] != played_tiles[-1][0][1] :
            right = self.countRight(played_tiles,True)
            if len(right)!=0:
                for i in range(len(right)):
                    dominos.append(right[i])
        if played_tiles[0][0][0] != played_tiles[-1][0][1]:
            left = self.countLeft(played_tiles,True)
            if len(left)!=0:
                for i in range(len(left)):
                    dominos.append(left[i])

        #Testing
        #print("Possible domino the player is able to play: ", str([row[0] for row in dominos]))

        if len(dominos)==0:
            return "PASS"
        else:
            biggest_tile = [0, 0]
            for tile in dominos :
                temp = tile[0][0] + tile[0][1]

                if temp > biggest_tile[0] :
                    biggest_tile[0] = temp
                    biggest_tile[1] = tile
                    
            return biggest_tile[1]

#---------------------------------------------------

    def get_suitable_tiles(self, left_value, right_value):
        """
        get_suitable_tiles(left_value, right_value)
            returns a list of tuples that contains the suitable tiles
            to play.
            if there are no suitable tiles, returns an empty list.
        """
        suitable_tiles=[]

        for tile in self._tiles_list :
            if (left_value in tile[0]) or (right_value in tile[0]) :
                suitable_tiles.append(tile)

        return suitable_tiles

#---------------------------------------------------

    def get_best_tile(self, played_tiles, suitable_tiles):

        priority_list=[]
        left_value = played_tiles[0][0][0]
        right_value = played_tiles[-1][0][1]

        #build the priority_list
        priority_list =[ 0 for x in suitable_tiles ]

        #fill the priority_list
        for j in range(len(suitable_tiles)) :

            dot_count=suitable_tiles[j][0][0] + suitable_tiles[j][0][1]
            DUO = 0

            #check for the first condition (Total number is Large)
            if dot_count > 7:
                priority_list[j] += (dot_count - 7) + 3

            #check for the second condition (the tile is DUO
            #and I can play on both sides)
            if suitable_tiles[j][0][0] == suitable_tiles[j][0][1]:

                DUO = 1

                left_value_check = 0
                right_value_check = 0

                for tile in suitable_tiles :
                    if left_value in tile[0] :
                        left_value_check = 1
                    if right_value in tile[0] :
                        right_value_check = 1

                if (left_value_check == 1) and (right_value_check == 1):
                    priority_list[j] += 5
                else :
                    priority_list[j] += 2

            #check for the third condition, "Keep The Game Open"
            #only in the beginning of the game
            #NEEDS TO BE TUNED FOR THE NUMBER OF PLAYERS
            if len(self._tiles_list) > 4 :
                x,y = suitable_tiles[j][0]

                x_count = 0
                y_count = 0

                for tile in self._tiles_list :
                    if x in tile[0] :
                        x_count += 1
                    if y in tile[0] :
                        y_count += 1

                if (x_count == 1) or (y_count == 1):
                    priority_list[j] -= 3

            #Check for the fourth condition, Watch out if the
            #tile is played 6 times
            x,y = suitable_tiles[j][0]

            x_count = 0
            y_count = 0

            for tile in played_tiles :
                if x in tile[0] :
                    x_count += 1
                if y in tile[0] :
                    y_count += 1

            if (x_count == 6) or (y_count == 6):
                priority_list[j] -= 10

        #Check for the fifth condition, the Biggest tile
        #gets extra 2 points
        sum_list=[]
        for tile, position in suitable_tiles :
            sum_list.append(tile[0] + tile[1])

        max_tile = sum_list.index(max(sum_list))
        priority_list[max_tile] += 2

        #FINALLY, return the best tile
        best_tile_index = priority_list.index(max(priority_list))
        return suitable_tiles[best_tile_index]

