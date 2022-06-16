import json
import logging
import socket
import sys

import pygame
import uuid


class ClientInterface:
    def __init__(self, idplayer='1'):
        self.idplayer = idplayer
        self.server_address = ('192.168.1.4', 6666)
        # self.server_address = ('127.0.0.1',6666)

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

    def register_id(self):
        command_str = f"register_id {self.idplayer}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            return hasil
        else:
            return False

    def get_is_started(self):
        command_str = f"get_is_started {self.idplayer}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            is_started = hasil['is_started']
            return is_started
        else:
            return False

    def disconnect(self):
        command_str = f"disconnect {self.idplayer}"
        hasil = self.send_command(command_str)
        if (hasil['status'] == 'OK'):
            is_disconnected = hasil['is_disconnected']
            return is_disconnected
        else:
            return False


class Player:
    def __init__(self, pnum):
        # set player number/id
        self.pnum = pnum

        # player type (p1/p2)
        self.player_type = None

        # load sumo
        self.sumo = pygame.image.load("assets/sumo-baru.png")

        # craate client interface
        self.ci = ClientInterface(pnum)

        # is winning
        self.is_winning = None

    def send_push(self):
        self.ci.send_command(f'add_push {self.pnum}')

    def get_position(self):
        return self.ci.get_location()

    def get_win_state(self):
        self.is_winning = self.ci.get_win_state()
        return self.is_winning

    def register_id(self):
        hasil = self.ci.register_id()
        is_success = hasil['is_success']
        if (is_success):
            self.player_type = hasil['player_type']
        return is_success

    def get_is_started(self):
        return self.ci.get_is_started()

    def disconnect(self):
        return self.ci.disconnect()

    # def draw(self):


class Game:
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

        # load background
        self.wait_bg = pygame.image.load("assets/wait_bg.jpg")
        self.background = pygame.image.load("assets/bg.jpg")
        black_transparent = (0, 0, 0, 120)

        # soundeffect
        self.win_sound = pygame.mixer.Sound("assets/win_sound.mp3")
        self.lose_sound = pygame.mixer.Sound("assets/lose_sound.mp3")
        # self.start_sound = pygame.mixer.Sound("assets/finishhim.mp3")

        # load img
        self.img_spacepush_keydown = pygame.image.load('assets/space_push_keydown.png')
        self.img_spacepush_keyup = pygame.image.load('assets/space_push_keyup.png')

        # game state
        self.done = self.quit = False

    def set_screen_size(self, width=720, height=480):
        # set screen + its size
        SIZE = width, height = 720, 480
        self.screenHalfWidth = width / 2
        self.screenHalfHeight = height / 2
        self.screen = pygame.display.set_mode(SIZE)

    def set_text(self, text="", color=(255, 255, 255), size=48, y_offset=0, font="assets/shanghai.ttf"):
        # set pygame font
        FONT_SIZE = size
        GAME_FONT = pygame.freetype.Font(font, FONT_SIZE)

        # get text surface + position
        text_surface, textRect = GAME_FONT.render(text, color)
        textHalfWidth = text_surface.get_width() / 2
        textHalfHeight = text_surface.get_height() / 2
        textPosition = (self.screenHalfWidth - textHalfWidth, self.screenHalfHeight - textHalfHeight + y_offset)
        return [text_surface, textPosition]

    def set_img(self, img, y_offset=0):

        # set img position
        imgHalfWidth = img.get_width() / 2
        imgHalfHeight = img.get_height() / 2
        imgRect = img.get_rect().move(self.screenHalfWidth - imgHalfWidth, self.screenHalfHeight - imgHalfHeight + y_offset)
        return [img, imgRect]

    def set_fps(self, fps=30):
        return int(1000 / fps)

    def show_waiting_for_connecton(self):

        # get event (biar ga not responding)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.disconnect()
                sys.exit()

        # set wait bg
        self.screen.blit(self.wait_bg, (0, 0))

        # set waiting text
        color = (255, 0, 0)
        self.screen.blit(*self.set_text('Waiting for opponent...', color))

        # render display
        pygame.display.update()

    def show_play_again(self):

        # get event (biar ga not responding)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try_again = True
                    return try_again

        # set waiting text
        color = (255, 0, 0)
        self.screen.blit(*self.set_text('Press enter to play again', color, y_offset=100, size=24))

        # render display
        pygame.display.update()

        # wait try again
        try_again = False
        return try_again

    def is_game_ended(self):
        return player.is_winning is not None

    def render(self):

        spacepush_img_pressed = False

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

            if self.done or self.is_game_ended():
                if self.quit:
                    player.disconnect()
                    pygame.quit()
                    break
                elif self.done or self.is_game_ended():
                    break

            # get current location
            curr_location = self.player.get_position()
            print(f'curr location: {curr_location}')
            x, y = curr_location

            # draw background, player
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.player.sumo, (x, y))


            # draw P1/P2
            color = (255, 255, 0)
            p_type = str(self.player.player_type).upper()
            self.screen.blit(*self.set_text(f"You're {p_type}", color=color, size=32, y_offset=-210))

            # draw spacepush img
            spacepush_img_pressed = not spacepush_img_pressed
            if spacepush_img_pressed: self.screen.blit(*self.set_img(self.img_spacepush_keydown, 200))
            else: self.screen.blit(*self.set_img(self.img_spacepush_keyup, 200))

            # draw text win/lose
            win_state = self.player.get_win_state()
            if win_state:
                self.screen.blit(*self.set_text('You Win!'))
                self.win_sound.play()
            elif win_state is not None:
                self.screen.blit(*self.set_text('You Lose!'))
                self.lose_sound.play()

            # render display
            pygame.display.update()

            # wait for another render
            pygame.time.wait(self.timePerRender)


if __name__ == "__main__":

    while True:

        # init player with player id
        random_id = uuid.uuid1()
        player = Player(str(random_id)[0:6])
        print(random_id)

        # register player id
        is_success = player.register_id()
        while not is_success:
            pygame.time.wait(1500)
            is_success = player.register_id()

        # init game
        game = Game(player)
        game.set_screen_size()

        # waiting for opponent
        is_game_started = player.get_is_started()
        while not is_game_started:
            game.show_waiting_for_connecton()
            pygame.time.wait(game.timePerRender)
            is_game_started = player.get_is_started()

        # render gameplay
        game.render()

        # wait until game ended
        is_game_started = player.get_is_started()
        while is_game_started:
            pygame.time.wait(500)

        # if ended: disconnect, and give try again ui
        is_disconnected = player.disconnect()
        while not is_disconnected:
            pygame.time.wait(500)
            is_disconnected = player.disconnect()

        while is_disconnected:
            try_again = game.show_play_again()
            pygame.time.wait(game.timePerRender)
            if (try_again): break