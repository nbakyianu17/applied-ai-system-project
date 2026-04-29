from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

TEMPO_MIN = 60
TEMPO_MAX = 160

MAX_SCORE = 7.0

# Point weights per feature
WEIGHTS = {
    "genre":            2.00,
    "mood":             1.00,
    "energy":           1.00,
    "valence":          0.75,
    "instrumentalness": 0.75,
    "acousticness":     0.50,
    "tempo_bpm":        0.50,
    "bass_level":       0.25,
    "speechiness":      0.25,
}


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    bass_level: float = 0.5
    instrumentalness: float = 0.5
    speechiness: float = 0.05


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        prefs = {
            "genre":                   user.favorite_genre,
            "mood":                    user.favorite_mood,
            "target_energy":           user.target_energy,
            "target_acousticness":     0.80 if user.likes_acoustic else 0.20,
            "target_valence":          0.65,
            "target_instrumentalness": 0.70,
            "target_bass_level":       0.40,
            "target_speechiness":      0.04,
            "target_tempo_bpm":        90,
        }
        song_dicts = [s.__dict__ for s in self.songs]
        results = recommend_songs(prefs, song_dicts, k)
        ids = {s.id for s, *_ in [(self.songs[i], *r[1:]) for i, r in enumerate(results)]}
        return [s for s in self.songs if s.id in ids][:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        prefs = {
            "genre": user.favorite_genre,
            "mood":  user.favorite_mood,
            "target_energy": user.target_energy,
            "target_acousticness":     0.80 if user.likes_acoustic else 0.20,
            "target_valence":          0.65,
            "target_instrumentalness": 0.70,
            "target_bass_level":       0.40,
            "target_speechiness":      0.04,
            "target_tempo_bpm":        90,
        }
        _, reasons = score_song(prefs, song.__dict__)
        return " | ".join(reasons)


def confidence_label(score: float) -> Tuple[float, str]:
    """Return (0-1 confidence, High/Medium/Low label) for a raw score."""
    pct = round(score / MAX_SCORE, 3)
    if pct >= 0.80:
        return pct, "High"
    if pct >= 0.55:
        return pct, "Medium"
    return pct, "Low"


def load_songs(csv_path: str) -> List[Dict]:
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":               int(row["id"]),
                "title":            row["title"],
                "artist":           row["artist"],
                "genre":            row["genre"],
                "mood":             row["mood"],
                "energy":           float(row["energy"]),
                "tempo_bpm":        float(row["tempo_bpm"]),
                "valence":          float(row["valence"]),
                "danceability":     float(row["danceability"]),
                "acousticness":     float(row["acousticness"]),
                "bass_level":       float(row.get("bass_level", 0.5)),
                "instrumentalness": float(row.get("instrumentalness", 0.5)),
                "speechiness":      float(row.get("speechiness", 0.05)),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    # --- Categorical: binary match ---
    if song["genre"] == user_prefs.get("genre"):
        score += WEIGHTS["genre"]
        reasons.append(f"genre match ({song['genre']}): +{WEIGHTS['genre']}")
    else:
        reasons.append(f"genre mismatch ({song['genre']} ≠ {user_prefs.get('genre')}): +0.0")

    if song["mood"] == user_prefs.get("mood"):
        score += WEIGHTS["mood"]
        reasons.append(f"mood match ({song['mood']}): +{WEIGHTS['mood']}")
    else:
        reasons.append(f"mood mismatch ({song['mood']} ≠ {user_prefs.get('mood')}): +0.0")

    # --- Numerical: proximity scoring ---
    def proximity(target_key: str, song_key: str, weight: float, normalize: bool = False) -> float:
        target = user_prefs.get(target_key, 0.5)
        value  = song.get(song_key, 0.5)
        if normalize:
            target = (target - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
            value  = (value  - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
        pts = round(weight * (1.0 - abs(target - value)), 4)
        reasons.append(f"{song_key} proximity: +{pts:.2f} (target={target:.2f}, song={value:.2f})")
        return pts

    score += proximity("target_energy",           "energy",           WEIGHTS["energy"])
    score += proximity("target_valence",           "valence",          WEIGHTS["valence"])
    score += proximity("target_instrumentalness",  "instrumentalness", WEIGHTS["instrumentalness"])
    score += proximity("target_acousticness",      "acousticness",     WEIGHTS["acousticness"])
    score += proximity("target_tempo_bpm",         "tempo_bpm",        WEIGHTS["tempo_bpm"], normalize=True)
    score += proximity("target_bass_level",        "bass_level",       WEIGHTS["bass_level"])
    score += proximity("target_speechiness",       "speechiness",      WEIGHTS["speechiness"])

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        scored.append((song, s, " | ".join(reasons)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
