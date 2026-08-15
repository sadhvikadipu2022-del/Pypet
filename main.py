import pygame
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("PyPet")
# 0 = very low, 100 = full. 100 hunger means starving.
pet_stats = {
    "hunger": 30,
    "happiness": 80,
    "energy": 70
}
is_sleeping = False
pet_message = "Welcome to PyPet!"
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
stats_font = pygame.font.SysFont(None, 28) 
font = pygame.font.SysFont(None, 36)
facing_left = False
running = True
while running:
    if pet_stats["hunger"] >= 80:
        pet_message = "I'm starving!"
    elif pet_stats["happiness"] <= 20:
        pet_message = "I'm bored!"
    elif pet_stats["energy"] <= 20:
        pet_message = "I need a nap!"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if is_sleeping:
                    pet_message = "The pet shouldn't eat while sleeping!"
                else:
                    pet_stats["hunger"] = max(0, pet_stats["hunger"] - 20)
                    pet_stats["happiness"] = min(100, pet_stats["happiness"] + 5)
                    pet_stats["energy"] = min(100, pet_stats["energy"] + 5)
                    pet_message = "Yummy!"
            if event.key == pygame.K_p:
                if is_sleeping:
                    pet_message = "The pet shouldn't play while sleeping!"
                elif pet_stats["energy"] < 20:
                    pet_message = "I'm too tired!"
                else:
                    pet_stats["happiness"] = min(100, pet_stats["happiness"] + 15)
                    pet_stats["energy"] = max(0, pet_stats["energy"] - 20)
                    pet_stats["hunger"] = min(100, pet_stats["hunger"] + 10)
                    pet_message = "Yay! Let's play!"
            if event.key == pygame.K_s:
                is_sleeping = True
                pet_stats["energy"] = 100
                pet_message = "Zzz... Sleeping..."
            if event.key == pygame.K_w:
                is_sleeping = False
                pet_message = "Good morning!"
    if not is_sleeping:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            facing_left = False
            pet_x -= pet_speed
        elif keys[pygame.K_RIGHT]:
            facing_left = True
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
    msg_surface = stats_font.render(pet_message, True, (100, 100, 100))
    msg_x = pet_x + (PET_SIZE // 2) - (msg_surface.get_width() // 2)
    msg_y = pet_y - 65
    screen.fill((117, 216, 200))
    screen.blit(current_pet_image, (pet_x, pet_y))
    screen.blit(name_surface, (text_x, text_y))
    screen.blit(msg_surface, (msg_x, msg_y))
    stats_string = f"Hunger: {pet_stats['hunger']} | Happiness: {pet_stats['happiness']} | Energy: {pet_stats['energy']}"
    stats_surface = stats_font.render(stats_string, True, (255, 255, 255))
    screen.blit(stats_surface, (15, 15))
    pygame.display.flip()
pygame.quit()
