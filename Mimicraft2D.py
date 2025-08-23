import sys
import math
import random
import pygame
import asyncio

# Add these imports at the top of the file
import json
import os

# Add these constants after the existing ones
DEFAULT_SETTINGS = {
    "keybinds": {
        "move_left": pygame.K_a,
        "move_right": pygame.K_d,
        "jump": pygame.K_SPACE,
        "inventory": pygame.K_e,
        "sprint": pygame.K_LSHIFT
    },
    "max_fps": 60,
    "render_distance": 8,
    "music_volume": 50,
    "sound_volume": 70,
    "last_seed": None
}

# Add this function to handle settings
def load_settings():
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                return json.load(f)
    except:
        pass
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
    except:
        pass

# Add menu rendering functions
def draw_main_menu(screen, fonts, selected_option):
    screen.fill((40, 40, 80))
    
    # Title
    title = fonts['big'].render("MIMICRAFT2D", True, (255, 255, 255))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))
    
    # Menu options
    options = ["Play Game", "Settings", "Quit"]
    for i, option in enumerate(options):
        color = (255, 255, 0) if i == selected_option else (200, 200, 200)
        text = fonts['big'].render(option, True, color)
        screen.blit(text, (SCREEN_W // 2 - text.get_width() // 2, 250 + i * 60))
    
    # Footer
    footer = fonts['small'].render("Use Arrow Keys to navigate, Enter to select", True, (150, 150, 150))
    screen.blit(footer, (SCREEN_W // 2 - footer.get_width() // 2, SCREEN_H - 50))

def draw_settings_menu(screen, fonts, settings, selected_option, editing_keybind=None):
    screen.fill((40, 40, 80))
    
    # Title
    title = fonts['big'].render("SETTINGS", True, (255, 255, 255))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))
    
    # Settings options
    options = [
        f"Move Left: {pygame.key.name(settings['keybinds']['move_left'])}",
        f"Move Right: {pygame.key.name(settings['keybinds']['move_right'])}",
        f"Jump: {pygame.key.name(settings['keybinds']['jump'])}",
        f"Inventory: {pygame.key.name(settings['keybinds']['inventory'])}",
        f"Sprint: {pygame.key.name(settings['keybinds']['sprint'])}",
        f"Max FPS: {settings['max_fps']}",
        f"Render Distance: {settings['render_distance']}",
        f"Music Volume: {settings['music_volume']}%",
        f"Sound Volume: {settings['sound_volume']}%",
        "Back to Main Menu"
    ]
    
    for i, option in enumerate(options):
        color = (255, 255, 0) if i == selected_option else (200, 200, 200)
        if editing_keybind == i:
            color = (255, 100, 100)
            option += " (Press a key...)"
        
        text = fonts['medium'].render(option, True, color)
        screen.blit(text, (SCREEN_W // 2 - text.get_width() // 2, 120 + i * 40))
    
    # Instructions
    instructions = fonts['small'].render("Use Arrow Keys to navigate, Enter to change, Escape to go back", True, (150, 150, 150))
    screen.blit(instructions, (SCREEN_W // 2 - instructions.get_width() // 2, SCREEN_H - 50))

def draw_world_gen_menu(screen, fonts, seed_input, selected_option):
    screen.fill((40, 40, 80))
    
    # Title
    title = fonts['big'].render("WORLD GENERATION", True, (255, 255, 255))
    screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 50))
    
    # Options
    options = [
        "Use Random Seed",
        f"Custom Seed: {seed_input}",
        "Generate World",
        "Back to Main Menu"
    ]
    
    for i, option in enumerate(options):
        color = (255, 255, 0) if i == selected_option else (200, 200, 200)
        text = fonts['medium'].render(option, True, color)
        screen.blit(text, (SCREEN_W // 2 - text.get_width() // 2, 120 + i * 50))
    
    # Instructions
    instructions = fonts['small'].render("Use Arrow Keys to navigate, Enter to select, Type to enter seed", True, (150, 150, 150))
    screen.blit(instructions, (SCREEN_W // 2 - instructions.get_width() // 2, SCREEN_H - 50))

# Add menu navigation functions
def run_main_menu(screen, fonts, settings):
    selected_option = 0
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Play Game
                        return "world_gen", None
                    elif selected_option == 1:  # Settings
                        return "settings", None
                    elif selected_option == 2:  # Quit
                        return "quit", None
        
        draw_main_menu(screen, fonts, selected_option)
        pygame.display.flip()
        pygame.time.delay(100)
    
    return "quit", None

def run_settings_menu(screen, fonts, settings):
    selected_option = 0
    editing_keybind = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", settings
            elif event.type == pygame.KEYDOWN:
                if editing_keybind is not None:
                    # Capture the key for keybind
                    keybind_names = ["move_left", "move_right", "jump", "inventory", "sprint"]
                    settings["keybinds"][keybind_names[editing_keybind]] = event.key
                    editing_keybind = None
                else:
                    if event.key == pygame.K_ESCAPE:
                        return "main_menu", settings
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 10
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 10
                    elif event.key == pygame.K_RETURN:
                        if selected_option < 5:  # Keybinds
                            editing_keybind = selected_option
                        elif selected_option == 5:  # Max FPS
                            settings["max_fps"] = min(240, max(30, settings["max_fps"] + 10))
                        elif selected_option == 6:  # Render Distance
                            settings["render_distance"] = min(16, max(4, settings["render_distance"] + 2))
                        elif selected_option == 7:  # Music Volume
                            settings["music_volume"] = min(100, max(0, settings["music_volume"] + 10))
                        elif selected_option == 8:  # Sound Volume
                            settings["sound_volume"] = min(100, max(0, settings["sound_volume"] + 10))
                        elif selected_option == 9:  # Back to Main Menu
                            return "main_menu", settings
                    elif event.key == pygame.K_LEFT:
                        if selected_option == 5:  # Max FPS
                            settings["max_fps"] = min(240, max(30, settings["max_fps"] - 10))
                        elif selected_option == 6:  # Render Distance
                            settings["render_distance"] = min(16, max(4, settings["render_distance"] - 2))
                        elif selected_option == 7:  # Music Volume
                            settings["music_volume"] = min(100, max(0, settings["music_volume"] - 10))
                        elif selected_option == 8:  # Sound Volume
                            settings["sound_volume"] = min(100, max(0, settings["sound_volume"] - 10))
                    elif event.key == pygame.K_RIGHT:
                        if selected_option == 5:  # Max FPS
                            settings["max_fps"] = min(240, max(30, settings["max_fps"] + 10))
                        elif selected_option == 6:  # Render Distance
                            settings["render_distance"] = min(16, max(4, settings["render_distance"] + 2))
                        elif selected_option == 7:  # Music Volume
                            settings["music_volume"] = min(100, max(0, settings["music_volume"] + 10))
                        elif selected_option == 8:  # Sound Volume
                            settings["sound_volume"] = min(100, max(0, settings["sound_volume"] + 10))
        
        draw_settings_menu(screen, fonts, settings, selected_option, editing_keybind)
        pygame.display.flip()
        pygame.time.delay(100)
    
    return "quit", settings

def run_world_gen_menu(screen, fonts, settings):
    selected_option = 0
    seed_input = ""
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "main_menu", None
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % 4
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 4
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Random Seed
                        settings["last_seed"] = None
                        return "play", None
                    elif selected_option == 1:  # Custom Seed
                        # Already editing seed
                        pass
                    elif selected_option == 2:  # Generate World
                        if seed_input:
                            try:
                                settings["last_seed"] = int(seed_input)
                            except:
                                settings["last_seed"] = hash(seed_input) % (2**32)
                        else:
                            settings["last_seed"] = None
                        return "play", settings["last_seed"]
                    elif selected_option == 3:  # Back to Main Menu
                        return "main_menu", None
                elif selected_option == 1:  # Editing seed
                    if event.key == pygame.K_BACKSPACE:
                        seed_input = seed_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        # Already handled above
                        pass
                    else:
                        # Only allow alphanumeric characters
                        if event.unicode.isalnum() or event.unicode in ['-', '_']:
                            seed_input += event.unicode
        
        draw_world_gen_menu(screen, fonts, seed_input, selected_option)
        pygame.display.flip()
        pygame.time.delay(100)
    
    return "quit", None

# Import all block constants from your config files
from Blockbehconfig import (
    AIR, GRASS, DIRT, STONE, WOOD, LEAVES, SAND, PLANKS, COBBLE, GLASS,
    WATER, LAVA, BEDROCK, IRON_ORE, COAL_ORE, GOLD_ORE, DIAMOND_ORE,
    REDSTONE_ORE, OBSIDIAN, GRAVEL, BRICKS, MOSSY_COBBLE, SPONGE, BOOKSHELF,
    BLOCKS, is_solid, get_drop, get_break_time, PLACEABLE_IDS
)

from Blocktexconfig import TILE_SIZE, generate_textures

# ------------------------------
# Game settings (reduced for web)
# ------------------------------
SCREEN_W, SCREEN_H = 800, 450  # Smaller for web
FPS = 60
GRAVITY = 2200  # pixels/s^2
MOVE_SPEED = 250  # pixels/s
JUMP_VEL = -700  # pixels/s
REACH_TILES = 5
WORLD_W, WORLD_H = 200, 100  # Smaller world for web

# ------------------------------
# Helper functions
# ------------------------------
def in_bounds(wx, wy):
    return 0 <= wx < WORLD_W and 0 <= wy < WORLD_H

def get_tile(world, wx, wy):
    if in_bounds(wx, wy):
        return world[wx][wy]
    return AIR

def set_tile(world, wx, wy, block_id):
    if in_bounds(wx, wy):
        world[wx][wy] = block_id

def rect_collides_solid(world, rect):
    # Check tiles overlapped by rect
    x0 = max(int(rect.left // TILE_SIZE) - 1, 0)
    x1 = min(int(rect.right // TILE_SIZE) + 1, WORLD_W - 1)
    y0 = max(int(rect.top // TILE_SIZE) - 1, 0)
    y1 = min(int(rect.bottom // TILE_SIZE) + 1, WORLD_H - 1)
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            bid = get_tile(world, tx, ty)
            if is_solid(bid):
                tile_rect = pygame.Rect(tx * TILE_SIZE, ty * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if rect.colliderect(tile_rect):
                    return True
    return False

def move_and_collide(world, player, dt):
    # Horizontal movement
    dx = player.vx * dt
    new_x = player.x + dx
    new_rect = pygame.Rect(new_x, player.y, player.w, player.h)
    
    if not rect_collides_solid(world, new_rect):
        player.x = new_x
    else:
        # Collision resolution - move until contact
        if dx > 0:  # Moving right
            while not rect_collides_solid(world, pygame.Rect(player.x + 1, player.y, player.w, player.h)):
                player.x += 1
        elif dx < 0:  # Moving left
            while not rect_collides_solid(world, pygame.Rect(player.x - 1, player.y, player.w, player.h)):
                player.x -= 1
        player.vx = 0

    # Vertical movement
    player.vy += GRAVITY * dt
    dy = player.vy * dt
    new_y = player.y + dy
    new_rect = pygame.Rect(player.x, new_y, player.w, player.h)
    
    if not rect_collides_solid(world, new_rect):
        player.y = new_y
        player.on_ground = False
    else:
        # Collision resolution - move until contact
        if dy > 0:  # Falling down
            while not rect_collides_solid(world, pygame.Rect(player.x, player.y + 1, player.w, player.h)):
                player.y += 1
            player.on_ground = True
            player.vy = 0
        elif dy < 0:  # Jumping up
            while not rect_collides_solid(world, pygame.Rect(player.x, player.y - 1, player.w, player.h)):
                player.y -= 1
            player.vy = 0

def screen_to_world(cam_x, cam_y, mx, my):
    wx = int((mx + cam_x) // TILE_SIZE)
    wy = int((my + cam_y) // TILE_SIZE)
    return wx, wy

def tile_center(wx, wy):
    return wx * TILE_SIZE + TILE_SIZE / 2, wy * TILE_SIZE + TILE_SIZE / 2

def dist_tiles(ax, ay, bx, by):
    return math.hypot(ax - bx, ay - by)

def can_place(world, wx, wy, player_rect):
    if not in_bounds(wx, wy) or get_tile(world, wx, wy) != AIR:
        return False
    # Prevent placing inside player
    tile_rect = pygame.Rect(wx * TILE_SIZE, wy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    if tile_rect.colliderect(player_rect):
        return False
    # Require adjacency to at least one solid block (to avoid floating placement)
    neighbors = [(1,0), (-1,0), (0,1), (0,-1)]
    return any(in_bounds(wx+dx, wy+dy) and is_solid(get_tile(world, wx+dx, wy+dy)) for dx, dy in neighbors)

# ------------------------------
# Player class
# ------------------------------
class Player:
    def __init__(self, x, y):
        self.w = TILE_SIZE * 0.8
        self.h = TILE_SIZE * 1.8  # Slightly taller for more realistic proportions
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.direction = 1  # 1 for right, -1 for left

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h))

# ------------------------------
# World generation (simplified for web)
# ------------------------------
def make_world(width, height, seed=None):
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
    
    world = [[AIR for _ in range(height)] for _ in range(width)]
    rng = random.Random(seed)
    
    # Store the seed in the world for reference
    world_seed = seed
    
    # Generate terrain height using Perlin noise
    base = height // 2 + 10
    height_map = [base] * width
    
    # Simple terrain generation with multiple layers
    for x in range(width):
        # Base terrain height with noise
        height_map[x] = base + int(8 * math.sin(x / 20.0)) + rng.randint(-3, 3)
        
        # Generate bedrock at the bottom
        for y in range(height - 5, height):
            world[x][y] = BEDROCK
            
        # Generate stone layer
        stone_depth = rng.randint(5, 10)
        for y in range(height_map[x] + stone_depth, height - 5):
            world[x][y] = STONE
            
            # Generate ores with different probabilities
            ore_chance = rng.random()
            if ore_chance < 0.01:  # 1% chance for diamond
                world[x][y] = DIAMOND_ORE
            elif ore_chance < 0.04:  # 3% chance for gold
                world[x][y] = GOLD_ORE
            elif ore_chance < 0.08:  # 4% chance for redstone
                world[x][y] = REDSTONE_ORE
            elif ore_chance < 0.15:  # 7% chance for iron
                world[x][y] = IRON_ORE
            elif ore_chance < 0.25:  # 10% chance for coal
                world[x][y] = COAL_ORE
        
        # Generate dirt layer
        for y in range(height_map[x] + 1, height_map[x] + stone_depth):
            world[x][y] = DIRT
            
        # Generate grass on top
        if 0 <= height_map[x] < height:
            world[x][height_map[x]] = GRASS
            
        # Generate sand near water level
        if height_map[x] < base - 2:
            for y in range(height_map[x], min(height_map[x] + 3, height)):
                world[x][y] = SAND
                
        # Generate water
        water_level = base - 5
        if height_map[x] < water_level:
            for y in range(height_map[x] + 1, water_level):
                world[x][y] = WATER
        
        # Generate trees
        if rng.random() < 0.03 and height_map[x] > 10 and height_map[x] < height - 10:
            tree_height = rng.randint(4, 6)
            # Trunk
            for ty in range(height_map[x] - tree_height, height_map[x]):
                if 0 <= ty < height:
                    world[x][ty] = WOOD
            # Leaves
            for lx in range(x - 2, x + 3):
                for ly in range(height_map[x] - tree_height - 2, height_map[x] - tree_height + 2):
                    if 0 <= lx < width and 0 <= ly < height:
                        if (lx - x)**2 + (ly - (height_map[x] - tree_height))**2 < 9:
                            world[lx][ly] = LEAVES
    
    # Generate caves
    for _ in range(width // 10):
        cave_x = rng.randint(10, width - 10)
        cave_y = rng.randint(20, height - 20)
        cave_size = rng.randint(3, 8)
        
        for dx in range(-cave_size, cave_size + 1):
            for dy in range(-cave_size, cave_size + 1):
                nx, ny = cave_x + dx, cave_y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if dx*dx + dy*dy < cave_size*cave_size:
                        if world[nx][ny] != BEDROCK and world[nx][ny] != AIR:
                            world[nx][ny] = AIR
    
    return world

# ------------------------------
# Inventory system
# ------------------------------
# All available blocks
ALL_BLOCKS = [
    GRASS, DIRT, STONE, WOOD, LEAVES, SAND, PLANKS, COBBLE, GLASS,
    WATER, LAVA, BEDROCK, IRON_ORE, COAL_ORE, GOLD_ORE, DIAMOND_ORE,
    REDSTONE_ORE, OBSIDIAN, GRAVEL, BRICKS, MOSSY_COBBLE, SPONGE, BOOKSHELF
]

# Default hotbar with 10 slots
HOTBAR_SIZE = 10
DEFAULT_HOTBAR = [GRASS, DIRT, STONE, COBBLE, WOOD, PLANKS, SAND, GLASS, LEAVES, BRICKS]

# ------------------------------
# UI functions
# ------------------------------
def draw_hotbar(screen, fonts, textures, hotbar, selected_index):
    padding = 8
    slot_size = TILE_SIZE + 12
    total_width = slot_size * HOTBAR_SIZE
    x_start = (SCREEN_W - total_width) // 2
    y_start = SCREEN_H - (slot_size + padding)

    for i, block_id in enumerate(hotbar):
        if i >= HOTBAR_SIZE:
            break
            
        x = x_start + i * slot_size
        rect = pygame.Rect(x, y_start, slot_size, slot_size)
        pygame.draw.rect(screen, (30, 30, 30), rect, border_radius=6)
        inner_rect = rect.inflate(-6, -6)
        pygame.draw.rect(screen, (60, 60, 60), inner_rect, width=2, border_radius=4)

        # Draw texture
        if block_id in textures:
            tex = textures[block_id]
            img = pygame.transform.smoothscale(tex, (TILE_SIZE, TILE_SIZE))
            screen.blit(img, (inner_rect.centerx - TILE_SIZE // 2, inner_rect.centery - TILE_SIZE // 2))
        else:
            # Draw placeholder for missing textures
            pygame.draw.rect(screen, (255, 0, 255), inner_rect)

        # Selection highlight
        if i == selected_index:
            pygame.draw.rect(screen, (255, 230, 90), inner_rect, width=3, border_radius=4)

def draw_inventory(screen, fonts, textures, hotbar, selected_index, inventory_open):
    if not inventory_open:
        return
        
    # Draw background
    inventory_rect = pygame.Rect(SCREEN_W // 4, SCREEN_H // 4, SCREEN_W // 2, SCREEN_H // 2)
    pygame.draw.rect(screen, (40, 40, 40), inventory_rect, border_radius=10)
    pygame.draw.rect(screen, (80, 80, 80), inventory_rect, width=3, border_radius=10)
    
    # Draw title
    title = fonts['big'].render("Inventory", True, (230, 230, 230))
    screen.blit(title, (inventory_rect.centerx - title.get_width() // 2, inventory_rect.top + 20))
    
    # Draw blocks in a grid
    block_rows = 4
    block_cols = 6
    block_slot_size = TILE_SIZE + 10
    block_start_x = inventory_rect.left + 20
    block_start_y = inventory_rect.top + 60
    
    for i, block_id in enumerate(ALL_BLOCKS):
        if i >= block_rows * block_cols:
            break
            
        row = i // block_cols
        col = i % block_cols
        x = block_start_x + col * block_slot_size
        y = block_start_y + row * block_slot_size
        
        # Draw slot
        slot_rect = pygame.Rect(x, y, block_slot_size, block_slot_size)
        pygame.draw.rect(screen, (60, 60, 60), slot_rect, border_radius=5)
        inner_slot = slot_rect.inflate(-6, -6)
        pygame.draw.rect(screen, (80, 80, 80), inner_slot, width=2, border_radius=4)
        
        # Draw block texture
        if block_id in textures:
            tex = textures[block_id]
            img = pygame.transform.smoothscale(tex, (TILE_SIZE, TILE_SIZE))
            screen.blit(img, (inner_slot.centerx - TILE_SIZE // 2, inner_slot.centery - TILE_SIZE // 2))
        
        # Highlight if this block is in the hotbar
        if block_id in hotbar:
            pygame.draw.rect(screen, (90, 180, 90), inner_slot, width=2, border_radius=4)
    
    # Draw instructions
    instructions = fonts['small'].render("Click on a block to add it to your hotbar", True, (200, 200, 200))
    screen.blit(instructions, (inventory_rect.centerx - instructions.get_width() / 2, 
                              inventory_rect.bottom - 30))

def draw_player(screen, player, cam_x, cam_y):
    # Draw a Minecraft-style player with white shirt, blue pants, and detailed face
    px = int(player.x - cam_x)
    py = int(player.y - cam_y)
    
    # Calculate body part dimensions (Minecraft proportions)
    head_size = int(player.w * 0.8)  # Head is almost as wide as the player
    body_width = int(player.w * 0.6)
    body_height = int(player.h * 0.3)
    arm_width = int(player.w * 0.25)  # Wider arms
    arm_height = int(player.h * 0.4)
    leg_width = int(player.w * 0.3)   # Wider legs
    leg_height = int(player.h * 0.4)
    
    # Custom colors
    skin_color = (220, 180, 140)      # Light tan skin
    shirt_color = (255, 255, 255)     # White shirt
    pants_color = (60, 100, 200)      # Blue pants
    shoe_color = (40, 40, 40)         # Black shoes
    hair_color = (30, 30, 30)         # Dark gray hair
    eye_color = (0, 0, 0)             # Black eyes
    
    # Head (8x8 pixel style but scaled)
    head_rect = pygame.Rect(px + (player.w - head_size) // 2, py, head_size, head_size)
    pygame.draw.rect(screen, skin_color, head_rect)
    
    # Hair/helmet (covering top and sides of head)
    hair_top_rect = pygame.Rect(px + (player.w - head_size) / 2, py, head_size, head_size / 4)
    hair_left_rect = pygame.Rect(px + (player.w - head_size) / 2, py, head_size / 8, head_size)
    hair_right_rect = pygame.Rect(px + (player.w - head_size) / 2 + head_size - head_size / 8, 
                                 py, head_size / 8, head_size)
    pygame.draw.rect(screen, hair_color, hair_top_rect)
    pygame.draw.rect(screen, hair_color, hair_left_rect)
    pygame.draw.rect(screen, hair_color, hair_right_rect)
    
    # Body (white shirt)
    body_rect = pygame.Rect(px + (player.w - body_width) / 2, py + head_size, body_width, body_height)
    pygame.draw.rect(screen, shirt_color, body_rect)
    
    # Arms (position based on direction)
    if player.direction > 0:  # Facing right
        left_arm_rect = pygame.Rect(px + (player.w - body_width) / 2 - arm_width, 
                                   py + head_size, arm_width, arm_height)
        right_arm_rect = pygame.Rect(px + (player.w - body_width) / 2 + body_width, 
                                    py + head_size, arm_width, arm_height)
    else:  # Facing left
        left_arm_rect = pygame.Rect(px + (player.w - body_width) / 2 + body_width, 
                                   py + head_size, arm_width, arm_height)
        right_arm_rect = pygame.Rect(px + (player.w - body_width) / 2 - arm_width, 
                                    py + head_size, arm_width, arm_height)
    
    # Draw arms with skin color
    pygame.draw.rect(screen, skin_color, left_arm_rect)
    pygame.draw.rect(screen, skin_color, right_arm_rect)
    
    # Legs (blue pants)
    left_leg_rect = pygame.Rect(px + (player.w - body_width) / 2, 
                               py + head_size + body_height, leg_width, leg_height)
    right_leg_rect = pygame.Rect(px + (player.w - body_width) / 2 + body_width - leg_width, 
                                py + head_size + body_height, leg_width, leg_height)
    pygame.draw.rect(screen, pants_color, left_leg_rect)
    pygame.draw.rect(screen, pants_color, right_leg_rect)
    
    # Shoes (bottom of legs)
    left_shoe_rect = pygame.Rect(left_leg_rect.x, left_leg_rect.y + leg_height - leg_width / 2, 
                                leg_width, leg_width / 2)
    right_shoe_rect = pygame.Rect(right_leg_rect.x, right_leg_rect.y + leg_height - leg_width / 2, 
                                 leg_width, leg_width / 2)
    pygame.draw.rect(screen, shoe_color, left_shoe_rect)
    pygame.draw.rect(screen, shoe_color, right_shoe_rect)
    
    # Face details
    eye_size = head_size / 8
    mouth_width = head_size / 4
    mouth_height = head_size / 16
    
    # Eye positions
    left_eye_x = head_rect.x + head_size / 4 - eye_size / 2
    right_eye_x = head_rect.x + head_size * 3 / 4 - eye_size / 2
    eye_y = head_rect.y + head_size / 3 - eye_size / 2
    
    # Draw eyes
    pygame.draw.rect(screen, eye_color, (left_eye_x, eye_y, eye_size, eye_size))
    pygame.draw.rect(screen, eye_color, (right_eye_x, eye_y, eye_size, eye_size))
    
    # Mouth (simple line)
    mouth_x = head_rect.x + head_size / 2 - mouth_width / 2
    mouth_y = head_rect.y + head_size * 2 / 3
    pygame.draw.rect(screen, (0, 0, 0), (mouth_x, mouth_y, mouth_width, mouth_height))
    
    # Add eyebrows for more expression
    eyebrow_height = head_size / 20
    eyebrow_width = eye_size * 1.5
    left_eyebrow_x = left_eye_x - (eyebrow_width - eye_size) / 2
    right_eyebrow_x = right_eye_x - (eyebrow_width - eye_size) / 2
    pygame.draw.rect(screen, hair_color, (left_eyebrow_x, eye_y - eyebrow_height, eyebrow_width, eyebrow_height))
    pygame.draw.rect(screen, hair_color, (right_eyebrow_x, eye_y - eyebrow_height, eyebrow_width, eyebrow_height))

# ------------------------------
# Main game (async for web)
# ------------------------------
async def main():
    # Initialize pygame
    pygame.init()
    
    # Create screen
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Mimicraft2D")
    
    # Create clock
    clock = pygame.time.Clock()

    # Create fonts
    fonts = {
        'small': pygame.font.SysFont("Arial", 16),
        'big': pygame.font.SysFont("Arial", 22, bold=True),
    }

    # Generate textures with error handling
    try:
        textures = generate_textures()
    except:
        textures = {}
        # Create a simple fallback texture
        fallback_tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        fallback_tex.fill((255, 0, 255))  # Magenta for missing textures
        for bid in ALL_BLOCKS:
            textures[bid] = fallback_tex

    # Create world
    world = make_world(WORLD_W, WORLD_H)
    
    # Create player
    player = Player(5 * TILE_SIZE, 10 * TILE_SIZE)

    # Initialize hotbar
    hotbar = DEFAULT_HOTBAR[:]  # Copy the default hotbar
    selected_index = 0  # Currently selected slot

    # Game state
    running = True
    cam_x, cam_y = 0.0, 0.0
    inventory_open = False

    # Main game loop
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if inventory_open:
                        inventory_open = False
                    else:
                        running = False
                if pygame.K_1 <= event.key <= pygame.K_0:
                    # Handle number keys 1-9 and 0 (for slot 10)
                    key_index = event.key - pygame.K_1
                    if key_index == 9:  # 0 key should select slot 10
                        key_index = 9
                    if key_index < HOTBAR_SIZE:
                        selected_index = key_index
                if event.key == pygame.K_e:
                    inventory_open = not inventory_open
            elif event.type == pygame.MOUSEWHEEL:
                # Scroll through hotbar
                selected_index = (selected_index - event.y) % HOTBAR_SIZE
            elif event.type == pygame.MOUSEBUTTONDOWN and inventory_open:
                # Handle inventory clicks
                if event.button == 1:  # Left click
                    mx, my = pygame.mouse.get_pos()
                    
                    # Check if click is in blocks section
                    inventory_rect = pygame.Rect(SCREEN_W / 4, SCREEN_H / 4, SCREEN_W / 2, SCREEN_H / 2)
                    block_rows = 4
                    block_cols = 6
                    block_slot_size = TILE_SIZE + 10
                    block_start_x = inventory_rect.left + 20
                    block_start_y = inventory_rect.top + 60
                    
                    # Check blocks
                    for i, block_id in enumerate(ALL_BLOCKS):
                        if i >= block_rows * block_cols:
                            break
                            
                        row = i // block_cols
                        col = i % block_cols
                        x = block_start_x + col * block_slot_size
                        y = block_start_y + row * block_slot_size
                        
                        if x <= mx <= x + block_slot_size and y <= my <= y + block_slot_size:
                            # Add this block to the hotbar at the selected position
                            hotbar[selected_index] = block_id
                            break

        # Only process movement if inventory is closed
        if not inventory_open:
            keys = pygame.key.get_pressed()
            player.vx = 0
            if keys[pygame.K_a]:
                player.vx = -MOVE_SPEED
                player.direction = -1
            if keys[pygame.K_d]:
                player.vx = MOVE_SPEED
                player.direction = 1
            if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and player.on_ground:
                player.vy = JUMP_VEL
                player.on_ground = False

            move_and_collide(world, player, dt)

            # Camera follows player, clamp to world
            cam_x = max(0, min(player.x + player.w / 2 - SCREEN_W / 2, WORLD_W * TILE_SIZE - SCREEN_W))
            cam_y = max(0, min(player.y + player.h / 2 - SCREEN_H / 2, WORLD_H * TILE_SIZE - SCREEN_H))

            # Mouse world tile
            mx, my = pygame.mouse.get_pos()
            wx, wy = screen_to_world(cam_x, cam_y, mx, my)

            # Interaction reach
            px, py = (player.x + player.w / 2) / TILE_SIZE, (player.y + player.h / 2) / TILE_SIZE
            in_reach = dist_tiles(wx + 0.5, wy + 0.5, px, py) <= REACH_TILES

            mouse_buttons = pygame.mouse.get_pressed(3)

            # Breaking (instant)
            if mouse_buttons[0] and in_reach and in_bounds(wx, wy) and get_tile(world, wx, wy) != AIR:
                set_tile(world, wx, wy, AIR)

            # Placement
            sel_bid = hotbar[selected_index]
            if mouse_buttons[2] and in_reach and sel_bid in PLACEABLE_IDS:
                if can_place(world, wx, wy, player.rect):
                    set_tile(world, wx, wy, sel_bid)
            #R to place block
            key_index = pygame.key.get_pressed()
            if key_index[pygame.K_r] and in_reach and sel_bid in PLACEABLE_IDS:
                if can_place(world, wx, wy, player.rect):
                    set_tile(world, wx, wy, sel_bid)
        

        # Render
        screen.fill((110, 180, 255))  # sky

        # Visible tile bounds
        x0 = max(0, int(cam_x // TILE_SIZE))
        y0 = max(0, int(cam_y // TILE_SIZE))
        x1 = min(WORLD_W - 1, int((cam_x + SCREEN_W) // TILE_SIZE) + 1)
        y1 = min(WORLD_H - 1, int((cam_y + SCREEN_H) // TILE_SIZE) + 1)

        # Draw tiles
        for tx in range(x0, x1 + 1):
            for ty in range(y0, y1 + 1):
                bid = world[tx][ty]
                if bid != AIR:
                    tex = textures.get(bid)
                    if tex:
                        screen.blit(tex, (tx * TILE_SIZE - cam_x, ty * TILE_SIZE - cam_y))

        # Draw aim highlight
        if not inventory_open and in_bounds(wx, wy) and in_reach:
            outline_rect = pygame.Rect(wx * TILE_SIZE - cam_x, wy * TILE_SIZE - cam_y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 255, 255), outline_rect, width=1)

        # Draw player
        if not inventory_open:
            draw_player(screen, player, cam_x, cam_y)

        # UI
        draw_hotbar(screen, fonts, textures, hotbar, selected_index)
        
        # Draw inventory if open
        draw_inventory(screen, fonts, textures, hotbar, selected_index, inventory_open)

        # Title info
        sel_bid = hotbar[selected_index]
        info = f"Mimicraft2D  |  FPS: {int(clock.get_fps())}  |  Selected: {BLOCKS.get(sel_bid, {}).get('name', 'Unknown')}"
        label = fonts['small'].render(info, True, (20, 20, 20))
        screen.blit(label, (10, 8))

        pygame.display.flip()
        await asyncio.sleep(0)  # Important for web version

    pygame.quit()