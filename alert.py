import pygame
import time
from parameter import Parameter


pygame.init()
class Alert(Parameter):
    def __init__(self):
        super().__init__()

    """遊戲失敗"""
    def game_over(self,win_surface,score):
        """遊戲失敗圖片"""
        gameOverImg = pygame.image.load("GameOver.jpg")
        gameOverImgSurf = pygame.transform.scale(gameOverImg, (self.win_width,self.win_height))
        gameOverImgRect = gameOverImgSurf.get_rect()
        gameOverImgRect.center = (self.win_width//2,self.win_height//2)

        win_surface.blit(gameOverImgSurf, gameOverImgRect)

        """遊戲失敗文字"""
        gameOverFont = pygame.font.Font(None, 55)
        gameOverFontSurf = gameOverFont.render(f'Your score {score}', True, (255,255,255))
        gameOverFontRect = gameOverFontSurf.get_rect()
        gameOverFontRect.midtop = (self.win_width//2,self.win_height//2 + 90)
        win_surface.blit(gameOverFontSurf, gameOverFontRect)

        """重新開始的文字"""
        restartFont = pygame.font.Font(None, 40)
        restartSurf = restartFont.render('Press Enter Restart', True, (255,255,255))
        restartFontRect = restartSurf.get_rect()
        restartFontRect.midtop = (self.win_width//2,self.win_height//2 + 140)
        win_surface.blit(restartSurf, restartFontRect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            keys = pygame.key.get_pressed()
            if (keys[pygame.K_RETURN]):
                break

