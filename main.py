import asyncio
import pygame
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your game
from Mimicraft2D import main

# This is the entry point for Pygbag
if __name__ == "__main__":
    asyncio.run(main())