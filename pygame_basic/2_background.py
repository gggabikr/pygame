import pygame

pygame.init()  #초기화(반드시 필요한 부분)

#화면 크기 설정
screen_width = 480  #가로 크기
screen_height = 640   #세로크기
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀 설정

pygame.display.set_caption("Jason's Game")  #게임 이름

#배경 이미지 불러오기
background = pygame.image.load("C:/Users/gggab/OneDrive/Desktop/PythonWorkspace/pygame_basic/background.png")

#이벤트 루프 
running = True #게임이 진행중인가??
while running:
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: #창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님

    # screen.fill((0,0,255)) #RGB값
    screen.blit(background, (0,0)) #배경파일 그리기, 
                            #위치는 (0,0). (0,0)은 화면의 가장왼쪽가장위를 뜻함
    pygame.display.update() #게임화면 다시 그리기! 계속 다시 해야한다.
#pygame = 종료
pygame.quit()