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
- **Select Tile**: Click on a tile
- **Swap Tiles**: Click on an adjacent tile to swap positions
- **Game automatically detects matches** and calculates score

## Game Features
- **Progressive Difficulty**: Higher levels require more points to complete
- **Time Limit**: Complete each level before time runs out
- **Visual Feedback**: Highlighted selected tiles and match animations
- **Sound Effects**: Audio feedback for matches and game events

Project created for video game programming practice course.