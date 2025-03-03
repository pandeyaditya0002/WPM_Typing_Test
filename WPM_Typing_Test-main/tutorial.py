import curses
from curses import wrapper
import time
import random
import os

# Function to display the start screen
def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!\n")
    stdscr.addstr("Press any key to begin!\n")
    stdscr.refresh()
    stdscr.getkey()

# Function to display the text and user input
def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target + "\n")  # Display target text
    stdscr.addstr(f"WPM: {wpm}\n")  # Display WPM count

    # Loop through user input and compare with target text
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)  # Default color for correct input
        if char != correct_char:
            color = curses.color_pair(2)  # Incorrect input in red

        stdscr.addstr(0, i, char, color)

# Function to load a random text from 'text.txt'

def load_text():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "text.txt")
    if not os.path.exists(file_path):
        print(f"Error: 'text.txt' not found at {file_path}")
        exit()
    with open(file_path, "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


# Function to handle the typing test
def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)  # Non-blocking input

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # Calculate WPM

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        # Check if the user has completed the text
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        # Exit on 'Esc' key press
        if len(key) == 1 and ord(key) == 27: 
            break

        # Handle backspace
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

# Main function to initialize the game
def main(stdscr):
    # Initialize color pairs for highlighting
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Correct input
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Incorrect input
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Default text

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr("\nYou completed the text! Press any key to continue...\n")
        key = stdscr.getkey()
        
        # Exit on 'Esc' key press
        if ord(key) == 27:
            break

# Run the program
wrapper(main)
