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
character_to_x_LEFT = 0
character_to_x_RIGHT = 0
left_pressed = False
right_pressed = False
#좌우 동시눌렀을떄 키 충돌을 막기위해 character_to_x하나가아닌 좌우 두개로 나눔

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

#공 만들기 (4개의 크기에 대해 따로 처리)
ball_images = [\
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

#공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]  #index 0,1,2,3에 해당하는 값

#공들(리스트)
balls = []

#최초 발생하는 큰 공 추가(dictionary 타입으로 생성)
balls.append({
    "pos_x": 50,    #공의 x 좌표
    "pos_y":50,     #공의 y 좌표
    "img_idx" : 0,  #공의 이미지 인덱스
    "to_x":3,        #공의 x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y": -6,      #공의 y축 이동방향, 처음에 살짝 위로올라갔다내려오게하기위해 -값으로 설정
    "init_spd_y": ball_speed_y[0]   #공의 y축 최초 속도
    })

#사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#폰트 정의
game_font = pygame.font.Font(None, 40)

#게임종료 메세지
#Time Over(시간 초과), Mission Complete(성공), Game Over(공에맞음)
game_result = "Game Over"   

#시간관련
total_time = 100
start_ticks = pygame.time.get_ticks() #시작시간 정의


running = True #게임이 진행중인가??
while running:
    dt = clock.tick(30) #dt=델타라고 읽음/ 게임화면의 초당 프레임 수를 설정

    #2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                character_to_x_LEFT -= character_speed   
                left_pressed = True
                if right_pressed:
                        character_to_x_RIGHT = 0
                        right_pressed = False
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
                right_pressed = True
                if left_pressed:
                        character_to_x_LEFT = 0
                        left_pressed = False
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos  #캐릭터의 머리위치에서 발사한다 가정
                weapons.append([weapon_x_pos,weapon_y_pos]) #weapons리스트에 x y위치정보를 또다른 리스트의 형태로 추가

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
                left_pressed = False

            if event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0
                right_pressed = False
    #3. 게임 캐릭터 위치 정의 및 경계값 처리
    character_x_pos += (character_to_x_LEFT +character_to_x_RIGHT)

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

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls): 
        #각각의 공 위치를 정의할때, 
        #공의 인덱스 넘버가 필요해서 이와같이 설정. 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        #가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width-ball_width:
            ball_val["to_x"] = ball_val["to_x"]*-1  
            #공이 벽에 부딪히면 x축 이동방향에 -1을 곱해서 반대로 바꿔줌.

        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height-stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        #볼에 아래를 향한 가속도를붙임.
        else:
            ball_val["to_y"] += 0.5
        #이렇게 되면 처음 to_y값(-6)으로 위로 올라가다가 점점 올라가는 속도가
        #줄어들게되고, 0이 되는순간부터는 아래로 점점 빠르게 내려오게된다.
        #그러다가 stage높이에 닿는순간 init_spd_y의 속도(-18)로 튕겨올라가고,
        #그것을 반복하는 움직임을 보이게 됨.

        #위에서 정리한 to_x 와 to_y의 값을 틱(tick)마다 공 위치에 반영
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    #4. 충돌 처리

    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #각각의 공에대한 공 rect 정보 업데이트
    for ball_idx, ball_val in enumerate(balls): 
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        
        #공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            running = False
            break

        #공과 무기들 충돌처리
        for weapon_idx, weapon_val in enumerate(weapons): 
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 rect정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx #해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx #해당 공 없애기 위한 값 설정

                #가장작은 크기의 공이 아니라면 다음단계의 공으로 나눠주기
                if ball_img_idx < 3: 
                    #현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    
                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),    
                        #ball_pos_x는 공의 왼쪽끝이니까 폭의 절반만큼 더함(이게 큰공 중앙x값)
                        #여기서 작은공의 폭의 절반만큼 뺌,그걸 기준으로 오른쪽에 그려지니까, 
                        #그 공중앙이 큰공중앙이었던 선에 맞게
                        "pos_y":ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        #마찬가지로 ball_pos_y는 공의 위쪽끝, 높이절반 더함 - 큰공중앙,
                        #여기서 작은공 높이 절반 뺌, 큰공중앙보다 작은공반지름만큼 높은위치.
                        #->그래야 작은공의 중앙이 큰공중앙이었던 선과 같은 높이가 되므로. 
                        "img_idx" : ball_img_idx + 1,  #공의 이미지 인덱스
                        "to_x": -3,        #공의 x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
                        "to_y": -6,      #공의 y축 이동방향, 처음에 살짝 위로올라갔다내려오게하기위해 -값으로 설정
                        "init_spd_y": ball_speed_y[ball_img_idx +1]})

                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x": ball_pos_x + (ball_width / 2) - (small_ball_width / 2),    
                        "pos_y":ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x": 3, #이것만 +3으로 하고 나머진 동일
                        "to_y": -6,  
                        "init_spd_y": ball_speed_y[ball_img_idx +1]})
                break
        else:
            continue    #안쪽 for문의 조건이 맞지않으면 continue, 바깥쪽 for문을 계속 수행
        break   #안쪽 for문에서 break를 만나면 여기로 진행 = 2중 for문을 한번에 탈출

    #위쪽 복잡한 구조를 아래와 같이 도식화 할 수있다.
    # for 바깥조건:
    #     바깥동작
    #     for 안쪽조건:
    #         안쪽동작
    #         if 충돌하면:
    #             break
    #     else:
    #         continue
    #     break

    #충돌된 공 and 무기 없애기
    if ball_to_remove > -1:     #이걸 위해서 위에 값을 -1로 설정해두었다.
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    #모든 공을 없앤 경우 게임 종료 (성공)
    if len(balls) ==0:      #balls리스트의 길이(내부 항목의 개수)가 0이면,
        game_result = "Mission Complete"
        running = False

    #5. 화면에 그리기 
    screen.blit(background, (0, 0))

    for weapon_x_pos,weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos,weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x,ball_pos_y))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos,character_y_pos))


    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10, 10))

    #시간 초과
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    #6. 업데이트
    pygame.display.update()

#게임오버 메세지
msg = game_font.render(game_result, True, (255, 255, 0)) #노란색
msg_rect = msg.get_rect(center = (int(screen_width/2), int(screen_height/2)))
#center에 저렇게 넣어서(int는 걍 소수말고 정수값할라고 넣은거) 화면 중앙위치반환
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()