import pygame

################################################
# 기본 초기화
pygame.init()  #초기화(반드시 필요한 부분)

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640   #세로크기
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Jason's Game")  #게임 이름

#FPS
clock = pygame.time.Clock()
################################################  이부분은 무조건 해야하는부분

#1. 사용자 게임 초기화(배경, 게임이미지, 좌표, 속도, 폰트등등)

running = True #게임이 진행중인가??
while running:
    dt = clock.tick(60) #dt=델타라고 읽음/ 게임화면의 초당 프레임 수를 설정

    #2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님

    #3. 게임 캐릭터 위치 정의 및 경계값 처리

    #4. 충돌 처리

    #5. 화면에 그리기 

    #6. 업데이트
    pygame.display.update() #

pygame.quit()