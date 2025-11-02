# Dice Game Rules

# **Starting Balance:**  
# Player starts with $3500 and bets $100 per round.

# **Dice Roll:**  
# Three dice are rolled each round (values 1–6, simulated with normal distribution).

# **Player Choices:**  
# The player chooses one of three options:  

# - **HIGH**: Guess the total sum will be high.  
# - **LOW**: Guess the total sum will be low.  
# - **EXACT**: Guess the exact total sum of the dice.

# **Winning Rules:**  
# - **HIGH**: If your guessed total matches a new 3-dice roll (up to 3 tries), you win 3× your bet.  
# - **LOW**: If your guessed total (from 2 dice) matches a new 3-dice roll (up to 2 tries), you win 4× your bet.  
# - **EXACT**: If your guessed total matches the current 3-dice roll, you win 5× your bet.

# **Losing:**  
# You lose your bet amount; broker gains it.

# **Game Reset:**  
# The game resets if your balance reaches $0 or less.


import random
import matplotlib.pyplot as plt
from enum import Enum
# import math # Not needed for this code

# --- Constants ---
STARTING_BALANCE = 10000
DEFAULT_BET = 100
TOTAL_ROUNDS = 10000
NORMAL_MEAN = 3.5
NORMAL_STDDEV = 1.2

# --- Choice Definition ---
class Choice(Enum):
    HIGH = '1'
    LOW = '2'
    EXACT = '3'
    DIE_HIGH = '4'
    DIE_LOW = '5'
    PATTERN = '6'

# --- Core Game Functions ---

def roll_dice_normal(mean=NORMAL_MEAN, stddev=NORMAL_STDDEV, num_dice=3):
    """Simulate a dice roll using a normal distribution (approximation)."""
    dice = []
    for _ in range(num_dice):
        # Generate a normal deviate and round to the nearest integer
        roll = int(round(random.gauss(mean, stddev)))
        # Clamp the result to be between 1 and 6
        roll = max(1, min(6, roll))
        dice.append(roll)
    return dice

def smart_choice():
    """Weighted AI choice: favor HIGH (45%), LOW (35%), EXACT (20%)."""
    return random.choices(
        [Choice.PATTERN , Choice.HIGH, Choice.LOW, Choice.EXACT, Choice.DIE_HIGH , Choice.DIE_LOW], 
        weights= [0.16, 0.16, 0.16, 0.16, 0.16, 0.16],
        k=1
    )[0]

def determine_win(choice, dice_result):
    """
    Apply the complex winning logic based on the original code's implementation.
    The logic for HIGH and LOW is corrected to consistently use sum comparison,
    based on the apparent pattern in the user's code.
    """
    total = sum(dice_result)
    win = False
    bet_multiplier = 1

    if choice == Choice.HIGH:
        # Original logic: guess total, then check if that guess total matches
        # the sum of a NEW 3-dice roll up to 3 times.
        guess = sum(roll_dice_normal())
        for _ in range(3):
            if guess == sum(roll_dice_normal()):
                win = True
                bet_multiplier = 2
                break
    
    elif choice == Choice.LOW:

        # Original intent was confusing. Corrected to:
        # 1. Guess total of 2 dice.
        # 2. Check if that 2-dice guess total matches the sum of a NEW 3-dice roll up to 2 times.

        guess_rolls = roll_dice_normal()
        guess_rolls.pop() # Only 2 dice for the guess total
        guess = sum(guess_rolls)
        
        for _ in range(2):
            if guess == sum(roll_dice_normal()):
                win = True
                bet_multiplier = 3
                break

    elif choice == Choice.DIE_HIGH:
        # Pick first die as example
        if dice_result[0] >= 5:
            win = True
            bet_multiplier = 2

    elif choice == Choice.DIE_LOW:
        if dice_result[0] <= 2:
            win = True
            bet_multiplier = 2

    elif choice == Choice.PATTERN:
        if len(set(dice_result)) == 1:  # Example: all same
            win = True
            bet_multiplier = 3

    elif choice == Choice.EXACT:
        # Standard logic: guess total of 3 dice, check if it matches the current dice_result total.
        guess = sum(roll_dice_normal())
        if guess == total:
            win = True
            bet_multiplier = 5

    return win, bet_multiplier

