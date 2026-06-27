from pygame import *
from random import randint

a = 5
b = a + 3

init()
size = 1200, 800
window = display.set_mode(size)
clock = time.Clock()

background = image.load("images/background.png")
background = transform.scale(background, size)

player = image.load("images/player.png")
player = transform.scale(player, (100, 100))

truba = image.load("images/truba.png")

score = 0
lose = False
main_font = font.Font(None, 36)
y_vel = 2

player_rect = Rect(150, size[1] // 2 - 100, 100, 100)


def generate_pipes(count, pipe_width=120, gap=200, min_height=50, max_height=440, distance=650):
    pipes_list = []
    start_x = size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, size[1] - (height + gap))
        pipes_list.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes_list


pipes = generate_pipes(150)

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.blit(background, (0, 0))

    window.blit(player, (player_rect.x, player_rect.y))

    if len(pipes) < 8:
        pipes = generate_pipes(150)

    for pipe in pipes:
        pipe.x -= 10

        if pipe.y == 0:
            pipe_img = transform.scale(truba, (pipe.width, pipe.height))
            window.blit(pipe_img, (pipe.x, pipe.y))
        else:
            pipe_img = transform.scale(truba, (pipe.width, pipe.height))
            pipe_img = transform.flip(pipe_img, False, True)  
            window.blit(pipe_img, (pipe.x, pipe.y))

        if pipe.x <= -100:
            pipes.remove(pipe)
            score += 1

        if player_rect.colliderect(pipe):
            lose = True

    score_text = main_font.render(f"{int(score)}", 1, "white")
    center_text = size[0] // 2 - score_text.get_rect().w // 2
    window.blit(score_text, (center_text, 40))

    clock.tick(60)
    display.update()

    keys = key.get_pressed()
    if keys[K_w] and not lose:
        player_rect.y -= 15
    if keys[K_s] and not lose:
        player_rect.y += 15

    if lose:
        player_rect.y += y_vel
        y_vel *= 1.1
