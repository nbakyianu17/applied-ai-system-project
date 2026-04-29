# VibeFinder — AI Music Recommender

> A content-based music recommendation system that scores songs against a user's taste profile using weighted feature matching and AI-generated explanations.

---

## What It Does and Why It Matters

VibeFinder takes a user's musical preferences — genre, mood, energy level, tempo, and more — and returns a ranked list of the best-matching songs from a catalog, along with a plain-language explanation of why each song was recommended.

Most recommendation systems are black boxes. You get a playlist and no reason why. VibeFinder inverts that: every recommendation includes a feature-by-feature breakdown showing exactly how it scored, making the system transparent and auditable. That kind of explainability matters — in music it's a convenience, but in higher-stakes AI systems (hiring, lending, healthcare) it's essential.

---

## Original Project (Module 3)

This project started as a **Module 3 simulation exercise**: build a content-based music recommender from scratch using only Python and a hand-crafted CSV catalog. The original goal was to understand how recommendation algorithms turn structured data into ranked predictions — no libraries, no machine learning, just a scoring formula and a sorted list. That version had six hardcoded user profiles and produced terminal output showing ranked results with feature-by-feature score breakdowns.

This Module 4 version upgrades that foundation by adding an AI layer (Claude API) for natural language preference input and explanation generation, a session logger, and a structured reliability test suite — turning a classroom exercise into something closer to a real portfolio project.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                        USER                              │
│      Natural language input or structured profile       │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
          ┌─────────────────────────┐
          │  Claude API             │
          │  Preference Extractor   │  Parses free text →
          │                         │  structured prefs dict
          └─────────────┬───────────┘
                        │  genre · mood · energy · tempo · ...
                        ▼
    ┌───────────────────────────────────────┐
    │         Recommender Engine            │
    │  src/recommender.py                   │
    │  score_song() × N songs               │
    │  Weighted proximity across 9 features │
    └──────────────┬────────────────────────┘
                   │          ▲
                   │          │
                   │    data/songs.csv
                   │    (20 songs, 13 features each)
                   │
          ┌────────┴────────┐
          │  Ranked Results  │  Top-K songs with scores (0–7.0)
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────────────┐
          │  Claude API             │
          │  Explanation Generator  │  Scores → plain-English
          └─────────────┬───────────┘  justification
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
  ┌─────────────────┐     ┌───────────────────────┐
  │  Output to User  │     │  Logger               │
  │  Songs + reasons │     │  logs/session.log     │
  └─────────────────┘     └──────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         ▼                          ▼
              ┌────────────────────┐    ┌───────────────────┐
              │  Reliability Tests  │    │  Human Review     │
              │  5 preset scenarios │    │  Spot-check AI    │
              │  auto-graded        │    │  explanations     │
              └────────────────────┘    └───────────────────┘
```

Full diagram with component table: [assets/architecture.md](assets/architecture.md)

**Three data flows:**
1. **Happy path** — user input → Claude extracts prefs → engine scores songs → Claude explains results → user sees ranked output
2. **Observability** — every session is written to `logs/session.log` with timestamp, query, and top results
3. **Reliability loop** — test suite runs 5 preset profiles through the engine and auto-grades whether the expected genre/mood appears in the top result

---

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- An Anthropic API key (for the Claude-powered input and explanation features)

### Step 1 — Clone and enter the repo

```bash
git clone https://github.com/na959/applied-ai-system-project.git
cd applied-ai-system-project
```

### Step 2 — Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Mac / Linux
.venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set your API key

```bash
export ANTHROPIC_API_KEY=your_key_here    # Mac / Linux
set ANTHROPIC_API_KEY=your_key_here       # Windows
```

### Step 5 — Run the recommender

```bash
python -m src.main
```

### Running tests

```bash
pytest
```

---

## Sample Interactions

### Example 1 — Chill Study Session (Lofi Profile)

**User preference input:**
```
genre: lofi  |  mood: focused  |  energy target: 0.40  |  tempo: 80 BPM
acousticness: 0.70  |  instrumentalness: 0.75
```

**Top result:**
```
══════════════════════════════════════════════════════════════
  📚  Profile 2 — Chill Lofi (Study Session)
  Genre: lofi  |  Mood: focused
