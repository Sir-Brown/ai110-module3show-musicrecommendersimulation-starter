# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real recommenders work

Platforms like Spotify and YouTube mix two ideas. *Collaborative filtering* uses other people's behavior (likes, skips, replays, playlists, listening history) to say "people like you enjoyed this." *Content-based filtering* uses the song's own attributes (genre, mood, tempo, energy) to say "this is similar to what you like." Real systems blend both, plus context like time of day.

My version is purely content-based. It has no other users, so it can't learn from a crowd. It compares each song's attributes to one user's stated taste and prioritizes genre first, then mood, then how close a song's energy is to the user's target.

### Features

- **`Song`**: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
- **`UserProfile`**: `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`

The catalog (`data/songs.csv`) has 18 songs across 15 genres and 14 moods. The default profile is:

```python
{"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}
```

### Algorithm Recipe

**Scoring rule (one song):**

- +2.0 for a genre match
- +1.0 for a mood match
- Up to +1.0 for energy closeness: `1 - |song.energy - target_energy|`
- Up to +0.5 for acoustic fit: if `likes_acoustic` is true, `0.5 * song.acousticness`; if false, `0.5 * (1 - song.acousticness)`
- Maximum possible score: 4.5
- Every point added also records a reason, e.g. `genre match (+2.0)`

**Ranking rule (whole catalog):** score every song with the scoring rule, sort from highest to lowest, and return the top *k* with their reasons.

```
User prefs  -->  Loop over every song in the CSV  -->  Score each song  -->  Sort high to low  -->  Top K
(genre, mood,    (score_song judges one song         (points + reasons)                            recommendations
 target energy)   at a time)
```

### Expected Biases

- Genre is worth twice as much as mood, so the system may bury great songs that match the mood and energy but not the genre. For example, "indie pop" never matches "pop" because genre is compared exactly.
- A genre match can outweigh a mood mismatch. For a pop/happy profile, *Gym Hero* (pop, intense) should rank above *Rooftop Lights* (indie pop, happy) on genre alone, even though "intense" is not "happy."
- Most moods appear only once, so mood rarely helps tell songs apart and genre does most of the ranking. A user who wants "sad" at high energy will get no mood match at all.
- With only 18 songs, a catalog this small limits variety and can create a filter bubble.
- Acousticness is a small bonus (max 0.5), so it only breaks ties. It can't pull a song from the wrong genre into the top results.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

Profile: pop / happy / energy 0.8 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Sunrise City by Neon Echo  --  Score: 4.39
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.98)
   - acoustic fit (+0.41)

2. Gym Hero by Max Pulse  --  Score: 3.35
   - genre match (+2.00)
   - energy closeness (+0.87)
   - acoustic fit (+0.47)

3. Rooftop Lights by Indigo Parade  --  Score: 2.29
   - mood match (+1.00)
   - energy closeness (+0.96)
   - acoustic fit (+0.33)

4. Block Party Anthem by Marcus Vale  --  Score: 1.42
   - energy closeness (+0.98)
   - acoustic fit (+0.44)

5. Night Drive Loop by Neon Echo  --  Score: 1.34
   - energy closeness (+0.95)
   - acoustic fit (+0.39)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this