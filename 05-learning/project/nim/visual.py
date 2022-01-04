import pygame
import sys
import time

# import tictactoe as ttt
from nim import Nim, NimAI

CIRCLE = 'O'
EMPTY = None
N_GAMES = 10001
VISUALIZE_EACH = 50
SLOW_VISUALIZE_EACH = 1000

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
# board = ttt.initial_state()
game = Nim()
INITIAL_PILE = game.piles.copy()
# Keep track of last move made by either player
last = {
    0: {"state": None, "action": None},
    1: {"state": None, "action": None}
}

piles = game.piles
player = NimAI()

def clean_board():
    # initialize board
    board = []
    for j in range(len(INITIAL_PILE)):
            board.append([EMPTY] * max(INITIAL_PILE))

    return board

def populate_board(piles):
    board = clean_board()
    
    for i, pile in enumerate(piles):
        for j in range(pile):
            board[i][j] = CIRCLE
    
    return board

def draw_game_state(screen, board, title=''):
    # Draw game board
    title = largeFont.render(title, True, white)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 50)
    screen.blit(title, titleRect)

    tile_size = 60
    tile_origin = (width / 2 - (3 * tile_size),
                    height / 2 - (1.5 * tile_size))

    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 3)

            if board[i][j] != None:# ttt.EMPTY:
                move = moveFont.render(board[i][j], True, white)
                moveRect = move.get_rect()
                moveRect.center = rect.center
                screen.blit(move, moveRect)
    
    pygame.display.flip()

    return screen, board

def highlight_move(screen, board, action, player, title=''):
    # Draw game board
    title = largeFont.render(title, True, white)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 50)
    screen.blit(title, titleRect)


    tile_size = 60
    tile_origin = (width / 2 - (3 * tile_size),
                    height / 2 - (1.5 * tile_size))
    
    pile_number = action[0]
    count = action[1]

    for i in range(len(board)):
        row = []
        for j in reversed(range(len(board[0]))):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 3)


            if board[i][j] != None and i == pile_number:
                if count > 0:
                    if player:
                        move = moveFont.render('X', True, red)
                    else:
                        move = moveFont.render('X', True, blue)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                    count -= 1

    pygame.display.flip()

    return screen, board



board = clean_board()
ai_turn = False

# General Game Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Nim", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playX = mediumFont.render("Train AI", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = NimAI()
                
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                pass

    else:
        if playXButton:
            print('Training...')
            # play 10 games
            for game_number in range(N_GAMES):
                # specific game loop
                game = Nim()
                piles = game.piles
                title = f'Game #{game_number}'

                while True:
                    screen.fill(black)
                    if game.piles == INITIAL_PILE:
                        fl_first_move = True

                    board = populate_board(piles)
                    # Print content of piles

                    if game_number % VISUALIZE_EACH == 0:
                        screen, board = draw_game_state(screen, board, title)
                    #time.sleep(0.1)
                    
                    # Keep track of current state and action
                    state = game.piles.copy()
                    action = player.choose_action(game.piles, epsilon=True)

                    # Keep track of last state and action
                    last[game.player]["state"] = state
                    last[game.player]["action"] = action

                    # Make move (game.move switches player)
                    game.move(action)
                    new_state = game.piles.copy()

                    if game_number % SLOW_VISUALIZE_EACH == 0 and game_number > 0:
                        # highlight best possible actions
                        if fl_first_move:
                            print(('Red' if game.player else 'Blue') + ' player begins')
                            fl_first_move = False
                        if game.winner is not None:
                            print(('Red' if not game.winner else 'Blue') + ' player wins')
                            # a move that leads to a winning move makes the player a loser
                    
                        time.sleep(0.2)
                        screen, board = highlight_move(screen, board, action, game.player, title)
                        time.sleep(1)

                    # When game is over, update Q values with rewards
                    if game.winner is not None:
                        # if that move led to a game.winner
                        # then it means that it was a LOSING move. 
                        # so we need to give a reward of -1
                        player.update(state, action, new_state, -1)

                        # if that move was a LOSING move, the move before that 
                        # has led to a WINNING, which means we need to give 
                        # a reward of +1
                        player.update(
                            last[game.player]["state"],
                            last[game.player]["action"],
                            new_state,
                            1
                        )
                        # it's interesting because the AI won and lost at the same time,
                        # both leading to a new knowledge/reward.
                        break


                    # If game is continuing, no rewards yet
                    elif last[game.player]["state"] is not None:
                        player.update(
                            last[game.player]["state"],
                            last[game.player]["action"],
                            new_state,
                            0
                        )
                    
            # exit game
            print(dict(sorted(player.q.items(), key=lambda x : -x[1])[:10]))
            break

    pygame.display.flip()



