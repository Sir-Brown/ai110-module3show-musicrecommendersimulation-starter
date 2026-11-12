import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Scoring weights (see "Algorithm Recipe" in README.md).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for a user, best match first."""
        prefs = asdict(user)
        ranked = sorted(
            self.songs,
            key=lambda s: (-score_song(prefs, asdict(s))[0], s.title),
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song matches a user."""
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against a user profile; return (score, list of reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"].strip().lower() == user_prefs["favorite_genre"].strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.2f})")

    if song["mood"].strip().lower() == user_prefs["favorite_mood"].strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.2f})")

    energy_gap = abs(float(song["energy"]) - float(user_prefs["target_energy"]))
    energy_points = ENERGY_WEIGHT * (1 - energy_gap)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    acousticness = float(song["acousticness"])
    fit = acousticness if user_prefs["likes_acoustic"] else 1 - acousticness
    acoustic_points = ACOUSTIC_WEIGHT * fit
    score += acoustic_points
    reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves the catalog untouched; ties break by title.
    return sorted(scored, key=lambda item: (-item[1], item[0]["title"]))[:k]