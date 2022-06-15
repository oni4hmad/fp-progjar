import json
import logging
import socket
import sys
import pygame


class ClientInterface:
    def __init__(self, idplayer='1'):
        self.idplayer = idplayer
        self.server_address = ('192.168.1.4', 6666)

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

    def get_location(self):
        player = self.idplayer
        command_str = f"get_location {player}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            lokasi = hasil['location'].split(',')
            return (int(lokasi[0]), int(lokasi[1]))
        else:
            return False

    def get_win_state(self):
        player = self.idplayer
        command_str = f"get_is_win {player}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            is_win = hasil['is_win']
            return is_win
        else:
            return None


class Player:
    def __init__(self, pnum):
        # set player number/id
        self.pnum = pnum

        # load sumo
        self.sumo = pygame.image.load("assets/sumo.png")

        # craate client interface
        self.ci = ClientInterface(pnum)

    def send_push(self):
        self.ci.send_command(f'add_push {self.pnum}')

    def get_position(self):
        return self.ci.get_location()

    def get_win_state(self):
        return self.ci.get_win_state()

    # def draw(self):


class Game():
    def __init__(self, player=Player('1'), title="Pendorong Handal"):
        pygame.init()

        # set window title
        self.title = title
        pygame.display.set_caption(self.title)

        # init player
        self.player = player

        # set screen
        self.screenHalfWidth = None
        self.screenHalfHeight = None
        self.screen = None

        # set render delay
        self.timePerRender = self.set_fps(30)

        # laod background
        self.background = pygame.image.load("assets/bg.jpg")
        black_transparent = (0, 0, 0, 120)

        # game state
        self.done = self.quit = False

    def set_screen_size(self, width=720, height=480):
        # set screen + its size
        SIZE = width, height = 720, 480
        self.screenHalfWidth = width / 2
        self.screenHalfHeight = height / 2
        self.screen = pygame.display.set_mode(SIZE)

    def set_text(self, text="", color=(255, 255, 255), size=48, font="assets/shanghai.ttf"):
        # set pygame font
        FONT_SIZE = size
        GAME_FONT = pygame.freetype.Font(font, FONT_SIZE)

        # get text surface + position
        text_surface, textRect = GAME_FONT.render(text, color)
        textHalfWidth = text_surface.get_width() / 2
        textHalfHeight = text_surface.get_height() / 2
        textPosition = (self.screenHalfWidth - textHalfWidth, self.screenHalfHeight - textHalfHeight)
        return [text_surface, textPosition]

    def set_fps(self, fps=30):
        return int(1000 / fps)

    def render(self):

        while True:

            # get event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    self.quit = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.player.send_push()
                        print("SPACE pressed")

            if self.done:
                # wait for another render
                pygame.time.wait(self.timePerRender)

                if quit:
                    pygame.quit()
                    break

                continue

            # get current location
            curr_location = self.player.get_position()
            print(f'curr location: {curr_location}')
            x, y = curr_location

            # draw background, player
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.sumo, (x, y))

            # draw text win/lose
            win_state = self.player.get_win_state()
            print("win_state", win_state)
            if win_state:
                self.screen.blit(*self.set_text('You Win!'))
            elif win_state == False:
                self.screen.blit(*self.set_text('You Lose!'))

            # render display
            pygame.display.update()

            # wait for another render
            pygame.time.wait(self.timePerRender)


if __name__ == "__main__":
    player = Player('2')
    game = Game(player)
    game.set_screen_size()
    game.render()
