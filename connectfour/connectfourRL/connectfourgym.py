from connectfour.connectfourRL import connectfourgame, connectfourqlearner
import numpy as np
import random
import pygame
import sys
import math
import copy


class ConnectFourGym:
	def __init__(self, numberOfGames):
		cf = connectfourgame.ConnectFourGame()
		ql = connectfourqlearner.ConnectFourQLearner()
		for x in range(numberOfGames):
			self.playGame(cf, ql)

# Put our learning ai in initial state
	def playGame(self, cf, ql):
		board = cf.create_board()
		cf.print_board(board)
		game_over = False
		pygame.init()

		width = cf.COLUMN_COUNT * cf.SQUARESIZE
		height = (cf.ROW_COUNT+1) * cf.SQUARESIZE

		size = (width, height)

		screen = pygame.display.set_mode(size)
		cf.draw_board(board, screen, height)
		pygame.display.update()

		myfont = pygame.font.SysFont("monospace", 75)

		turn = random.randint(cf.PLAYER, cf.AI)

		while not game_over:#
			for event in pygame.event.get():
				previousBoard = copy.deepcopy(board[0:len(board)])
				if event.type == pygame.QUIT:
					cf.sys.exit()

				pygame.display.update()

				if turn == cf.PLAYER and not game_over:
					action = {'col' : 99 }
					while(not cf.is_valid_location(board, action.get('col'))): #sort this mess out to not call the function twice
						action = ql.select_action(board)
						if(cf.is_valid_location(board, action.get('col'))):
							break

					row = cf.get_next_open_row(board, action.get('col'))
					cf.drop_piece(board, row, action.get('col'), cf.PLAYER_PIECE)
					result = {"gameOver":False}
					if cf.winning_move(board, cf.PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, cf.RED)
						result = {"gameOver":True, "winner":1}
						screen.blit(label, (40,10))
						game_over = True

					ql.learn(board, previousBoard, action.get('col'), result)
					turn += 1
					turn = turn % 2

					cf.print_board(board)
					cf.draw_board(board, screen, height)

				if turn == cf.AI and not game_over:

					print("AI TURN!")
					col, minimax_score = cf.minimax(board, 5, -math.inf, math.inf, True)

					if cf.is_valid_location(board, col):
						row = cf.get_next_open_row(board, col)
						print("dropping here: "+ str(row))
						cf.drop_piece(board, row, col, cf.AI_PIECE)
						result = {"gameOver":False}

						if cf.winning_move(board, cf.AI_PIECE):
							label = myfont.render("Player 2 wins!!", 1, cf.YELLOW)
							screen.blit(label, (40,10))
							game_over = True
							result = {"gameOver":True, "winner":2}

						ql.learn(board, previousBoard, col, result)
						cf.print_board(board)
						cf.draw_board(board, screen, height)

						turn += 1
						turn = turn % 2
