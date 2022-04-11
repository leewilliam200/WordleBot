import pygame
import random
# from environment import CustomEnv

class wordleGame:

    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('Wordle')

        self.titleFont = pygame.font.Font('freesansbold.ttf', 32)
        self.font = pygame.font.Font('freesansbold.ttf', 26)

        self.reset()

    def reset(self):
        with open("testingWords.txt") as file:
            self.file = file
            self.lines  = self.file.readlines()
        self.random_string = str(random.choice(self.lines))
        self.random_string_arr = [self.random_string[0].lower(), self.random_string[1], 
        self.random_string[2], self.random_string[3], self.random_string[4]]
        
        self.state = [0] * 15

        self.window.fill((255, 255, 255))
        
        self.score = 0

        title = 'Wordle'
        self.firstCol = [''] * 5
        self.secondCol = [''] * 5
        self.thirdCol = [''] * 5
        self.fourthCol = [''] * 5
        self.fifthCol = [''] * 5
        self.sixthCol = [''] * 5
        self.seventhCol = [''] * 5

        self.imgTitle = self.titleFont.render(title, True, (0, 0, 0))
        self.imgTitleR = self.imgTitle.get_rect()
        self.imgTitleR.topleft = (250, 50)

        self.frame_iteration = 0

    def checkCorrectPlace(self, arrLetter, letter):
        if arrLetter == letter:
            return True

    def checkCorrectLetter(self, arr, letter):
        if letter in arr:
            return True

    def correctWord(self, wordArr, word):
        print(word)
        for i in wordArr:
            j = str(i).lower()
            if j.strip() == word:
                return True  
        return False
    
    def get_correct(self, arr):
        for i in range(5):
            if len(arr[i]) > 1:
                if int(arr[i][1]) != 1:
                    return False
            else:
                return False
        return True

    def play_step(self, action):
        random_string = self.lines[action]
        final_word = [random_string[0].lower(), random_string[1], 
        random_string[2], random_string[3], random_string[4]]
        print(random_string)
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        if '' in self.firstCol:
            reward, game_over = self.eventCatcher(final_word, self.firstCol, 200, 100)
            self.frame_iteration += 1
        elif '' in self.secondCol:
            reward, game_over = self.eventCatcher(final_word, self.secondCol, 200, 140)
            self.frame_iteration += 1
        elif '' in self.thirdCol:
            reward, game_over = self.eventCatcher(final_word, self.thirdCol, 200, 180)
            self.frame_iteration += 1
        elif '' in self.fourthCol:
            reward, game_over = self.eventCatcher(final_word, self.fourthCol, 200, 220)
            self.frame_iteration += 1
        elif '' in self.fifthCol:
            reward, game_over = self.eventCatcher(final_word, self.fifthCol, 200, 260)
            self.frame_iteration += 1
        elif '' in self.sixthCol:
            reward, game_over = self.eventCatcher(final_word, self.sixthCol, 200, 300)
            self.frame_iteration += 1
        elif '' in self.seventhCol:
            reward, game_over = self.eventCatcher(final_word, self.seventhCol, 200, 340)
            self.frame_iteration += 1
            game_over = True

        self.window.blit(self.imgTitle, self.imgTitleR)

        pygame.display.flip()

        return reward, game_over, self.score
    
    def eventCatcher(self, action, firstCol, xcoord, ycoord):
        reward = 0
        firstCol[0] = action[0]
        firstCol[1] = action[1]
        firstCol[2] = action[2]
        firstCol[3] = action[3]
        firstCol[4] = action[4]

        if self.correctWord(self.lines, ''.join(firstCol)):
            for i in range(5):
                if self.checkCorrectPlace(firstCol[i].lower(), self.random_string[i].lower()):
                    firstCol[i] += '1'
                    self.score += 100
                    reward += 100
                elif self.checkCorrectLetter(self.random_string_arr, firstCol[i].lower()):
                    firstCol[i] += '2'
                    self.score += 1
                    reward += 1
        else:
            return 0, True
        
        if self.get_correct(firstCol):
            self.score += 1000
            reward += 10000
            return reward, True

        if len(firstCol[0]) == 0 or len(firstCol[0]) == 1:
            img1 = self.font.render(firstCol[0], True, (0, 0, 0))
            imgR1 = img1.get_rect()
            pygame.draw.rect(img1, (0, 0, 0), imgR1, 1)
            self.state[0] = 1
            self.state[1] = 0
            self.state[2] = 0
        elif firstCol[0][1] == '1':
            img1 = self.font.render(firstCol[0][0], True, (0, 0, 0))
            imgR1 = img1.get_rect()
            pygame.draw.rect(img1, (0, 255, 0), imgR1, 1)
            self.state[0] = 0
            self.state[1] = 1
            self.state[2] = 0
        elif firstCol[0][1] == '2':
            img1 = self.font.render(firstCol[0][0], True, (0, 0, 0))
            imgR1 = img1.get_rect()
            pygame.draw.rect(img1, (255, 0, 0), imgR1, 1)
            self.state[0] = 0
            self.state[1] = 0
            self.state[2] = 1

        if len(firstCol[1]) == 0 or len(firstCol[1]) == 1:
            img2 = self.font.render(firstCol[1], True, (0, 0, 0))
            imgR2 = img2.get_rect()
            pygame.draw.rect(img2, (0, 0, 0), imgR2, 1)
            self.state[3] = 1
            self.state[4] = 0
            self.state[5] = 0
        elif firstCol[1][1] == '1':
            img2 = self.font.render(firstCol[1][0], True, (0, 0, 0))
            imgR2 = img2.get_rect()
            pygame.draw.rect(img2, (0, 255, 0), imgR2, 1)
            self.state[3] = 0
            self.state[4] = 1
            self.state[5] = 0
        elif firstCol[1][1] == '2':
            img2 = self.font.render(firstCol[1][0], True, (0, 0, 0))
            imgR2 = img2.get_rect()
            pygame.draw.rect(img2, (255, 0, 0), imgR2, 1)
            self.state[3] = 0
            self.state[4] = 0
            self.state[5] = 1
        
        if len(firstCol[2]) == 0 or len(firstCol[2]) == 1:
            img3 = self.font.render(firstCol[2], True, (0, 0, 0))
            imgR3 = img3.get_rect()
            pygame.draw.rect(img3, (0, 0, 0), imgR3, 1)
            self.state[6] = 1
            self.state[7] = 0
            self.state[8] = 0
        elif firstCol[2][1] == '1':
            img3 = self.font.render(firstCol[2][0], True, (0, 0, 0))
            imgR3 = img3.get_rect()
            pygame.draw.rect(img3, (0, 255, 0), imgR3, 1)
            self.state[6] = 0
            self.state[7] = 1
            self.state[8] = 0
        elif firstCol[2][1] == '2':
            img3 = self.font.render(firstCol[2][0], True, (0, 0, 0))
            imgR3 = img3.get_rect()
            pygame.draw.rect(img3, (255, 0, 0), imgR3, 1)
            self.state[6] = 0
            self.state[7] = 0
            self.state[8] = 1

        if len(firstCol[3]) == 0 or len(firstCol[3]) == 1:
            img4 = self.font.render(firstCol[3], True, (0, 0, 0))
            imgR4 = img4.get_rect()
            pygame.draw.rect(img4, (0, 0, 0), imgR4, 1)
            self.state[9] = 1
            self.state[10] = 0
            self.state[11] = 0
        elif firstCol[3][1] == '1':
            img4 = self.font.render(firstCol[3][0], True, (0, 0, 0))
            imgR4 = img4.get_rect()
            pygame.draw.rect(img4, (0, 255, 0), imgR4, 1)
            self.state[9] = 0
            self.state[10] = 1
            self.state[11] = 0
        elif firstCol[3][1] == '2':
            img4 = self.font.render(firstCol[3][0], True, (0, 0, 0))
            imgR4 = img4.get_rect()
            pygame.draw.rect(img4, (255, 0, 0), imgR4, 1)
            self.state[9] = 0
            self.state[10] = 0
            self.state[11] = 1

        if len(firstCol[4]) == 0 or len(firstCol[4]) == 1:
            img5 = self.font.render(firstCol[4], True, (0, 0, 0))
            imgR5 = img5.get_rect()
            pygame.draw.rect(img5, (0, 0, 0), imgR5, 1)
            self.state[12] = 1
            self.state[13] = 0
            self.state[14] = 0
        elif firstCol[4][1] == '1':
            img5 = self.font.render(firstCol[4][0], True, (0, 0, 0))
            imgR5 = img5.get_rect()
            pygame.draw.rect(img5, (0, 255, 0), imgR5, 1)
            self.state[12] = 0
            self.state[13] = 1
            self.state[14] = 0
        elif firstCol[4][1] == '2':
            img5 = self.font.render(firstCol[4][0], True, (0, 0, 0))
            imgR5 = img5.get_rect()
            pygame.draw.rect(img5, (255, 0, 0), imgR5, 1)
            self.state[12] = 0
            self.state[13] = 0
            self.state[14] = 1
        
        self.window.blit(img1, (xcoord, ycoord))
        self.window.blit(img2, (xcoord + 50, ycoord))
        self.window.blit(img3, (xcoord + 100, ycoord))
        self.window.blit(img4, (xcoord + 150, ycoord))
        self.window.blit(img5, (xcoord + 200, ycoord))

        pygame.display.flip()

        return reward, False