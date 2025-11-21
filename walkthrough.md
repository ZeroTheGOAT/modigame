# My Mario Game Walkthrough

This is a custom version of Super Mario Python with specific assets and gameplay changes.

## Features

- **Custom Character**: The main character is replaced by `character.jpeg`.
- **Custom Enemies**: Goombas are replaced by `enemy.jpg`.
- **Happy State**: When collecting a coin, the character transforms into `happy_character.jpeg` for 2 seconds.
- **Winning Condition**: At the end of the level (around x=58), you will meet `Meloni`.
- **Win Sequence**: Upon meeting Meloni, a "You Won!" screen appears first. Then, a video `win_video.mp4` plays (rotated 90 degrees clockwise and scaled to fit) while `end.mp3` plays on loop.
- **Sound Effects**:
    - `coins.mp3`: Plays when collecting a coin.
    - `ah.mp3`: Plays when defeating an enemy.
- **Resizable Window**: The game window can be maximized or resized, and the game content will scale to fit.

## How to Play

1.  Navigate to `c:\projects\game\modi\my_mario_game`.
2.  Run `python main.py`.
3.  Controls:
    - **Arrow Keys**: Move
    - **Space**: Jump
    - **Shift**: Sprint
    - **Maximize/Resize**: Drag window corners or click maximize button.

## Implementation Details

- **Assets**: All custom assets are located in `img/` and `sfx/`.
- **Code Changes**:
    - `main.py`: Implemented virtual screen and scaling logic to support window resizing. Refactored event loop to pass events to components.
    - `classes/Menu.py`, `classes/Pause.py`: Removed direct display updates and updated `update`/`checkInput` to accept events.
    - `classes/Input.py`: Updated `checkForInput` to accept events instead of calling `pygame.event.get()`.
    - `classes/Sprites.py`: Modified to load custom images and override default sprites, including Koopas.
    - `classes/Sound.py`: Added loading of `ah.mp3`, `coins.mp3`, and `end.mp3`.
    - `entities/Mario.py`: Added logic for "happy" state timer and animation switching. Added collision detection for `Meloni` and the `winGame` method using `cv2` for video playback (text first, then rotated video with looping music). Added `ah.mp3` playback on entity kill. Updated `gameOver`, `winGame`, and `update` to handle scaling and passed events.
    - `classes/Level.py`: Added `Meloni` entity spawning at the end of the level.
    - `entities/Meloni.py`: New entity class for the win target.

## Requirements

- Python 3
- `pygame`
- `opencv-python` (for video playback)
