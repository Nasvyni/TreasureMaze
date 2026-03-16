from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 60:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 60:
            self.rect.y += self.speed

class Enemy(GameSprite):
    side = "left"
    def update(self):
        if self.rect.x <= 470:
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface([self.width, self.height])
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
 
    def draw_wall(self):
        draw.rect(window, (self.color_1, self.color_2, self.color_3), (self.rect.x, self.rect.y, self.width, self.height))

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Labirin")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

w1 = Wall(154, 205, 50, 100, 20 , 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20 , 10, 380)
w4 = Wall(154, 205, 50, 200, 130, 10, 350)
w5 = Wall(154, 205, 50, 450, 130, 10, 360)
w6 = Wall(154, 205, 50, 300, 20, 10, 350)
w7 = Wall(154, 205, 50, 390, 120, 130, 10)

walls = [w1, w2, w3, w4, w5, w6, w7]

packman = Player('hero.png', 5, win_height - 80, 4)
monster = Enemy('cyborg.png', win_width - 80, 280, 2)
final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
game_font = font.Font(None, 70)
hint_font = font.Font(None, 30)

win = game_font.render('YOU WIN!', True, (255, 215, 0))
lose = game_font.render('YOU LOSE!', True, (180, 0, 0))
retry_text = hint_font.render('Press R to Restart', True, (255, 255, 255))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_r and finish:
                packman.rect.x = 5
                packman.rect.y = win_height - 80
                finish = False

    if finish != True:
        window.blit(background,(0, 0))
        packman.update()
        monster.update()
        
        packman.reset()
        monster.reset()
        final.reset()
        
        for w in walls:
            w.draw_wall()

        if sprite.collide_rect(packman, monster) or any(sprite.collide_rect(packman, w) for w in walls):
            finish = True
            window.blit(lose, (200, 200))
            window.blit(retry_text, (260, 270))
            kick.play()

        if sprite.collide_rect(packman, final):
            finish = True
            window.blit(win, (200, 200))
            window.blit(retry_text, (260, 270))
            money.play()

    display.update()
    clock.tick(FPS)