# --- Game Simulation (Modified for Choice Tracking) ---

def play_auto_game(total_rounds=TOTAL_ROUNDS, bet_amount=DEFAULT_BET, live_plot=False, delay=0.01):
    """
    Simulate the auto-dice game and track the empirical win rate per choice per round.
    """
    balance = STARTING_BALANCE
    broker = STARTING_BALANCE
    game_number = 1

    # Statistics Tracking
    balances = [balance]
    broker_balances = [broker]
    losing_streaks = []
    current_streak = 0
    total_win = 0
    total_lose = 0
    total_win_amount = 0
    total_lose_amount = 0
    
    # NEW: Choice-specific tracking
    choice_stats = {
        Choice.HIGH: {'wins': 0, 'attempts': 0, 'win_rates': []},
        Choice.LOW: {'wins': 0, 'attempts': 0, 'win_rates': []},
        Choice.EXACT: {'wins': 0, 'attempts': 0, 'win_rates': []},
        Choice.DIE_HIGH: {'wins': 0, 'attempts': 0, 'win_rates': []},
        Choice.DIE_LOW: {'wins': 0, 'attempts': 0, 'win_rates': []},
        Choice.PATTERN: {'wins': 0, 'attempts': 0, 'win_rates': []} 
    }

    if live_plot:
        plt.ion()
        fig, ax = plt.subplots(figsize=(10,5))
        print(f"\n🚀 Starting live simulation for {total_rounds} rounds...")

    for round_num in range(1, total_rounds + 1):
        choice = smart_choice()
        dice_result = roll_dice_normal()
        win, bet_multiplier = determine_win(choice, dice_result)
        bet = bet_amount * bet_multiplier
        
        # Update choice-specific attempts
        choice_stats[choice]['attempts'] += 1

        if win:
            broker -= bet
            balance += bet
            total_win += 1
            total_win_amount += bet
            
            choice_stats[choice]['wins'] += 1 # Update choice-specific wins
            
            if current_streak > 0:
                losing_streaks.append(current_streak)
            current_streak = 0
        else:
            broker += bet_amount 
            balance -= bet_amount 
            total_lose += 1
            total_lose_amount += bet_amount
            current_streak += 1

        balances.append(balance)
        broker_balances.append(broker)
        
        # Calculate and store cumulative win rates for ALL choices
        for c in choice_stats.keys():
            stats = choice_stats[c]
            # Avoid division by zero
            # We must pad the win_rates list to be the same length as the simulation
            # The rate is calculated based on the total rounds *up to this point*.
            current_rate = (stats['wins'] / stats['attempts']) * 100 if stats['attempts'] > 0 else 0
            
            # Find the last calculated rate for the current choice
            last_rate = choice_stats[c]['win_rates'][-1] if choice_stats[c]['win_rates'] and len(choice_stats[c]['win_rates']) == round_num - 1 else 0
            
            # If the current choice was selected this round, update the rate.
            # If not selected, append the previous round's rate to keep the lists aligned with round_num.
            if c == choice:
                 choice_stats[c]['win_rates'].append(current_rate)
            else:
                # If this choice wasn't made, use its previous rate for the plot alignment
                choice_stats[c]['win_rates'].append(last_rate if last_rate != 0 else current_rate)


        # Live plot update
        if live_plot and round_num % 10 == 0:
            ax.clear()
            ax.plot(balances, color='blue', label='Player')
            ax.plot(broker_balances, color='red', label='Broker')
            ax.legend()
            ax.set_title(f"🎲 Balance Over Time — Round {round_num}")
            ax.set_xlabel("Rounds")
            ax.set_ylabel("Balance")
            ax.grid(True)
            plt.pause(delay)

        # Reset game if player bankrupt
        if balance <= 0:
            print(f"💀 Player bankrupt at round {round_num}. Starting **Game {game_number + 1}**...")
            balance = STARTING_BALANCE
            balances.append(balance)
            broker_balances.append(broker)
            game_number += 1
    
    if live_plot:
        plt.ioff()
        plt.close(fig)

    # Record last streak if the game ended with losses
    if current_streak > 0:
        losing_streaks.append(current_streak)

    # Return data for plotting and summary
    return (balances, broker_balances, losing_streaks, total_win, total_lose, 
            total_win_amount, total_lose_amount, game_number, choice_stats)

