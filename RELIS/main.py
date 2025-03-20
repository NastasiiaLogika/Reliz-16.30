from pygame import *
from random import randint
from time import time as timer

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
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

img_back = "images.png"
img_hero = "rocket.png"
img_enemy = "enemy.png"
img_ast = "mateorit.png"
img_comet = "mateorit.png"
img_bullet = "bullet.png"
font.init()
font2 = font.Font(None, 36)

score = 0
lost = 0
goal = 20
max_lost = 10
life = 3
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))

background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
comets = sprite.Group()
bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0
level = 1  # Initial level
level_up_time = 0  # To track the time for level-up message

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    ship.fire()
                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Lost: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.update()
        monsters.draw(window)

        ship.update()
        ship.reset()

        asteroids.update()
        asteroids.draw(window)

        comets.update()
        comets.draw(window)

        bullets.update()
        bullets.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reloading...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False) or sprite.spritecollide(ship, comets, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            sprite.spritecollide(ship, comets, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            game_over_text = font2.render("Game Over", 1, (255, 0, 0))
            window.blit(game_over_text, (200, 200))

        if score >= goal:
            level += 1
            goal += 10 * level
            for m in monsters:
                m.speed += 1
            for i in range(level):
                asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)
            for i in range(level - 1):
                comet = Enemy(img_comet, randint(50, win_width - 50), -40, 80, 50, randint(2, 6))
                comets.add(comet)
            level_up_time = timer()

        # Show Level 2 message when level reaches 2
        if level == 2:
            level_text = font2.render("Level 2", 1, (255, 255, 0))
            window.blit(level_text, (win_width // 2 - 60, win_height // 2 - 30))

        # Victory message when level > 5
        if level > 5:
            finish = True
            victory_text = font2.render("Final Victory! You won!", 1, (0, 255, 0))
            window.blit(victory_text, (win_width // 2 - 120, win_height // 2 - 30))

        display.update()
        time.delay(50)
