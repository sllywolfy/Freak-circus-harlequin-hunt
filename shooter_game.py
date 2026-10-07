#Create your own shooter

from pygame import *
from random import randint

score = 0
miss = 0
health = 3
cooldown = 0
cooldown_time = 2000

mixer.init()
mixer.music.load("backgrund sound.mp3")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.5)

window = display.set_mode((700, 500))
display.set_caption("shot")
background = transform.scale(image.load("background.jpg"), (700, 500))

font.init()
font1 = font.Font(None, 70)
win = font1.render('Yayy you win :3', True, (255, 215, 0))
lose = font1.render('You lost >:3', True, (180, 0, 0))

font2 = font.Font(None, 40)

title_font = font.Font(None, 70)
menu_font = font.SysFont("arial", 40)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(GameSprite):
    def update (self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def gun (self):
        pewpew = Pewpew("bullet.png", self.rect.centerx - 8, self.rect.top, 15, 20, 15)
        pewpews.add(pewpew)

class Pewpew(GameSprite):
    def update (self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update (self):
        global miss
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            miss += 1

player = Player("jester.png", 350, 350, 100, 100, 10)
num_monster = 5
monsters = sprite.Group()
pewpews = sprite.Group()

for i in range(num_monster):
    monster = Enemy("harlequin.png", randint(80, 700 - 80), -40, 100, 100, randint(1,5))
    monsters.add(monster)

clock = time.Clock()

finish = False
run = True
menu = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if menu:
                if e.key == K_SPACE:
                    menu = False
            elif not finish:
                if e.key == K_SPACE:
                    player.gun()
                    fire_sound.play()
    if menu:
        # Start menu
        window.blit(background, (0, 0))

        title = title_font.render("SPACE SHOOTER", True, (255, 255, 255))
        start_text = menu_font.render("Press SPACE to Start", True, (255, 255, 255))
        control_text = menu_font.render("LEFT / RIGHT - Move", True, (255, 255, 255))
        shoot_text = menu_font.render("SPACE - Shoot", True, (255, 255, 255))
        exit_text = menu_font.render("ESC - Exit", True, (255, 255, 255))

        window.blit(title, (150, 100))
        window.blit(start_text, (210, 220))
        window.blit(control_text, (210, 280))
        window.blit(shoot_text, (210, 330))
        window.blit(exit_text, (210, 380))

        display.update()
    elif not finish:
        window.blit(background,(0,0))
        player.reset()
        player.update()
        pewpews.update()
        pewpews.draw(window)
        monsters.update()
        monsters.draw(window)
        collides = sprite.groupcollide(monsters, pewpews, True, True)
        for c in collides:
            score += 1
            monster = Enemy("harlequin.png", randint(80, 700 - 80), -40, 100, 100, randint(1,5))
            monsters.add(monster)
        if cooldown <= 0:
            if sprite.spritecollide(player, monsters, False):
                health -= 1
                cooldown = cooldown_time
        if cooldown > 0:
            cooldown -= clock.get_time()

        text = font2.render("Score:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10,20))
        text = font2.render("Misses:" + str(miss), 1, (255, 255, 255))
        window.blit(text, (10,50))
        text = font2.render("Health:" + str(health), 1, (255, 255, 255))
        window.blit(text, (10,80))
        if score >= 50:
            finish = True 
            window.blit(win,(200,200))
        if health == 0 or miss == 5:
            finish = True 
            window.blit(lose,(200,200))
        display.update()
    clock.tick(30)