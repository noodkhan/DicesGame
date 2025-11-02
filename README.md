🎲 Dice Game Simulation — Python Monte Carlo Dice Strategy Analyzer
🧠 Overview

This project simulates a probabilistic dice betting game where a player starts with a fixed balance and competes against a broker.
The game includes multiple betting strategies (HIGH, LOW, EXACT, DIE HIGH/LOW, and PATTERN), each with distinct rules and reward multipliers.

It visualizes game dynamics through real-time and summary plots, helping analyze:

Player vs Broker balance trends

Choice-specific win rates

Losing streak probability distributions

🕹️ Game Rules
Starting Balance:

Player starts with $3500 and bets $100 per round.

Dice Roll:

Three dice are rolled per round (values 1–6), simulated using a normal distribution for realistic variation.

Player Choices:

HIGH → Guess the total will be high.

LOW → Guess the total will be low.

EXACT → Guess the exact total of the three dice.

DIE HIGH / DIE LOW → Predict an individual die’s range.

PATTERN → Predict repeating or unique number patterns (e.g., all dice the same).

Winning Rules:
Choice	Description	Reward
HIGH	If guessed total matches a new 3-dice roll (up to 3 tries)	3× bet
LOW	If guessed total (from 2 dice) matches new 3-dice roll (up to 2 tries)	4× bet
EXACT	If guessed total matches current 3-dice roll	5× bet
DIE HIGH / DIE LOW	Predicts one die value range	2× bet
PATTERN	If all dice have the same value	3× bet

Losing Condition: You lose your bet amount (broker gains it).
Reset: Game restarts if your balance ≤ $0.

📊 Features

Monte Carlo–style simulation of thousands of rounds

Weighted AI decision-making (adjustable strategy bias)

Detailed tracking of win rates, streaks, and total earnings

Matplotlib visualizations for:

Player vs Broker balance

Cumulative win rates per choice

Losing streak distribution

🧩 Example Output

Console summary:

📊 ====== SIMULATION SUMMARY ======
Total rounds simulated: 10000
Total games (resets) played: 2
Overall win rate: 46.72%
Avg broker gain per game: $128.43

-- Choice-Specific Performance --
  HIGH (1634 attempts): Win Rate = 45.12%
  LOW (1663 attempts): Win Rate = 47.33%
  EXACT (1680 attempts): Win Rate = 12.45%
  DIE_HIGH (1684 attempts): Win Rate = 50.12%
  DIE_LOW (1677 attempts): Win Rate = 49.73%
  PATTERN (1662 attempts): Win Rate = 3.91%


Plots generated:

📈 Player vs Broker balance over time

🧮 Cumulative win rate per choice

📉 Distribution of losing streaks

⚙️ Installation
git clone https://github.com/yourusername/dice-game-simulation.git
cd dice-game-simulation
pip install matplotlib
python dice_game.py

🧠 Future Improvements

Implement Q-learning to make the AI smarter per round.

Add configurable betting strategy weights.

Export statistics to CSV/JSON for deeper analysis.

🏁 License

MIT License © 2025 — feel free to use, modify, and experiment.
