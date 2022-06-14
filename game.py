import sys, pygame
pygame.init()

# set screen + its size
size = width, height = 720, 480
screen = pygame.display.set_mode(size)
screenHalfWidth = width/2
screenHalfHeight = height/2

# set window title
pygame.display.set_caption('Sumo Battle!')

# set pygame font
FONT_SIZE = 72
GAME_FONT = pygame.freetype.Font("asset/shanghai.ttf", FONT_SIZE)
def getText(text):
    text_surface, textRect = GAME_FONT.render(text, (255, 255, 0))
    textHalfWidth = text_surface.get_width() / 2
    textHalfHeight = text_surface.get_height() / 2
    textPosition = (screenHalfWidth - textHalfWidth, screenHalfHeight - textHalfHeight)
    return [text_surface, textPosition]

# set push power
pushPower = 5

# load sumo
sumo = pygame.image.load("asset/somo_battle.png")

# laod backgorund

background = pygame.image.load("asset/background.jpg")
black_transparent = (0, 0, 0, 120)

# set sumo position
sumoHalfWidth = sumo.get_width()/2
sumoHalfHeight = sumo.get_height()/2
sumoRect = sumo.get_rect().move(screenHalfWidth-sumoHalfWidth, screenHalfHeight-sumoHalfHeight)

# set fps
fps = 30
timePerRender = int(1000/fps)

done = quit = False
while True:

    # get event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            quit = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                sumoRect = sumoRect.move(-pushPower, 0)
            elif event.key == pygame.K_RIGHT:
                sumoRect = sumoRect.move(pushPower, 0)

    if done:
        # wait for another render
        pygame.time.wait(timePerRender)

        if quit:
            pygame.quit()
            break

        continue

    # draw background, image, text
    screen.blit(background, (0, 0))
    screen.blit(sumo, sumoRect)

    # cek winner
    if sumoRect.left < 0:
        print('player 1 win')
        screen.blit(*getText("You Lose!"))
        done = True
    elif sumoRect.right > width:
        print('player 2 win')
        screen.blit(*getText("You Win!"))
        done = True

    # render display
    pygame.display.update()

    # wait for another render
    pygame.time.wait(timePerRender)