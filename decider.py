#!/usr/bin/env python3
import random
import time

# ASCII art for YES
YES_ART = """
██    ██ ███████ ███████
 ██  ██  ██      ██
  ████   █████   ███████
   ██    ██           ██
   ██    ███████ ███████
"""

# ASCII art for NO
NO_ART = """
███    ██  ██████
████   ██ ██    ██
██ ██  ██ ██    ██
██  ██ ██ ██    ██
██   ████  ██████
"""

def main():
    # Get the dilemma from the user
    dilemma = input("What is your dilemma? ")

    # Show processing message
    print("\nCalculating optimal corporate synergy...")

    # Wait 3 seconds
    time.sleep(3)

    # Randomly choose YES or NO
    decision = random.choice(['YES', 'NO'])

    # Print the result in ASCII art
    if decision == 'YES':
        print(YES_ART)
    else:
        print(NO_ART)

if __name__ == "__main__":
    main()
