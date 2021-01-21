import pygame, sys, os, random, noise # import pygame and sys

#game Files
clock = pygame.time.Clock() # set up the clock

from pygame.locals import *

pygame.init() # initiates pygame

# Handles Sound for the game
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(64)

# Sets the Caption of the window
pygame.display.set_caption('Icurus World') # set the window name

# Window Size
WINDOW_SIZE = (800,600)

# initiate screen
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)

# Used as the surface for rendering, which is scaled
display = pygame.Surface((400,300))

import constants

#Sets the Chunk size of the world default is set to 8
CHUNK_SIZE = 20
CHUNK_WIDTH = 20
CHUNK_HEIGHT = 20

#Font for the text in game. Set to something different later on
font = pygame.font.SysFont(None, 20)

#Sets the rendering for the text to be displayed
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


#Main Menu
def main_menu():
    while True:
        screen.fill((0,0,0))
        draw_text('Icurus World', font, (255, 255, 255), screen, 20, 20)
        mx, my = pygame.mouse.get_pos()

        button_1 = screen.blit(constants.BUTTON_START, (50,100))
        button_2 = screen.blit(constants.BUTTON_OPTIONS, (50, 200))
        #button_2 = pygame.Rect(50, 200, 200, 30)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        #pygame.draw.rect(screen, (255, 0, 0), button_1)
        #draw_text('Start Game', font, (255, 255, 255), screen, (50+(100/2)), (100+(50/2)))
        #pygame.draw.rect(screen, (255, 0, 0), button_2)
        #draw_text('Options', font, (255, 255, 255), screen, (50+(100/2)), (200+(50/2)))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        clock.tick(60)

#Generates the Chunks in the world. I need to find a better method for this other than noise.
def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(CHUNK_SIZE):
        chunk_data.append([])
        for x_pos in range(CHUNK_SIZE):
            target_x = x * CHUNK_SIZE + x_pos
            target_y = y * CHUNK_SIZE + y_pos
            tile_type = 0 # nothing

            height = int(noise.pnoise1(target_x * 0.1, repeat=9999999) * 5)

            if target_y > 8 - height:
                tile_type = 2 # dirt

            elif target_y == 8 - height :
                tile_type = 1 # grass

            elif target_y == 8 - height - 1:
                if random.randint(1,5) == 1:
                   tile_type = 3 # plant

            if target_y == 3 - height - 1:
                if random.randint(1,10) == 1:
                   tile_type = 11 # tree

            chunk_data[y_pos].append([[target_x,target_y],tile_type, [x_pos,y_pos]])

    chunk_data = load_map(chunk_data)

    return chunk_data

#This checks the tile next to dirt, if it is air than it will add the proper corner blocks.
def load_map(chunk_data):
    for y in range(CHUNK_SIZE):
        for x in range(CHUNK_SIZE):
            if chunk_data[y][x][1] == 1 and x + 1 < CHUNK_SIZE:
                if chunk_data[y][x + 1][1] == 0 and x > 1:
                    chunk_data[y][x][1] = 5
                elif chunk_data[y][x - 1][1] == 0 and x > 1:
                    chunk_data[y][x][1] = 4
    return chunk_data

#Animation
global animation_frames
animation_frames = {}

#sets up the animation of the player.
def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame


animation_database = {}

animation_database['run'] = load_animation('images/PlayerSprite/run',[7,7])
animation_database['idle'] = load_animation('images/PlayerSprite/idle',[7,7,40])

game_map = {}

#Load Tile Set. default tile set for now. biomesbiomes will be added later
tleft = pygame.image.load('images/TileMap/DirtGrass/t-left.png').convert_alpha()       # Top Left Tile Map
grass = pygame.image.load('images/TileMap/DirtGrass/t-center.png').convert_alpha()     # Top Center Tile Map
tright = pygame.image.load('images/TileMap/DirtGrass/t-right.png').convert_alpha()     # Top Right Tile Map
cleft = pygame.image.load('images/TileMap/DirtGrass/c-left.png').convert_alpha()       # Center Left Tile Map
cright = pygame.image.load('images/TileMap/DirtGrass/c-right.png').convert_alpha()     # Center Right Tile Map
dirt = pygame.image.load('images/TileMap/DirtGrass/center.png').convert_alpha()        # Center This is the main Dirt Tile as of now
bleft = pygame.image.load('images/TileMap/DirtGrass/b-left.png').convert_alpha()       # Bottom Left Tile Map
bcenter = pygame.image.load('images/TileMap/DirtGrass/b-center.png').convert_alpha()   # Bottom Center Tile Map
bright = pygame.image.load('images/TileMap/DirtGrass/b-right.png').convert_alpha()     # Bottom Right Tile Map
plant = pygame.image.load('images/WorldObjects/plant.png').convert_alpha()             # Plant Image
plant.set_colorkey((255,255,255))
tree = pygame.image.load('images/WorldObjects/tree.png').convert_alpha()               # Tree Image


