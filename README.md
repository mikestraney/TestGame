# Test Game

A lightweight side-scrolling run-and-gun prototype inspired by 8-bit classics.
The game is written entirely in Python and powered by the Pygame framework.

## Gameplay

Guide a commando across a horizontal battlefield, jumping over obstacles and
blasting enemies that march in from the right. Every defeated foe boosts your
score, while a single collision ends the run.

### Controls

- **Move:** Arrow keys
- **Jump:** Z or Up arrow
- **Shoot:** Space bar

Sprites, basic physics, and collision detection are handled with Pygame's sprite
system. Bullets fly across the screen and disappear when they leave the play
area.

## Libraries

The project purposefully keeps dependencies minimal:

- [Pygame](https://www.pygame.org/) – provides the window, main loop, event
  handling, sprite groups, fonts, and drawing operations.
- Python's standard library for core language features and timing.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python game.py
   ```

Enjoy experimenting with this small codebase or use it as a starting point for your own shooter.
