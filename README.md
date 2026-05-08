# 🌍 NationIO

**NationIO** is a browser-based geography guessing game built with Python and Flask. Players are given up to 5 progressive hints about a mystery country — capital city, world region, population, flag, and currency — and must guess the correct country. The fewer hints used, the higher the score.

---

## 📸 Screenshots

> Start the development server and visit `http://127.0.0.1:5000` to see the game in action.

---

## 🎮 How It Works

Each game consists of **5 rounds**. In every round:

1. The player is shown the **first hint** for a mystery country.
2. The player can either:
   - **Submit a guess** — correct guesses are rewarded, wrong guesses are penalised.
   - **Reveal the next hint** — each additional hint costs **5 points** from the score pool.
3. After 5 rounds, the game ends and a **results screen** displays the final score alongside all correct answers, colour-coded by whether they were guessed correctly.

### Scoring (Non Timed Modes)

| Action | Points |
|---|---|
| Starting score | 30 |
| Correct guess (fewer hints = more points) | `(6 - hints_shown) × 5` |
| Requesting an extra hint | −5 |
| Incorrect guess | −5 |

The maximum achievable score per round is **25 points** (correct on the first hint).

### Scoring (Timed Mode)

| Action | Points |
|---|---|
| Starting score | 30 |
| Correct guess (fewer hints = more points) | `(6 - hints_shown) × 5 × (time_remaining / 60)` |
| Requesting an extra hint | −5 |
| Incorrect guess | −5 |

### Hint Sequence

| # | Hint Type | Description |
|---|---|---|
| 1 | Capital | The country's capital city |
| 2 | Region | The world region (e.g. Europe, Asia) |
| 3 | Population | The country's population |
| 4 | Flag | The country's flag (displayed as an image) |
| 5 | Currencies | Currency symbol and ISO code |

---

## 🕹️ Game Modes

### Standard
The full 5-hint experience. Capital city is the opening hint.

### Hard Mode
Removes the Capital hint, forcing players to rely on region, population, flag, and currency alone. Implemented as a `HardGameInstance` subclass — no core game logic was modified.

### Timed Mode
Standard hint set with a 60-second countdown per round. Score is multiplied by time remaining, rewarding fast, confident guesses.

---

## 🏗️ Architecture

```
nationio/
├── app.py                           # Flask application & route definitions
├── requirements.txt                 # Python dependencies
│
├── services/
│   ├── game_instance_builder.py     # GameInstance, HardGameInstance, TimedGameInstance
│   └── hint_bundler.py              # Async API fetching, retry logic, caching & hint assembly
│
├── utils/
│   ├── country_randomiser.py        # Random ISO code sampling
│   ├── country_name_csv_packer.py   # One-time script to populate countrycodes.csv
│   ├── autocomplete_dict_packer.py  # One-time script to populate autocomplete.json
│   ├── extensions.py                # Flask extension instances (cache)
│   └── __init__.py
│
├── templates/
│   ├── base.html                    # Shared layout with nav and footer
│   ├── index.html                   # Home / landing page
│   ├── game.html                    # Main game view
│   └── end.html                     # End-of-game results screen
│
└── static/
    ├── scripts/
    │   └── autocomplete.js          # Client-side autocomplete logic
    ├── autocomplete.json            # Pre-built country name index for autocomplete
    └── styles/
        └── styles.css               # Global stylesheet
```

### Key Components

