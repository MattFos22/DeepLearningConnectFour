import math
import pygame

class HumanPlayer:
        def select_action(self, qTable, state, cf, event, iteration):
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx/100))
                return {'col' : col }
            else:
                return {'col' : 99}