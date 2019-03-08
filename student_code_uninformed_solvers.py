from solver import *
from collections import deque


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True
        potential_moves = self.gm.getMovables()

        for move in potential_moves:
            self.gm.makeMove(move)

            game_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            game_state.parent = self.currentState

            if game_state not in self.visited:
                self.currentState.children.append(game_state)
                self.visited[game_state] = False

            elif not self.visited[game_state]:
                self.currentState.children.append(game_state)

            self.gm.reverseMove(move)

        child_num = self.currentState.nextChildToVisit

        total_num_children = len(self.currentState.children)
        while self.currentState.depth != 0 and child_num == total_num_children:
            self.currentState = self.currentState.parent

            self.gm.reverseMove(self.currentState.requiredMovable)

            child_num = self.currentState.nextChildToVisit

        current_state_child = self.currentState.children[child_num]
        if not self.visited[current_state_child]:
            self.currentState.nextChildToVisit += 1

            self.gm.makeMove(self.currentState.children[child_num].requiredMovable)

            self.currentState = self.currentState.children[child_num]

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.myList = dict()
        self.myQueue = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """


        if self.currentState.state == self.victoryCondition:
            return True


        self.visited[self.currentState] = True
        potential_moves = self.gm.getMovables()

        if not self.currentState.depth:
            self.myList[self.currentState] = []

        for move in potential_moves:
            self.gm.makeMove(move)

            game_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

            if game_state not in self.visited:

                self.currentState.children.append(game_state)
                self.visited[game_state] = False
                self.myQueue.append(game_state)
                self.myList[game_state] = []

                for x in self.myList[self.currentState]:
                    self.myList[game_state].append(x)

                self.myList[game_state].append(game_state)
            self.gm.reverseMove(move)
        index = len(self.myList[self.currentState])

        for i in range(index):
            self.gm.reverseMove(self.myList[self.currentState][index - i - 1].requiredMovable)

        self.currentState = self.myQueue.popleft()

        for move in self.myList[self.currentState]:
            self.gm.makeMove(move.requiredMovable)

        return False
