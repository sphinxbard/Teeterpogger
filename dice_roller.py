import math
from random import randint

def roll_dice(num_dice, num_sides):
    return [randint(1, num_sides) for _ in range(num_dice)]

def main():
    while True:
        try:
            user_input = input("Enter the number of dice and sides (e.g., 2d6) or 'exit' to quit: ")
            if user_input.lower() == 'exit':
                break
            
            parts = user_input.lower().split('d')
            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                print("Invalid input format. Please use the format NdM (e.g., 2d6).")
                continue
            
            num_dice = int(parts[0])
            num_sides = int(parts[1])
            
            if num_dice <= 0 or num_sides <= 0:
                print("Number of dice and sides must be positive integers.")
                continue
            
            rolls = roll_dice(num_dice, num_sides)
            print(f"Rolled: {rolls} | Total: {sum(rolls)}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()