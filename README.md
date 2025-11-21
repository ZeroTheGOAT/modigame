# Super Mario Web Game

A web-playable Mario game with mobile touch controls, built with Pygame and Pygbag.

## Features

- 🎮 Play in your browser (desktop or mobile)
- 📱 Mobile touch controls (landscape mode)
- 🎵 Sound effects and music
- 🏆 Multiple levels and enemies

## Play Online

Visit the deployed game at: [Your Vercel URL here]

## Controls

### Desktop
- **Arrow Keys / H,L**: Move left/right
- **Space / Up / K**: Jump
- **Shift**: Run faster
- **ESC / F5**: Pause

### Mobile
- **Left Button**: Move left
- **Right Button**: Move forward/right
- **Jump Button**: Jump
- Please rotate your device to landscape mode for the best experience

## Local Development

1. Install dependencies:
   ```bash
   pip install pygame pygbag
   ```

2. Run locally:
   ```bash
   python main.py
   ```

3. Build for web:
   ```bash
   pygbag my_mario_game
   ```
   Then open `localhost:8000` in your browser.

## Deployment to Vercel

1. Build the game:
   ```bash
   cd my_mario_game
   pygbag .
   ```

2. Deploy to Vercel:
   ```bash
   vercel deploy
   ```

3. Or connect your GitHub repository to Vercel for automatic deployments.

## Credits

Based on Super Mario Bros with custom modifications for web play.
