import pygame
import os

################################################
# 기본 초기화
pygame.init()  #초기화(반드시 필요한 부분)

#화면 크기 설정
screen_width = 640  #가로 크기
screen_height = 480   #세로크기
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Jason's second game")  #게임 이름

#FPS
clock = pygame.time.Clock()

#1. 사용자 게임 초기화(배경, 게임이미지, 좌표, 속도, 폰트등등)

#이전과 다른 방식으로 배경을 가져와보기
current_path = os.path.dirname(__file__)  #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images")  #images 폴더 위치 반환

#배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]  #스테이지의 높이 위에 캐릭터두기, 공 튕기게 하기위해.

#캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character_front.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width/2) - (character_width/2)
character_y_pos = screen_height - character_height - stage_height +10

#캐릭터 이동 방향
character_to_x = 0

#캐릭터 이동 속도
character_speed = 5

#무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한번에 여러발 발사 가능
weapons = []    #리스트로 일단 생성

#무기 이동 속도
weapon_speed = 15


running = True #게임이 진행중인가??
while running:
    dt = clock.tick(60) #dt=델타라고 읽음/ 게임화면의 초당 프레임 수를 설정

    #2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                character_to_x -= character_speed   
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos  #캐릭터의 머리위치에서 발사한다 가정
                weapons.append([weapon_x_pos,weapon_y_pos]) #weapons리스트에 x y위치정보를 또다른 리스트의 형태로 추가




        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    #3. 게임 캐릭터 위치 정의 및 경계값 처리
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width


    #무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] #무기 위치를 위로 올림
    #여기서의 w는 weapons안에있는 하나의 list(x,y데이터를 가진)값. 그 w의 첫번째, 두번째 값을 불러온후, 
    #어떤처리를(두번째 값에다가 speed를 빼는 작업) 한후, 다시 weapons로 값을 집어넣어라, 그런의미.
    #ex) (100,200)에서 무기발사했다면, 그 위치가 (100,190), (100,180), (100,170)...
    #    (500,200)에서 발사한건 (500,190), (500,180), (500,170)... 이렇게 바뀌어야함.

    #천장에 닿은 무기 제거
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0 ]
    #weapons안의 w를 다시한번 불러와서, 그중에서 y값이 0보다 큰것만 weapons로 넣겠다는 의미.
    #결론적으로 y값이 0과 같거나 작아지는 순간(천장에 닿는 순간), 그건 weapons리스트에서 
    #없어진 데이터가 되어버리므로, 사라지게된다.

    #4. 충돌 처리

    #5. 화면에 그리기 
    screen.blit(background, (0, 0))

    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos,weapon_y_pos))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))


    #6. 업데이트
    pygame.display.update()

pygame.quit()