══════════════════════════════════════════════════════════════

  #1  Focus Flow  —  LoRoom
       [████████████████████░░░░]  6.91/7.0  (99%)
       lofi · focused · energy=0.40 · bpm=80
       Reasons:
         • genre match (lofi): +2.0
         • mood match (focused): +1.0
         • energy proximity: +1.00 (target=0.40, song=0.40)
         • instrumentalness proximity: +0.73 (target=0.75, song=0.80)
         • acousticness proximity: +0.46 (target=0.70, song=0.78)
```

**AI explanation (Claude):**
> "Focus Flow is a near-perfect match for a study session. It hits your genre and mood exactly, its energy sits right where you need it for sustained focus, and it's almost entirely instrumental — no vocals to break your concentration."

---

### Example 2 — High-Energy Pop

**User preference input:**
```
genre: pop  |  mood: happy  |  energy target: 0.90  |  tempo: 128 BPM
valence: 0.85  |  bass_level: 0.75
```

**Top result:**
```
══════════════════════════════════════════════════════════════
  🎵  Profile 1 — High-Energy Pop
  Genre: pop  |  Mood: happy
══════════════════════════════════════════════════════════════

  #1  Sunrise City  —  Neon Echo
       [███████████████████░░░░░]  5.97/7.0  (85%)
       pop · happy · energy=0.82 · bpm=118
       Reasons:
         • genre match (pop): +2.0
         • mood match (happy): +1.0
         • energy proximity: +0.92 (target=0.90, song=0.82)
         • valence proximity: +0.74 (target=0.85, song=0.84)
```

**AI explanation (Claude):**
> "Sunrise City matches your genre and mood precisely, and its energy and brightness are close to your targets. It's slightly below your ideal BPM (118 vs 128) but the overall vibe is consistent with what you described."

---

### Example 3 — Edge Case: Genre Orphan (Classical Fan)

**User preference input:**
```
genre: classical  |  mood: peaceful  |  energy target: 0.22  |  tempo: 60 BPM
acousticness: 0.95  |  instrumentalness: 0.95
```

**Result showing catalog scarcity:**
```
  #1  Morning Sonata  —  Clara Voss     6.96/7.0  (100%)  ← near-perfect
  #2  Spacewalk Thoughts  —  Orbit Bloom  4.21/7.0  (60%)  ← ambient filler
  #3  Library Rain  —  Paper Lanterns    4.05/7.0  (58%)  ← lofi filler
  #4  Campfire Hymn  —  River & Rye      3.87/7.0  (55%)  ← folk filler
  #5  Coffee Shop Stories  —  Slow Stereo 3.71/7.0  (53%)  ← jazz filler
