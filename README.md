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
| Correct guess (fewer hints = more points) | `(6 - hints_shown) × 5` |
| Requesting an extra hint | −5 |
| Incorrect guess | −5 |

The maximum achievable score per round is **25 points** (correct on the first hint).

### Hint Sequence

| # | Hint Type | Description |
|---|---|---|
| 1 | Capital | The country's capital city |
| 2 | Region | The world region (e.g. Europe, Asia) |
| 3 | Population | The country's population |
| 4 | Flag | The country's flag (displayed as an image) |
| 5 | Currencies | Currency symbol and ISO code |

### Hard Mode

Hard mode removes the Capital hint and increases internal difficulty, forcing players to rely on region, population, flag, and currency alone. It is implemented as a `HardGameInstance` subclass of `GameInstance`, following the Open/Closed principle — no core game logic was modified.

---

## 🏗️ Architecture

```
nationio/
├── app.py                          # Flask application & route definitions
├── extensions.py                   # Flask extension instances (cache)
├── countrynames.csv                # Local dataset of ~250 country names
├── requirements.txt                # Python dependencies
│
├── services/
│   ├── game_instance_builder.py    # GameInstance & HardGameInstance — game state & logic
│   └── hint_bundler.py             # Async API fetching, caching & hint assembly
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
    ├── autocomplete.json           # Pre-built country name index for autocomplete
    └── styles/
        └── styles.css              # Global stylesheet
```

### Key Components

#### `app.py` — Flask Router
Defines all HTTP routes and manages Flask sessions. Game state is serialised to the session via `GameInstance.to_dict()` / `GameInstance.from_dict()` on every request, ensuring stateless HTTP is handled correctly.

| Route | Method | Description |
|---|---|---|
| `/` | GET | Landing page |
| `/game/new` | GET | Initialises or resets a standard game session |
| `/game/new/hard` | GET | Initialises a hard mode game session |
| `/game` | GET | Renders the active round |
| `/game/next-hint` | POST | Reveals the next hint, saves state |
| `/game/guess` | POST | Processes the player's guess, saves state |
| `/game/end` | GET | Renders the final results screen |

#### `services/game_instance_builder.py` — Game Logic

The game logic is structured across three classes:

- **`GameInstanceMixin`** — handles `reset_game` and `new_game` orchestration, keeping lifecycle logic separate from state
- **`GameInstance`** — core game state, round progression, hint visibility, score calculation, and full dict serialisation for Flask session storage. Accepts injected `country_source` and `hint_bundler` dependencies for testability
- **`HardGameInstance(GameInstance)`** — subclass that overrides `DEFAULT_HINT_NAMES` and `DEFAULT_DIFFICULTY` to configure hard mode without modifying the base class

#### `services/hint_bundler.py` — Async API Layer with Caching

Uses `asyncio` and `aiohttp` to **concurrently fetch** hint data for all 5 countries via `asyncio.gather`. Per-country responses are cached using **Flask-Caching** (`SimpleCache`) with a 24-hour TTL, reducing repeat game load times from ~14s to ~0.3s. A 5-second per-request timeout prevents slow upstream responses from hanging the game. If any country's data is incomplete, the batch is discarded and retried up to 3 times.

#### `utils/country_randomiser.py`
Reads `countrynames.csv` and uses `random.sample` to select 5 unique countries per game.

#### `static/autocomplete.json`
A pre-indexed JSON file mapping first letters to country names, used to power the guess input's autocomplete dropdown client-side without any additional API calls.

---

## ⚡ Performance

| Metric | Before | After |
|---|---|---|
| New game load time | ~14s | ~0.3s |

Achieved by:
- Parallelising all 5 country API requests with `asyncio.gather`
- Caching per-country API responses with Flask-Caching (24hr TTL)
- Adding per-request timeouts via `aiohttp.ClientTimeout`

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
| `Flask-Caching` | Server-side response caching |
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

The API is free and requires no authentication. Responses are cached per-country for 24 hours. The application includes retry logic (up to 3 attempts) to handle transient failures gracefully.

---

## 🧩 Design Decisions

- **Session-based state**: Flask's signed cookie session persists `GameInstance` state between requests. The game object is fully serialised to a plain dictionary on every write and deserialised on every read, keeping the server stateless.
- **Dependency injection**: `GameInstance` accepts `country_source` and `hint_bundler` as constructor arguments, decoupling it from concrete implementations and making it straightforward to test with mocks.
- **Subclass-based difficulty**: `HardGameInstance` overrides class-level defaults (`DEFAULT_HINT_NAMES`, `DEFAULT_DIFFICULTY`) rather than branching inside `GameInstance`, following the Open/Closed principle.
- **Async concurrency + caching**: `aiohttp` + `asyncio.gather` fires all 5 country API requests in parallel. Flask-Caching stores results per country, so repeat games are served from cache with no network overhead.
- **Client-side autocomplete**: Country name suggestions are served from a static pre-indexed JSON file, avoiding any server round-trip on keypress.
- **Local country CSV**: A local dataset decouples country selection from the API, avoiding an extra network call just to pick which countries to use.

---

## 🔮 Potential Improvements

- [ ] Leaderboard with persistent storage (SQLite / PostgreSQL)
- [ ] Multiplayer sessions via WebSockets
- [ ] Dockerise the application for easier deployment
- [ ] Unit tests for `GameInstance` and `hint_bundler`
- [x] Hard mode (reduced hint set, increased difficulty)
- [x] Autocomplete dropdown for country name input
- [x] API response caching to minimise latency

---

## 📄 Licence

This project is open source and available under the MIT Licence.

---

## 🙏 Acknowledgements

- Country data provided by [REST Countries](https://restcountries.com/)
- Built with [Flask](https://flask.palletsprojects.com/)