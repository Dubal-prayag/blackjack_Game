import random
import tkinter as tk
from tkinter import messagebox
import time

# Initialize player balance
balance = 1000
bet_amount = 0

# Define the card deck
card_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # J, Q, K treated as 10
user_cards = []
dealer_cards = []

# Create the GUI window
root = tk.Tk()
root.title("Blackjack Casino")
root.geometry("500x600")
root.configure(bg="#228B22")  # Green casino-style background

# Create a canvas for animations
canvas = tk.Canvas(root, width=500, height=300, bg="#006400")
canvas.pack()

# Function to deal a card
def deal_card():
    return random.choice(card_deck)

# Function to calculate the score
def calculate_score(cards):
    score = sum(cards)
    if 11 in cards and score + 10 <= 21:
        score += 10  # Ace counts as 11 unless bust
    return score

# Function to animate cards moving
def animate_card(x_start, y_start, x_end, y_end, text, delay):
    card = canvas.create_text(x_start, y_start, text=text, font=("Arial", 16, "bold"), fill="white")
    for _ in range(20):  # Steps for animation
        canvas.move(card, (x_end - x_start) / 20, (y_end - y_start) / 20)
        root.update()
        time.sleep(delay)

# Function to update display
def update_display():
    balance_var.set(f"Balance: ${balance}")
    user_score.set(f"Your Cards: {user_cards} | Score: {calculate_score(user_cards)}")
    if dealer_cards:
        dealer_score.set(f"Dealer's First Card: {dealer_cards[0]}")
    else:
        dealer_score.set("Dealer's First Card: ?")

# Function to place bet
def place_bet():
    global bet_amount
    try:
        bet_amount = int(bet_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Bet", "Enter a valid number!")
        return
    if bet_amount > balance or bet_amount <= 0:
        messagebox.showerror("Invalid Bet", "Enter a valid bet amount!")
    else:
        messagebox.showinfo("Bet Placed", f"Betting ${bet_amount}. Good luck!")
        play_game()

# Function to check results
def check_result():
    global balance
    user_total = calculate_score(user_cards)
    dealer_total = calculate_score(dealer_cards)

    while dealer_total != 0 and dealer_total < 17:
        dealer_cards.append(deal_card())
        dealer_total = calculate_score(dealer_cards)
        animate_card(400, 50, 250 + (len(dealer_cards) * 30), 50, f"{dealer_cards[-1]}", 0.05)

    update_display()

    if user_total > 21:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"You went over! You lose!\nNew Balance: ${balance}")
    elif dealer_total > 21:
        balance += bet_amount
        messagebox.showinfo("Game Over", f"Dealer went over! You win!\nNew Balance: ${balance}")
    elif user_total == dealer_total:
        messagebox.showinfo("Game Over", "It's a draw!")
    elif user_total == 0:
        balance += int(bet_amount * 1.5)  # Blackjack pays 1.5x
        messagebox.showinfo("Game Over", f"Blackjack! You win!\nNew Balance: ${balance}")
    elif dealer_total == 0:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"Dealer has Blackjack! You lose!\nNew Balance: ${balance}")
    elif user_total > dealer_total:
        balance += bet_amount
        messagebox.showinfo("Game Over", f"Congratulations! You win!\nNew Balance: ${balance}")
    else:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"You lose!\nNew Balance: ${balance}")

    if balance <= 0:
        messagebox.showerror("Game Over", "You are out of money! Restart the game.")
        root.quit()

# Function when user clicks "Hit"
def hit():
    card = deal_card()
    user_cards.append(card)
    x_position = 250 + (len(user_cards) * 30)  # Space cards 30 pixels apart
    animate_card(100, 200, x_position, 200, f"{card}", 0.05)
    update_display()
    if calculate_score(user_cards) > 21:
        check_result()

# Function when user clicks "Stand"
def stand():
    check_result()

# Function to start the game
def play_game():
    global user_cards, dealer_cards
    canvas.delete("all")  # Clear the canvas to avoid overlapping cards
    user_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]
    update_display()

    animate_card(100, 200, 250, 200, f"{user_cards[0]}", 0.05)
    animate_card(100, 200, 300, 200, f"{user_cards[1]}", 0.05)
    animate_card(400, 50, 250, 50, f"{dealer_cards[0]}", 0.05)

# Variables for labels
balance_var = tk.StringVar()
user_score = tk.StringVar()
dealer_score = tk.StringVar()
update_display()

# GUI Elements
tk.Label(root, text="Blackjack Casino", font=("Arial", 24, "bold"), fg="gold", bg="#228B22").pack(pady=10)
tk.Label(root, textvariable=balance_var, font=("Arial", 14), fg="white", bg="#228B22").pack()
tk.Label(root, text="Place Your Bet:", font=("Arial", 14), fg="white", bg="#228B22").pack()
bet_entry = tk.Entry(root, font=("Arial", 14))
bet_entry.pack()
tk.Button(root, text="Confirm Bet", command=place_bet, font=("Arial", 12), bg="gold").pack(pady=5)
tk.Label(root, textvariable=user_score, font=("Arial", 14), fg="white", bg="#228B22").pack()
tk.Label(root, textvariable=dealer_score, font=("Arial", 14), fg="white", bg="#228B22").pack()
tk.Button(root, text="Hit", command=hit, width=10, font=("Arial", 12), bg="red", fg="white").pack(pady=5)
tk.Button(root, text="Stand", command=stand, width=10, font=("Arial", 12), bg="blue", fg="white").pack(pady=5)

# Start GUI loop
root.mainloop()