```

**AI explanation (Claude):**
> "Morning Sonata is an excellent match for your preferences, but the catalog has only one classical song. Positions 2–5 are drawn from ambient and acoustic genres as the closest available alternatives. A larger catalog would serve classical listeners much better."

*This edge case exposes a known limitation: a single-song genre produces one great recommendation and four mediocre fillers. The AI explanation surfaces this transparently instead of pretending the results are equally good.*

---

## Design Decisions

### Why weight genre at 2.0 (28% of total)?

Genre is the single strongest signal of musical identity. A jazz fan who gets a pop recommendation — even a soft, calm one — will feel the system missed the point entirely. Weighting genre heavily ensures that the worst outcome (wrong genre at #1) is nearly impossible as long as the catalog contains a genre match. The trade-off is a "filter bubble": songs from neighboring genres (lofi and jazz, for example) can never break through even when they would feel right to the listener.

### Why is mood a binary match instead of a spectrum?

Simplicity. Partial-credit mood matching would require a similarity table between every pair of moods — a small engineering problem that would add complexity without meaningfully improving results at a 20-song catalog scale. At scale, mood similarity scoring would be worth building. Here, it would be over-engineering.

### Why content-based filtering instead of collaborative?

Collaborative filtering requires data from multiple users. This is a single-user system with no persistent listening history. Content-based filtering works with only song attributes and a stated preference, making it the right tool for the problem as scoped.

### Why add Claude for natural language input?

The original system required structured dictionaries with exact numeric keys. That's fine for testing but unusable by a real person. Adding Claude as a preference extractor means a user can say "something calm to study to" and get meaningful results — the AI translates intent into the structure the engine already knows how to process. The recommender core didn't change; only the interface did.

### What trade-offs were made given time constraints?

- The catalog stays at 20 songs. Expanding it would improve results but doesn't demonstrate new capabilities.
- Tempo normalization is linear (60–160 BPM range). A real system might use logarithmic scaling.
- Danceability is stored but not scored — it was dropped after testing showed it added noise without improving result quality.

---

## Testing Summary

### Unit tests (`tests/test_recommender.py`)

Two tests cover the core engine:

| Test | What it checks | Result |
|---|---|---|
| `test_recommend_returns_songs_sorted_by_score` | Top result for a pop/happy/high-energy profile is a pop song | Pass |
| `test_explain_recommendation_returns_non_empty_string` | Explanation function returns a non-empty string | Pass |

Run with: `pytest`

### Manual profile evaluation (6 scenarios)

| Profile | Expected top genre | Actual top genre | Pass? |
|---|---|---|---|
| High-Energy Pop | pop | pop | ✅ |
| Chill Lofi Study | lofi | lofi | ✅ |
| Deep Intense Rock | rock | rock | ✅ |
| Sad Bangers (high energy + dark mood) | metal | metal | ✅ |
| Classical Fan (genre orphan) | classical | classical | ✅ |
| Perfectly Average (flat preferences) | indie pop | indie pop | ✅ |

**6/6 top results matched the expected genre.** However, positions 2–5 degraded significantly for the Classical Fan and Sad Bangers profiles due to catalog scarcity and conflicting preference signals.

### What worked

- The scoring formula separated "easy" profiles (lofi, rock, pop) almost perfectly.
- Explainability worked as intended: the feature-by-feature breakdown made it immediately obvious why a result ranked where it did.
- The edge cases were more revealing than the main profiles — they exposed exactly where the system fails and why.

### What didn't work

- The genre filter bubble is real. A lofi fan who might enjoy jazz will never see a jazz song.
- Mood is too strict. "Chill" and "focused" are treated as completely different when they feel nearly identical.
- The Perfectly Average profile produced essentially random results at positions 2–5 — when there's no strong signal, the system has nothing to differentiate on.

---

## Reflection

Building this system clarified something I hadn't fully understood before: every recommendation system is a set of choices someone made. The weights, the feature selection, the binary-vs-spectrum decision for mood — each one advantages some users and disadvantages others. The system I built works well for pop, lofi, and rock listeners and fails noticeably for classical and country listeners. That's not a bug in the code. It's a direct consequence of who the catalog was built for and what the weights reward.

The most useful thing I learned is the gap between *numeric correctness* and *vibe accuracy*. When the "Sad Bangers" profile returned a scattered top-5 across metal, blues, and pop, the system wasn't wrong mathematically — it was finding the closest numeric matches in a 20-song space. But the output felt incoherent. That gap between "the math is right" and "the result is right" is probably the hardest problem in applied AI, and it shows up clearly even at this small scale.

Adding Claude as a natural language interface also shifted how I think about the human-AI boundary. The recommender engine doesn't need to understand language — it needs numbers. Claude's job is just translation: turning what a person means into what the engine can process. Keeping those concerns separate made both components simpler and easier to debug.

If I continued this project, I'd explore collaborative filtering — recommending based on what users with similar taste histories have listened to — and a "surprise me" mode that intentionally introduces one off-profile song per session to help users discover music outside their bubble. That's what I always hope a real platform will do, and it almost never does.

---

## Project Structure

```
applied-ai-system-project/
├── src/
│   ├── main.py              # Entry point and user profile runner
│   └── recommender.py       # Core scoring engine, Song and UserProfile classes
├── data/
│   └── songs.csv            # 20-song catalog with 13 features per song
├── tests/
│   └── test_recommender.py  # Unit tests for recommender and explanation logic
├── assets/
│   ├── architecture.md      # System diagram (Mermaid)
│   └── terminal_output.png  # Sample terminal output screenshot
├── logs/
│   └── session.log          # Auto-generated session log (created on first run)
├── model_card.md            # Ethics, bias analysis, and intended use
├── reflection.md            # Detailed profile-by-profile analysis
├── requirements.txt
└── README.md
```

---

## License

MIT — free to use, modify, and build on.
