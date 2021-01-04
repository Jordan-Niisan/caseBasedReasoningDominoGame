#!/usr/bin/env python

#------------------IMPORTS------------------------
import pygame
from pygame.locals import *
from sys import exit
from time import sleep
from computer import *
from computerMinimax import *
from computerGreedyAlgo import *
from Tile import *
from os import path
from VariablesAndConstants import *
from GenerateAndDistribute import *
#----------------------------------------------------------------------------

def seticon(iconname):
    """
    seticon(iconname)
        give an iconname, a bitmap sized 32x32 pixels, black (0,0,0) will be alpha channel
        the window icon will be set to the bitmap, but the black pixels will be full alpha channel
        can only be called once after pygame.init() and before somewindow = pygame.display.set_mode()
    """
    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))
    rawicon=pygame.image.load(iconname)
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)


#----------------------------------------------------------------------------

def draw_bg(screen):
    """
    draw_bg()
        drawing the board background, and all necessary buttons
    """

    # PLayer number
    player_number = pygame.image.load("images/player.png")
    button_2 = pygame.image.load("images/button_2.png")
    button_4 = pygame.image.load("images/button_4.png")

    # load all images
    pass_button = pygame.image.load("images/deactive_pass.png")
    replay_button = pygame.image.load("images/normal_replay.png")
    exit_button = pygame.image.load("images/normal_exit.png")
    computer_tiles_background = pygame.image.load("images/computer_tiles_background.png")
    computer_tiles_background2 = pygame.image.load("images/computer_tiles_background2.png")
    computer_tiles_background3 = pygame.image.load("images/computer_tiles_background3.png")
    human_tiles_background = pygame.image.load("images/human_tiles_background.png")
    center_image = pygame.image.load("images/center_image.png")

    # create and draw the center rectangle
    center_rectangle_start = (0, main_window_resolution[1] / 4)
    center_rectangle_size = (main_window_resolution[0], main_window_resolution[1] / 2)
    center_rectangle = Rect(center_rectangle_start, center_rectangle_size)
    pygame.draw.rect(screen, INNER_COLOR, center_rectangle)

    # draw the center image
    center_image_X = (main_window_resolution[0] - 780) / 2
    center_image_Y = (main_window_resolution[1] - 280) / 2
    screen.blit(center_image, (center_image_X, center_image_Y))

    # Draw the upper and lower rectangles
    upper_rectangle_start = (0, 0)
    upper_rectangle_size = (main_window_resolution[0], main_window_resolution[1] / 4)

    lower_rectangle_Y = main_window_resolution[1] - main_window_resolution[1] / 4
    lower_rectangle_start = (0, lower_rectangle_Y)
    lower_rectangle_size = (main_window_resolution[0], main_window_resolution[1] / 4)

    upper_rectangle = Rect(upper_rectangle_start, upper_rectangle_size)
    lower_rectangle = Rect(lower_rectangle_start, lower_rectangle_size)

    pygame.draw.rect(screen, OUTER_COLOR, upper_rectangle)
    pygame.draw.rect(screen, OUTER_COLOR, lower_rectangle)

    # draw the background behind tiles
    X_start = (main_window_resolution[0] - 565) / 2

    computer_tiles_background_Y = (main_window_resolution[1] / 8) - 60
    human_tiles_background_Y = main_window_resolution[1] - (main_window_resolution[1] / 8) - 60

    screen.blit(computer_tiles_background, (X_start, computer_tiles_background_Y))
    screen.blit(computer_tiles_background2, (X_start-250, computer_tiles_background_Y+100))
    screen.blit(computer_tiles_background3, (X_start+690, computer_tiles_background_Y+100))

    screen.blit(human_tiles_background, (X_start, human_tiles_background_Y))

    # draw the buttons
    REPLAY_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) / 2
    EXIT_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) / 2

    REPLAY_BUTTON_PLACE[1] = human_tiles_background_Y + 25
    EXIT_BUTTON_PLACE[1] = REPLAY_BUTTON_PLACE[1] + 40

    PASS_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 + 565) + (
            (main_window_resolution[0] - 565) / 2 - 99) / 2
    PASS_BUTTON_PLACE[1] = human_tiles_background_Y + 37

    # draw player number buttons
    PLAYER_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 150) / 2
    PLAYER_BUTTON_PLACE[1] = human_tiles_background_Y + 108

    BUTTON_2_PLACE[0] = ((main_window_resolution[0] - 65) / 2 - 150) / 2
    BUTTON_2_PLACE[1] = human_tiles_background_Y + 108

    BUTTON_4_PLACE[0] = ((main_window_resolution[0] - 5) / 2 - 100) / 2
    BUTTON_4_PLACE[1] = human_tiles_background_Y + 108

    screen.blit(replay_button, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
    screen.blit(exit_button, (EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
    screen.blit(pass_button, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

    # Draw player number buttons on window
    screen.blit(player_number, (PLAYER_BUTTON_PLACE[0], PLAYER_BUTTON_PLACE[1]))
    screen.blit(button_2, (BUTTON_2_PLACE[0], BUTTON_2_PLACE[1]))
    screen.blit(button_4, (BUTTON_4_PLACE[0], BUTTON_4_PLACE[1]))

    # refresh the pygame display
    pygame.display.update()


#----------------------------------------------------------------------------

def draw_tiles(screen):
    """
    draw_tiles()
        this function draws both computer's and human's tiles
    """

    if NUMBER_OF_PLAYERS==2:
        #Print the human Tiles on the screen
        for i in range(len(HUMAN_TILES)):
            current_tile = HUMAN_TILES[i][0]
            current_position = HUMAN_TILES[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_vertical()

        # #Print the Computer Tiles (up-side-down)
        # #TODO (DONE) changing the Computer tiles image
        # for i in range(len(COMPUTER_TILES)):
        #     current_position = COMPUTER_TILES[i][1]
        #     temp_tile = Tile(9, 8, screen, current_position[0], current_position[1])
        #     temp_tile.show_vertical()

        for i in range(len(COMPUTER_TILES)):
            current_tile = COMPUTER_TILES[i][0]
            current_position = COMPUTER_TILES[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_vertical()

    elif NUMBER_OF_PLAYERS==4:
        #Print the human Tiles on the screen
        for i in range(len(HUMAN_TILES)):
            current_tile = HUMAN_TILES[i][0]
            current_position = HUMAN_TILES[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_vertical()

        # #Print the Computer Tiles (up-side-down)
        # #TODO (DONE) changing the Computer tiles image
        # for i in range(len(COMPUTER_TILES)):
        #     current_position = COMPUTER_TILES[i][1]
        #     temp_tile = Tile(9, 8, screen, current_position[0], current_position[1])
        #     temp_tile.show_vertical()

        for i in range(len(COMPUTER_TILES)):
            current_tile = COMPUTER_TILES[i][0]
            current_position = COMPUTER_TILES[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_vertical()
        
        for i in range(len(COMPUTER_TILES2)):
            current_tile = COMPUTER_TILES2[i][0]
            current_position = COMPUTER_TILES2[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_horizontal()

        for i in range(len(COMPUTER_TILES3)):
            current_tile = COMPUTER_TILES3[i][0]
            current_position = COMPUTER_TILES3[i][1]
            temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
            temp_tile.show_horizontal()

#----------------------------------------------------------------------------

def initialize(screen):
    """
    initialize(screen)
        This function takes a "display" and creates the tiles sets for
        the players then displays them on the "display"
    """
    global complete_tiles
    #Generate two random Tile lists
    complete_tiles_set = generate_tiles()
    both_players_tiles = distribute_tiles(complete_tiles_set, NUMBER_OF_PLAYERS)
    complete_tiles= generate_tiles()
    #Constructing the Human Tiles list
    identifier = 0

    x_start = (main_window_resolution[0]- 565) // 2 + 25
    x_end = x_start + 514
    y_start = main_window_resolution[1] - (main_window_resolution[1]/8) - 34

    for i in range(x_start, x_end, 80):
        HUMAN_TILES.append([both_players_tiles[0][identifier], (i, y_start)])
        identifier += 1


    #Constructing the Computer Tiles list
    y_start = (main_window_resolution[1] / 8) -34

    # 4 player 
    # x_s = (main_window_resolution[0] / 8) -34
    # y_s = (main_window_resolution[1] / 8) -34
    y_end = int(y_start) + 514

    if NUMBER_OF_PLAYERS == 2:
        identifier = 0
        for i in range(x_start, x_end, 80):
            COMPUTER_TILES.append([both_players_tiles[1][identifier], (i, y_start)])
            identifier += 1
    elif NUMBER_OF_PLAYERS==4:
        identifier = 0
        for i in range(x_start, x_end, 80):
            COMPUTER_TILES.append([both_players_tiles[1][identifier], (i, y_start)])
            identifier += 1
        identifier = 0
        for i in range(x_start, x_end, 80):
            # print("(y_start,i)" ,(y_start,i))
            COMPUTER_TILES2.append([both_players_tiles[2][identifier], (y_start-20,i-120)])
            COMPUTER_TILES3.append([both_players_tiles[3][identifier], (y_start+900,i-120)])
            identifier += 1

    print("HUMAN_TILES: ", str([row[0] for row in HUMAN_TILES]))
    print("COMPUTER_TILES: ", str([row[0] for row in COMPUTER_TILES]))
    print("COMPUTER_TILES2: ",str([row[0] for row in COMPUTER_TILES2]))
    print("COMPUTER_TILES3: ",str([row[0] for row in COMPUTER_TILES3]))
    print("")
    #draw the background and dominos tiles on the screen
    draw_bg(screen)
    draw_tiles(screen)

#----------------------------------------------------------------------------

def clicked_on_tile(mouse_position, tile_position):
    """
    clicked_on_tile(mouse_position, tile_position)
        takes two positions as "tuples", and returns True if the
        mouse is on the tile, and returns False otherwise.
    """
    if mouse_position[0] > tile_position[0]\
    and mouse_position[0] < (tile_position[0] + 34)\
    and mouse_position[1] > tile_position[1]\
    and mouse_position[1] < (tile_position[1] + 68) :
        return True
    else :
        return False

#----------------------------------------------------------------------------

def tile_check(tile):
    """
    tile_check(tile)
        this function takes a tile as a tuple and returns a list
        of the tile in it's suitable state (as a tuple), and the position
        where it should played in (as a string).
        If the tile can be played on both sides, the returning list will
        contain 4 items which are both states that the tile can have.
        If this tile is the first tile to be played, this function will
        return None.
    """

    right = 0
    left = 0
    right_flip = 0
    left_flip = 0

    # If this is the first tile to be played
    if len(PLAYED_TILES) == 0:
        return tile[0], None

    # check if the tile can be played on the right
    if tile[0][0] == PLAYED_TILES[-1][0][1]:
        right = 1

    elif tile[0][1] == PLAYED_TILES[-1][0][1]:
        right = 1
        right_flip = 1

    # check if the tile can be played on the left
    if tile[0][1] == PLAYED_TILES[0][0][0]:
        left = 1

    elif tile[0][0] == PLAYED_TILES[0][0][0]:
        left = 1
        left_flip = 1

    # If the tile can be played on both sides
    if (right == 1) and (left == 1):

        if len(tile) != 2:
            if tile[2] == "left" or tile[2] == "right":
                if tile[2] == 'left' and left_flip == 1:
                    return (tile[0][1], tile[0][0]), tile[2]
                elif tile[2] == "left":
                    return tile[0], tile[2]

                if tile[2] == 'right' and right_flip == 1:
                    return (tile[0][1], tile[0][0]), tile[2]
                elif tile[2] == 'right':
                    return tile[0], tile[2]
        else:
            # construct empty result list
            result = []

            # Manage the right side
            if right_flip == 1:
                result.extend([(tile[0][1], tile[0][0]), "right"])

            else:
                result.extend([tile[0], "right"])

            # Manage the left side
            if left_flip == 1:
                result.extend([(tile[0][1], tile[0][0]), "left"])

            else:
                result.extend([tile[0], "left"])

            # return the result
            return result

    # If the tile can be played on the right side only
    elif right == 1:
        if right_flip == 1:
            return (tile[0][1], tile[0][0]), "right"
        else:
            return tile[0], "right"

    # If the tile can be played on the left side only
    elif left == 1:
        if left_flip == 1:
            return (tile[0][1], tile[0][0]), "left"
        else:
            return tile[0], "left"

    # If the tile isn't suitable
    else:
        return None

#----------------------------------------------------------------------------
# easy
def play(tile, screen, place = None):
    """
    play(tile, screen, place)
        this function takes a tile as a "tuple", display
        and a place ("left" or "right"). then draws the tile on the screen.
    """

    #Initialize the flag that determines the orientation of the tile
    orientation = "horizontal"
    #Initialize the flag that determines if the tile would be painted reversed
    reverse_tile = 0

    #Initialize the place of the tile
    tile_x = 0
    tile_y = 0

    #make python recognize these variables as global
    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile

    #set a variables determines if the tile is DUO or not
    tile_is_DUO = 0

    if tile[0] == tile[1] :
        tile_is_DUO = 1

    #check if this tile is the first tile to be played
    if len(PLAYED_TILES) == 0 :

        #check if the tile is DUO, then place it in the right place
        if tile_is_DUO:
            tile_x = main_window_resolution[0]/2 - 17
            tile_y = main_window_resolution[1]/2 - 34
            orientation = "vertical"

        else :
            tile_x = main_window_resolution[0]/2 - 34
            tile_y = main_window_resolution[1]/2 - 17

        #append the tile to the PLAYED_TILES list
        PLAYED_TILES.append([tile,(tile_x, tile_y)])

    #if the tile is going to be played in the left direction
    elif place == "left" :

        #make some variables to ease understanding the code
        previous_tile = PLAYED_TILES[0][0]
        previous_position = PLAYED_TILES[0][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #PLAY TO THE LEFT DIRECTION
        if TOTAL_X["left"] < resolution[0]/2 - 150 : # change main_window_resolution[0]

            if tile_is_DUO :
                TOTAL_X["left"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] - 36
                tile_y = previous_position[1] - 17

            else :
                if previous_tile_is_DUO :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1]

        #reached the left end of the window
        else :

            #PLAY TO THE UP DIRECTION
            if TOTAL_Y["up"] < resolution[1]/4 -110 : # change main_window_resolution[0]

                #this is the first tile going to be played UP
                if this_is_first_UP_tile :
                    this_is_first_UP_tile = 0

                    #previous tile is DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] - 70

                    #previous tile is NOT DUO
                    else :
                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17

                            #act like the next tile will be the first UP,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_UP_tile = 1

                        else :
                            TOTAL_Y["up"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

                #this is NOT the first tile that is going to be played UP
                else :

                    #previous tile is DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] - 70

                    #previous tile is NOT DUO
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36

                        else :
                            TOTAL_Y["up"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

            #PLAY TO THE RIGHT DIRECTION
            else :

                #this is the first tile to be played RIGHT
                if this_is_first_RIGHT_tile :
                    this_is_first_RIGHT_tile = 0

                    #the previous tile was DUO
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    #the previous tile was NOT DUO
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36

                            #act like the next tile will be the first UP,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_RIGHT_tile = 1

                        else :
                            #we will add 36 to TOTAL_Y["up"] because if we didn't, next
                            #time it would be considered "first time right" again
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] + 36
                            tile_y = previous_position[1]
                            reverse_tile = 1

                #this is NOT the first tile to be played RIGHT
                else :

                    #the previous tile was DUO
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 36
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                        else :
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #APPEND THE PLAYED TILE TO THE PLAYED_TILES LIST
        PLAYED_TILES.insert(0, [tile, (tile_x, tile_y)])


    #if the tile is going to be played in the right direction
    elif place == "right" :

        #make some variables to ease understanding the code
        previous_tile = PLAYED_TILES[-1][0]
        previous_position = PLAYED_TILES[-1][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #PLAY TO THE RIGHT DIRECTION
        if TOTAL_X["right"] < resolution[0]/2 - 150 : # change main_window_resolution[0]

            #if this tile is DUO
            if tile_is_DUO :
                TOTAL_X["right"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] + 70
                tile_y = previous_position[1] - 17

            #if this tile is NOT DUO
            else :

                if previous_tile_is_DUO :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 36
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 70
                    tile_y = previous_position[1]

        #reached the right end of the window
        else :

            #PLAY TO DOWN DIRECTION
            if TOTAL_Y["down"] < resolution[1]/4 - 110 : # change main_window_resolution[1]

                #this is the first tile to be played in the DOWN direction
                if this_is_first_DOWN_tile :
                    this_is_first_DOWN_tile = 0

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] + 70

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                            #act like the next tile will be the first DOWN,
                            #because if it didn't, the computer would think that
                            #this tile was horizontal, which causes calculation error
                            this_is_first_DOWN_tile = 1

                        else :
                            TOTAL_Y["down"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0] + 34
                            tile_y = previous_position[1] + 36

                #this is NOT the first tile to be played in the DOWN direction
                else :

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] + 36

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 36

                        else :
                            TOTAL_Y["down"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] + 70

            #PLAY TO LEFT DIRECTION (REVERSED TILES)
            else :

                #if this tile is the first tile to be played LEFT
                if this_is_first_LEFT_tile :
                    this_is_first_LEFT_tile = 0

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    ##if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 70

                            #act like the next tile will be the first LEFT,
                            #because if it didn't, the computer would think that
                            #this tile was vertical, which causes calculation error
                            this_is_first_LEFT_tile = 1

                        else :
                            #we will add 36 to TOTAL_Y["up"] because if we didn't, next
                            #time it would be considered "first time right" again
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1] + 34
                            reverse_tile = 1

                #if this tile is NOT the first tile to be played LEFT
                else :

                    #if the previous tile was DUO
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #if the previous tile was NOT DUO
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17

                        else :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #ADD THE PLAYED TILE TO THE PLAYED_TILES LIST
        PLAYED_TILES.append([tile,(tile_x, tile_y)])


    #if the programmer didn't pass the place variable, raise an exception
    else :
        raise ValueError

    #Create a Tile object
    if reverse_tile :
        temp_tile = Tile(tile[1], tile[0], screen, tile_x, tile_y)
    else :
        temp_tile = Tile(tile[0], tile[1], screen, tile_x, tile_y)

    #show the tile according to it's suitable orientation
    if orientation == "horizontal" :
        temp_tile.show_horizontal()

    else :
        temp_tile.show_vertical()

#----------------------------------------------------------------------------

def computer_play(auto_player, comp, screen):
    '''
    computer_play(auto_player, screen)
        this function takes an object from the Computer class and a display,
        then it does all the necessary actions related to the computer player.
    '''
    
    #identify __PASS__ as global variable
    global __PASS__

    playedtile_sound = path.join('sounds','playedtile.wav')
    playedtile_soundtrack = pygame.mixer.Sound(playedtile_sound)
    playedtile_soundtrack.set_volume(0.9)

    # function to get the domino in left of the chain and right of the chain
    #calculateChain()

    #Ask the computer to play
    
    chosen_tile = auto_player.play(PLAYED_TILES)
        
    if chosen_tile != "PASS" :
        final_tile = tile_check(chosen_tile)
        pygame.time.wait(1000)
        pygame.event.clear()
        play(final_tile[0], screen, final_tile[1])
        playedtile_soundtrack.play(0)

        if comp == 2 or comp==3:
            hide_tile(chosen_tile[1][0], chosen_tile[1][1], True, screen)
        else:
            hide_tile(chosen_tile[1][0], chosen_tile[1][1], False, screen)

        #set the __PASS__ flag to off
        __PASS__ = 0

        #refresh the display
        pygame.display.update()

    #if the computer said "PASS"
    else :

        #If the human said "PASS" last time, End the game
        if __PASS__ == 1 :
            END_GAME(screen)
            return

        #If the human didn't say "PASS" last time, set __PASS__ to 1
        else :
            ############
            if comp==2 and NUMBER_OF_PLAYERS==4:
                __PASS__ = 1
            elif NUMBER_OF_PLAYERS==2:
                __PASS__ = 1

            computer_note_x = main_window_resolution[0]/2 - 196
            computer_note_y = main_window_resolution[1]/2 - 190

            computer_note_img = pygame.image.load("images/computer_passed.png")
            clear_img = pygame.image.load("images/clear.png")

            note_sound = path.join('sounds','note.wav')
            note_soundtrack = pygame.mixer.Sound(note_sound)
            note_soundtrack.set_volume(0.9)

            note_soundtrack.play(0)
            screen.blit(computer_note_img,(computer_note_x,computer_note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(computer_note_x,computer_note_y))


    #check if the human can't play.
    if not human_has_suitable_tile() :
        print(comp)
        #if the computer passed last time, then the game is ended
        if __PASS__ == 1 :
            END_GAME(screen)

        #if the game isn't ended, change the pass button image to green
        else :
            switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def human_play4(tile, exact_tile, screen, position, auto_player,auto_player2,auto_player3):
    '''
    human_play(tile, exact_tile, screen, position, auto_player)
        this function is responsible for all the actions that should be
        taken when the human clicks on a suitable tile.
    '''

    global __PASS__

    playedtile_sound = path.join('sounds','playedtile.wav')
    playedtile_soundtrack = pygame.mixer.Sound(playedtile_sound)
    playedtile_soundtrack.set_volume(0.9)

    #play the human tile
    playedtile_soundtrack.play(0)
    play(exact_tile, screen, position)
    HUMAN_TILES.remove(tile)
    hide_tile(tile[1][0], tile[1][1],False, screen )

    #set the __PASS__ flag to off
    __PASS__ = 0

    #refresh the display before the computer plays
    #because the computer will sleep for one second
    pygame.display.update()

    #check if the human finished his tiles, end the game
    if len(HUMAN_TILES) == 0 :
        END_GAME(screen)

    #if the human didn't finish his tiles
    else :

        #ask the computer to play
        computer_play(auto_player3, 3,screen)
        computer_play(auto_player, 1, screen)
        computer_play(auto_player2, 2,screen)
        

        #check if the computer finished his tiles, end the game
        if len(COMPUTER_TILES) == 0 or len(COMPUTER_TILES2) == 0 or len(COMPUTER_TILES3) == 0 :
            END_GAME(screen)

        #check if the human can't play.
        elif not human_has_suitable_tile() :

            #if the computer passed last time, then the game is ended
            if __PASS__ == 1 :
                END_GAME(screen)

            #if the game isn't ended, change the pass button image to green
            else :
                switch_pass_button("enable", screen)

#----------------------------------------------------------------------------
def human_play(tile, exact_tile, screen, position, auto_player):
    '''
    human_play(tile, exact_tile, screen, position, auto_player)
        this function is responsible for all the actions that should be
        taken when the human clicks on a suitable tile.
    '''

    global __PASS__

    playedtile_sound = path.join('sounds','playedtile.wav')
    playedtile_soundtrack = pygame.mixer.Sound(playedtile_sound)
    playedtile_soundtrack.set_volume(0.9)

    #play the human tile
    playedtile_soundtrack.play(0)
    play(exact_tile, screen, position)
    HUMAN_TILES.remove(tile)
    hide_tile(tile[1][0], tile[1][1],False, screen )

    #set the __PASS__ flag to off
    __PASS__ = 0

    #refresh the display before the computer plays
    #because the computer will sleep for one second
    pygame.display.update()

    #check if the human finished his tiles, end the game
    if len(HUMAN_TILES) == 0 :
        END_GAME(screen)

    #if the human didn't finish his tiles
    else :

        #ask the computer to play
        computer_play(auto_player, 1, screen)
        

        #check if the computer finished his tiles, end the game
        if len(COMPUTER_TILES) == 0 :
            
            END_GAME(screen)

        #check if the human can't play.
        elif not human_has_suitable_tile() :
            
            #if the computer passed last time, then the game is ended
            if __PASS__ == 1 :
                END_GAME(screen)

            #if the game isn't ended, change the pass button image to green
            else :
                switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def hide_tile(x, y, flag, screen):
    '''
    hide_tile(x, y, screen)
        this function takes the position of a tile, then it hides it
        with the color defined on the global variable HIDE_TILE_COLOR.
    '''

    if flag:
        #print("Domino 2 and 3: ", x, y)
        hiding_rectangle = Rect(x, y, 68, 34)
        pygame.draw.rect(screen, HIDE_TILE_COLOR, hiding_rectangle) 
    else:
        # print("Domino 1: ", x, y)
        hiding_rectangle = Rect(x, y, 34, 68)
        pygame.draw.rect(screen, HIDE_TILE_COLOR, hiding_rectangle)

#----------------------------------------------------------------------------

def clear_area(x, y, width, height, screen, fill_color):
    '''
    clear_area(x, y, width, height, screen, fill_color)
        this function hides anything with your desired color.
    '''

    hiding_rectangle = Rect(x, y, width, height)
    pygame.draw.rect(screen, fill_color, hiding_rectangle)

#----------------------------------------------------------------------------

def switch_pass_button(action, screen):
    '''
    switch_pass_button(action, screen)
        switches the PASS button to "enabled", or "disabled", according
        to the action that you pass to it "enable", or "disable".
    '''

    #initialize the PASS_BUTTON_STATUS as global variable
    global PASS_BUTTON_STATUS

    #the action is to disable pass button
    if action == "enable" :

        #clear the place of the pass button
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #change the pass button image back to green
        pass_button_image = pygame.image.load("images/active_pass.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #change the PASS_BUTTON_STATUS to be enabled
        PASS_BUTTON_STATUS = 1

        #refresh the display
        pygame.display.update()


    #the action is to enable the pass button
    elif action == "disable" :

        #clear the place of the pass button
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #change the pass button image back to red
        pass_button_image = pygame.image.load("images/deactive_pass.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #change the PASS_BUTTON_STATUS to be disabled
        PASS_BUTTON_STATUS = 0

        #refresh the display
        pygame.display.update()


    #if the programmer didn't pass the action correctly
    else :
        raise ValueError

#----------------------------------------------------------------------------

def human_has_suitable_tile():
    """
    human_has_suitable_tile()
        this function returns True if there is any suitable
        tile to be played, in the HUMAN_TILES list.
    """

    #If this is the first tile to be played, then the human
    #has some suitable tiles. So, return True.
    if len(PLAYED_TILES) == 0 :
        return True

    left_value = PLAYED_TILES[0][0][0]
    right_value = PLAYED_TILES[-1][0][1]

    for tile in HUMAN_TILES :

        #if we found a suitable tile, stop and return True
        if (left_value in tile[0]) or (right_value in tile[0]) :
            return True

        else :
            continue

    #if the loop finished without finding any suitable tiles, return False
    return False

#----------------------------------------------------------------------------

def left_or_right(screen):
    '''
    left_or_right(screen)
        this function is called whenever the human clicks on a tile that can be
        played on both sides, then it takes all the necessary actions like drawing
        the two green arrows and switching the game to the BOTH_SIDES mode.
    '''

    left_image = pygame.image.load("images/left.png")
    right_image = pygame.image.load("images/right.png")

    x1 = PASS_BUTTON_PLACE[0] + 5
    y1 = PASS_BUTTON_PLACE[1] - 30

    x2 = PASS_BUTTON_PLACE[0] + 62
    y2 = PASS_BUTTON_PLACE[1] - 30

    for i in range(2) :

        screen.blit(left_image,(x1, y1))
        screen.blit(right_image,(x2, y2))

        pygame.display.update()

        pygame.time.wait(200)

        clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)

        pygame.display.update()

        pygame.time.wait(200)

    screen.blit(left_image,(x1, y1))
    screen.blit(right_image,(x2, y2))

#----------------------------------------------------------------------------

def check_if_clicked_on_exit(screen, x, y, check_for_popup = 0):
    '''
    check_if_clicked_on_exit(screen, x, y, check_for_popup = 0)
        this function checks if the human clicked on the "exit"
        or "replay" buttons, then it takes the necessary actions
        according to that.
    '''
    global NUMBER_OF_PLAYERS
    global PLAYED_TILES

    #Checking whether the user clicked on the REPLAY button
    if x > REPLAY_BUTTON_PLACE[0] and x < (REPLAY_BUTTON_PLACE[0] + 81)\
     and y > REPLAY_BUTTON_PLACE[1] and y< (REPLAY_BUTTON_PLACE[1] + 29) :

        pressed_replay = pygame.image.load("images/pressed_replay.png")
        screen.blit(pressed_replay, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        PLAYED_TILES = []
        RESET_GAME()

    # Player number buttons
    if x > BUTTON_2_PLACE[0] and x < (BUTTON_2_PLACE[0] + 21)\
     and y > BUTTON_2_PLACE[1] and y< (BUTTON_2_PLACE[1] + 29) :
        
        NUMBER_OF_PLAYERS = 2
        PLAYED_TILES = []
        RESET_GAME()

    if x > BUTTON_4_PLACE[0] and x < (BUTTON_4_PLACE[0] + 21)\
     and y > BUTTON_4_PLACE[1] and y< (BUTTON_4_PLACE[1] + 29) :
        
        NUMBER_OF_PLAYERS = 4
        PLAYED_TILES = []
        RESET_GAME()

    #Checking whether the user clicked on a the EXIT button
    elif x > EXIT_BUTTON_PLACE[0] and x < (EXIT_BUTTON_PLACE[0] + 81)\
     and y > EXIT_BUTTON_PLACE[1] and y< (EXIT_BUTTON_PLACE[1] + 29) :

        pressed_exit = pygame.image.load("images/pressed_exit.png")
        screen.blit(pressed_exit,(EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        exit()


    #if the user want to check on the POPUP message too
    if check_for_popup == 1 :

        #Load the highlight image
        button_highlight_img = pygame.image.load("images/on_clicked_button.png")

        #load the needed sound files
        replay_sound = path.join('sounds','replay.wav')
        replay_soundtrack = pygame.mixer.Sound(replay_sound)
        replay_soundtrack.set_volume(0.9)

        cancelReplay_sound = path.join('sounds','cancel_replay.wav')
        cancelReplay_soundtrack = pygame.mixer.Sound(cancelReplay_sound)
        cancelReplay_soundtrack.set_volume(0.9)

        #get the place of the POP UP message
        popup_x = main_window_resolution[0]/2 - 252
        popup_y = main_window_resolution[1]/2 - 173

        #if the player clicked on the exit button on the POP UP message
        if x > (popup_x + 113) and x < (popup_x + 230)\
         and y > (popup_y + 286) and y< (popup_y + 334) :
            screen.blit(button_highlight_img,(popup_x + 115,popup_y + 288))
            cancelReplay_soundtrack.play(0)
            pygame.display.update()
            pygame.time.wait(100)
            #exit the game
            exit()

        #if the player clicked on the replay button on the POP UP message
        elif x > (popup_x + 278) and x < (popup_x + 395)\
         and y > (popup_y + 288) and y< (popup_y + 336) :
            screen.blit(button_highlight_img,(popup_x + 278,popup_y + 288))
            replay_soundtrack.play(0)
            pygame.display.update()
            pygame.time.wait(500)
            #reset the game
            PLAYED_TILES = []
            RESET_GAME()

#----------------------------------------------------------------------------

def check_if_clicked_on_pass(screen, auto_player, num, x, y):
    '''
    check_if_clicked_on_pass(screen, auto_player, x, y)
        this function checks if the human clicked on the "PASS"
        button, then it takes the necessary actions according to that.
    '''

    global __PASS__

    #Checking whether the user clicked on a the PASS button
    if x > PASS_BUTTON_PLACE[0] and x < (PASS_BUTTON_PLACE[0] + 99)\
     and y > PASS_BUTTON_PLACE[1] and y < (PASS_BUTTON_PLACE[1] + 44):

        #if the human has any suitable tiles to play, ignore him
        if human_has_suitable_tile() :

            #load the required image
            bad_pass = pygame.image.load("images/bad_pass.png")
            clear_img = pygame.image.load("images/clear.png")

            #note message coordinates
            note_x = main_window_resolution[0]/2 - 196
            note_y = main_window_resolution[1] - main_window_resolution[1]/4 -35

            #load the sound file
            note_sound = path.join('sounds','note.wav')
            note_soundtrack = pygame.mixer.Sound(note_sound)
            note_soundtrack.set_volume(0.9)

            #view the note and play the sound
            note_soundtrack.play(0)
            screen.blit(bad_pass,(note_x, note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(note_x,note_y))

        #if the human DOESN'T have any suitable tiles to played.
        else :
            #check if the __PASS__ flag is ON, end the game
            if __PASS__ == 1 :
                END_GAME(screen)

            else :

                #set the __PASS__ flag to on
                __PASS__ = 1

                #disable the pass button
                switch_pass_button("disable", screen)

                #ask the computer to play
                computer_play(auto_player, num, screen)

                #check if the computer finished his tiles, end the game
                if len(COMPUTER_TILES) == 0 :
                    
                    
                    END_GAME(screen)

        return True

    else :
        return False

#----------------------------------------------------------------------------

def score_count(WHOS_TILE):
    '''
    score_count(WHOS_TILE)
        this function takes a "tiles list" and returns the score count.
    '''

    tiles_length = len(WHOS_TILE)
    tiles_count = 0
    for i in range(0, tiles_length):
        tiles_count += WHOS_TILE[i][0][0]
        tiles_count += WHOS_TILE[i][0][1]
    return tiles_count

#----------------------------------------------------------------------------

def END_GAME(screen):
    '''
    END_GAME(screen)
        This function is called when the game ends.
        It determines who has won and prints the suitable message
        then it switches the game into the GAME_OVER mode.
    '''

    #constructing game_over_bg designs
    game_over_bg = pygame.image.load("images/game_over_bg.png")
    won_game_img = pygame.image.load("images/you_won_img.png")
    lose_game_img = pygame.image.load("images/you_lose_img.png")
    game_drawn_img = pygame.image.load("images/drawn_img.png")

    # constructing x,y for the game_over_bg
    draw_x = main_window_resolution[0]/2 - 252
    draw_y = main_window_resolution[1]/2 - 173

    #identify GAME_OVER as global variable
    global GAME_OVER
    global i
    global NUMBER_OF_PLAYERS

    #set the GAME_OVER flag to on
    GAME_OVER = 1

    #count both human's and computer's points
    human_score = score_count(HUMAN_TILES)
    computer_score = score_count(COMPUTER_TILES)
    computer_score2 = score_count(COMPUTER_TILES2)
    computer_score3 = score_count(COMPUTER_TILES3)

    #if the human won
    if NUMBER_OF_PLAYERS==4:
        if human_score == 0 or   human_score+computer_score < computer_score2+computer_score3:

            winner_sound = path.join('sounds','game_over_win.wav')
            winner_soundtrack = pygame.mixer.Sound(winner_sound)
            winner_soundtrack.set_volume(0.9)

            winner_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(won_game_img,(draw_x + 120, draw_y + 220))

        #if the computer won
        elif human_score+computer_score > computer_score2+computer_score3:

            loser_sound = path.join('sounds','game_over_lose.wav')
            loser_soundtrack = pygame.mixer.Sound(loser_sound)
            loser_soundtrack.set_volume(0.9)

            loser_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(lose_game_img,(draw_x + 141, draw_y + 220))

        #if the game ended draw
        else :

            nonwinner_sound = path.join('sounds','none_winer.wav')
            nonwinner_soundtrack = pygame.mixer.Sound(nonwinner_sound)
            nonwinner_soundtrack.set_volume(0.9)

            nonwinner_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(game_drawn_img,(draw_x + 187, draw_y + 220))
        
        #constructing the font score_text and render it to the screen
        font = pygame.font.SysFont("arial", 25)
        screen.blit(font.render(str(human_score+computer_score),True,(0,0,0)),(draw_x + 365,draw_y + 113))
        screen.blit(font.render(str(computer_score2+computer_score3),True,(0,0,0)),(draw_x + 365,draw_y + 166))

    elif NUMBER_OF_PLAYERS==2:
        if human_score < computer_score :

            winner_sound = path.join('sounds','game_over_win.wav')
            winner_soundtrack = pygame.mixer.Sound(winner_sound)
            winner_soundtrack.set_volume(0.9)

            winner_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(won_game_img,(draw_x + 120, draw_y + 220))

        #if the computer won
        elif human_score > computer_score :

            loser_sound = path.join('sounds','game_over_lose.wav')
            loser_soundtrack = pygame.mixer.Sound(loser_sound)
            loser_soundtrack.set_volume(0.9)

            loser_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(lose_game_img,(draw_x + 141, draw_y + 220))

        #if the game ended draw
        else :

            nonwinner_sound = path.join('sounds','none_winer.wav')
            nonwinner_soundtrack = pygame.mixer.Sound(nonwinner_sound)
            nonwinner_soundtrack.set_volume(0.9)

            nonwinner_soundtrack.play(0)
            screen.blit(game_over_bg,(draw_x,draw_y))
            screen.blit(game_drawn_img,(draw_x + 187, draw_y + 220))

        #constructing the font score_text and render it to the screen
        font = pygame.font.SysFont("arial", 25)
        screen.blit(font.render(str(human_score),True,(0,0,0)),(draw_x + 365,draw_y + 113))
        screen.blit(font.render(str(computer_score),True,(0,0,0)),(draw_x + 365,draw_y + 166))

    

#----------------------------------------------------------------------------

def storePoints(gameNo,computer):
    points = open("points.txt","a")
    str1 = [str(gameNo), " ", str(computer), "\n"]
    points.writelines(str1)

#----------------------------------------------------------------------------

def RESET_GAME():
    '''
    RESET_GAME()
        Resets all game counters and flags, redistribute new tiles
        to all players and redraw everything on the screen.
    '''

    global __PASS__
   # global NUMBER_OF_PLAYERS
    global HUMAN_TILES
    global COMPUTER_TILES
    global COMPUTER_TILES2
    global COMPUTER_TILES3
    

    global PLAYED_TILES

    global REPLAY_BUTTON_PLACE
    global EXIT_BUTTON_PLACE
    global PASS_BUTTON_PLACE

    global TOTAL_X
    global TOTAL_Y

    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile

    global GAME_OVER

    global BOTH_SIDES

    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_RESULT

    global PASS_BUTTON_STATUS


    __PASS__ = 0

    HUMAN_TILES = []
    COMPUTER_TILES = []
    COMPUTER_TILES2 = []
    COMPUTER_TILES3 = []

    PLAYED_TILES = []

    REPLAY_BUTTON_PLACE = [0, 0]
    EXIT_BUTTON_PLACE = [0, 0]
    PASS_BUTTON_PLACE = [0, 0]

    TOTAL_X = {"left":0, "right":0}
    TOTAL_Y = {"up":0, "down":0}

    this_is_first_DOWN_tile = 1
    this_is_first_LEFT_tile = 1
    this_is_first_UP_tile = 1
    this_is_first_RIGHT_tile = 1

    GAME_OVER = 0

    BOTH_SIDES = 0

    ARGUMENTATIVE_TILE = None
    ARGUMENTATIVE_RESULT = None

    PASS_BUTTON_STATUS = 0
    main()

#----------------------------------------------------------------------------

def main():
    '''
    main()
        the main Dominos function. Initializes the game and starts the main game loop.
    '''

    #identify the global variables
    global __PASS__
    global GAME_OVER
    global BOTH_SIDES
    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_TILE_CHECK_RESULT
    global complete_tiles
    global NUMBER_OF_PLAYERS

    #note message coordinates
    note_x = main_window_resolution[0]/2 - 196
    note_y = main_window_resolution[1] - main_window_resolution[1]/4 -35

    #Initialize PyGame
    pygame.init()

    #adding window icon
    seticon('images/icon.png')

    #create the Main window
    screen = pygame.display.set_mode(main_window_resolution)
    #screen = pygame.display.set_mode(main_window_resolution,FULLSCREEN, 32)
    pygame.display.set_caption("Dominos!")

    #load the sound file
    note_sound = path.join('sounds','note.wav')
    note_soundtrack = pygame.mixer.Sound(note_sound)
    note_soundtrack.set_volume(0.9)

    #load needed images
    bad_tile = pygame.image.load("images/bad_tile.png")
    clear_img = pygame.image.load("images/clear.png")

    #initialize the game
    initialize(screen)
    if NUMBER_OF_PLAYERS==4:
        auto_player =  computer(COMPUTER_TILES)
        auto_player2 = computerMinimax(COMPUTER_TILES2)
        auto_player3 = computer(COMPUTER_TILES3)
    else:
        auto_player =  computer(COMPUTER_TILES)
    auto_player.complete_tiles = complete_tiles

    # For computer Hint
    human_hint = computerMinimax(HUMAN_TILES)

#####################  MAIN LOOP  #######################
    r = random.randint(0, len(HUMAN_TILES)-1)
    while True:

        # Hint 
        myfont = pygame.font.SysFont('Sans serif', 30)
        if len(PLAYED_TILES) == 0: # If played tiles = 0 to prevent errors
            if len(HUMAN_TILES)==7:
                textsurface = myfont.render('Hint: (4,5)' , False, (0, 0, 0)) 
                screen.blit(textsurface,(480,850))
            else:
                textsurface = myfont.render('Hint: ' + str(HUMAN_TILES[r][0]), False, (0, 0, 0)) 
                screen.blit(textsurface,(480,850))
        elif GAME_OVER != 1 : # check if game is over or function will call minmax and error will be produced
            temp = human_hint.minmax(PLAYED_TILES)
            textsurface = myfont.render('Hint: ' + str(temp[0]), False, (0, 0, 0)) 
            screen.blit(textsurface,(480,850))
        
        #Handling PyGame events
        event = pygame.event.wait()

        #Handling the QUIT signal
        if event.type == QUIT:
            exit()

        #if the game has ended.
        elif GAME_OVER == 1 :

            #check only on the "MOUSEBUTTONDOWN" event if it clicked on the exit button
            if event.type == MOUSEBUTTONDOWN :

                #get the mouse position
                x, y = event.pos

                #check if the user clicked on the exit or replay buttons
                check_if_clicked_on_exit(screen, x, y, 1)



        #Handling the Mouse Events IF THE PLAYER CAN PLAY ON BOTH SIDES
        elif BOTH_SIDES == 1 :

            if event.type == MOUSEBUTTONDOWN :

                #get the mouse position
                x, y = event.pos

                #check if the user clicked on the exit or replay buttons
                check_if_clicked_on_exit(screen, x, y)

                #get the place of the arrows
                x1 = PASS_BUTTON_PLACE[0] + 5
                y1 = PASS_BUTTON_PLACE[1] - 30
                x2 = PASS_BUTTON_PLACE[0] + 62
                y2 = PASS_BUTTON_PLACE[1] - 30

                #if the user chose to play to the left
                if x > x1 and x < (x1 + 30) and y > y1 and y < (y1 + 22) :

                    #clear the arrows from the screen
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0
                    if NUMBER_OF_PLAYERS == 2:
                        human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[2], screen, ARGUMENTATIVE_RESULT[3], auto_player)
                    elif NUMBER_OF_PLAYERS==4:
                        human_play4(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[2], screen, ARGUMENTATIVE_RESULT[3], auto_player,auto_player2,auto_player3)

                #if the user chose to play to the right
                elif x > x2 and x < (x2 + 30) and y > y2 and y < (y2 + 22) :

                    #clear the arrows from the screen
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0
                    if NUMBER_OF_PLAYERS == 2:
                        human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[0], screen, ARGUMENTATIVE_RESULT[1], auto_player)
                    elif NUMBER_OF_PLAYERS == 4:
                        human_play4(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[0], screen, ARGUMENTATIVE_RESULT[1],auto_player,auto_player2,auto_player3)


        #Handling the Mouse Events IF THE GAME IS STILL RUNNING
        elif event.type == MOUSEBUTTONDOWN :

            #get the mouse position
            x,y = event.pos

            check_if_clicked_on_exit(screen, x, y)

            #Checking whether the user clicked on a the PASS button
            if check_if_clicked_on_pass(screen, auto_player, 1, x, y):
                continue
            elif  NUMBER_OF_PLAYERS==4 and check_if_clicked_on_pass(screen, auto_player2, 2, x, y):
                continue 
            elif NUMBER_OF_PLAYERS==4 and check_if_clicked_on_pass(screen, auto_player3, 3, x, y) :
                continue 

            #check if the user clicked on a tile
            else :
                # Remove Previous Hit
                screen.fill(pygame.Color(109,72,31), (480,850, 400,80))

                #loop over the HUMA_TILES
                for tile in HUMAN_TILES :

                    #if the human clicked on a tile
                    if clicked_on_tile(event.pos, tile[1]):

                        #check where to play the tile
                        result = tile_check(tile)

                        #if the user clicked on a NON-SUITABLE tile
                        if result is None :
                            note_soundtrack.play(0)
                            screen.blit(bad_tile,(note_x,note_y))
                            pygame.display.update()
                            pygame.time.wait(2000)
                            screen.blit(clear_img,(note_x,note_y))

                        #if the user clicked on a suitable
                        elif len(result) == 2 :
                            if NUMBER_OF_PLAYERS == 2:
                                human_play(tile, result[0], screen, result[1], auto_player)
                            elif NUMBER_OF_PLAYERS == 4:
                                human_play4(tile, result[0], screen, result[1], auto_player,auto_player2,auto_player3)

                        #if the tile can be played on both sides
                        elif len(result) == 4 :
                            BOTH_SIDES = 1
                            ARGUMENTATIVE_TILE = tile
                            ARGUMENTATIVE_RESULT = result
                            left_or_right(screen)
            
        # hit escape to exit
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

        pygame.display.update()


#run the game if the module was called independently
if __name__ == "__main__":
    main()


