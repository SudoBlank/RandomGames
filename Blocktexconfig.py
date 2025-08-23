import pygame
import random

# Import block constants
from Blockbehconfig import (
    GRASS, DIRT, STONE, WOOD, LEAVES, SAND, PLANKS, COBBLE, GLASS,
    WATER, LAVA, BEDROCK, IRON_ORE, COAL_ORE, GOLD_ORE, DIAMOND_ORE,
    REDSTONE_ORE, OBSIDIAN, GRAVEL, BRICKS, MOSSY_COBBLE, SPONGE, BOOKSHELF
)

TILE_SIZE = 32

def generate_textures():
    try:
        textures = {}
        
        # Base colors for blocks
        colors = {
            "air": (0, 0, 0, 0),
            "grass_top": (80, 180, 40),
            "grass_side": (100, 140, 50),
            "dirt": (120, 100, 60),
            "stone": (130, 130, 130),
            "wood": (150, 120, 80),
            "wood_rings": (130, 100, 60),
            "leaves": (50, 140, 40),
            "sand": (230, 220, 150),
            "planks": (200, 170, 100),
            "cobble": (120, 120, 120),
            "cobble_dark": (100, 100, 100),
            "glass": (200, 220, 240, 150),
            "water": (60, 120, 220, 150),
            "lava": (240, 120, 40, 200),
            "bedrock": (80, 80, 80),
            "iron_ore": (180, 180, 190),
            "coal_ore": (60, 60, 60),
            "gold_ore": (240, 210, 60),
            "diamond_ore": (100, 200, 220),
            "redstone_ore": (200, 60, 60),
            "obsidian": (40, 20, 60),
            "gravel": (150, 140, 130),
            "bricks": (180, 100, 80),
            "bricks_mortar": (150, 150, 150),
            "mossy_cobble": (100, 130, 100),
            "sponge": (220, 220, 100),
            "bookshelf_side": (180, 150, 100),
            "bookshelf_top": (150, 120, 80),
        }
        
        # Function to add noise to a color
        def add_noise(base_color, intensity=10):
            if len(base_color) == 4:  # RGBA
                r, g, b, a = base_color
                r = max(0, min(255, r + random.randint(-intensity, intensity)))
                g = max(0, min(255, g + random.randint(-intensity, intensity)))
                b = max(0, min(255, b + random.randint(-intensity, intensity)))
                return (r, g, b, a)
            else:  # RGB
                r, g, b = base_color
                r = max(0, min(255, r + random.randint(-intensity, intensity)))
                g = max(0, min(255, g + random.randint(-intensity, intensity)))
                b = max(0, min(255, b + random.randint(-intensity, intensity)))
                return (r, g, b)
        
        # Generate grass texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if y < TILE_SIZE // 3:
                    tex.set_at((x, y), add_noise(colors["grass_top"], 15))
                else:
                    tex.set_at((x, y), add_noise(colors["grass_side"], 15))
        textures[GRASS] = tex
        
        # Generate dirt texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["dirt"], 20))
        textures[DIRT] = tex
        
        # Generate stone texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["stone"], 15))
        textures[STONE] = tex
        
        # Generate wood texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if x % 8 == 0:
                    tex.set_at((x, y), add_noise(colors["wood_rings"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["wood"], 15))
        textures[WOOD] = tex
        
        # Generate leaves texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.1:  # 90% coverage
                    tex.set_at((x, y), add_noise(colors["leaves"], 25))
        textures[LEAVES] = tex
        
        # Generate sand texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["sand"], 15))
        textures[SAND] = tex
        
        # Generate planks texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if x % 4 == 0 or y % 4 == 0:
                    tex.set_at((x, y), add_noise(colors["wood_rings"], 5))
                else:
                    tex.set_at((x, y), add_noise(colors["planks"], 10))
        textures[PLANKS] = tex
        
        # Generate cobblestone texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if (x + y) % 3 == 0:
                    tex.set_at((x, y), add_noise(colors["cobble_dark"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["cobble"], 10))
        textures[COBBLE] = tex
        
        # Generate glass texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if x % 8 == 0 or y % 8 == 0:
                    tex.set_at((x, y), (255, 255, 255, 100))
                else:
                    tex.set_at((x, y), add_noise(colors["glass"], 5))
        textures[GLASS] = tex
        
        # Generate water texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["water"], 5))
        textures[WATER] = tex
        
        # Generate lava texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["lava"], 15))
        textures[LAVA] = tex
        
        # Generate bedrock texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if (x + y) % 4 < 2:
                    tex.set_at((x, y), add_noise(colors["bedrock"], 5))
                else:
                    tex.set_at((x, y), add_noise((60, 60, 60), 5))
        textures[BEDROCK] = tex
        
        # Generate iron ore texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.7:
                    tex.set_at((x, y), add_noise(colors["iron_ore"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["stone"], 10))
        textures[IRON_ORE] = tex
        
        # Generate coal ore texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.7:
                    tex.set_at((x, y), add_noise(colors["coal_ore"], 5))
                else:
                    tex.set_at((x, y), add_noise(colors["stone"], 10))
        textures[COAL_ORE] = tex
        
        # Generate gold ore texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.8:
                    tex.set_at((x, y), add_noise(colors["gold_ore"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["stone"], 10))
        textures[GOLD_ORE] = tex
        
        # Generate diamond ore texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.85:
                    tex.set_at((x, y), add_noise(colors["diamond_ore"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["stone"], 10))
        textures[DIAMOND_ORE] = tex
        
        # Generate redstone ore texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.75:
                    tex.set_at((x, y), add_noise(colors["redstone_ore"], 10))
                else:
                    tex.set_at((x, y), add_noise(colors["stone"], 10))
        textures[REDSTONE_ORE] = tex
        
        # Generate obsidian texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.9:
                    tex.set_at((x, y), add_noise((80, 40, 100), 10))
                else:
                    tex.set_at((x, y), add_noise(colors["obsidian"], 5))
        textures[OBSIDIAN] = tex
        
        # Generate gravel texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["gravel"], 20))
        textures[GRAVEL] = tex
        
        # Generate bricks texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if x % 8 == 0 or y % 8 == 0:
                    tex.set_at((x, y), add_noise(colors["bricks_mortar"], 5))
                else:
                    tex.set_at((x, y), add_noise(colors["bricks"], 10))
        textures[BRICKS] = tex
        
        # Generate mossy cobblestone texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if random.random() > 0.8:
                    tex.set_at((x, y), add_noise(colors["mossy_cobble"], 15))
                else:
                    tex.set_at((x, y), add_noise(colors["cobble"], 10))
        textures[MOSSY_COBBLE] = tex
        
        # Generate sponge texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                tex.set_at((x, y), add_noise(colors["sponge"], 20))
        textures[SPONGE] = tex
        
        # Generate bookshelf texture
        tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        for y in range(TILE_SIZE):
            for x in range(TILE_SIZE):
                if y < 4 or y > TILE_SIZE - 5:
                    tex.set_at((x, y), add_noise(colors["bookshelf_top"], 10))
                elif x % 6 == 0 or x % 6 == 1:
                    tex.set_at((x, y), add_noise((30, 30, 30), 5))  # Books
                else:
                    tex.set_at((x, y), add_noise(colors["bookshelf_side"], 10))
        textures[BOOKSHELF] = tex
        
        return textures
        
    except Exception as e:
        print(f"Error generating textures: {e}")
        # Return a minimal set of textures to prevent complete failure
        fallback_textures = {}
        fallback_tex = pygame.Surface((TILE_SIZE, TILE_SIZE))
        fallback_tex.fill((255, 0, 255))  # Magenta for missing textures
        for bid in [GRASS, DIRT, STONE, WOOD, LEAVES, SAND, PLANKS, COBBLE, GLASS]:
            fallback_textures[bid] = fallback_tex
        return fallback_textures