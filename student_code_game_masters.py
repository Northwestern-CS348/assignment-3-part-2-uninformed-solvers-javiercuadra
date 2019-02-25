from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        '''
        Pseudo Code
        Go through each peg and get bindings
            If no bindings, return empty tuple
            If has bindings,
                Cycle through bindings to get the disks on the peg
                put them in a tuple.
            Create tuple of the current peg
        Return tuple of all three pegs' tuples


        '''
        peg1_ask = parse_input("fact: (on ?x peg1)")
        peg2_ask = parse_input("fact: (on ?x peg2)")
        peg3_ask = parse_input("fact: (on ?x peg3)")

        peg1_bindings = self.kb.kb_ask(peg1_ask)
        peg2_bindings = self.kb.kb_ask(peg2_ask)
        peg3_bindings = self.kb.kb_ask(peg3_ask)


        all_peg_bindings = [peg1_bindings, peg2_bindings, peg3_bindings]

        game_state = []

        # Cycle through each peg
        for peg_bindings in all_peg_bindings:
            disks_on_peg = []
            if peg_bindings:
                for peg_binding in peg_bindings:
                    for disk_name in peg_binding.bindings:
                        disk_number = int(str(disk_name)[-1])
                        disks_on_peg.append(disk_number)
                        disks_on_peg.sort()

            game_state.append(tuple(disks_on_peg))

        game_state = tuple(game_state)
        return game_state


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        '''
        Check if it is a movable statement
            If is a movable, check if it is a legal movable
                If it is legal, 
                    Check if new peg is empty
                        If newpeg is empty, retract that it is empty
                        If not, then do nothing
                    Add that it is on new peg and that it is on top
                    Retract that it is on old peg and on top of the old peg
                    Check if old peg is now empty
                        If old peg is now empty, assert that it is empty
                        If not, then do nothing
                If it is not legal, return error
            If it is not a movable, return error


        '''

        #Get names of terms
        movable_disk = str(movable_statement.terms[0])
        initial_peg = str(movable_statement.terms[1])
        destination_peg = str(movable_statement.terms[2])

        #Remove old disk location and top

        old_disk_location = Fact(["on", movable_disk, initial_peg])
        old_disk_top = Fact(["top", movable_disk, initial_peg])

        self.kb.kb_retract(old_disk_location)
        self.kb.kb_retract(old_disk_top)

        below_movable_disk_fact = Fact(["onTopOf", movable_disk, "?disk"])
        below_movable_disk_ask = self.kb.kb_ask(below_movable_disk_fact)

        if below_movable_disk_ask:
            below_movable_disk = str(below_movable_disk_ask[0].bindings[0].constant)
            old_onTopOf = Fact(["onTopOf", movable_disk, below_movable_disk])
            new_initial_top = Fact(["top", below_movable_disk, initial_peg])
            self.kb.kb_retract(old_onTopOf)
            self.kb.kb_assert(new_initial_top)
        else:
            new_initial_empty = Fact(["empty", initial_peg])
            self.kb.kb_assert(new_initial_empty)

        destination_empty_fact = Fact(["empty", destination_peg])
        destination_empty_ask = self.kb.kb_ask(destination_empty_fact)

        if destination_empty_ask:
            self.kb.kb_retract(destination_empty_fact)
        else:
            old_destination_top_fact = parse_input("fact: (top ?disk " + destination_peg + ")")
            old_destination_top_ask = self.kb.kb_ask(old_destination_top_fact)
            old_destination_top = str(old_destination_top_ask[0].bindings[0].constant)
            old_top_destination = Fact(["top", old_destination_top, destination_peg])
            new_onTopOf = Fact(["onTopOf", movable_disk, old_destination_top])
            self.kb.kb_retract(old_top_destination)
            self.kb.kb_assert(new_onTopOf)


        new_disk_location = Fact(["on", movable_disk, destination_peg])
        new_disk_top = Fact(["top", movable_disk, destination_peg])

        self.kb.kb_assert(new_disk_location)
        self.kb.kb_assert(new_disk_top)

        return






    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here

        '''
        Cycle through first row
        Get the tiles in those positions (bindings)
        Create tuple for the three tiles (first row)
        Repeat for 2nd and 3rd rows
        return tuple of tuples
        '''
        # Create a list of the rows to cycle through
        all_rows = ["pos1", "pos2", "pos3"]

        # Create a game state list to store all the peg tuples
        game_state = []
        # Cycle through each row
        for row in all_rows:
            # Create an empty list to hold the row state
            row_state = [-1, -1, -1]
            # Create the fact that will be asked to the KB to find which tiles are in the current row
            my_fact = parse_input("fact: (coordinate ?tile ?x " + row + ")")
            # Find out which disks are on the current peg
            tiles_on_row = self.kb.kb_ask(my_fact)
            # Cycle through each tile in the row
            for tile in tiles_on_row:
                # Get the binding from the binding dictionary for the position
                pos_num = tile.bindings_dict["?x"]
                # Get rid of the pos part of the position
                pos_num = pos_num.replace("pos", "")
                # Turn the pos number into an integer
                pos_num = int(pos_num)
                # Get the binding from the binding dictionary for the tile
                tile_num = tile.bindings_dict["?tile"]
                # Check if the tile is empty
                if tile_num != "empty":
                    # Get rid of the tile part of the name
                    tile_num = tile_num.replace("tile", "")
                    # Turn the tile number into an integer
                    tile_num = int(tile_num)
                    # Append the current disk to the peg state list
                    row_state[pos_num - 1] = tile_num
            # Create a tuple of the tiles in the row from the list of the tiles in the row
            row_state_tuple = tuple(row_state)
            # Append the tuple of the disks on the peg to the game state list
            game_state.append(row_state_tuple)

        # Create a tuple of the game state from the game state list
        game_state_tuple = tuple(game_state)
        # Return the tuple of the game state
        return game_state_tuple

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        '''
        Check if it is a movable statement
            If is a movable, check if it is a legal movable
                If it is legal, 
                    Flip positions for tile moved and empty and reassert
                    Retract old positions
                If it is not legal, return error
            If it is not a movable, return error
        '''
        tile_name = str(movable_statement.terms[0])
        initial_x = str(movable_statement.terms[1])
        initial_y = str(movable_statement.terms[2])
        destination_x = str(movable_statement.terms[3])
        destination_y = str(movable_statement.terms[4])

        empty_tile = Fact(["coordinate", "empty", initial_x, initial_y])
        new_tile = Fact(["coordinate", tile_name, destination_x, destination_y])
        old_empty_tile = Fact(["coordinate", "empty", destination_x, destination_y])
        old_tile = Fact(["coordinate", tile_name, initial_x, initial_y])

        self.kb.kb_assert(empty_tile)
        self.kb.kb_assert(new_tile)
        self.kb.kb_retract(old_empty_tile)
        self.kb.kb_retract(old_tile)
        return


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
