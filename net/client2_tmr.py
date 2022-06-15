import json
import logging
import socket
import sys
import pygame


class ClientInterface:
    def __init__(self, idplayer='1'):
        self.idplayer = idplayer
        self.server_address = ('192.168.0.126', 6666)

    def send_command(self, command_str=""):
        global server_address
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.server_address)
        logging.warning(f"connecting to {self.server_address}")
        try:
            logging.warning(f"sending message ")
            sock.sendall(command_str.encode())
            # Look for the response, waiting until socket is done (no more data)
            data_received = ""  # empty string
            while True:
                # socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
                data = sock.recv(16)
                if data:
                    # data is not empty, concat with previous content
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        break
                else:
                    # no more data, stop the process by break
                    break
            # at this point, data_received (string) will contain all data coming from the socket
            # to be able to use the data_received as a dict, need to load it using json.loads()
            hasil = json.loads(data_received)
            logging.warning("data received from server:")
            return hasil
        except:
            logging.warning("error during data receiving")
            return False

    # def set_location(self, x=100, y=100):
    #     player = self.idplayer
    #     command_str = f"set_location {player} {x} {y}"
    #     hasil = self.send_command(command_str)
    #     if (hasil['status'] == 'OK'):
    #         return True
    #     else:
    #         return False

    def get_location(self):
        player = self.idplayer
        command_str = f"get_location {player}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]), int(lokasi[1]))
        else:
            return False

pygame.init()

# set screen + its size
SIZE = width, height = 720, 480
screen = pygame.display.set_mode(SIZE)
screenHalfWidth = width/2
screenHalfHeight = height/2
clock = pygame.time.Clock()

# set window title
pygame.display.set_caption('Pendorong Handal')

# set pygame font
FONT_SIZE = 48
GAME_FONT = pygame.freetype.Font("assets/shanghai.ttf", FONT_SIZE)
def getText(text):
    text_surface, textRect = GAME_FONT.render(text, (255, 255, 255))
    textHalfWidth = text_surface.get_width() / 2
    textHalfHeight = text_surface.get_height() / 2
    textPosition = (screenHalfWidth - textHalfWidth, screenHalfHeight - textHalfHeight)
    return [text_surface, textPosition]

# set push power
pushPower = 5

# load sumo
sumo = pygame.image.load("assets/sumo.png")

# laod background
background = pygame.image.load("assets/bg.jpg")
black_transparent = (0, 0, 0, 120)

# set sumo position
sumoHalfWidth = sumo.get_width()/2
sumoHalfHeight = sumo.get_height()/2
sumoRect = sumo.get_rect().move(screenHalfWidth-sumoHalfWidth, screenHalfHeight-sumoHalfHeight)
print(sumoRect)

# set fps
fps = 30
timePerRender = int(1000/fps)

# init client interface
pnum = '2'
ci_2 = ClientInterface()


done = quit = False

initial_ticks = pygame.time.get_ticks()

while True:
    seconds = (pygame.time.get_ticks() - initial_ticks) / 1000
    # get event
    if seconds > 10:
        break
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    ci_1.send_command(f'add_push {pnum}')
                    print("SPACE pressed")
    print(seconds)

    if done:
        # wait for another render
        pygame.time.wait(timePerRender)

        if quit:
            pygame.quit()
            break

        continue

    # get current location
    curr_location = ci_2.get_location()
    print(f'curr location: {curr_location}')
    x, y = curr_location

    # draw background, image, text
    screen.blit(background, (0, 0))
    screen.blit(sumo, (x, y))

    # render display
    pygame.display.update()

    # wait for another render
    pygame.time.wait(timePerRender)