"""
Command line runner for the Music Recommender Simulation.
"""

from recommender import load_songs, recommend_songs

SEPARATOR = "─" * 60


def print_recommendations(user_prefs: dict, songs: list, k: int = 5) -> None:
    label = f"Genre: {user_prefs['genre'].upper()}  |  Mood: {user_prefs['mood'].upper()}"
    print(f"\n{'🎵 ' + label}")
    print(SEPARATOR)

    results = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(results, 1):
        bar_filled  = int((score / 7.0) * 20)
        bar         = "█" * bar_filled + "░" * (20 - bar_filled)
        pct         = (score / 7.0) * 100

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       [{bar}]  {score:.2f}/7.0  ({pct:.0f}%)")
        print(f"       Genre: {song['genre']}  |  Mood: {song['mood']}  "
              f"|  Energy: {song['energy']}  |  BPM: {int(song['tempo_bpm'])}")
        print("       Reasons:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print(f"\n{SEPARATOR}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}")

    # ── Profile 1: default pop/happy listener ──────────────────────────────
    pop_happy = {
        "genre":                   "pop",
        "mood":                    "happy",
        "target_energy":           0.80,
        "target_valence":          0.82,
        "target_tempo_bpm":        120,
        "target_acousticness":     0.20,
        "target_bass_level":       0.60,
        "target_instrumentalness": 0.06,
        "target_speechiness":      0.08,
    }

    # ── Profile 2: late-night lofi/focused listener ────────────────────────
    lofi_focused = {
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

    print_recommendations(pop_happy,    songs, k=5)
    print_recommendations(lofi_focused, songs, k=5)


if __name__ == "__main__":
    main()
