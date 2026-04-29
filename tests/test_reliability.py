"""
Reliability test suite — 6 preset profiles, each with an expected top-genre.

Run:   pytest tests/test_reliability.py -v
Report: pytest tests/test_reliability.py -v --tb=short
"""

import pytest
from src.recommender import load_songs, recommend_songs, confidence_label

CATALOG = "data/songs.csv"

# (profile_name, prefs_dict, expected_top_genre, expected_top_mood)
PROFILES = [
    (
        "High-Energy Pop",
        {
            "genre": "pop", "mood": "happy",
            "target_energy": 0.90, "target_valence": 0.85,
            "target_tempo_bpm": 128, "target_acousticness": 0.08,
            "target_bass_level": 0.75, "target_instrumentalness": 0.04,
            "target_speechiness": 0.10,
        },
        "pop", "happy",
    ),
    (
        "Chill Lofi Study",
        {
            "genre": "lofi", "mood": "focused",
            "target_energy": 0.40, "target_valence": 0.60,
            "target_tempo_bpm": 80, "target_acousticness": 0.70,
            "target_bass_level": 0.42, "target_instrumentalness": 0.75,
            "target_speechiness": 0.04,
        },
        "lofi", "focused",
    ),
    (
        "Deep Intense Rock",
        {
            "genre": "rock", "mood": "intense",
            "target_energy": 0.92, "target_valence": 0.45,
            "target_tempo_bpm": 150, "target_acousticness": 0.08,
            "target_bass_level": 0.80, "target_instrumentalness": 0.18,
            "target_speechiness": 0.06,
        },
        "rock", "intense",
    ),
    (
        "Sad Bangers (high energy + dark mood)",
        {
            "genre": "metal", "mood": "melancholic",
            "target_energy": 0.90, "target_valence": 0.20,
            "target_tempo_bpm": 155, "target_acousticness": 0.06,
            "target_bass_level": 0.85, "target_instrumentalness": 0.25,
            "target_speechiness": 0.05,
        },
        "metal", None,  # mood match not expected — only 1 metal song, mood=aggressive
    ),
    (
        "Classical Fan (genre orphan)",
        {
            "genre": "classical", "mood": "peaceful",
            "target_energy": 0.22, "target_valence": 0.70,
            "target_tempo_bpm": 60, "target_acousticness": 0.95,
            "target_bass_level": 0.12, "target_instrumentalness": 0.95,
            "target_speechiness": 0.02,
        },
        "classical", "peaceful",
    ),
    (
        "Perfectly Average (flat preferences)",
        {
            "genre": "indie pop", "mood": "relaxed",
            "target_energy": 0.50, "target_valence": 0.50,
            "target_tempo_bpm": 100, "target_acousticness": 0.50,
            "target_bass_level": 0.50, "target_instrumentalness": 0.50,
            "target_speechiness": 0.05,
        },
        "indie pop", None,  # only 1 indie pop song; mood match not guaranteed
    ),
]


@pytest.fixture(scope="module")
def songs():
    return load_songs(CATALOG)


@pytest.mark.parametrize("name,prefs,expected_genre,expected_mood", PROFILES)
def test_top_result_genre(name, prefs, expected_genre, expected_mood, songs):
    results = recommend_songs(prefs, songs, k=1)
    top = results[0][0]
    assert top["genre"] == expected_genre, (
        f"[{name}] expected genre '{expected_genre}', got '{top['genre']}'"
    )


@pytest.mark.parametrize("name,prefs,expected_genre,expected_mood", PROFILES)
def test_top_result_mood(name, prefs, expected_genre, expected_mood, songs):
    if expected_mood is None:
        pytest.skip(f"[{name}] mood match not expected for this edge case")
    results = recommend_songs(prefs, songs, k=1)
    top = results[0][0]
    assert top["mood"] == expected_mood, (
        f"[{name}] expected mood '{expected_mood}', got '{top['mood']}'"
    )


@pytest.mark.parametrize("name,prefs,expected_genre,expected_mood", PROFILES)
def test_confidence_is_valid(name, prefs, expected_genre, expected_mood, songs):
    results = recommend_songs(prefs, songs, k=5)
    for song, score, _ in results:
        pct, label = confidence_label(score)
        assert 0.0 <= pct <= 1.0, f"[{name}] confidence out of range: {pct}"
        assert label in ("High", "Medium", "Low"), f"[{name}] unexpected label: {label}"


@pytest.mark.parametrize("name,prefs,expected_genre,expected_mood", PROFILES)
def test_returns_five_results(name, prefs, expected_genre, expected_mood, songs):
    results = recommend_songs(prefs, songs, k=5)
    assert len(results) == 5, f"[{name}] expected 5 results, got {len(results)}"


# ── Standalone reliability report ─────────────────────────────────────────────

def run_reliability_report() -> None:
    """Print a human-readable reliability summary to stdout."""
    songs = load_songs(CATALOG)
    passed = 0
    total = len(PROFILES)
    scores_all = []

    print("\n" + "═" * 62)
    print("  RELIABILITY REPORT — VibeFinder")
    print("═" * 62)

    for name, prefs, expected_genre, expected_mood in PROFILES:
        results = recommend_songs(prefs, songs, k=5)
        top_song, top_score, _ = results[0]

        genre_ok = top_song["genre"] == expected_genre
        mood_ok  = (expected_mood is None) or (top_song["mood"] == expected_mood)
        ok = genre_ok and mood_ok
        if ok:
            passed += 1

        conf_pct, conf_label = confidence_label(top_score)
        scores_all.append(conf_pct)

        status = "PASS" if ok else "FAIL"
        print(f"\n  [{status}] {name}")
        print(f"         Top result : {top_song['title']} ({top_song['genre']} · {top_song['mood']})")
        print(f"         Score      : {top_score:.2f}/7.0  |  Confidence: {conf_pct:.0%} ({conf_label})")
        if not genre_ok:
            print(f"         ✗ genre: expected '{expected_genre}', got '{top_song['genre']}'")
        if expected_mood and not mood_ok:
            print(f"         ✗ mood: expected '{expected_mood}', got '{top_song['mood']}'")

    avg_conf = sum(scores_all) / len(scores_all)
    print("\n" + "─" * 62)
    print(f"  Result  : {passed}/{total} tests passed")
    print(f"  Avg confidence (top result) : {avg_conf:.0%}")
    high = sum(1 for s in scores_all if s >= 0.80)
    print(f"  High-confidence results     : {high}/{total}")
    print("═" * 62 + "\n")


if __name__ == "__main__":
    run_reliability_report()