tile_index = {
              1:grass,      #Main Block for Grass
              2:dirt,       #Main Block for Dirt
              3:plant,      #Horrible Grass Tile, Will remake it
              4:tleft,      #Top left
              5:tright,     #Top Right
              6:cleft,      #Center left
              7:cright,     #Center Right
              8:bleft,      #Bottom left
              9:bcenter,    #Bottom Center
              10:bright,    #Bottom Right
              11:tree       #Tree Image
              }

#handles the sound for the world.
#jump_sound = pygame.mixer.Sound('Sounds/WorldObjects/jump.wav')
grass_sounds = [pygame.mixer.Sound('Sounds/WorldObjects/grass_0.wav'), pygame.mixer.Sound('Sounds/WorldObjects/grass_1.wav')]
grass_sounds[0].set_volume(1.0)
grass_sounds[1].set_volume(1.0)

pygame.mixer.music.load('Sounds/WorldObjects/grass_0.wav')
pygame.mixer.music.play(-1)

# Parallax background
background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.1,[300,80,120,400]]]

#handles collision
def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#handles player move and collosion
def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


#Main game
def game():
    running = True
    moving_right = False
    moving_left = False
    vertical_momentum = 0
    air_timer = 0

    grass_sound_timer = 0

    player_rect = pygame.Rect(100,100,18,27)
    player_flip = False
    player_action = 'idle'
    player_frame = 0

    tile_rects = []
    true_scroll = [0,0]

    if grass_sound_timer > 0:
        grass_sound_timer -= 1

    while running:
        display.fill((146,244,255))

        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display,(20,170,150),obj_rect)
            else:
                pygame.draw.rect(display,(15,76,73),obj_rect)

        for y in range(3):
            for x in range(4):
                target_x = x - 1 + int(round(scroll[0]/(CHUNK_SIZE*16)))
                target_y = y - 1 + int(round(scroll[1]/(CHUNK_SIZE*16)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x,target_y)
                for row in game_map[target_chunk]:
                    for tile in row:
                        if tile[1] != 0:
                            display.blit(tile_index[tile[1]],(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                        if tile[1] in [1,2,4,5,6,7,8,9,10]: #add collosion tiles here
                            tile_rects.append(pygame.Rect(tile[0][0]*16,tile[0][1]*16,16,16))

        player_movement = [0,0]
        if moving_right == True:
            player_movement[0] += 2
        if moving_left == True:
            player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        if player_movement[0] == 0:
            player_action,player_frame = change_action(player_action,player_frame,'idle')
        if player_movement[0] > 0:
            player_flip = False
            player_action,player_frame = change_action(player_action,player_frame,'run')
        if player_movement[0] < 0:
            player_flip = True
            player_action,player_frame = change_action(player_action,player_frame,'run')

        player_rect, collisions = move(player_rect, player_movement, tile_rects)

        if collisions['bottom']:
            vertical_momentum = 0
            air_timer = 0
            if player_movement[0] != 0:
                if grass_sound_timer == 0:
                    grass_sound_timer = 30
                    random.choice(grass_sounds).play()
            else:
                air_timer += 1

        player_frame += 1
        if player_frame >= len(animation_database[player_action]):
            player_frame = 0
        player_img_id = animation_database[player_action][player_frame]
        player_img = animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_img,player_flip,False),(player_rect.x-scroll[0],player_rect.y-scroll[1]))
        for event in pygame.event.get():  # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_d:
                    moving_right = True
                if event.key == K_a:
                    moving_left = True
                if event.key == K_SPACE:
                    if air_timer < 6:
                        vertical_momentum = -5
            if event.type == KEYUP:
                if event.key == K_d:
                    moving_right = False
                if event.key == K_a:
                    moving_left = False
        tile_rects = []


        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
main_menu()
game()
