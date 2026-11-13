"""
Command line runner for the Music Recommender Simulation.

Run from the project root with:  python -m src.main

Options:
  --mode {balanced,genre_first,mood_first,energy_focused}   ranking strategy
  --diverse                                                  penalize repeat artists/genres
  --list                                                     show the plain list format instead of a table
  --advanced                                                 also run the advanced-feature profiles
  --profile NAME                                             only run profiles whose name contains NAME
"""

import argparse
import textwrap
from pathlib import Path

try:  # works with `python -m src.main` from the project root
    from src.recommender import DEFAULT_MODE, MODES, load_songs, recommend_songs
except ImportError:  # works when running src/main.py directly (e.g. from the IDE)
    from recommender import DEFAULT_MODE, MODES, load_songs, recommend_songs

# Resolve the CSV relative to this file so it works from any working directory.
SONGS_CSV = Path(__file__).resolve().parent.parent / "data" / "songs.csv"

LINE = "-" * 60


def _profile(genre: str, mood: str, energy: float, acoustic: bool, **advanced) -> dict:
    """Build a user taste profile dict (advanced preferences are optional keyword args)."""
    return {
        "favorite_genre": genre,
        "favorite_mood": mood,
        "target_energy": energy,
        "likes_acoustic": acoustic,
        **advanced,
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

# Profiles that use the advanced song attributes (Challenge 1); run with --advanced.
ADVANCED_PROFILES = {
    "Dreamy Instrumental Study": _profile(
        "lofi", "chill", 0.35, True,
        preferred_decade=2020, preferred_detailed_mood="dreamy",
        target_popularity=55, prefers_instrumental=True,
    ),
    "Nostalgic Throwback": _profile(
        "country", "nostalgic", 0.5, True,
        preferred_decade=1990, preferred_detailed_mood="nostalgic",
        target_popularity=50, prefers_instrumental=False, preferred_language="en",
    ),
}

ADVANCED_LABELS = {
    "preferred_decade": "decade",
    "preferred_detailed_mood": "detailed mood",
    "target_popularity": "popularity",
    "prefers_instrumental": "instrumental",
    "preferred_language": "language",
}


def _wrap_reasons(explanation: str, width: int) -> list:
    """Split an explanation into one wrapped line group per reason."""
    lines = []
    for reason in explanation.split("; "):
        lines.extend(textwrap.wrap(reason, width, subsequent_indent="  ") or [reason])
    return lines


def format_table(recommendations: list, reason_width: int = 50) -> str:
    """Return an ASCII table of rank, title, artist, score, and the scoring reasons."""
    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            [str(rank)], [song["title"]], [song["artist"]], [f"{score:.2f}"],
            _wrap_reasons(explanation, reason_width),
        ])

    widths = [
        max(len(h), *(len(line) for row in rows for line in row[i]))
        for i, h in enumerate(headers)
    ]
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells: list) -> str:
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

    out = [sep, fmt(headers), sep]
    for row in rows:
        for i in range(max(len(cell) for cell in row)):
            out.append(fmt([cell[i] if i < len(cell) else "" for cell in row]))
        out.append(sep)
    return "\n".join(out)


def print_recommendations(
    name: str, user_prefs: dict, recommendations: list,
    mode: str = DEFAULT_MODE, diversity: bool = False, table: bool = True,
) -> None:
    """Print a readable ranked list (or table) with each song's score and scoring reasons."""
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    print(f"\n=== {name} ===")
    print(
        f"Profile: {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
        f"energy {user_prefs['target_energy']} / likes acoustic: {acoustic}"
    )

    extras = [f"{label} {user_prefs[key]}" for key, label in ADVANCED_LABELS.items()
              if user_prefs.get(key) is not None]
    if extras:
        print("Also wants: " + ", ".join(extras))
    if mode != DEFAULT_MODE or diversity:
        print(f"Mode: {mode} | diversity penalty: {'on' if diversity else 'off'}")

    print(f"\nTop {len(recommendations)} recommendations")
    print(LINE)

    if table:
        print(format_table(recommendations))
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  --  Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"   - {reason}")
        print()


def parse_args(argv=None) -> argparse.Namespace:
    """Parse command-line options."""
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=sorted(MODES), default=DEFAULT_MODE,
                        help="ranking strategy (default: balanced)")
    parser.add_argument("--diverse", action="store_true",
                        help="penalize songs whose artist or genre is already in the results")
    parser.add_argument("--table", action="store_true", help=argparse.SUPPRESS)  # table is the default; kept so old commands still work
    parser.add_argument("--list", action="store_true",
                        help="print the plain list format instead of the default table")
    parser.add_argument("--advanced", action="store_true",
                        help="also run the profiles that use the advanced song attributes")
    parser.add_argument("--profile", help="only run profiles whose name contains this text")
    return parser.parse_args(argv)


def main(argv=None) -> None:
    args = parse_args(argv)
    songs = load_songs(str(SONGS_CSV))
    print(f"Loaded songs: {len(songs)}")

    profiles = dict(PROFILES)
    if args.advanced:
        profiles.update(ADVANCED_PROFILES)
    if args.profile:
        profiles = {n: p for n, p in profiles.items() if args.profile.lower() in n.lower()}

    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(
            user_prefs, songs, k=5, mode=args.mode, diversity=args.diverse
        )
        print_recommendations(
            name, user_prefs, recommendations,
            mode=args.mode, diversity=args.diverse, table=not args.list,
        )


if __name__ == "__main__":
    main()
