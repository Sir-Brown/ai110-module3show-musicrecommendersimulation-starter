import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Scoring modes (Strategy pattern, Challenge 2)
# ---------------------------------------------------------------------------
# A scoring mode is just a bundle of weights. score_song() takes the mode as a
# parameter, so adding a new ranking strategy means adding one entry to MODES
# and nothing else changes.

@dataclass(frozen=True)
class ScoringMode:
    """A named bundle of weights that defines one ranking strategy."""
    name: str
    genre: float
    mood: float
    energy: float
    acoustic: float


# Weights for the default "balanced" mode (see "Algorithm Recipe" in README.md).
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5

MODES: Dict[str, ScoringMode] = {
    "balanced": ScoringMode("balanced", GENRE_WEIGHT, MOOD_WEIGHT, ENERGY_WEIGHT, ACOUSTIC_WEIGHT),
    "genre_first": ScoringMode("genre_first", 3.0, 0.75, 0.5, 0.25),
    "mood_first": ScoringMode("mood_first", 1.0, 3.0, 1.0, 0.5),
    "energy_focused": ScoringMode("energy_focused", 0.75, 0.5, 3.0, 0.5),
}
DEFAULT_MODE = "balanced"

# ---------------------------------------------------------------------------
# Advanced feature weights (Challenge 1). These only apply when the user
# profile supplies the matching optional preference.
# ---------------------------------------------------------------------------
DECADE_WEIGHT = 0.5          # exact decade; one decade away earns half
DETAILED_MOOD_WEIGHT = 0.75  # e.g. "nostalgic", "aggressive", "euphoric"
POPULARITY_WEIGHT = 0.5      # closeness to a target popularity (0-100)
INSTRUMENTAL_WEIGHT = 0.25   # instrumental vs. vocal preference
LANGUAGE_WEIGHT = 0.25

# ---------------------------------------------------------------------------
# Diversity penalties (Challenge 3)
# ---------------------------------------------------------------------------
ARTIST_PENALTY = 1.0
GENRE_PENALTY = 0.5

INT_FIELDS = ("id", "popularity", "release_decade")
FLOAT_FIELDS = (
    "energy", "tempo_bpm", "valence", "danceability", "acousticness", "instrumentalness",
)


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
    # Advanced attributes (optional so older data and tests still work)
    popularity: Optional[int] = None
    release_decade: Optional[int] = None
    detailed_mood: Optional[str] = None
    instrumentalness: Optional[float] = None
    language: Optional[str] = None


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
    # Advanced preferences (optional; skipped when None)
    preferred_decade: Optional[int] = None
    preferred_detailed_mood: Optional[str] = None
    target_popularity: Optional[int] = None
    prefers_instrumental: Optional[bool] = None
    preferred_language: Optional[str] = None


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(
        self, user: UserProfile, k: int = 5,
        mode: Union[str, ScoringMode] = DEFAULT_MODE, diversity: bool = False,
    ) -> List[Song]:
        """Return the top k Song objects for a user, best match first."""
        by_id = {s.id: s for s in self.songs}
        results = recommend_songs(
            asdict(user), [asdict(s) for s in self.songs], k, mode=mode, diversity=diversity
        )
        return [by_id[song["id"]] for song, _, _ in results]

    def explain_recommendation(
        self, user: UserProfile, song: Song, mode: Union[str, ScoringMode] = DEFAULT_MODE,
    ) -> str:
        """Return a plain-language explanation of why a song matches a user."""
        _, reasons = score_song(asdict(user), asdict(song), mode)
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in INT_FIELDS:
                if row.get(field) not in (None, ""):
                    row[field] = int(row[field])
            for field in FLOAT_FIELDS:
                if row.get(field) not in (None, ""):
                    row[field] = float(row[field])
            songs.append(row)
    return songs


def _same(a: Optional[str], b: Optional[str]) -> bool:
    """Case-insensitive, whitespace-tolerant string comparison."""
    return a is not None and b is not None and a.strip().lower() == b.strip().lower()


