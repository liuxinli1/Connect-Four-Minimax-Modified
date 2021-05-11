import copy
import random
from typing import List


class Player:
    """
    this class declare two players.
    '🔵'  U+1F535 black
    '🟠'  U+1F7E0 white
    """
    '''
    Edit: Swapped black to 🟦 U+1F7E6 instead for better visual
    '''
    BLACK, WHITE = '🟦', '🟠'


class GameStatus:
    B_WIN = 'Black play wins the game!'
    W_WIN = 'White play wins the game!'
    DRAW = 'Draw! No one wins!'
    ING = 'Game has not finish yet!'


class Game:

    def __init__(self):
        self.empty = '  '
        self.board: List[List[str]] = [[self.empty for _ in range(7)] for _ in range(6)]

        # the current player to move. Black moves first
        self.cur = Player.BLACK
        self.status = GameStatus.ING

    def get_status(self):
        return self.status

    def can_move(self, col):
        """
        :param col: the column player want to move
        :return: True if player can make movement
        """
        try:
            col = int(col) - 1
        except ValueError:
            return False
        return 0 <= col < 7 and self.board[0][col] == self.empty

    def check_win(self):
        # the backtrack does not increase the speed, use exhaustive
        # row   →
        # col   ↓
        # diag1 ↗
        # diag2 ↘

        for row in range(6):
            for col in range(7):
                cur = self.board[row][col]
                if cur == self.empty:
                    continue
                # check row
                if col <= 3:
                    if cur == self.board[row][col + 1] == self.board[row][col + 2] == self.board[row][col + 3]:
                        return GameStatus.B_WIN if cur == Player.BLACK else GameStatus.W_WIN
                # check col
                if row <= 2:
                    if cur == self.board[row + 1][col] == self.board[row + 2][col] == self.board[row + 3][col]:
                        return GameStatus.B_WIN if cur == Player.BLACK else GameStatus.W_WIN
                # check diag1
                if row >= 3 and col <= 3:
                    if cur == self.board[row - 1][col + 1] == self.board[row - 2][col + 2] == \
                            self.board[row - 3][col + 3]:
                        return GameStatus.B_WIN if cur == Player.BLACK else GameStatus.W_WIN
                # check diag2
                if row <= 2 and col <= 3:
                    if cur == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == \
                            self.board[row + 3][col + 3]:
                        return GameStatus.B_WIN if cur == Player.BLACK else GameStatus.W_WIN

        for col in range(7):
            if self.board[0][col] == self.empty:
                return GameStatus.ING
        return GameStatus.DRAW

    def move(self, col):
        """
        :param col: the column player want to move
        :return: True if movement success
        """

        if not self.can_move(col):
            return False

        col = int(col) - 1
        for row in range(5, -1, -1):
            if self.board[row][col] == self.empty:
                self.board[row][col] = self.cur
                break

        self.cur = Player.WHITE if self.cur == Player.BLACK else Player.BLACK
        self.status = self.check_win()
        return True

    def __str__(self):
        indexes = ['0' + str(i) for i in range(1, 8)]
        res = ' ' + ' '.join(indexes) + '\n'
        for index, line in zip(indexes, self.board):
            res += '|' + ('|'.join(line)) + '|\n'
        return res


class AI:
    def __init__(self):
        pass

    def playMove(self, game):
        best = -99
        bestMove = -1
        possibleMove = [x for x in range(1, 8) if game.can_move(x)]
        for i in possibleMove:
            tempGame = copy.deepcopy(game)
            tempGame.move(i)
            #print(tempGame)
            score = self.minmax(tempGame, False, 4)
            print("position:", i, "score:", score)
            if score > best:
                best = score
                bestMove = i
        if game.move(bestMove) == False:
            print("AI cannot move to this spot", bestMove)

    def minmax(self, game, maximizingPlayer, depth):
        if game.status == GameStatus.B_WIN:
            #print('player Win', board)
            return -1
        if game.status == GameStatus.W_WIN:
            #print('cpu Win', board)
            return 1
        if game.status == GameStatus.DRAW:
            #print('tie', board)
            return 0
        if depth == 0:
            return 0
        if maximizingPlayer:
            score = -99
            for i in range(1, 8):
                tempGame = copy.deepcopy(game)
                tempGame.move(i)
                score = max(score, self.minmax(tempGame, False, depth-1))
            return score
        else:
            score = 99
            for i in range(1, 8):
                tempGame = copy.deepcopy(game)
                tempGame.move(i)
                score = min(score, self.minmax(tempGame, True, depth-1))
            return score





def run_game():
    game = Game()
    print(game)
    ai = AI()

    while True:
        print(f"Player {game.cur}'s turn to move!")
        #if game.cur == Player.BLACK:
        move = input()
        #elif game.cur == Player.WHITE:
        if game.move(move) is False:
            print("Please enter valid movement!")
            continue
        print(game)
        ai.playMove(game)
        print(game)
        if game.status != GameStatus.ING:
            print(game.status)
            exit()


if __name__ == '__main__':
    run_game()
