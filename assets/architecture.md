# System Architecture — AI Music Recommender

## Data Flow Diagram

```mermaid
flowchart TD
    USER([👤 User\nNatural Language Input\ne.g. 'chill study music'])

    subgraph AI_LAYER ["AI Layer (Claude API)"]
        EXTRACT["🧠 Preference Extractor\nParses free-text → structured prefs\ngenre · mood · energy · tempo · acousticness"]
        EXPLAIN["🧠 Explanation Generator\nProduces human-readable\njustification for top picks"]
    end

    subgraph CORE ["Recommender Engine (src/recommender.py)"]
        SCORE["score_song()\nWeighted proximity scoring\nacross 9 audio features"]
        RANK["Ranked Results\nTop-K songs with scores\n(0.0 – 7.0)"]
    end

    subgraph DATA ["Data Layer"]
        CATALOG[("🎵 Song Catalog\ndata/songs.csv\n20 songs")]
    end

    subgraph RELIABILITY ["Reliability & Testing"]
        TESTS["🧪 Reliability Tester\ntests/test_recommender.py\n5 preset query scenarios"]
        REPORT["📊 Test Report\npass/fail · accuracy %\nconfidence scores"]
        HUMAN_EVAL([👤 Human Review\nManual spot-check\nof recommendations])
    end

    subgraph OBSERVABILITY ["Observability"]
        LOG["📝 Logger\nlogs/session.log\ntimestamp · query · results"]
    end

    OUTPUT([👤 User\nRanked Songs +\nAI Explanation])

    USER --> EXTRACT
    EXTRACT --> SCORE
    CATALOG --> SCORE
    SCORE --> RANK
    RANK --> EXPLAIN
    EXPLAIN --> OUTPUT
    RANK --> LOG

    TESTS --> SCORE
    SCORE --> REPORT
    REPORT --> HUMAN_EVAL
```

---

## Component Summary

| Component | File | Role |
|---|---|---|
| Preference Extractor | Claude API (ai_interface.py) | Converts natural language → structured prefs dict |
| Recommender Engine | src/recommender.py | Scores every song; returns ranked top-K |
| Song Catalog | data/songs.csv | 20 songs with 9 audio features each |
| Explanation Generator | Claude API (ai_interface.py) | Generates a plain-English justification for picks |
| Logger | logs/session.log | Records every query + result for audit/debugging |
| Reliability Tester | tests/test_recommender.py | 5 preset scenarios; auto-grades expected vs actual |
| Human Review | Manual | Spot-checks AI explanations for accuracy and tone |

---

## Input → Output Example

```
Input:  "I need something calm and instrumental to focus while coding"

          ↓  Claude extracts:
          genre=lofi, mood=focused, energy=0.40,
          instrumentalness=0.80, acousticness=0.70

          ↓  Recommender scores 20 songs

          ↓  Top pick: "Focus Flow" — LoRoom (score: 6.31/7.0)

Output: "Focus Flow by LoRoom is a strong match — lofi genre,
         focused mood, low energy (0.40), and highly instrumental
         (0.80), which suits a distraction-free coding session."
```
