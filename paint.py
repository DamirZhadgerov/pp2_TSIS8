import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 10
    mode = 'blue'
    points = []

    while True:

        for event in pygame.event.get():

            # Check for quit event
            if event.type == pygame.QUIT:
                return

            # Check for key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = 'red'  # Change brush color to red when 'R' key is pressed
                elif event.key == pygame.K_b:
                    mode = 'blue'  # Change brush color to blue when 'B' key is pressed
                elif event.key == pygame.K_g:
                    mode = 'green'  # Change brush color to green when 'G' key is pressed

            if event.type == pygame.MOUSEMOTION:
                # Add point to list when mouse moves
                position = event.pos
                points.append(position)
                points = points[-256:]  # Keep only the last 256 points

        screen.fill((0, 0, 0))

        # Draw all points
        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1

        pygame.display.flip()

        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


main()
