"""
Command line runner for the Music Recommender Simulation.
"""

import sys
from src.recommender import load_songs, recommend_songs, confidence_label
from src.logger import log_session, log_error, get_logger

SEPARATOR = "─" * 62


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print(f"\n\n{'═' * 62}")
    print(f"  {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}")
    print(f"{'═' * 62}")

    try:
        results = recommend_songs(user_prefs, songs, k=k)
    except Exception as exc:
        log_error(label, exc)
        print(f"  ERROR: could not generate recommendations — {exc}")
        return

    log_session(label, user_prefs, results)

    for rank, (song, score, explanation) in enumerate(results, 1):
        conf_pct, conf_label = confidence_label(score)
        bar_filled = int((score / 7.0) * 24)
        bar        = "█" * bar_filled + "░" * (24 - bar_filled)
        pct        = conf_pct * 100

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       [{bar}]  {score:.2f}/7.0  ({pct:.0f}%)  confidence: {conf_label}")
        print(f"       {song['genre']} · {song['mood']} · "
              f"energy={song['energy']} · bpm={int(song['tempo_bpm'])}")
        print("       Reasons:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print(f"\n{SEPARATOR}")


def main() -> None:
    log = get_logger()
    log.info("=" * 50)
    log.info("VibeFinder session started")

    try:
        songs = load_songs("data/songs.csv")
    except Exception as exc:
        log_error("load_songs", exc)
        print(f"Fatal: could not load catalog — {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"\nLoaded songs: {len(songs)}")
    log.info("Loaded %d songs from catalog", len(songs))

    # ── 1. High-Energy Pop ─────────────────────────────────────────────────
    high_energy_pop = {
        "genre":                   "pop",
        "mood":                    "happy",
        "target_energy":           0.90,
        "target_valence":          0.85,
        "target_tempo_bpm":        128,
        "target_acousticness":     0.08,
        "target_bass_level":       0.75,
        "target_instrumentalness": 0.04,
        "target_speechiness":      0.10,
    }

    # ── 2. Chill Lofi ──────────────────────────────────────────────────────
    chill_lofi = {
        "genre":                   "lofi",
        "mood":                    "focused",
        "target_energy":           0.40,
        "target_valence":          0.60,
        "target_tempo_bpm":        80,
        "target_acousticness":     0.70,
        "target_bass_level":       0.42,
        "target_instrumentalness": 0.75,
        "target_speechiness":      0.04,
    }

    # ── 3. Deep Intense Rock ───────────────────────────────────────────────
    intense_rock = {
        "genre":                   "rock",
        "mood":                    "intense",
        "target_energy":           0.92,
        "target_valence":          0.45,
        "target_tempo_bpm":        150,
        "target_acousticness":     0.08,
        "target_bass_level":       0.80,
        "target_instrumentalness": 0.18,
        "target_speechiness":      0.06,
    }

    # ── 4. EDGE CASE: High energy but sad/dark mood ────────────────────────
    sad_bangers = {
        "genre":                   "metal",
        "mood":                    "melancholic",
        "target_energy":           0.90,
        "target_valence":          0.20,
        "target_tempo_bpm":        155,
        "target_acousticness":     0.06,
        "target_bass_level":       0.85,
        "target_instrumentalness": 0.25,
        "target_speechiness":      0.05,
    }

    # ── 5. EDGE CASE: Genre orphan ─────────────────────────────────────────
    classical_fan = {
        "genre":                   "classical",
        "mood":                    "peaceful",
        "target_energy":           0.22,
        "target_valence":          0.70,
        "target_tempo_bpm":        60,
        "target_acousticness":     0.95,
        "target_bass_level":       0.12,
        "target_instrumentalness": 0.95,
        "target_speechiness":      0.02,
    }

    # ── 6. EDGE CASE: Perfectly average ───────────────────────────────────
    plain_listener = {
        "genre":                   "indie pop",
        "mood":                    "relaxed",
        "target_energy":           0.50,
        "target_valence":          0.50,
        "target_tempo_bpm":        100,
        "target_acousticness":     0.50,
        "target_bass_level":       0.50,
        "target_instrumentalness": 0.50,
        "target_speechiness":      0.05,
    }

    profiles = [
        ("🎵  Profile 1 — High-Energy Pop",              high_energy_pop),
        ("📚  Profile 2 — Chill Lofi (Study Session)",   chill_lofi),
        ("🤘  Profile 3 — Deep Intense Rock",            intense_rock),
        ("⚡  Edge Case 1 — Sad Bangers (high energy + dark valence)", sad_bangers),
        ("🎻  Edge Case 2 — Classical Fan (genre orphan)",             classical_fan),
        ("😐  Edge Case 3 — Perfectly Average (no strong preference)", plain_listener),
    ]

    for label, prefs in profiles:
        print_recommendations(label, prefs, songs, k=5)

    log.info("Session complete — %d profiles run", len(profiles))


if __name__ == "__main__":
    main()
