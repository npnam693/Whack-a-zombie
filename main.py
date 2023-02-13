import pygame
import random
# --------
class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = zombies[random.randint(0,2)]
        rand = list(range(0, 11))
        for zom in zombie_group:
            if zom.index in rand:
                rand.remove(zom.index)
        self.index = rand[random.randint(0,len(rand)-1)]
        self.rect = self.image.get_rect(center = positions[self.index])
        self.time_live = game_level
        self.hit = False
        self.missed = False
    
    def time_countdown(self):
        self.time_live -= 1
        if self.time_live <= 0 :
            if self.hit == True:
                self.kill()
            else:
                if self.missed == False:
                    self.time_live = 32
                    self.missed = True
                    global miss_count
                    miss_count += 1
                else: 
                    self.kill()
    def movement(self):
        if not self.hit and not self.missed:
            if self.time_live % 2 == 0:
                self.rect.x += 2
            else:
                self.rect.x -= 2
    
    def hiting(self):
        self.hit = True
        global hit_count
        hit_count += 1
        self.time_live = 20
    
    def show_message(self):
        if self.hit == True:
            screen.blit(test_font.render('+1', False, 'Green') , (positions[self.index][0] - 10 , positions[self.index][1] - 60 + self.time_live))
        if self.missed == True:
            # screen.blit(test_font.render('+1', False, 'Red') , (positions[self.index][0] - 10 , positions[self.index][1] - 60 + self.time_live))
            self.image = test_font.render('+1', False, 'Red')
            self.rect = self.image.get_rect(center = (positions[self.index][0], positions[self.index][1] - 60 + self.time_live))

    def update(self):
        self.time_countdown()
        self.movement()
        self.show_message()
# --------
pygame.init()
pygame.display.set_caption('Whack a zombie!!')
screen = pygame.display.set_mode((900,600))
test_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

intro_surface = pygame.image.load('graphics/intro.png').convert()
background_surface = pygame.image.load('graphics/background.png').convert()

start_btn_surf = test_font.render('START GAME', False, 'Green')
start_btn_rect = start_btn_surf.get_rect(topleft = (500, 430))

zombie_1 = pygame.image.load('graphics/zombie_1.png').convert_alpha()
zombie_2 = pygame.image.load('graphics/zombie_2.png').convert_alpha()
zombie_3 = pygame.image.load('graphics/zombie_3.png').convert_alpha()
zombies = [zombie_1, zombie_2, zombie_3]
zombie_group = pygame.sprite.Group()


hammer_sound = pygame.mixer.Sound('sounds/hammer.wav')
hammer_sound.set_volume(0.5)


list_index = [False, False, False, False, False, False, False, False, False, False, False]
positions = [(65,351),(279,332),(202,365),(513,326),(664,344),(810,322),(115,513),(290,480),(537,459),(667,500),(829,523)]

zombie_appear = pygame.USEREVENT + 1
pygame.time.set_timer(zombie_appear,1500)

hit_count = 0
miss_count = 0
game_level = 40
game_active = False
while True: # main game loop
    game_level = 40 - int(hit_count / 5)*5
    print(game_level)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                hammer_sound.play()
                for zombie in zombie_group:
                    if zombie.rect.collidepoint(event.pos) and zombie.hit == False:
                        zombie.hiting()
            else:
                if start_btn_rect.collidepoint(event.pos):
                    hit_count = 0
                    miss_count = 0  
                    zombie_group = pygame.sprite.Group()
                    game_active = True
        if game_active:
            if event.type == zombie_appear:
                zombie_group.add(Zombie())
    if game_active:
        screen.blit(background_surface, (0,0))
        zombie_group.draw(screen)
        zombie_group.update()
        screen.blit(test_font.render('Hit:' + str(hit_count) , False, 'Green') , (20,20))
        screen.blit(test_font.render('Miss:' + str(miss_count) , False, 'Red') , (150,20))
        if miss_count == 10:
            game_active = False
    else:
        if miss_count != 0:
            screen.blit(intro_surface, (0,0))
            screen.blit(test_font.render('Hit:' + str(hit_count) , False, 'Green') , (580,340))
            screen.blit(test_font.render('Miss:' + str(miss_count) , False, 'Red') , (580,390))
            screen.blit(start_btn_surf, start_btn_rect)
        else:
            screen.blit(intro_surface, (0,0))
            screen.blit(start_btn_surf, start_btn_rect)

    pygame.display.update()
    clock.tick(60) 