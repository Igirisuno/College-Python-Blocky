#!/usr/bin/python

import sys
import pygame
from pygame import *

import levels
from levels import *

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#defines the window resolutions for use with the display and camera
winWidth = 800
winHeight = 640
window = (winWidth, winHeight)
#halves the window resolution to center the camera
winHalfWidth = int(winWidth / 2)
winHalfHeight = int(winHeight / 2)

### Main Menu Code ###


class MenuItem(pygame.font.Font):

    #Defines the function for the MenuItem initialisation code.
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, (pos_x, pos_y)=(0, 0)):
        #Creates variables to be used by the main menu
        #Such as font, colour, size, position... etc.
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    #Defines the function for checking which menu item the mouse is selecting.
    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
                (posy >= self.pos_y and posy <= self.pos_y + self.height):
            return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


#Main code for the menu


class GameMenu():

    def __init__(self, screen, items, funcs, bg_color=BLACK, font=None,
                 font_size=30, font_color=WHITE):
        #Sets window caption
        pygame.display.set_caption('Blocky! - Menu')

        self.screen = screen
        self.scr_width = winWidth
        self.scr_height = winHeight

        self.bg_color = bg_color

        #Clock is used to manage the framerate of the game.
        self.clock = pygame.time.Clock()
        self.funcs = funcs

        self.items = []
        #This for loop ensures that each menu item is placed
        #beneath the previous with the initial item being centered.
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + \
                (index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    #This function checks if mouse_is_visible is set to True or False
    #and enables/disables the mouse cursor accordingly.
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        #Marks the MenuItem chosen via up and down keys.
        for item in self.items:
            #Returns text style to neutral
            item.set_italic(False)
            item.set_font_color(WHITE)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            #Find the chosen item
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        #Changes the text style of the selected item.
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(RED)

        #Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text]()

    def set_mouse_selection(self, item, mpos):
        #Marks the MenuItem the mouse cursor hovers on.
        if item.is_mouse_selection(mpos):
            #Changes the text style of the selected item.
            item.set_font_color(RED)
            item.set_italic(True)
        else:
            #Returns text style to neutral.
            item.set_font_color(WHITE)
            item.set_italic(False)

    def run(self):
        mainloop = True
        while mainloop:
            #Limits framerate to 60 FPS.
            self.clock.tick(60)

            #gets the current mouse position and sets it as 'mpos'.
            mpos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                #Exits the game without crashing should the
                #QUIT event be raised or the 'Escape' key pushed.
                if event.type == pygame.QUIT:
                    raise SystemExit('QUIT')
                if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    raise SystemExit('ESCAPE')
                elif event.type == pygame.KEYDOWN:
                    #Disables the mouse cursor if key is pressed.
                    self.mouse_is_visible = False
                    #Passes the pressed key to the
                    #set_keyboard_selection function.
                    self.set_keyboard_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Runs a function depending on which item the mouse clicks.
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text]()

            #Reenables the mouse once movement is detected.
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            #Redraw the background
            self.screen.fill(self.bg_color)

            #Creates the menu from the menu_items
            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            #Refreshes the display
            pygame.display.flip()

### Start Screen Code ###


def startScreen():
    #Loads the startScreen image and blits it to the screen.
    imgStartScreen = pygame.image.load("images/startScreen.png").convert()
    screen.blit(imgStartScreen, (0, 0))
    pygame.display.flip()

    #Checks for button presses and starts the game
    #if one is detected.
    while 1:
        for e in pygame.event.get():
            if e.type == KEYDOWN or e.type == MOUSEBUTTONDOWN:
                main()
                return


### Game Code ###


def main():
    global cameraX, cameraY
    #creates the window
    screen = pygame.display.set_mode(window)
    pygame.display.set_caption("Blocky!")

    timer = pygame.time.Clock()

    #sets the following variables initial state to false
    up = down = left = right = running = False
    #creates the background blocks
    bg = Surface((32, 32))
    bg.convert()
    bg.fill(Color("#000000"))
    entities = pygame.sprite.Group()
    #defines player start position
    player = Player(32, 32)

    #creates empty variables for use in building the level
    platforms = []
    x = y = 0

    #builds the level by going through the level1 variable from the
    #levels module and checking if the position in the array is a
    #'P' or and 'E' and adds the appropriate block to the "platforms" array.
    for row in levels.level1:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            if col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            x += 32
        y += 32
        x = 0

    totalLevelWidth = len(levels.level1[0])*32
    totalLevelHeight = len(levels.level1)*32
    camera = Camera(complex_camera, totalLevelWidth, totalLevelHeight)
    entities.add(player)

    while 1:
        timer.tick(60)

        #Defines the user controls.
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update(up, down, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+winHalfWidth, -t+winHalfHeight, w, h  # center player

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-winWidth), l)   # stop scrolling at the right edge
    t = max(-(camera.height-winHeight), t)  # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)


#creates base class for entities
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #Defines initial variables for "Player" such as velocity, size, colour
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32, 32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            #only jump if on the ground
            if self.onGround:
                self.yvel -= 10
        if down:
            pass
        #defines speed of player under different conditions
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            #only accelerate player with gravity if in the air
            self.yvel += 0.3
            #terminal velocity
            if self.yvel > 100:
                self.yvel = 100
        if not(left or right):
            self.xvel = 0
        #increment in x direction
        self.rect.left += self.xvel
        #do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        #increment in y direction
        self.rect.top += self.yvel
        #assuming we're in the air
        self.onGround = False
        #do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        #defines outcomes for collisions with different blocks.
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    #quits game if Player collides with the ExitBlock.
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        #Defines initial variables for "Platform" blocks such as size, colour
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        #Uses the variables from a "Platform" block and changes the colour.
        Platform.__init__(self, x, y)
        self.image.fill(Color("#FF0000"))


if __name__ == "__main__":

    # Creating the screen
    screen = pygame.display.set_mode((winWidth, winHeight), 0, 32)

    menu_items = ('Start', 'Quit')
    funcs = {'Start': startScreen,
             'Quit': sys.exit}

    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()
