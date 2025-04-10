# Match-3 Game

Classic Match-3 puzzle game implementation in Python using Pygame and Gale libraries.

## Requirements
- Python
- Pygame
- Gale

## Installation

### Windows
1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/).
   - During installation, ensure you check the box "Add Python to PATH".

2. **Clone repository**:
   ```bash
   git clone https://github.com/Trysdan/04-Match3.git
   cd 04-Match3
   ```

3. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Note on Virtual Environment Activation in PowerShell**  
   If you encounter an error when trying to activate the virtual environment using the `venv\Scripts\activate` command in PowerShell, it may be due to the script execution policy on your system. To resolve this, run the following command in PowerShell before activating the virtual environment:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Linux
1. **Install Python**:
   - Most Linux distributions come with Python pre-installed. Check your version:
     ```bash
     python3 --version
     ```
   - If Python is not installed, use your package manager:
     - Debian/Ubuntu:
       ```bash
       sudo apt update
       sudo apt install python3
       ```
     - Fedora:
       ```bash
       sudo dnf install python3
       ```

2. **Clone repository**:
   ```bash
   git clone https://github.com/Trysdan/04-Match3.git
   cd 04-Match3
   ```

3. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
1. **Start the game**:
   ```bash
   python main.py
   ```

2. **Deactivate virtual environment when done**:
   ```bash
   deactivate
   ```

## Controls
- **Move tiles:** Click, hold and drag to adjacent positions
- **Activate power-ups:** Click on power-up tiles
  - **Cross:** Clears entire row and column (created by matching 4 tiles)
  - **Circle:** Clears all tiles of same color (created by matching 5+ tiles)

## Features
- Automatic board reshuffle when no valid moves remain
- Level progression with time limits
- Visual and sound effects for matches
- Move validation (only allows matches)

## How to Play
1. Drag tiles to create groups of 3+ matching colors
2. Match 4 tiles to create Cross power-ups
3. Match 5+ tiles to create Circle power-ups
4. Click power-ups when needed for special effects
5. Complete level objectives before time runs out

Project created for video game programming practice course.