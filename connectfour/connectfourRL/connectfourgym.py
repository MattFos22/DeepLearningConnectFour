from connectfour.connectfourRL import connectfourgame, connectfourqlearner
import numpy as np
import random
import pygame
import sys
import math
import copy


class ConnectFourGym:
	def __init__(self, numberOfGames, player1, player2):
		cf = connectfourgame.ConnectFourGame()
		ql = connectfourqlearner.ConnectFourQLearner()
		self.player1 = player1
		self.player2 = player2
		for x in range(numberOfGames):
			self.iteration = x
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

					action = self.player1.select_action(ql.q, board, cf.ACTIONS, event, self.iteration)
					if(cf.is_valid_location(board, action.get('col'))):
						row = cf.get_next_open_row(board, action.get('col'))
						cf.drop_piece(board, row, action.get('col'), cf.PLAYER_PIECE)
						result = {"gameOver":False}
						if cf.winning_move(board, cf.PLAYER_PIECE):
							label = myfont.render("Player 1 wins!!", 1, cf.RED)
							result = {"gameOver":True, "winner":1}
							screen.blit(label, (40,10))
							game_over = True
							print("ai 1 won")
						if cf.checkForDraw(board):
							print("it was a draw")
							result = {"gameOver":True, "winner":0}

						ql.learn(board, previousBoard, action.get('col'), result)
						turn += 1
						turn = turn % 2

						cf.print_board(board)
						cf.draw_board(board, screen, height)

				if turn == cf.AI and not game_over:
					print("AI TURN!")

					action = self.player2.select_action(ql.q, board, cf.ACTIONS, event, self.iteration)
					if(cf.is_valid_location(board, action.get('col'))):
						row = cf.get_next_open_row(board, action.get('col'))
						cf.drop_piece(board, row, action.get('col'), cf.AI_PIECE)
						result = {"gameOver":False}
						if cf.winning_move(board, cf.AI_PIECE):
							label = myfont.render("Player 2 wins!!", 1, cf.YELLOW)
							screen.blit(label, (40,10))
							game_over = True
							result = {"gameOver":True, "winner":2}
							print("AI2 won")
						if cf.checkForDraw(board):
							print("it was a draw")
							result = {"gameOver":True, "winner":0}

						ql.learn(board, previousBoard, action.get('col'), result)
						cf.print_board(board)
						cf.draw_board(board, screen, height)

						turn += 1
						turn = turn % 2
