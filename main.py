import pygame
import random
pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("PyPet")
# 0 = very low, 100 = full. 100 hunger means starving.
import json
import os

DEFAULT_GAME_DATA = {
    "pet_name": "PyPet",
    "coins": 100,
    "inventory": [],
    "stats": {
        "Hunger": 70,
        "Happiness": 50,
        "Energy": 70,
        "food_eaten": 0,
        "times_slept": 0,
        "minigames_won": 0
    }
}
def load_game():
    if os.path.exists("save_file.json"):
        try:
            with open("save_file.json", "r") as f:
                print("Save file loaded successfully!")
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Save file broken or empty! Starting a new game...")
            return DEFAULT_GAME_DATA.copy()
    else:
        print("No save file found. Starting a new game...")
        return DEFAULT_GAME_DATA.copy()

def save_game(data):
    try:
        with open("save_file.json", "w") as f:
            json.dump(data, f, indent=4)
            print("Game auto-saved successfully!")
    except IOError:
        print("Failed to save game data.")
game_data = load_game()
SHOP_ITEMS = {
    "Fish Snack": {"price": 20, "effect": "Hunger +15"},
    "Hat": {"price": 50, "effect": "Happiness +20 (Unique)"},
    "Fancy Bed": {"price": 100, "effect": "Energy +30 (Unique)"}
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
show_shop = False
shop_button_rect = pygame.Rect(790, 15, 90, 45)
running = True
while running:
    current_time = pygame.time.get_ticks()
    if game_data["stats"]["Hunger"] >= 80:
        pet_message = "I'm starving!"
    elif game_data["stats"]["Happiness"] <= 20:
        pet_message = "I'm bored!"
    elif game_data["stats"]["Energy"] <= 20:
        pet_message = "I need a nap!"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game(game_data)
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if is_sleeping:
                    pet_message = "The pet shouldn't eat while sleeping!"
                else:
                    game_data["stats"]["Hunger"] = max(0, game_data["stats"]["Hunger"] - 20)
                    game_data["stats"]["Happiness"] = min(100, game_data["stats"]["Happiness"] + 5)
                    game_data["stats"]["Energy"] = min(100, game_data["stats"]["Energy"] + 5)
                    pet_message = "Yummy!"
                    pet_state = "eating"
                    target_x = bowl_x - 75
            if event.key == pygame.K_p:
                if is_sleeping:
                    pet_message = "The pet shouldn't play while sleeping!"
                elif game_data["stats"]["Energy"] < 20:
                    pet_message = "I'm too tired!"
                else:
                    game_data["stats"]["Happiness"] = min(100, game_data["stats"]["Happiness"] + 15)
                    game_data["stats"]["Energy"] = max(0, game_data["stats"]["Energy"] - 20)
                    game_data["stats"]["Hunger"] = min(100, game_data["stats"]["Hunger"] + 10)
                    pet_message = "Yay! Let's play!"
                    pet_state = "playing"
                    target_x = ball_x - 90
            if event.key == pygame.K_s:
                is_sleeping = True
                game_data["stats"]["Energy"] = 100
                pet_message = "Zzz... Sleeping..."
                pet_state = "sleeping"
                target_x = bed_x - 50
            if event.key == pygame.K_w:
                is_sleeping = False
                pet_state = "idle"
                pet_message = "Good morning!"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if shop_button_rect.collidepoint(mouse_x, mouse_y):
                show_shop = not show_shop
                continue
            ball_rect = pygame.Rect(ball_x, ball_y, 60, 60)
            if ball_rect.collidepoint(mouse_x, mouse_y) and not is_sleeping:
                game_data["stats"]["Happiness"] = min(100, game_data["stats"]["Happiness"] + 10)
                game_data["coins"] += 5
                pet_message = "Caught the ball! +5 Coins"
                ball_x = random.randint(100, 750)
                ball_y = random.randint(100, 450)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                show_shop = not show_shop
            if show_shop:
                chosen_item = None
                if event.key == pygame.K_1:
                    chosen_item = "Fish Snack"
                elif event.key == pygame.K_2:
                    chosen_item = "Hat"
                elif event.key == pygame.K_3:
                    chosen_item = "Fancy Bed"

                if chosen_item:
                    item_details = SHOP_ITEMS[chosen_item]
                    price = item_details["price"]
                    if chosen_item in ["Hat", "Fancy Bed"] and chosen_item in game_data["inventory"]:
                        pet_message = f"You already own the {chosen_item}!"
                    elif game_data["coins"] >= price:
                        game_data["coins"] -= price
                        game_data["inventory"].append(chosen_item)
                        pet_message = f"Bought {chosen_item}! {item_details['effect']}"

                        if chosen_item == "Fish Snack":
                            game_data["stats"]["Hunger"] = min(100, game_data["stats"]["Hunger"] + 15)
                    else:
                        pet_message = "Not enough coins!"
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
        game_data["stats"]["Hunger"] = min(100, game_data["stats"]["Hunger"] + 2)
        game_data["stats"]["Happiness"] = max(0, game_data["stats"]["Happiness"] - 1)
        if not is_sleeping:
            game_data["stats"]["Energy"] = max(0, game_data["stats"]["Energy"] - 1)
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
    stats_string = f"Hunger: {game_data['stats']['Hunger']} | Happiness: {game_data['stats']['Happiness']} | Energy: {game_data['stats']['Energy']}"
    stats_surface = stats_font.render(stats_string, True, (255, 255, 255))
    screen.blit(stats_surface, (15, 15))
    stats_string = f"Hunger: {game_data['stats']['Hunger']} | Happiness: {game_data['stats']['Happiness']} | Energy: {game_data['stats']['Energy']} | Coins: {game_data['coins']}"
    stats_surface = stats_font.render(stats_string, True, (255, 255, 255))
    screen.blit(stats_surface, (15, 15))
    coins_string = f"Coins: {game_data['coins']}"
    coins_surface = stats_font.render(coins_string, True, (255, 215, 0)) # Gold Color
    screen.blit(coins_surface, (10, 70))
    total_interactions = (game_data["stats"]["food_eaten"] + 
                      game_data["stats"]["times_slept"] + 
                      game_data["stats"]["minigames_won"])
    activities = {
    "Eating": game_data["stats"]["food_eaten"],
    "Sleeping": game_data["stats"]["times_slept"],
    "Playing": game_data["stats"]["minigames_won"]
    }
    fav_activity = max(activities, key=activities.get) if total_interactions > 0 else "None yet"
    stats_summary = f"Total Actions: {total_interactions} | Fav: {fav_activity}"
    summary_surface = stats_font.render(stats_summary, True, (128, 128, 128)) # Grey Color
    screen.blit(summary_surface, (10, 100))
    inv_string = f"Inventory: {', '.join(game_data['inventory']) if game_data['inventory'] else 'Empty'}"
    inv_surface = stats_font.render(inv_string, True, (255, 255, 255))
    screen.blit(inv_surface, (10, 130))
    pygame.draw.rect(screen, (42, 83, 92), shop_button_rect, border_radius=6)
    shop_label = stats_font.render("SHOP (B)", True, (255, 255, 255))
    shop_label_x = shop_button_rect.centerx - shop_label.get_width() // 2
    shop_label_y = shop_button_rect.centery - shop_label.get_height() // 2
    screen.blit(shop_label, (shop_label_x, shop_label_y))
    if show_shop:
        shop_panel_rect = pygame.Rect(560, 80, 320, 230)
        pygame.draw.rect(screen, (245, 245, 235), shop_panel_rect, border_radius=8)
        pygame.draw.rect(screen, (42, 83, 92), shop_panel_rect, 3, border_radius=8)
        shop_title = font.render("Pet Shop", True, (42, 83, 92))
        screen.blit(shop_title, (580, 95))
        shop_lines = [
            "1: Fish Snack - 20 coins",
            "2: Hat - 50 coins",
            "3: Fancy Bed - 100 coins",
            "Click SHOP (B) or press B to close"
        ]
        for line_index, line in enumerate(shop_lines):
            line_surface = stats_font.render(line, True, (70, 70, 70))
            screen.blit(line_surface, (580, 145 + line_index * 35))
    pygame.display.flip()
pygame.quit()
