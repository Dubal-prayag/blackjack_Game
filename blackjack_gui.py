import random
import tkinter as tk
from tkinter import messagebox
import time

# ----------------- Initialize Global Variables -----------------
balance = 1000
bet_amount = 0
card_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # J, Q, K as 10
user_cards = []
dealer_cards = []

# ----------------- Create the GUI Window -----------------
root = tk.Tk()
root.title("Blackjack Casino")
root.geometry("500x600")
root.configure(bg="#228B22")  # Green casino-style background

# ----------------- Create a Canvas for Animations -----------------
canvas = tk.Canvas(root, width=500, height=300, bg="#006400")
canvas.pack()

# ----------------- Game Functions -----------------
def deal_card():
    """Draw a random card from the deck."""
    return random.choice(card_deck)

def calculate_score(cards):
    """Calculate the score and adjust for Ace if needed."""
    score = sum(cards)
    if 11 in cards and score > 21:
        cards.remove(11)
        cards.append(1)  # Convert Ace from 11 to 1 if over 21
    return score

def animate_card(x_start, y_start, x_end, y_end, text, delay):
    """Create a smooth card animation on the canvas."""
    card = canvas.create_text(x_start, y_start, text=text, font=("Arial", 16, "bold"), fill="white")
    for _ in range(20):  # Steps for animation
        canvas.move(card, (x_end - x_start) / 20, (y_end - y_start) / 20)
        root.update()
        time.sleep(delay)

def update_display():
    """Update the balance and game status in the UI."""
    balance_var.set(f"Balance: ${balance}")
    user_score.set(f"Your Cards: {user_cards} | Score: {calculate_score(user_cards)}")
    if dealer_cards:
        dealer_score.set(f"Dealer's First Card: {dealer_cards[0]}")
    else:
        dealer_score.set("Dealer's First Card: ?")

def place_bet():
    """Handle betting logic before the game starts."""
    global bet_amount
    try:
        bet_amount = int(bet_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Bet", "Enter a valid number!")
        return
    if bet_amount > balance or bet_amount <= 0:
        messagebox.showerror("Invalid Bet", "You don't have enough money!")
    else:
        messagebox.showinfo("Bet Placed", f"Betting ${bet_amount}. Good luck!")
        play_game()

def check_result():
    """Determine the game outcome and update the balance."""
    global balance
    user_total = calculate_score(user_cards)
    dealer_total = calculate_score(dealer_cards)

    while dealer_total != 0 and dealer_total < 17:
        dealer_cards.append(deal_card())
        dealer_total = calculate_score(dealer_cards)
        animate_card(400, 50, 250 + (len(dealer_cards) * 30), 50, f"{dealer_cards[-1]}", 0.05)

    update_display()

    # Determine results
    if user_total > 21:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"You went over! You lose!\nNew Balance: ${balance}")
    elif dealer_total > 21:
        balance += bet_amount
        messagebox.showinfo("Game Over", f"Dealer went over! You win!\nNew Balance: ${balance}")
    elif user_total == dealer_total:
        messagebox.showinfo("Game Over", "It's a draw!")
    elif user_total == 21:
        balance += int(bet_amount * 1.5)  # Blackjack pays 1.5x
        messagebox.showinfo("Game Over", f"Blackjack! You win!\nNew Balance: ${balance}")
    elif dealer_total == 21:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"Dealer has Blackjack! You lose!\nNew Balance: ${balance}")
    elif user_total > dealer_total:
        balance += bet_amount
        messagebox.showinfo("Game Over", f"Congratulations! You win!\nNew Balance: ${balance}")
    else:
        balance -= bet_amount
        messagebox.showinfo("Game Over", f"You lose!\nNew Balance: ${balance}")

    # Handle game over condition
    if balance <= 0:
        messagebox.showerror("Game Over", "You are out of money! Restart the game.")
        root.quit()

def hit():
    """Player draws a card."""
    card = deal_card()
    user_cards.append(card)
    x_position = 250 + (len(user_cards) * 30)  # Space cards apart
    animate_card(100, 200, x_position, 200, f"{card}", 0.05)
    update_display()
    if calculate_score(user_cards) > 21:
        check_result()

def stand():
    """End the player's turn and let the dealer play."""
    check_result()

def play_game():
    """Start the Blackjack round after betting."""
    global user_cards, dealer_cards
    canvas.delete("all")  # Clear old animations
    user_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card(), deal_card()]
    update_display()

    # Animate the initial cards
    animate_card(100, 200, 250, 200, f"{user_cards[0]}", 0.05)
    animate_card(100, 200, 300, 200, f"{user_cards[1]}", 0.05)
    animate_card(400, 50, 250, 50, f"{dealer_cards[0]}", 0.05)

# ----------------- GUI Variables -----------------
balance_var = tk.StringVar()
user_score = tk.StringVar()
dealer_score = tk.StringVar()
update_display()

# ----------------- GUI Elements -----------------
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

# ----------------- Start the GUI Loop -----------------
root.mainloop()
