import pygame
import random
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
pet_state = "idle"
personality = "playful"
coins = 0
sleeping_img = pygame.transform.scale(pygame.image.load("sleeping.png"), (250, 250))
eating_img = pygame.transform.scale(pygame.image.load("eating.png"), (250, 250))
playing_img = pygame.transform.scale(pygame.image.load("playing.png"), (250, 250))
walk_frames = [
    pygame.transform.scale(pygame.image.load("Frame1.png"), (250, 250)),
    pygame.transform.scale(pygame.image.load("Frame2.png"), (250, 250)),
    pygame.transform.scale(pygame.image.load("Frame3.png"), (250, 250))
]
walk_frame_index = 0
last_frame_update = pygame.time.get_ticks()
frame_delay = 150
bed_img = pygame.transform.scale(pygame.image.load("bed.png"), (150, 150))
bowl_img = pygame.transform.scale(pygame.image.load("bowl.png"), (100, 100))
ball_img = pygame.transform.scale(pygame.image.load("ball.png"), (60, 60))
bed_x, bed_y = 50, 400
bowl_x, bowl_y = 720, 430
ball_x, ball_y = random.randint(100, 750), random.randint(100, 450)
last_stat_decay = pygame.time.get_ticks()
last_action_change = pygame.time.get_ticks()
random_messages = ["Meow!", "I'm bored!", "Can we play?", "Where's my food?"]
target_x = pet_x
running = True
while running:
    current_time = pygame.time.get_ticks()
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
                    pet_state = "eating"
                    target_x = bowl_x - 75
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
                    pet_state = "playing"
                    target_x = ball_x - 90
            if event.key == pygame.K_s:
                is_sleeping = True
                pet_stats["energy"] = 100
                pet_message = "Zzz... Sleeping..."
                pet_state = "sleeping"
                target_x = bed_x - 50
            if event.key == pygame.K_w:
                is_sleeping = False
                pet_state = "idle"
                pet_message = "Good morning!"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            ball_rect = pygame.Rect(ball_x, ball_y, 60, 60)
            if ball_rect.collidepoint(mouse_x, mouse_y) and not is_sleeping:
                pet_stats["happiness"] = min(100, pet_stats["happiness"] + 10)
                coins += 5
                pet_message = "Caught the ball! +5 Coins"
                ball_x = random.randint(100, 750)
                ball_y = random.randint(100, 450)
                pet_state = "playing"
    if not is_sleeping:
        keys = pygame.key.get_pressed()
        is_moving_manual = False
        if keys[pygame.K_LEFT]:
            facing_left = False
            pet_x -= pet_speed
        elif keys[pygame.K_RIGHT]:
            facing_left = True
            pet_x += pet_speed
            is_moving_manual = True
        if keys[pygame.K_UP]:
            pet_y -= pet_speed
            is_moving_manual = True
        if keys[pygame.K_DOWN]:
            pet_y += pet_speed
            is_moving_manual = True
        if is_moving_manual:
            pet_state = "walking"
            target_x = pet_x
        elif pet_state == "walking" and abs(pet_x - target_x) < 5:
            pet_state = "idle"
    if current_time - last_stat_decay > 3000:
        pet_stats["hunger"] = min(100, pet_stats["hunger"] + 2)
        pet_stats["happiness"] = max(0, pet_stats["happiness"] - 1)
        if not is_sleeping:
            pet_stats["energy"] = max(0, pet_stats["energy"] - 1)
        last_stat_decay = current_time
    if current_time - last_action_change > 5000 and not is_sleeping:
        last_action_change = current_time
        choice_pool = ["idle", "walk", "message"]
        if personality == "playful":
            chosen_action = random.choice(choice_pool)
            choice_pool.extend(["walk", "message"])
            chosen_action = random.choice(choice_pool)
        if chosen_action == "walk":
            target_x = random.randint(50, SCREEN_WIDTH - PET_SIZE)
            pet_state = "walking"
        elif chosen_action == "message":
            pet_message = random.choice(random_messages)
    if pet_state == "walking" and pet_x != target_x:
        if pet_x < target_x:
            pet_x += pet_speed
            facing_left = True
        elif pet_x > target_x:
            pet_x -= pet_speed
            facing_left = False
        if abs(pet_x - target_x) <= pet_speed:
            pet_x = target_x
            if is_catching_ball:
                pet_stats["happiness"] = min(100, pet_stats["happiness"] + 10)
                coins += 5
                pet_message = "Caught the ball! +5 Coins"
                ball_x = random.randint(100, 750)
                ball_y = random.randint(100, 450)
                pet_state = "playing"
                is_catching_ball = False
            else:
                pet_state = "idle"
    pet_x = max(0, min(SCREEN_WIDTH - PET_SIZE, pet_x))
    pet_y = max(0, min(SCREEN_HEIGHT - PET_SIZE, pet_y))
    if pet_state == "sleeping":
        active_sprite = sleeping_img
    elif pet_state == "eating":
        active_sprite = eating_img
    elif pet_state == "playing":
        active_sprite = playing_img
    elif pet_state == "walking":
        if current_time - last_frame_update > frame_delay:
            walk_frame_index = (walk_frame_index + 1) % len(walk_frames)
            last_frame_update = current_time
        active_sprite = walk_frames[walk_frame_index]
    else:
        active_sprite = pet_image
    current_pet_image = pygame.transform.flip(active_sprite, facing_left, False)
    name_surface = font.render(pet_name, True, (128, 128, 128))
    text_x = pet_x + (PET_SIZE // 2) - (name_surface.get_width() // 2)
    text_y = pet_y - 12
    msg_surface = stats_font.render(pet_message, True, (100, 100, 100))
    msg_x = pet_x + (PET_SIZE // 2) - (msg_surface.get_width() // 2)
    msg_y = pet_y - 65
    screen.fill((117, 216, 200))
    screen.blit(bed_img, (bed_x, bed_y))
    screen.blit(bowl_img, (bowl_x, bowl_y))
    screen.blit(ball_img, (ball_x, ball_y))
    screen.blit(current_pet_image, (pet_x, pet_y))
    screen.blit(name_surface, (text_x, text_y))
    screen.blit(msg_surface, (msg_x, msg_y))
    stats_string = f"Hunger: {pet_stats['hunger']} | Happiness: {pet_stats['happiness']} | Energy: {pet_stats['energy']}"
    stats_surface = stats_font.render(stats_string, True, (255, 255, 255))
    screen.blit(stats_surface, (15, 15))
    stats_string = f"Hunger: {pet_stats['hunger']} | Happiness: {pet_stats['happiness']} | Energy: {pet_stats['energy']} | Coins: {coins}"
    stats_surface = stats_font.render(stats_string, True, (255, 255, 255))
    screen.blit(stats_surface, (15, 15))
    pygame.display.flip()
pygame.quit()