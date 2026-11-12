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


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print a readable ranked list with each song's score and scoring reasons."""
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    print(
        f"\nProfile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
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

    # Default "pop/happy" profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()