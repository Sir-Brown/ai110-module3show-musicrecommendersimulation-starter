from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# ---------------------------------------------------------------------------
# Optional extensions: scoring modes, diversity, advanced features, table
# ---------------------------------------------------------------------------
from pathlib import Path

import pytest

from src.main import format_table
from src.recommender import load_songs, recommend_songs, score_song

PREFS = {
    "favorite_genre": "pop", "favorite_mood": "happy",
    "target_energy": 0.8, "likes_acoustic": False,
}


def _song(title, artist="A", genre="pop", mood="happy", energy=0.8, acousticness=0.1, **extra):
    return {
        "id": hash(title) % 10_000, "title": title, "artist": artist, "genre": genre,
        "mood": mood, "energy": energy, "acousticness": acousticness, **extra,
    }


def test_scoring_modes_change_the_ranking():
    genre_match_far_energy = _song("GenreMatch", genre="pop", mood="sad", energy=0.2)
    energy_match_wrong_genre = _song("EnergyMatch", genre="rock", mood="sad", energy=0.8)
    songs = [genre_match_far_energy, energy_match_wrong_genre]

    genre_first = recommend_songs(PREFS, songs, k=2, mode="genre_first")
    energy_focused = recommend_songs(PREFS, songs, k=2, mode="energy_focused")

    assert genre_first[0][0]["title"] == "GenreMatch"
    assert energy_focused[0][0]["title"] == "EnergyMatch"


def test_unknown_mode_raises():
    with pytest.raises(KeyError):
        score_song(PREFS, _song("X"), mode="does_not_exist")


def test_diversity_penalty_demotes_repeat_artist_and_genre():
    songs = [
        _song("Best", artist="Same", genre="pop", mood="happy"),
        _song("Repeat", artist="Same", genre="pop", mood="happy", energy=0.79),
        # Different artist, same genre: only the smaller genre penalty applies to it.
        _song("Fresh", artist="Other", genre="pop", mood="happy", energy=0.70),
    ]
    plain = [s["title"] for s, _, _ in recommend_songs(PREFS, songs, k=3)]
    diverse = recommend_songs(PREFS, songs, k=3, diversity=True)

    assert plain[:2] == ["Best", "Repeat"]
    assert [s["title"] for s, _, _ in diverse][:2] == ["Best", "Fresh"]
    repeat_reasons = next(expl for s, _, expl in diverse if s["title"] == "Repeat")
    assert "diversity penalty" in repeat_reasons


def test_diversity_off_matches_plain_ranking():
    songs = load_songs(str(Path(__file__).resolve().parent.parent / "data" / "songs.csv"))
    assert recommend_songs(PREFS, songs, 5) == recommend_songs(PREFS, songs, 5, diversity=False)


def test_advanced_preferences_add_points_only_when_requested():
    song = _song("Adv", release_decade=1990, detailed_mood="nostalgic",
                 popularity=50, instrumentalness=0.0, language="en")
    base_score, _ = score_song(PREFS, song)

    advanced = {**PREFS, "preferred_decade": 1990, "preferred_detailed_mood": "Nostalgic",
                "target_popularity": 50, "prefers_instrumental": False,
                "preferred_language": "EN"}
    adv_score, reasons = score_song(advanced, song)

    # decade 0.5 + detailed mood 0.75 + popularity 0.5 + instrumental 0.25 + language 0.25
    assert adv_score == pytest.approx(base_score + 2.25, abs=0.01)
    assert any("detailed mood match" in r for r in reasons)


def test_load_songs_converts_numeric_and_advanced_fields():
    songs = load_songs(str(Path(__file__).resolve().parent.parent / "data" / "songs.csv"))
    first = songs[0]
    assert isinstance(first["id"], int) and isinstance(first["energy"], float)
    assert isinstance(first["popularity"], int) and isinstance(first["release_decade"], int)
    assert isinstance(first["instrumentalness"], float) and first["language"] == "en"


def test_format_table_contains_reasons_and_scores():
    recs = [(_song("Table Song"), 4.2, "genre match (+2.00); mood match (+1.00)")]
    table = format_table(recs)
    assert "Table Song" in table and "4.20" in table
    assert "genre match (+2.00)" in table and "mood match (+1.00)" in table
