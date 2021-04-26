import pygame

pygame.init()  #초기화(반드시 필요한 부분)

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640   #세로크기
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Jason's Game")  #게임 이름

#FPS
clock = pygame.time.Clock()

#배경 이미지 불러오기
background = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/background.png")

#스프라이트(캐릭터) 불러오기
character = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/character.png")
character_size = character.get_size()  #캐릭터 파일의 사이즈를 가져옴
character_width = character_size[0] #캐릭터의 가로크기 (위에서 불러온 데이터의 첫번째 값)
character_height = character_size[1] #캐릭터의 세로크기 (위에서 불러온 데이터의 두번째 값)
character_x_pos = (screen_width-character_width)/2 # 화면 가로길이의 절반위치에 위치((240-56)/2)(캐릭파일 가로 = 56)
# character_y_pos = screen_height #화면 세로길이의 가장 아래에 위치(640-70)(캐릭파일 세로 = 70)
#이경우 그림이 오른쪽 아래로 그려지기때문에 화면상에 보이지않는다.
character_y_pos = screen_height - character_height  #화면 세로길이의 가장 아래에 위치(640)

#이동할 좌표
to_x = 0
to_y = 0

#이동속도
character_speed = 0.6

#적 캐릭터 enemy
enemy = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/enemy.png")
enemy_size = enemy.get_size()
enemy_width = enemy_size[0]
enemy_height = enemy_size[1] 
enemy_x_pos = (screen_width-enemy_width)/2 
enemy_y_pos = (screen_height/2) - (enemy_height/2) 

#이벤트 루프 
running = True #게임이 진행중인가??
while running:
    dt = clock.tick(120) #dt=델타라고 읽음/ 게임화면의 초당 프레임 수를 설정
    print("fps : " +str(clock.get_fps()))

    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님
        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key ==pygame.K_LEFT:
                to_x -= character_speed   #위에서 to_x, to_y값 0으로 설정해준후에 써야한다.
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key ==pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed

        if event.type == pygame.KEYUP:  #방향키를 떼면(누르지않으면) 멈추도록
            if event.key ==pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key ==pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    character_x_pos += to_x * dt #위에서 쓴부분이 실제로 적용되도록 이부분을 써야함
    character_y_pos += to_y * dt #dt=1/fps 라서 이걸 곱해줌으로써 프레임별로 속도가 달라지는걸 방지할수있다.

    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos> screen_width-character_width:
        character_x_pos = screen_width-character_width

    #세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos> screen_height-character_height:
        character_y_pos = screen_height-character_height

    #충돌처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos   #아래쪽에서 blit함수 같은경우는 이미지를 원하는 위치에
    character_rect.top = character_y_pos    # 그림을 표시 해줄뿐, 실제의 위치를 변경시켜주진않는다.
                                            #그렇기때문에 이런 작업이 필요하다.
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos  
    enemy_rect.top = enemy_y_pos

    #충돌 체크
    if character_rect.colliderect(enemy_rect):   #colliderect = 사각형기준으로 충돌이 있었는지 체크
        print("충돌 했어요")
        running = False



    screen.blit(background, (0,0)) #배경파일 그리기, 
                            #위치는 (0,0). (0,0)은 화면의 가장왼쪽가장위를 뜻함
    screen.blit(character,(character_x_pos,character_y_pos))  #캐릭터 그리기(대상,좌표)
    screen.blit(enemy,(enemy_x_pos,enemy_y_pos))    #적그리기

    pygame.display.update() #게임화면 다시 그리기! 계속 다시 해야한다.

#pygame = 종료
pygame.quit()