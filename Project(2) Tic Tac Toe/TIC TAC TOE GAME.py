import copy
import sys
import pygame
import random
import numpy as np

from parameters import *
pygame.init()
playing_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI DESIGNED BY RAAD')
playing_screen.fill(BG_COLOR)
class THE_MAIN_BOARD:

    def __init__(YOU):
        YOU.positions = np.zeros((ROWS, COLS))
        YOU.availablesqrs = YOU.positions  # [positions]
        YOU.marked_sqrs = 0

    def endstate(YOU, show=False):
        # horizontal wins
        for row in range(ROWS):
            if YOU.positions[row][0] == YOU.positions[row][1] == YOU.positions[row][2] != 0:
                if show:
                    COLOR = CIRC_COLOR if YOU.positions[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQUARESIZE + SQUARESIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARESIZE + SQUARESIZE // 2)
                    pygame.draw.line(playing_screen, COLOR, iPos, fPos, LINE_WIDTH)
                return YOU.positions[row][0]
        # Check for vertical wins
        for column in range(COLS):
            if YOU.positions[0][column] == YOU.positions[1][column] == YOU.positions[2][column] != 0:
                if show:
                    COLOR = CIRC_COLOR if YOU.positions[0][column] == 2 else CROSS_COLOR
                    iPos = (column * SQUARESIZE + SQUARESIZE // 2, 20)
                    fPos = (column * SQUARESIZE + SQUARESIZE // 2, HEIGHT - 20)
                    pygame.draw.line(playing_screen, COLOR, iPos, fPos, LINE_WIDTH)
                return YOU.positions[0][column]
        # desc diagonal
        if YOU.positions[0][0] == YOU.positions[1][1] == YOU.positions[2][2] != 0:
            if show:
                COLOR = CIRC_COLOR if YOU.positions[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(playing_screen, COLOR, iPos, fPos, CROSS_WIDTH)
            return YOU.positions[1][1]

        # asc diagonal
        if YOU.positions[2][0] == YOU.positions[1][1] == YOU.positions[0][2] != 0:
            if show:
                COLOR = CIRC_COLOR if YOU.positions[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(playing_screen, COLOR, iPos, fPos, CROSS_WIDTH)
            return YOU.positions[1][1]

        # no win yet
        return 0

    def mark_sqr(YOU, row, column, player):
        YOU.positions[row][column] = player
        YOU.marked_sqrs += 1

    def availablesqr(YOU, row, column):
        return YOU.positions[row][column] == 0

    def get_availablesqrs(YOU):
        availablesqrs = []
        for row in range(ROWS):
            for column in range(COLS):
                if YOU.availablesqr(row, column):
                    availablesqrs.append((row, column))
        return availablesqrs

    def isfull(YOU):
        return YOU.marked_sqrs == 9

    def isempty(YOU):
        return YOU.marked_sqrs == 0

class Game:

    def __init__(YOU):
        YOU.board = THE_MAIN_BOARD()
        YOU.ai = AI()
        YOU.player = 1  
        YOU.gamemode = 'ai'  
        YOU.running = True
        YOU.show_lines()

    def show_lines(YOU):
        # bg
        playing_screen.fill(BG_COLOR)

        # vertical
        pygame.draw.line(playing_screen, LINE_COLOR, (SQUARESIZE, 0), (SQUARESIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(playing_screen, LINE_COLOR, (WIDTH - SQUARESIZE, 0), (WIDTH - SQUARESIZE, HEIGHT), LINE_WIDTH)

        # horizontal
        pygame.draw.line(playing_screen, LINE_COLOR, (0, SQUARESIZE), (WIDTH, SQUARESIZE), LINE_WIDTH)
        pygame.draw.line(playing_screen, LINE_COLOR, (0, HEIGHT - SQUARESIZE), (WIDTH, HEIGHT - SQUARESIZE), LINE_WIDTH)

    def drawfig(YOU, row, column):
        if YOU.player == 1:
            # draw cross
            # desc line
            start_desc = (column * SQUARESIZE + OFFSET, row * SQUARESIZE + OFFSET)
            end_desc = (column * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            pygame.draw.line(playing_screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # asc line
            start_asc = (column * SQUARESIZE + OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            end_asc = (column * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + OFFSET)
            pygame.draw.line(playing_screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif YOU.player == 2:
            # draw circle
            center = (column * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
            pygame.draw.circle(playing_screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

 
    def do_a_move(YOU, row, column):
        YOU.board.mark_sqr(row, column, YOU.player)
        YOU.drawfig(row, column)
        YOU.next_turn()

    def next_turn(YOU):
        YOU.player = YOU.player % 2 + 1

    def change_gamemode(YOU):
        YOU.gamemode = 'AI' if YOU.gamemode == 'pvp' else 'pvp'

    def Done(YOU):
        return YOU.board.endstate(show=True) != 0 or YOU.board.isfull()

    def reset(YOU):
        YOU.__init__()


class AI:
    def __init__(YOU, hardness=1, player=2):
        YOU.hardness = hardness
        YOU.player = player

   
    def Random(YOU, board):
        availablesqrs = board.get_availablesqrs()
        idx = random.randrange(0, len(availablesqrs))
        return availablesqrs[idx]  # (row, column)

    def minimax(YOU, board, maximizing):

        case = board.endstate()

        if case == 1:
            return 1, None

        if case == 2:
            return -1, None

        elif board.isfull():
            return 0, None

        if maximizing:
            bestscore= -1000
            best_move = None
            availablesqrs = board.get_availablesqrs()

            for (row, column) in availablesqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, column, 1)
                score = YOU.minimax(temp_board, False)[0]
                if score > bestscore:
                    bestscore= score
                    best_move = (row, column)

            return bestscore, best_move

        else:
            bestscore = 1000
            best_move = None
            availablesqrs = board.get_availablesqrs()

            for (row, column) in availablesqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, column, YOU.player)
                score = YOU.minimax(temp_board, True)[0]
                if score < bestscore:
                    bestscore = score
                    best_move = (row, column)
            return bestscore, best_move

    def score(YOU, main_board):
        if YOU.hardness == 0:
            score = 'random'
            choice = YOU.Random(main_board)
        else:
            score, choice = YOU.minimax(main_board, False)

        print(f'AI has opted to assign a score of{score} to the square in position option {choice}.')
        return choice

def main():
    tictactoe_game = Game()
    board = tictactoe_game.board
    ai = tictactoe_game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    tictactoe_game.change_gamemode()

                if event.key == pygame.K_r:
                    tictactoe_game.reset()
                    board = tictactoe_game.board
                    ai = tictactoe_game.ai

                if event.key == pygame.K_0:
                    ai.hardness = 0

                if event.key == pygame.K_1:
                    ai.hardness = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARESIZE
                column = pos[0] // SQUARESIZE

                if board.availablesqr(row, column) and tictactoe_game.running:
                    tictactoe_game.do_a_move(row, column)

                    if tictactoe_game.Done():
                        tictactoe_game.running = False

        if tictactoe_game.gamemode == 'ai' and tictactoe_game.player == ai.player and tictactoe_game.running:

            pygame.display.update()

            row, column = ai.score(board)
            tictactoe_game.do_a_move(row, column)

            if tictactoe_game.Done():
                tictactoe_game.running = False

        pygame.display.update()

main()
