"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main
"""

from pathlib import Path

try:  # works with `python -m src.main` from the project root
    from src.recommender import load_songs, recommend_songs
except ImportError:  # works when running src/main.py directly (e.g. from the IDE)
    from recommender import load_songs, recommend_songs

# Resolve the CSV relative to this file so it works from any working directory.
SONGS_CSV = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

LINE = "-" * 60


def _profile(genre: str, mood: str, energy: float, acoustic: bool) -> dict:
    """Build a user taste profile dict."""
    return {
        "favorite_genre": genre,
        "favorite_mood": mood,
        "target_energy": energy,
        "likes_acoustic": acoustic,
    }


# Evaluation profiles: three standard users, then four adversarial edge cases.
PROFILES = {
    # Standard profiles
    "High-Energy Pop": _profile("pop", "happy", 0.9, False),
    "Chill Lofi": _profile("lofi", "chill", 0.4, True),
    "Deep Intense Rock": _profile("rock", "intense", 0.92, False),
    # Adversarial / edge-case profiles
    "Sad but Energetic": _profile("blues", "sad", 0.9, False),  # genre and mood not in catalog
    "Genre Not in Catalog": _profile("k-pop", "happy", 0.8, False),  # no genre match possible
    "Acoustic EDM": _profile("edm", "euphoric", 0.95, True),  # high energy but loves acoustic
    "Dead-Center Energy": _profile("jazz", "relaxed", 0.5, False),  # mid-range target
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a readable ranked list with each song's score and scoring reasons."""
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    print(f"\n=== {name} ===")
    print(
        f"Profile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']} / likes acoustic: {acoustic}"
    )
    print(f"\nTop {len(recommendations)} recommendations")
    print(LINE)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  --  Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


def main() -> None:
    songs = load_songs(str(SONGS_CSV))
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()