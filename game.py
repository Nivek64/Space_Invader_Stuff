from multiprocessing.resource_sharer import stop
import pygame as pg
from settings import Settings
import game_functions as gf
from random import choice, randint

from laser import Lasers, LaserType
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
import obstacles
import sys

class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")
        self.speed_sound = Sound(bg_music="sounds/Speed_up_startrek.wav")
        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)  

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.settings.initialize_speed_settings()
        self.flag = False

        #UFO stuff
        self.ufo = pg.sprite.GroupSingle()
        self.ufo_spawn_time = randint(400, 800)

        #Going through shapes to make bunker at coordin
        self.shape = obstacles.shape
        self.block_size = 6
        self.blocks = pg.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (self.settings.screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_coordin = self.settings.screen_width / 15, y_coordin = 650)
    
    def drawmenu(self):
        button = pg.image.load(f'images/button1.png')
        menubg = pg.image.load(f'images/MenuBG.png')
        x, y = pg.mouse.get_pos()
        rect = button.get_rect(topleft = (x,y))

        self.screen.blit(menubg, (1, 1))
        self.screen.blit(button, (self.settings.screen_width - 730, 
                                 self.settings.screen_height - 200))
        for event in pg.event.get():
            if (event.type == pg.MOUSEBUTTONDOWN):
                if rect.collidepoint(pg.mouse.get_pos(x,y)):
                    self.flag = True
                    return
                    
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
        collisions = pg.sprite.groupcollide(self.blocks, self.ship_lasers.lasers, False, True)
        collisions_2 = pg.sprite.groupcollide(self.blocks, self.alien_lasers.lasers, False, True)
        collisions_3 = pg.sprite.groupcollide(self.alien_lasers.lasers, self.ship_lasers.lasers, False, True)
        if collisions:
            for block in collisions:
                block.kill()
        if collisions_2:
            for block in collisions_2:
                block.kill()
        if collisions_3:
            for lasers in collisions_3:
                lasers.kill()

    #def ufo_timer(self):
        #self.ufo_spawn_time -= 1
        #if self.ufo_spawn_time <= 0:
            #self.ufo.add(Ufo(choice(['right', 'left']), self.settings.screen_width))
            #self.ufo_spawn_time = randint(40, 80)
    
    #def block_reset(self): # NOTE: need to fix so that it resets with each round!!!
        #self.blocks.empty()

    def reset(self):
        print('Resetting game...')
        #self.block_reset()
        # self.lasers.reset()
        #self.blocks.draw(self.screen) 
        self.ship.reset()
        self.aliens.reset()
        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.sound.play_bg()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        pg.quit()
        sys.exit()


    def play(self):
        self.sound.play_bg()
        while True:
            self.screen.fill(self.settings.bg_color)
            self.scoreboard.update()
            self.drawmenu()
            pg.display.flip()
            if self.flag == True:
                break
        while True:
                gf.check_events(settings=self.settings, ship=self.ship)
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.scoreboard.update()
                #self.ufo_timer()
                self.ufo.update()
                self.collision_checks()
                self.blocks.draw(self.screen)   
                self.ufo.draw(self.screen)  
                pg.display.flip()
                    # self.lasers.update()


def main():
        g = Game()
        g.play()


if __name__ == '__main__':
    main()
