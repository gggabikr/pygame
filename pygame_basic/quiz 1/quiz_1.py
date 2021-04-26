import pygame


pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Jason's quiz_1")

clock = pygame.time.Clock()

background = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/quiz 1/-paper-textured-background_53876-42312.jpg")

game_font = pygame.font.Font(None, 40)
gameover_font = pygame.font.Font(None, 100)

character = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/quiz 1/pugs.jpg")
character_size = character.get_size()
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width-character_width)/2
character_y_pos = screen_height - character_height

to_x = 0
character_speed = 0.6

from random import*

poop = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/quiz 1/funny-poop.jpg")
poop_size = poop.get_size()
poop_width = poop_size[0]
poop_height = poop_size[1]
poop_x_pos = randrange(0,screen_width-poop_width)
poop_y_pos = 0 - poop_height+10

poop2 = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/quiz 1/funny-poop.jpg")
poop2_size = poop.get_size()
poop2_width = poop_size[0]
poop2_height = poop_size[1]
poop2_x_pos = randrange(0,screen_width-poop_width)
poop2_y_pos = 0 - poop_height+10


poop3 = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/quiz 1/funny-poop.jpg")
poop3_size = poop.get_size()
poop3_width = poop_size[0]
poop3_height = poop_size[1]
poop3_x_pos = randrange(0,screen_width-poop_width)
poop3_y_pos = 0 - poop_height+10
poop_speed = randint(7,15)
poop2_speed = randint(7,15)
poop3_speed = randint(5,10)

score = 0

running = True
while running:
    dt = clock.tick(40)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LEFT:
                    to_x -= character_speed
                elif event.key == pygame.K_RIGHT:
                    to_x += character_speed
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
  
    character_x_pos += to_x * dt 
    
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos> screen_width-character_width:
        character_x_pos = screen_width-character_width

    poop_y_pos += poop_speed
    poop2_y_pos += poop2_speed
    poop3_y_pos += poop3_speed

    if poop_y_pos > screen_height:
        poop_y_pos = 0- poop_height
        poop_x_pos = randrange(0,screen_width-poop_width)
        poop_speed = randint(7,15)
        score += 5

    if poop2_y_pos > screen_height:
        poop2_y_pos = 0- poop_height
        poop2_x_pos = randrange(0,screen_width-poop_width)
        poop2_speed = randint(7,15)
        score += 5

    if poop3_y_pos > screen_height:
        poop3_y_pos = 0- poop_height
        poop3_x_pos = randrange(0,screen_width-poop_width)
        poop3_speed = randint(5,10)
        score += 5

    #4. 충돌 처리
    character_rect = character.get_rect()
    character_rect.left = character_x_pos   #아래쪽에서 blit함수 같은경우는 이미지를 원하는 위치에
    character_rect.top = character_y_pos    # 그림을 표시 해줄뿐, 실제의 위치를 변경시켜주진않는다.
                                            #그렇기때문에 이런 작업이 필요하다.
  
    poop_rect = poop.get_rect()
    poop_rect.left = poop_x_pos  
    poop_rect.top = poop_y_pos

    
    poop2_rect = poop2.get_rect()
    poop2_rect.left = poop2_x_pos  
    poop2_rect.top = poop2_y_pos

    poop3_rect = poop3.get_rect()
    poop3_rect.left = poop3_x_pos  
    poop3_rect.top = poop3_y_pos

    gameover = gameover_font.render("GAME OVER", True, (0,0,0))
    scores = game_font.render("Score : "+str(score), True, (0,0,0))
    gameover_loctn = gameover.get_rect(center = (int(screen_width/2), int(screen_height/2)))

    screen.blit(background, (0, 0)) 
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(poop, (poop_x_pos, poop_y_pos))   
    screen.blit(poop2, (poop2_x_pos, poop2_y_pos)) 
    screen.blit(poop3, (poop3_x_pos, poop3_y_pos)) 
    screen.blit(scores, (10, 10))
    pygame.display.update()

    if character_rect.colliderect(poop_rect):
        # print("충돌 했어요")
        running = False

    if character_rect.colliderect(poop2_rect):
        # print("충돌 했어요")
        running = False
    if character_rect.colliderect(poop3_rect):
        # print("충돌 했어요")
        running = False

# screen.blit(gameover, (screen_width/2-210, screen_height/2-30))
screen.blit(gameover, gameover_loctn)
pygame.display.update()

pygame.time.delay(2000)
pygame.quit()