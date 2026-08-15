import pygame
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("PyPet")
pet_image = pygame.image.load("pet.png")
pet_image = pygame.transform.scale(pet_image, (250, 250))
pet_x = 400
pet_y = 250
pet_speed = 2
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
PET_SIZE = 250
pet_name = "Alfie"
font = pygame.font.SysFont(None, 36)
facing_left = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        facing_left = False
    elif keys[pygame.K_RIGHT]:
        facing_left = True
    if keys[pygame.K_LEFT]:
        pet_x -= pet_speed
    if keys[pygame.K_RIGHT]:
        pet_x += pet_speed
    if keys[pygame.K_UP]:
        pet_y -= pet_speed
    if keys[pygame.K_DOWN]:
        pet_y += pet_speed
    pet_x = max(0, min(SCREEN_WIDTH - PET_SIZE, pet_x))
    pet_y = max(0, min(SCREEN_HEIGHT - PET_SIZE, pet_y))
    current_pet_image = pygame.transform.flip(pet_image, facing_left, False)
    name_surface = font.render(pet_name, True, (128, 128, 128))
    text_x = pet_x + (PET_SIZE // 2) - (name_surface.get_width() // 2)
    text_y = pet_y - 12
    screen.fill((117, 216, 200))
    screen.blit(current_pet_image, (pet_x, pet_y))
    screen.blit(name_surface, (text_x, text_y))
    pygame.display.flip()
pygame.quit()
