# 🌍 NationIO

**NationIO** is a browser-based geography guessing game built with Python and Flask. Players are given up to 5 progressive hints about a mystery country — capital city, world region, population, flag, and currency — and must guess the correct country. The fewer hints used, the higher the score.

---

## 📸 Screenshots

> Start the development server and visit `http://127.0.0.1:5000` to see the game in action.

---

## 🎮 How It Works

Each game consists of **5 rounds**. In every round:

1. The player is shown the **first hint** (Capital city) for a mystery country.
2. The player can either:
   - **Submit a guess** — correct guesses are rewarded, wrong guesses are penalised.
   - **Reveal the next hint** — each additional hint costs **5 points** from the score pool.
3. After 5 rounds, the game ends and a **results screen** displays the final score alongside all correct answers, colour-coded by whether they were guessed correctly.

### Scoring

| Action | Points |
|---|---|
| Starting score | 30 |
| Guessing correctly (fewer hints used = more points) | `(6 - hints_shown) × 5` |
| Requesting an extra hint | −5 |
| Incorrect guess | −5 |

The maximum achievable score per round is **25 points** (correct guess on the first hint, no extra hints revealed).

### Hint Sequence

| # | Hint Type | Description |
|---|---|---|
| 1 | Capital | The country's capital city |
| 2 | Region | The world region (e.g. Europe, Asia) |
| 3 | Population | The country's population |
| 4 | Flag | The country's flag (displayed as an image) |
| 5 | Currencies | Currency symbol and ISO code |

---

## 🏗️ Architecture

```
nationio/
├── app.py                          # Flask application & route definitions
├── countrynames.csv                # Local dataset of ~250 country names
├── requirements.txt                # Python dependencies
│
├── services/
│   ├── game_instance_builder.py    # GameInstance class — core game state & logic
│   └── hint_bundler.py             # Async API fetching & hint assembly
│
├── utils/
│   ├── country_randomiser.py       # Random country sampling from CSV
│   ├── country_name_csv_packer.py  # One-time script to populate countrynames.csv
│   └── __init__.py
│
├── templates/
│   ├── base.html                   # Shared layout with nav and footer
│   ├── index.html                  # Home / landing page
│   ├── game.html                   # Main game view
│   └── end.html                    # End-of-game results screen
│
└── static/
    └── styles/
        └── styles.css              # Global stylesheet
```

### Key Components

#### `app.py` — Flask Router
Defines all HTTP routes and manages Flask sessions. Game state is serialised to the session via `GameInstance.to_dict()` / `GameInstance.from_dict()` on every request, ensuring stateless HTTP is handled correctly.

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/game/new` | GET | Initialises or resets a game session |
| `/game` | GET | Renders the active round |
| `/game/next-hint` | POST | Reveals the next hint, saves state |
| `/game/guess` | POST | Processes the player's guess, saves state |
| `/game/end` | GET | Renders the final results screen |

#### `services/game_instance_builder.py` — Game Logic
The `GameInstance` class is the heart of the application. It manages:
- Round progression (`rounds_played`, `init_new_round`)
- Hint visibility state (`current_hint`, `shown_hints`)
- Score calculation on correct/incorrect guesses
- Full serialisation to/from a plain dictionary for Flask session storage
- A `GameInstanceMixin` for cleanly separating `reset_game` and `new_game` logic

#### `services/hint_bundler.py` — Async API Layer
Uses `asyncio` and `aiohttp` to **concurrently fetch** hint data for all 5 countries in a single game from the [REST Countries API](https://restcountries.com/) (v4). All 5 network requests are fired in parallel via `asyncio.gather`, keeping load times low. If any country's data is incomplete, the entire batch is discarded and retried (up to 3 attempts).

#### `utils/country_randomiser.py`
Reads `countrynames.csv` and uses `random.sample` to select 5 unique countries per game, ensuring no repeats within a session.

#### `utils/country_name_csv_packer.py`
A standalone one-time script that calls the REST Countries API and writes all country common names to `countrynames.csv`. Run this to refresh the country list.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/nationio.git
   cd nationio
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS / Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Refresh the country dataset:**
   ```bash
   python utils/country_name_csv_packer.py
   ```
   This regenerates `countrynames.csv` from the REST Countries API. A pre-built CSV is already included.

5. **Run the development server:**
   ```bash
   python app.py
   ```

6. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `Flask` | Web framework and session management |
| `aiohttp` | Async HTTP client for concurrent API requests |
| `requests` | Sync HTTP client (used by the CSV packer script) |

See [`requirements.txt`](./requirements.txt) for pinned versions.

---

## 🌐 External API

NationIO fetches live hint data from the **[REST Countries API](https://restcountries.com/)** (v4).

**Endpoint used:**
```
GET https://restcountries.com/v4/name/{country}?fullText=true&fields=name,region,capital,population,flag,currencies
```

The API is free and requires no authentication. Data availability depends on REST Countries uptime; the application includes retry logic (up to 3 attempts) to handle transient failures gracefully.

---

## 🧩 Design Decisions

- **Session-based state**: Flask's signed cookie session is used to persist `GameInstance` state between requests. The game object is fully serialised to a plain dictionary on every write and deserialised on every read, making the server fully stateless between requests.
- **Async concurrency**: `aiohttp` + `asyncio.gather` fires all 5 country API requests in parallel, reducing round-start latency significantly versus sequential requests.
- **Local country CSV**: A local dataset of country names decouples country selection from the API, avoiding an extra network call just to pick which countries to use.
- **Mixin pattern**: `GameInstanceMixin` separates reset/new-game orchestration from the core `GameInstance` class, keeping responsibilities clean.

---

## 🔮 Potential Improvements

- [ ] Add difficulty levels (e.g., hard mode skips capital as a hint)
- [ ] Implement a leaderboard with persistent storage (SQLite / PostgreSQL)
- [ ] Add an autocomplete dropdown for country name input
- [ ] Support multiplayer sessions via WebSockets
- [ ] Dockerise the application for easier deployment
- [ ] Add comprehensive unit tests for `GameInstance` and `hint_bundler`

---

## 📄 Licence

This project is open source and available under the MIT Licence.

---

## 🙏 Acknowledgements

- Country data provided by [REST Countries](https://restcountries.com/)
- Built with [Flask](https://flask.palletsprojects.com/)