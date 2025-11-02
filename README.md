
  <section>
    <h2>Overview</h2>
    <p>This repository contains a flexible Python simulation of a dice betting game. It runs Monte Carlo-style experiments to analyze betting choices (HIGH, LOW, EXACT, single-die bets and pattern bets). The project produces summary statistics and Matplotlib visualizations to help understand house edge, win rates and streak behavior.</p>
  </section>

  <section>
    <h2>Game Rules (short)</h2>
    <ul>
      <li><strong>Starting Balance:</strong> Player starts with <code>$3500</code> and bets <code>$100</code> per round.</li>
      <li><strong>Dice Roll:</strong> 3 dice are rolled each round (values 1–6, simulated using a normal approximation).</li>
      <li><strong>Player Choices:</strong> HIGH, LOW, EXACT, DIE_HIGH, DIE_LOW, PATTERN.</li>
      <li><strong>Winning:</strong>
        <ul>
          <li><strong>HIGH</strong>: guessed total matches a <em>new</em> 3-dice roll (up to 3 tries) → payout multiplier (configurable).</li>
          <li><strong>LOW</strong>: guessed total from 2 dice matches a new 3-dice roll (up to 2 tries) → payout multiplier.</li>
          <li><strong>EXACT</strong>: guessed total matches the <em>current</em> roll → higher multiplier.</li>
          <li><strong>DIE_HIGH / DIE_LOW</strong>: predict a single die range → lower multiplier.</li>
          <li><strong>PATTERN</strong>: predict pattern like all same / pair → configurable multiplier.</li>
        </ul>
      </li>
      <li><strong>Losing:</strong> player loses their bet; broker gains it.</li>
      <li><strong>Reset:</strong> game restarts when balance ≤ $0.</li>
    </ul>
  </section>

  <section>
    <h2>Features</h2>
    <ul>
      <li>Monte Carlo simulation of thousands of rounds</li>
      <li>Multiple betting options & configurable multipliers</li>
      <li>Choice-level statistics (attempts, wins, empirical win rates)</li>
      <li>Balance tracking for player and broker</li>
      <li>Matplotlib visualizations: balance over time, win-rate curves, losing-streak distribution</li>
      <li>Easy to extend: add new bet types, add learning agents (Q-learning) or change weights</li>
    </ul>
  </section>

  <section>
    <h2>Quick Start</h2>
    <p class="muted">Clone, install dependencies and run the simulation script.</p>
cd dice-game-simulation
pip install -r requirements.txt   # or pip install matplotlib
python dice_game.py</code></pre>
    <p>Run with <code>live_plot=True</code> to see an animated balance plot during simulation.</p>
  </section>

  <section>
    <h2>Example Output (console)</h2>
    <pre><code>📊 ====== SIMULATION SUMMARY ======
Total rounds simulated: 10000
Total games (resets) played: 1
Overall win rate: 47.23%
Avg broker gain per game: $142.37

-- Choice-Specific Performance --
  HIGH (1600 attempts): Win Rate = 44.80%
  LOW (1700 attempts): Win Rate = 48.20%
  EXACT (1650 attempts): Win Rate = 10.30%
  DIE_HIGH (1675 attempts): Win Rate = 49.10%
  DIE_LOW (1675 attempts): Win Rate = 49.90%
  PATTERN (1700 attempts): Win Rate = 3.10%</code></pre>
    <p class="muted">Plots are generated for balances, win-rates and losing streaks.</p>
  </section>

  <section>
    <h2>Extending & AI</h2>
    <p>This codebase is intentionally modular so you can:</p>
    <ul>
      <li>Add a Q-learning agent to replace the random/weighted <code>smart_choice()</code>.</li>
      <li>Change multipliers and bet rules to model alternative casino variants.</li>
      <li>Export results to CSV/JSON for further analysis or build training datasets for ML models.</li>
    </ul>
    <p class="muted">Example: implement a simple Q-learning update after each round:</p>
    <pre><code># pseudocode
Q = {choice: 0.0 for choice in Choice}
choice = smart_choice_ai(Q, epsilon=0.2)
reward = compute_reward(choice, win, bet_amount)
Q[choice] += learning_rate * (reward - Q[choice])</code></pre>
  </section>

  <section>
    <h2>Project Structure (suggested)</h2>
    <table>
      <thead><tr><th>File</th><th>Purpose</th></tr></thead>
      <tbody>
        <tr><td><code>dice_game.py</code></td><td>Main simulation and plotting</td></tr>
        <tr><td><code>agents.py</code></td><td>Optional AI agents (Q-learning, policies)</td></tr>
        <tr><td><code>config.py</code></td><td>Constants and multipliers</td></tr>
        <tr><td><code>results/</code></td><td>Saved CSV/JSON outputs and plots</td></tr>
      </tbody>
    </table>
  </section>

  <section>
    <h2>License</h2>
    <p>MIT © <span id="year"></span> — free to use, modify and experiment.</p>
  </section>

<image src="https://images.unsplash.com/photo-1453733190371-0a9bedd82893?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=1974"></image>
  
