import random
import sys
from typing import List

import pygame
from pygame.locals import *


class Game:
    def __init__(self):
        pygame.init()
        self.show_solution = False
        self.game_clear = False
        self.click_motion_time = 0
        self.clicked_pos = []

        self.board, self.solution = self.generate_random()
        self.click_counter = [[0 for _ in range(5)] for _ in range(5)]

        self.screen = pygame.display.set_mode((390, 390))

        while True:
            self.window()
            pygame.display.update()
            self.event()
            self.check_clear()

    def window(self) -> None:
        self.px=50
        self.py=50
        self.click_motion_time -= 1 if self.click_motion_time > 0 else self.click_motion_time

        self.screen.fill((0, 0, 0))

        count_click = sum(sum(row) for row in self.click_counter)
        count_solution = sum(sum(row) for row in self.solution)

        font = pygame.font.Font(None, 35)
        if count_click <= count_solution:
            color = (51, 255, 51)
        elif count_click <= count_solution*2:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        gTxt = font.render(f"{count_click}/{count_solution}", True, color)
        self.screen.blit(gTxt, [280, 20])

        for i in range(5):
            for j in range(5):
                n = 5.0 - 0.1*abs(50-self.click_motion_time) if [i, j] in self.clicked_pos else 0
                if self.board[i][j] == 1:
                    pygame.draw.rect(self.screen, (20, 240, 40), Rect(self.px+(60*i)-(n/2), self.py+(60*j)-(n/2), 50+(n/2), 50+(n/2)), 0)
                elif self.board[i][j] == -1:
                    pygame.draw.rect(self.screen, (111, 111, 111), Rect(self.px+(60*i)-(n/2), self.py+(60*j)-(n/2), 50+(n/2), 50+(n/2)), 0)

                if self.show_solution and self.solution[i][j] == 1 and self.click_counter[i][j] % 2 == 0:
                    pygame.draw.circle(self.screen, (50, 50, 50), ((self.px*(3/2))+(60*i), (self.py*(3/2))+(60*j)), 5, 0)
                if self.show_solution and self.solution[i][j] == 0 and self.click_counter[i][j] % 2 == 1:
                    pygame.draw.circle(self.screen, (50, 50, 50), ((self.px*(3/2))+(60*i), (self.py*(3/2))+(60*j)), 5, 0)

        if self.game_clear:
            font = pygame.font.Font(None, 45)
            gTxt = font.render(f"Game Clear", True, (255, 255, 255))
            self.screen.blit(gTxt, [110, 177])

    def event(self) -> None:
        for event in pygame.event.get():
            if event. type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if self.game_clear:
                    self.new_game()
                else:
                    btn = event.button
                    x, y = event.pos

                    if btn == 1:
                        i, j = self.pos_to_tile(x, y)
                        if i != -1 and j != -1:
                            self.clicked_pos = self.click_motion_pos(i, j)
                            self.click_motion_time = 100
                            self.click_counter[i][j] += 1
                            self.clicked(i, j, self.board)

                    elif btn == 2:
                        self.show_solution = False if self.show_solution == True else True

                    elif btn == 3:
                        self.new_game()

    def new_game(self) -> None:
        self.board, self.solution = self.generate_random()
        self.click_counter = [[0 for _ in range(5)] for _ in range(5)]
        self.game_clear = False

    def click_motion_pos(self, i:int, j:int) -> List[List[int]]:
        pos = [[i, j]]
        if i - 1 in range(5): pos.append([i-1, j])
        if i + 1 in range(5): pos.append([i+1, j])
        if j - 1 in range(5): pos.append([i, j-1])
        if j + 1 in range(5): pos.append([i, j+1])
        return pos

    def clicked(self, i:int, j:int, board) -> None:
        board[i][j] = board[i][j] * -1
        if i - 1 in range(5): board[i-1][j] *= -1
        if i + 1 in range(5): board[i+1][j] *= -1
        if j - 1 in range(5): board[i][j-1] *= -1
        if j + 1 in range(5): board[i][j+1] *= -1


    def check_clear(self):
        board_sum = sum(sum(row) for row in self.board)
        if board_sum == -25:
            self.game_clear = True

    def generate_random(self) -> List[List[int]]:
        board = [[-1 for _ in range(5)] for _ in range(5)]
        solution = [[0 for _ in range(5)] for _ in range(5)]

        for i in range(5):
            for j in range(5):
                rand = random.randint(1, 100)
                if rand % 2 == 1:
                    solution[i][j] = 1
                    self.clicked(i, j, board)
        return board, solution


    def pos_to_tile(self, posX:int, posY:int) -> tuple[int]:
        if posX < 50 or 340 < posX: return (-1, -1)
        if posY < 50 or 340 < posY: return (-1, -1)

        for i in range(5):
            for j in range(5):
                if ( 50+(60*i) < posX and posX < 100+(60*i) ) and ( 50+(60*j) < posY and posY < 100+(60*j) ):
                    return (i, j)

        return (-1, -1)

if __name__ == "__main__":
    Game()
