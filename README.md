
# Python Snake Game with AI Agent

## Overview
This project is an implementation of the classic snake game in Python, with an added twist of an AI agent that learns to play the game. The project uses Pygame for graphical representation, TensorFlow for the AI model, and other Python libraries for various functionalities.

## Files
- **agent.py**: Contains the logic for the AI agent, including memory and training routines.
- **food.py**: Defines the Food class, which handles the generation and rendering of food in the game.
- **snake.py**: Contains the Snake class, managing the snake's movement, growth, and rendering.
- **model.py**: Defines the neural network model used by the AI agent.
- **helper.py**: Provides utility functions such as plotting training progress.
- **main.py**: The main game loop, integrating all components and running the game.

## Installation
1. Install Python 3.x
2. Install required packages: `pygame`, `torch`, `numpy`, `matplotlib`, `IPython`
    ```bash
    pip install pygame torch numpy matplotlib ipython
    ```
3. Clone this repository:
    ```bash
    git clone [repository_url]
    ```
4. Navigate to the project directory and run the game:
    ```bash
    python main.py
    ```

## Gameplay
- Use arrow keys to control the snake.
- Eat food to grow longer.
- Avoid hitting the walls or yourself.

## AI Agent
- The AI agent uses a neural network to learn the game.
- Training progress can be visualized using the plot function in `helper.py`.
- To train the agent, run `agent.py`.

## Customization
- Settings can be adjusted in `settings.py` (not included in the file list, but assumed to exist).
- Modify neural network parameters in `model.py` for different learning behaviors.
