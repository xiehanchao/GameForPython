import random
import pygame

# 屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 创建英雄发射子弹定时器
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed


class Background(GameSprite):
    def __init__(self, is_alt=False):
        super().__init__("./feiji/background.png")
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        super().update()

        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        super().__init__("./feiji/enemy1.png")
        # 指定随机速度
        self.speed = random.randint(1, 3)
        # 当rect.bottom = 0时,敌机默认为屏幕之外
        self.rect.bottom = 0;
        # X轴
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            # 将当前精灵从所有精灵组删除，并且会自动销毁
            self.kill()

    # 当对象销毁，会提前调用
    def __del__(self):
        pass


class Hero(GameSprite):
    isUpAndDown = False

    def __init__(self):
        super().__init__("./feiji/hero1.png", 0)
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        self.bullets = pygame.sprite.Group()

    def update(self):
        if self.isUpAndDown == True:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom
            
    def fire(self):
        bullet = Bullet()

        bullet.rect.bottom = self.rect.y - 20
        bullet.rect.centerx = self.rect.centerx

        self.bullets.add(bullet)


class Bullet(GameSprite):

    def __init__(self):
        super().__init__("./feiji/bullet1.png", -2)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
        print("子弹被销毁")
