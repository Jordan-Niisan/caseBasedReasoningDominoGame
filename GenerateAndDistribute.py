from random import randrange

def generate_tiles():
    """ generate_tiles()
        this function takes nothing and returns a complete dominos list of 28 elements
    each element of this list is a "tuple".
    """
    # TODO (DONE) make two loops instead of this mess :D
    temp = []
    for i in range(0,7):
        for j in range(i,7):
            temp.append((i,j))
    temp.remove((0,0))
    return temp

#----------------------------------------------------------------------------

def distribute_tiles(tiles_set, players_count):
    """
    distribute_tiles(tiles_set, players_count)
        Takes a complete dominos list and returns a list of lists
        each list contains 7 tiles as Tuples.
        WARNING! "players_count" should be less than 4.
    """
    
    #check the validity of the number of players
    if players_count > 4 :
        raise ValueError

    #create an empty list of lists, to hold the players' tiles
    final_list= [[] for x in range(players_count)]

    #fill the "final_list" with random tiles
    for i in range(0, 7):
        for j in range(players_count):
            random_number = randrange(0, len(tiles_set))
            # TODO (DONE) use the 'pop' method instead of the following active two lines
            final_list[j].append(tiles_set.pop(random_number))

    final_list = [ [(6, 6), (2, 6), (1, 4), (5, 5), (5, 6), (1, 3), (4, 5)] , [(1, 6), (2,3), (0, 1), (3, 3), (0, 6), (3, 5), (2, 4)],[(4, 4), (2, 5), (1, 5), (3, 4), (0, 0), (4, 6), (0, 5)], [(0, 3), (0, 4), (1,1), (2, 2), (0, 2), (1, 2), (3, 6)]]
    #final_list = [ [(3, 3), (4, 6), (1, 6), (2, 4), (4, 4), (1, 3), (5, 6)] , [(0, 0), (3,6), (0, 2), (3, 5), (4, 5), (1, 1), (0, 5)],[(2, 5), (1, 5), (1, 2), (5, 5), (2, 2), (1, 4), (6, 6)], [(2, 6), (3, 4), (0,6), (0, 4), (0, 3), (0, 1), (2, 3)]]
    #final_list = [ [(3, 3), (1, 1), (2, 2), (5, 5), (4, 4), (0, 0), (6, 6)] , [(1, 3), (3,6), (0, 2), (3, 5), (4, 5), (4, 6), (0, 5)],[(2, 5), (1, 5), (1, 2), (2, 4), (1, 6), (1, 4), (5, 6)], [(2, 6), (3, 4), (0,6), (0, 4), (0, 3), (0, 1), (2, 3)]]
    #final_list = [ [(2, 1), (2, 0), (2, 4), (6, 4), (2, 5), (2, 6), (1, 1)] , [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (5, 6)]]
    return final_list

#----------------------------------------------------------------------------
