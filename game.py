import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers
from alien import Aliens
from ship import Ship
import obstacles
from sound import Sound
from scoreboard import Scoreboard
import sys


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")

        self.scoreboard = Scoreboard(game=self)  
        self.lasers = Lasers(settings=self.settings)
        self.ship = Ship(game=self, screen=self.screen, settings=self.settings, sound=self.sound, lasers=self.lasers)
        self.aliens = Aliens(game=self, screen=self.screen, settings=self.settings, lasers=self.lasers, ship=self.ship)
        

        # launch screen TODO
        
        #Making the obstacles object
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (self.settings.screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_coordin = self.settings.screen_width / 15, y_coordin = 650)

        self.settings.initialize_speed_settings()
    
    #Going through shapes to make bunker at coordin
    def create_obstacle(self, x_coordin, y_coordin, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_coordin + col_index*self.block_size + offset_x
                    y = y_coordin + row_index*self.block_size
                    block = obstacles.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)
    # put a collision for bunker
    # random number generator - show damage until destroyed
    def create_multiple_obstacles(self, *offset, x_coordin, y_coordin):
        for offset_x in offset:
            self.create_obstacle(x_coordin, y_coordin, offset_x)

    #When laser hits the Bunker
    def collision_checks(self):
        #Work out some kinks on this line of code
        collisions = pg.sprite.spritecollide(self.ship, self.blocks, True)  #Changing self.ship to something else
        if collisions:
            for block in collisions:
                block.kill()

    def reset(self):
        print('Resetting game...')
        self.lasers.reset()
        self.ship.reset()
        self.aliens.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.lasers.update()
            self.scoreboard.update()
            self.collision_checks()
            self.blocks.draw(self.screen)
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
