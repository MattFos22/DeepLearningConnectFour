from connectfour.connectfourRL import connectfourgame, connectfourqlearner
import numpy as np
import random
import pygame
import sys
import math

# Yes, this is horrible. This is purely to help my small brain model the domains - Simulation, Game and rewards.
# Do not emulate
# This is the simulation!
cf = connectfourgame.ConnectFourGame()
board = cf.create_board()
cf.print_board(board)
game_over = False

# add the learner
ql = connectfourqlearner.ConnectFourQLearner(board)

pygame.init()

width = cf.COLUMN_COUNT * cf.SQUARESIZE
height = (cf.ROW_COUNT+1) * cf.SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)
cf.draw_board(board, screen, height)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(cf.PLAYER, cf.AI)

# Put our learning ai in initial state

while not game_over:#

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			cf.sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, cf.BLACK, (0,0, width, cf.SQUARESIZE))
			posx = event.pos[0]
			if turn == cf.PLAYER:
				pygame.draw.circle(screen, cf.RED, (posx, int(cf.SQUARESIZE/2)), cf.RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, cf.BLACK, (0,0, width, cf.SQUARESIZE))
			if turn == cf.PLAYER:
				# select_action
				# execute the action



				posx = event.pos[0]
				col = int(math.floor(posx/cf.SQUARESIZE))

				if cf.is_valid_location(board, col):
					row = cf.get_next_open_row(board, col)
					cf.drop_piece(board, row, col, cf.PLAYER_PIECE)

					if cf.winning_move(board, cf.PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, cf.RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					cf.print_board(board)
					cf.draw_board(board, screen, height)


		# # Ask for Player 2 Input
		if turn == cf.AI and not game_over:

			#col = random.randint(0, COLUMN_COUNT-1)
			#col = pick_best_move(board, AI_PIECE)
			print("AI TURN!")
			col, minimax_score = cf.minimax(board, 5, -math.inf, math.inf, True)

			if cf.is_valid_location(board, col):
				#pygame.time.wait(500)
				row = cf.get_next_open_row(board, col)
				print("dropping here: "+ str(row))
				cf.drop_piece(board, row, col, cf.AI_PIECE)

				if cf.winning_move(board, cf.AI_PIECE):
					label = myfont.render("Player 2 wins!!", 1, cf.YELLOW)
					screen.blit(label, (40,10))
					game_over = True

				cf.print_board(board)
				cf.draw_board(board, screen, height)

				turn += 1
				turn = turn % 2

		if game_over:
			pygame.time.wait(3000)