# --- Reporting and Plotting ---

def generate_report_and_plots(data):
    """Calculates statistics and generates the final plots."""
    (balances, broker_balances, losing_streaks, total_win, total_lose, 
     total_win_amount, total_lose_amount, game_number, choice_stats) = data

    total_rounds_played = total_win + total_lose
    
    # Avoid division by zero
    win_rate = (total_win / total_rounds_played) * 100 if total_rounds_played else 0
    avg_win_amount = total_win_amount / total_win if total_win else 0
    avg_lose_amount = total_lose_amount / total_lose if total_lose else 0
    avg_broker_gain_per_game = (total_lose_amount - total_win_amount) / game_number if game_number else 0
    avg_losing_streak = sum(losing_streaks) / len(losing_streaks) if losing_streaks else 0

    # --- Print Summary ---
    print("\n📊 ====== SIMULATION SUMMARY ======")
    print(f"Total rounds simulated: **{total_rounds_played}**")
    print(f"Total games (resets) played: **{game_number}**")
    print(f"Overall win rate: **{win_rate:.2f}%**")
    print(f"**Avg broker gain per game**: ${avg_broker_gain_per_game:.2f}")
    print("\n-- Choice-Specific Performance --")
    for choice, stats in choice_stats.items():
        # Get the final rate from the last element of the list
        final_rate = stats['win_rates'][-1] if stats['win_rates'] else 0
        print(f"  {choice.name} ({stats['attempts']} attempts): Win Rate = **{final_rate:.2f}%**")
    print("==================================\n")

    # --- Plot 1: Balances ---
    plt.figure(figsize=(12, 6))
    plt.plot(balances, color='blue', label='Player Balance')
    plt.plot(broker_balances, color='red', label='Broker Balance')
    plt.title("Player and Broker Balance Over Time (Total Simulation)")
    plt.xlabel("Rounds")
    plt.ylabel("Balance ($)")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # --- Plot 2: Choice Win Rates ---
    plt.figure(figsize=(12, 6))
    max_rounds = len(balances) - 1 # Use the number of rounds actually played
    rounds_axis = list(range(1, max_rounds + 1))
    
    for choice, stats in choice_stats.items():
        # Only plot the rate for rounds actually played/tracked
        if stats['attempts'] > 0:
            # We must use the minimum length between rounds_axis and win_rates
            plot_len = min(len(rounds_axis), len(stats['win_rates']))
            plt.plot(rounds_axis[:plot_len], stats['win_rates'][:plot_len], label=f'{choice.name} Win Rate ({choice_stats[choice]["attempts"]} attempts)')
    
    plt.title("Cumulative Empirical Win Rate per Choice")
    plt.xlabel("Rounds")
    plt.ylabel("Cumulative Win Rate (%)")
    plt.axhline(y=50, color='gray', linestyle='--', linewidth=0.8, label='50% Line')
    plt.legend()
    plt.grid(True)
    plt.show()

    # --- Plot 3: Losing Streaks ---
    if losing_streaks:
        plt.figure(figsize=(8, 5))
        bins = range(1, max(losing_streaks) + 2)
        plt.hist(losing_streaks, bins=bins, align='left', density=True, alpha=0.7, color='purple', edgecolor='black')
        plt.title("Distribution of Losing Streak Lengths")
        plt.xlabel("Consecutive Losses")
        plt.ylabel("Probability")
        plt.xticks(range(1, max(losing_streaks) + 1))
        plt.grid(axis='y', alpha=0.5)
        plt.show()
    else:
        print("🎉 No losing streaks recorded! (Highly unlikely for this game)")

# --- Execution ---

if __name__ == "__main__":
    # Set 'live_plot=True' if you want the slow, real-time graph
    simulation_data = play_auto_game(total_rounds=TOTAL_ROUNDS, live_plot=True) 
    generate_report_and_plots(simulation_data)