#### `app.py` — Flask Router
Defines all HTTP routes and manages Flask sessions. Game state is serialised to the session via `GameInstance.to_dict()` / `GameInstance.from_dict()` on every request, ensuring the server remains fully stateless between requests.

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/game/new` | GET | Initialises a standard game session |
| `/game/new/hard` | GET | Initialises a hard mode game session |
| `/game/new/timed_normal` | GET | Initialises a timed game session |
| `/game` | GET | Renders the active round |
| `/game/next-hint` | POST | Reveals the next hint, saves state |
| `/game/guess` | POST | Processes the player's guess, saves state |
| `/game/end` | GET | Renders the final results screen |

#### `services/game_instance_builder.py` — Game Logic

Game logic is structured across four classes:

- **`GameInstanceMixin`** — handles `reset_game`, `new_game`, and `stash_timer` orchestration, keeping lifecycle logic separate from state
- **`GameInstance`** — core game state, round progression, hint visibility, score calculation, and full dict serialisation for Flask session storage. Accepts an injected `json_bundler` dependency for testability
- **`HardGameInstance(GameInstance)`** — overrides `DEFAULT_HINT_NAMES` and `DEFAULT_DIFFICULTY` to remove the capital hint without modifying the base class
- **`TimedGameInstance(GameInstance)`** — adds a 60-second per-round timer and overrides `guess()` to factor time remaining into the score calculation

#### `services/hint_bundler.py` — Async API Layer with Smart Retry

Uses `asyncio` and `aiohttp` to **concurrently fetch** hint data for all 5 countries via `asyncio.gather`. Countries are looked up by **ISO cca2 code** for reliable API resolution, with common names returned separately for answer validation and display.

The retry logic is optimised — rather than discarding the entire batch on partial failure, only the failed lookups are replaced and re-fetched, keeping successful results and minimising redundant API calls.

Per-country responses are cached using **Flask-Caching** (`SimpleCache`) with a 24-hour TTL, reducing repeat game load times from ~14s to ~0.3s. A 2-second per-request timeout prevents slow upstream responses from hanging the game.

#### `utils/country_randomiser.py`
Reads `countrycodes.csv` and uses `random.sample` to select 5 unique ISO codes per game, decoupling country selection from the API entirely.

#### `static/autocomplete.json`
A pre-indexed JSON file mapping first letters to country names, powering the guess input's autocomplete dropdown client-side with no server round-trip on keypress.

---

## ⚡ Performance

| Metric | Before | After |
|---|---|---|
| New game load time | ~14s | ~0.3s |

Achieved by:
- Parallelising all country API requests with `asyncio.gather`
- Switching from name-based to ISO code lookups for reliable API resolution
- Caching per-country API responses with Flask-Caching (24hr TTL)
- Optimised retry logic — only failed fetches are replaced, not the full batch
- Per-request timeouts via `aiohttp.ClientTimeout`

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Ljkkj7/nationio.git
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
   This regenerates `countrycodes.csv` from the REST Countries API. A pre-built CSV is already included.

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
| `Flask-Caching` | Server-side response caching |
| `aiohttp` | Async HTTP client for concurrent API requests |
| `requests` | Sync HTTP client (used by utility scripts) |

See [`requirements.txt`](./requirements.txt) for pinned versions.

---

## 🌐 External API

NationIO fetches live hint data from the **[REST Countries API](https://restcountries.com/)** (v4).

**Endpoint used:**
```
GET https://restcountries.com/v4/alpha?codes={cca2}&fields=name,region,capital,population,flag,currencies
```

The API is free and requires no authentication. Responses are cached per-country for 24 hours. Partial batch failures trigger targeted retries — only failed country lookups are replaced and re-fetched, up to 3 attempts total.

---

## 🧩 Design Decisions

- **Session-based state**: Flask's signed cookie session persists `GameInstance` state between requests. The game object is fully serialised to a plain dictionary on every write and deserialised on every read, keeping the server stateless.
- **Dependency injection**: `GameInstance` accepts `json_bundler` as a constructor argument, decoupling it from the concrete implementation and making it straightforward to test with mocks.
- **Subclass-based difficulty**: `HardGameInstance` and `TimedGameInstance` override class-level defaults rather than introducing conditionals inside `GameInstance`, following the Open/Closed principle.
- **ISO code lookup**: Countries are selected and fetched by ISO cca2 code rather than name, eliminating encoding issues with special characters and improving API reliability.
- **Smart retry logic**: Failed fetches in a batch are replaced individually rather than discarding the entire batch, reducing unnecessary API calls on retry.
- **Async concurrency + caching**: `aiohttp` + `asyncio.gather` fires all country API requests in parallel. Flask-Caching stores results per country, so repeat games are served from cache instantly.
- **Client-side autocomplete**: Country name suggestions are served from a static pre-indexed JSON file, avoiding any server round-trip on keypress.

---

## 🔮 Potential Improvements

- [ ] Leaderboard with persistent storage (SQLite / PostgreSQL)
- [ ] Multiplayer sessions via WebSockets
- [ ] Dockerise the application for easier deployment
- [ ] Unit tests for `GameInstance` and `hint_bundler`
- [x] Hard mode (reduced hint set, increased difficulty)
- [x] Timed mode (60-second countdown with time-weighted scoring)
- [x] Autocomplete dropdown for country name input
- [x] API response caching to minimise latency
- [x] ISO code-based lookup for reliable API resolution
- [x] Optimised partial-batch retry logic

---

## 📄 Licence

This project is open source and available under the MIT Licence.

---

## 🙏 Acknowledgements

- Country data provided by [REST Countries](https://restcountries.com/)
- Built with [Flask](https://flask.palletsprojects.com/)