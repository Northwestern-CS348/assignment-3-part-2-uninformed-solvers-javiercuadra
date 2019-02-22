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
        # Create a list to cycle through containing all the pegs
        all_pegs = ["peg1", "peg2", "peg3"]
        # Create a game state list to store all the peg tuples
        game_state = []

        # Cycle through each peg
        for peg in all_pegs:
            # Create a list to store the disks if they are in the pegs
            peg_state = []
            # Create the fact that will be asked in the KB to find which disks are on the current peg
            my_fact = parse_input("fact: (on ?x " + peg + ")")
            # Find out which disks are on the current peg
            disks_on_peg = self.kb.kb_ask(my_fact)

            # Check if the peg is empty
            if disks_on_peg:
                # Cycle through each binding of a disk on the peg
                for disk_on_peg in disks_on_peg:
                    # Get the binding from the binding dictionary
                    disk_num = disk_on_peg.bindings_dict["?x"]
                    # Get rid of the disk part of the name
                    disk_num = disk_num.replace("disk", "")
                    # Turn the disk number into an integer
                    disk_num = int(disk_num)
                    # Append the current disk to the peg state list
                    peg_state.append(disk_num)
                # Ensure that the pegs are in numeric order
                peg_state.sort()
            # Create a tuple of the disks on the peg from the list of disks on the peg
            peg_state_tuple = tuple(peg_state)
            # Append the tuple of the disks on the peg to the game state list
            game_state.append(peg_state_tuple)

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
        # Check if the predicate is "movable"
        if movable_statement.predicate == "movable" and self.isMovableLegal(movable_statement):
            # Get the disk's name
            disk_name = str(movable_statement.terms[0])
            # Get the initial peg's name
            initial_peg = str(movable_statement.terms[1])
            # Get the destination peg's name
            destination_peg = str(movable_statement.terms[2])
            # Create a fact to check if the destination peg is empty
            destination_peg_empty = parse_input("fact: (empty " + destination_peg + ")")
            # Create a new fact that the initial peg is empty
            initial_peg_empty = parse_input("fact: (empty " + initial_peg + ")")
            # Create a fact to check if the initial peg still has disks on it
            initial_peg_has_disks = parse_input("fact: (on ?x " + initial_peg + ")")
            # Create a fact of the new location for the disk
            new_disk_location = parse_input("fact: (on " + disk_name + " " + destination_peg + ")")
            # Create a fact of the old location for the fact
            old_disk_location = parse_input("fact: (on " + disk_name + " " + initial_peg + ")")
            # Create a fact of the disk being on the top of the initial peg
            old_disk_on_top = parse_input("fact: (top " + disk_name + " " + initial_peg + ")")
            # Create a fact of the disk being on the top of the destination peg
            new_disk_on_top = parse_input("fact: (top " + disk_name + " " + destination_peg + ")")
            # Check if the destination peg is empty
            if self.kb.kb_ask(destination_peg_empty):
                # Retract that the destination peg is empty
                self.kb.kb_retract(destination_peg_empty)
            # Assert that the disk is on the destination peg
            self.kb.kb_assert(new_disk_location)
            # Assert that the disk is on the top of the destination peg
            self.kb.kb_assert(new_disk_on_top)
            # Retract that the disk was on the initial peg
            self.kb.kb_retract(old_disk_location)
            # Retract that the disk was on the top of the initial peg
            self.kb.kb_retract(old_disk_on_top)
            # Check if the initial peg has no more disks on it
            if not self.kb.kb_ask(initial_peg_has_disks):
                # Assert that the initial peg is now empty
                self.kb.kb_assert(initial_peg_empty)
            # There are disks below the movable disk
            else:
                # Get all the bindings for the disks on the peg
                disks_below_movable_disk = self.kb.kb_ask(initial_peg_has_disks)
                # Get the new top disk
                disk_below_movable_disk = disks_below_movable_disk[0].bindings_dict["?x"]
                # Create a fact of the new top of the stack for the initial peg
                top_of_initial_peg = parse_input("fact: (top " + disk_below_movable_disk + " " + initial_peg + ")")
                # Assert the new top to the initial peg.
                self.kb.kb_assert(top_of_initial_peg)
            return
        # If the movable statement is not movable, return an error
        else:
            print("The movable statement was not legal.")
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
        # Create a list of the columns to cycle through
        all_columns = ["pos1", "pos2", "pos3"]
        # Create a game state list to store all the peg tuples
        game_state = []
        # Cycle through each row
        for row in all_rows:
            # Create an empty list to hold the row state
            row_state = [-1, -1, -1]
            # Create the fact that will be asked to the KB to find which tiles are in the current row
            my_fact = parse_input("fact: (coord ?tile ?x " + row + ")")
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
        # Check if the predicate is "movable"
        if movable_statement.predicate == "movable" and self.isMovableLegal(movable_statement):
            # Get the tile's name
            tile_name = str(movable_statement.terms[0])
            # Get the initial position-x
            initial_x = str(movable_statement.terms[1])
            # Get the initial position-y
            initial_y = str(movable_statement.terms[2])
            # Get the destination position-x
            destination_x = str(movable_statement.terms[3])
            # Get the destination position-y
            destination_y = str(movable_statement.terms[4])
            # Create a fact of new empty tile position
            empty_tile = parse_input("fact: (coord empty " + initial_x + " " + initial_y + ")")
            # Create a fact of new tile position
            new_tile = parse_input("fact: (coord " + tile_name + " " + destination_x + " " + destination_y + ")")
            # Create a fact of the old empty tile position
            old_empty_tile = parse_input("fact: (coord empty " + destination_x + " " + destination_y + ")")
            # Create a fact of the old tile position
            old_tile = parse_input("fact: (coord " + tile_name + " " + initial_x + " " + initial_y + ")")
            # Assert the empty tile position to the KB
            self.kb.kb_assert(empty_tile)
            # Assert the new tile position to the KB
            self.kb.kb_assert(new_tile)
            # Retract the old empty tile positionfrom the KB
            self.kb.kb_retract(old_empty_tile)
            # Retract the old tile position from the KB
            self.kb.kb_retract(old_tile)
            return
        # If the movable statement is not legal, return an error
        else:
            print("The statement is not legal.")
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