def _advanced_points(user_prefs: Dict, song: Dict) -> List[Tuple[float, str]]:
    """Score the optional advanced attributes; only those the user cares about count."""
    out: List[Tuple[float, str]] = []

    want_decade, song_decade = user_prefs.get("preferred_decade"), song.get("release_decade")
    if want_decade is not None and song_decade is not None:
        gap = abs(int(want_decade) - int(song_decade)) // 10
        if gap == 0:
            out.append((DECADE_WEIGHT, f"decade match (+{DECADE_WEIGHT:.2f})"))
        elif gap == 1:
            half = DECADE_WEIGHT / 2
            out.append((half, f"nearby decade (+{half:.2f})"))

    if _same(user_prefs.get("preferred_detailed_mood"), song.get("detailed_mood")):
        out.append((DETAILED_MOOD_WEIGHT, f"detailed mood match (+{DETAILED_MOOD_WEIGHT:.2f})"))

    want_pop, song_pop = user_prefs.get("target_popularity"), song.get("popularity")
    if want_pop is not None and song_pop is not None:
        pts = POPULARITY_WEIGHT * (1 - abs(float(song_pop) - float(want_pop)) / 100)
        out.append((pts, f"popularity closeness (+{pts:.2f})"))

    wants_inst, song_inst = user_prefs.get("prefers_instrumental"), song.get("instrumentalness")
    if wants_inst is not None and song_inst is not None:
        fit = float(song_inst) if wants_inst else 1 - float(song_inst)
        pts = INSTRUMENTAL_WEIGHT * fit
        out.append((pts, f"instrumental fit (+{pts:.2f})"))

    if _same(user_prefs.get("preferred_language"), song.get("language")):
        out.append((LANGUAGE_WEIGHT, f"language match (+{LANGUAGE_WEIGHT:.2f})"))

    return out


def score_song(
    user_prefs: Dict, song: Dict, mode: Union[str, ScoringMode] = DEFAULT_MODE,
) -> Tuple[float, List[str]]:
    """Score one song against a user profile; return (score, list of reasons)."""
    weights = MODES[mode] if isinstance(mode, str) else mode
    score = 0.0
    reasons: List[str] = []

    if _same(song["genre"], user_prefs["favorite_genre"]):
        score += weights.genre
        reasons.append(f"genre match (+{weights.genre:.2f})")

    if _same(song["mood"], user_prefs["favorite_mood"]):
        score += weights.mood
        reasons.append(f"mood match (+{weights.mood:.2f})")

    energy_gap = abs(float(song["energy"]) - float(user_prefs["target_energy"]))
    energy_points = weights.energy * (1 - energy_gap)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    acousticness = float(song["acousticness"])
    fit = acousticness if user_prefs["likes_acoustic"] else 1 - acousticness
    acoustic_points = weights.acoustic * fit
    score += acoustic_points
    reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    for points, reason in _advanced_points(user_prefs, song):
        score += points
        reasons.append(reason)

    return round(score, 2), reasons


def _rerank_with_diversity(
    scored: List[Tuple[Dict, float, List[str]]], k: int,
) -> List[Tuple[Dict, float, str]]:
    """Greedily pick k songs, penalizing artists and genres already picked."""
    remaining = list(scored)
    picked: List[Tuple[Dict, float, str]] = []
    seen_artists, seen_genres = set(), set()

    while remaining and len(picked) < k:
        best = None
        for song, score, reasons in remaining:
            penalty, extra = 0.0, []
            if song["artist"].strip().lower() in seen_artists:
                penalty += ARTIST_PENALTY
                extra.append(f"diversity penalty (-{ARTIST_PENALTY:.2f}): artist already recommended")
            if song["genre"].strip().lower() in seen_genres:
                penalty += GENRE_PENALTY
                extra.append(f"diversity penalty (-{GENRE_PENALTY:.2f}): genre already recommended")
            adjusted = round(score - penalty, 2)
            key = (-adjusted, song["title"])
            if best is None or key < best[0]:
                best = (key, song, adjusted, reasons + extra)

        assert best is not None  # remaining is non-empty inside the loop
        _, song, adjusted, reasons = best
        picked.append((song, adjusted, "; ".join(reasons)))
        remaining = [item for item in remaining if item[0] is not song]
        seen_artists.add(song["artist"].strip().lower())
        seen_genres.add(song["genre"].strip().lower())

    return picked


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5,
    mode: Union[str, ScoringMode] = DEFAULT_MODE, diversity: bool = False,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append((song, score, reasons))

    if diversity:
        return _rerank_with_diversity(scored, k)

    # sorted() returns a new list and leaves the catalog untouched; ties break by title.
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["title"]))[:k]
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]
