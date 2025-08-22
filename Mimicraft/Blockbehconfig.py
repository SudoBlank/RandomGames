# Block behavior configuration
AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
WOOD = 4
LEAVES = 5
SAND = 6
PLANKS = 7
COBBLE = 8
GLASS = 9
WATER = 10
LAVA = 11
BEDROCK = 12
IRON_ORE = 13
COAL_ORE = 14
GOLD_ORE = 15
DIAMOND_ORE = 16
REDSTONE_ORE = 17
OBSIDIAN = 18
GRAVEL = 19
BRICKS = 20
MOSSY_COBBLE = 21
SPONGE = 22
BOOKSHELF = 23

# Define block properties
BLOCKS = {
    AIR: {"name": "Air", "solid": False, "transparent": True},
    GRASS: {"name": "Grass", "solid": True, "transparent": False},
    DIRT: {"name": "Dirt", "solid": True, "transparent": False},
    STONE: {"name": "Stone", "solid": True, "transparent": False},
    WOOD: {"name": "Wood", "solid": True, "transparent": False},
    LEAVES: {"name": "Leaves", "solid": True, "transparent": True},
    SAND: {"name": "Sand", "solid": True, "transparent": False},
    PLANKS: {"name": "Planks", "solid": True, "transparent": False},
    COBBLE: {"name": "Cobblestone", "solid": True, "transparent": False},
    GLASS: {"name": "Glass", "solid": True, "transparent": True},
    WATER: {"name": "Water", "solid": False, "transparent": True},
    LAVA: {"name": "Lava", "solid": False, "transparent": True},
    BEDROCK: {"name": "Bedrock", "solid": True, "transparent": False},
    IRON_ORE: {"name": "Iron Ore", "solid": True, "transparent": False},
    COAL_ORE: {"name": "Coal Ore", "solid": True, "transparent": False},
    GOLD_ORE: {"name": "Gold Ore", "solid": True, "transparent": False},
    DIAMOND_ORE: {"name": "Diamond Ore", "solid": True, "transparent": False},
    REDSTONE_ORE: {"name": "Redstone Ore", "solid": True, "transparent": False},
    OBSIDIAN: {"name": "Obsidian", "solid": True, "transparent": False},
    GRAVEL: {"name": "Gravel", "solid": True, "transparent": False},
    BRICKS: {"name": "Bricks", "solid": True, "transparent": False},
    MOSSY_COBBLE: {"name": "Mossy Cobblestone", "solid": True, "transparent": False},
    SPONGE: {"name": "Sponge", "solid": True, "transparent": False},
    BOOKSHELF: {"name": "Bookshelf", "solid": True, "transparent": False},
}

# Define what items can be placed
PLACEABLE_IDS = [GRASS, DIRT, STONE, WOOD, LEAVES, SAND, PLANKS, COBBLE, GLASS, 
                 WATER, LAVA, BEDROCK, IRON_ORE, COAL_ORE, GOLD_ORE, DIAMOND_ORE, 
                 REDSTONE_ORE, OBSIDIAN, GRAVEL, BRICKS, MOSSY_COBBLE, SPONGE, BOOKSHELF]

# Helper function to check if a block is solid
def is_solid(block_id):
    return BLOCKS.get(block_id, {}).get("solid", False)

# Define what drops from each block when broken
def get_drop(block_id):
    # For simplicity, most blocks drop themselves
    return block_id

# Define break time for each block (instant now)
def get_break_time(block_id, tool_power=1.0):
    return 0.001  # Almost instant