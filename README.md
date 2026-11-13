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

## Evaluation Profiles

Seven profiles were run through the recommender (top 5 each): three standard users and four adversarial edge cases. Output is copied straight from `python -m src.main`.

### Standard profiles

```
=== High-Energy Pop ===
Profile: pop / happy / energy 0.9 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Sunrise City by Neon Echo  --  Score: 4.33
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.92)
   - acoustic fit (+0.41)

2. Gym Hero by Max Pulse  --  Score: 3.44
   - genre match (+2.00)
   - energy closeness (+0.97)
   - acoustic fit (+0.47)

3. Rooftop Lights by Indigo Parade  --  Score: 2.19
   - mood match (+1.00)
   - energy closeness (+0.86)
   - acoustic fit (+0.33)

4. Storm Runner by Voltline  --  Score: 1.44
   - energy closeness (+0.99)
   - acoustic fit (+0.45)

5. Neon Overdrive by Pulse Theory  --  Score: 1.43
   - energy closeness (+0.94)
   - acoustic fit (+0.48)
```

```
=== Chill Lofi ===
Profile: lofi / chill / energy 0.4 / likes acoustic: yes

Top 5 recommendations
------------------------------------------------------------
1. Library Rain by Paper Lanterns  --  Score: 4.38
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.95)
   - acoustic fit (+0.43)

2. Midnight Coding by LoRoom  --  Score: 4.33
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.98)
   - acoustic fit (+0.35)

3. Focus Flow by LoRoom  --  Score: 3.39
   - genre match (+2.00)
   - energy closeness (+1.00)
   - acoustic fit (+0.39)

4. Spacewalk Thoughts by Orbit Bloom  --  Score: 2.34
   - mood match (+1.00)
   - energy closeness (+0.88)
   - acoustic fit (+0.46)

5. Coffee Shop Stories by Slow Stereo  --  Score: 1.42
   - energy closeness (+0.97)
   - acoustic fit (+0.45)
```

```
=== Deep Intense Rock ===
Profile: rock / intense / energy 0.92 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Storm Runner by Voltline  --  Score: 4.44
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.99)
   - acoustic fit (+0.45)

2. Gym Hero by Max Pulse  --  Score: 2.46
   - mood match (+1.00)
   - energy closeness (+0.99)
   - acoustic fit (+0.47)

3. Neon Overdrive by Pulse Theory  --  Score: 1.45
   - energy closeness (+0.96)
   - acoustic fit (+0.48)

4. Iron Throne by Black Cathedral  --  Score: 1.43
   - energy closeness (+0.95)
   - acoustic fit (+0.48)

5. Sunrise City by Neon Echo  --  Score: 1.31
   - energy closeness (+0.90)
   - acoustic fit (+0.41)
```

### Adversarial profiles

```
=== Sad but Energetic ===
Profile: blues / sad / energy 0.9 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Gym Hero by Max Pulse  --  Score: 1.44
   - energy closeness (+0.97)
   - acoustic fit (+0.47)

2. Storm Runner by Voltline  --  Score: 1.44
   - energy closeness (+0.99)
   - acoustic fit (+0.45)

3. Neon Overdrive by Pulse Theory  --  Score: 1.43
   - energy closeness (+0.94)
   - acoustic fit (+0.48)

4. Iron Throne by Black Cathedral  --  Score: 1.41
   - energy closeness (+0.93)
   - acoustic fit (+0.48)

5. Sunrise City by Neon Echo  --  Score: 1.33
   - energy closeness (+0.92)
   - acoustic fit (+0.41)
```

```
=== Genre Not in Catalog ===
Profile: k-pop / happy / energy 0.8 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Sunrise City by Neon Echo  --  Score: 2.39
   - mood match (+1.00)
   - energy closeness (+0.98)
   - acoustic fit (+0.41)

2. Rooftop Lights by Indigo Parade  --  Score: 2.29
   - mood match (+1.00)
   - energy closeness (+0.96)
   - acoustic fit (+0.33)

3. Block Party Anthem by Marcus Vale  --  Score: 1.42
   - energy closeness (+0.98)
   - acoustic fit (+0.44)

4. Gym Hero by Max Pulse  --  Score: 1.34
   - energy closeness (+0.87)
   - acoustic fit (+0.47)

5. Night Drive Loop by Neon Echo  --  Score: 1.34
   - energy closeness (+0.95)
   - acoustic fit (+0.39)
```

```
=== Acoustic EDM ===
Profile: edm / euphoric / energy 0.95 / likes acoustic: yes

Top 5 recommendations
------------------------------------------------------------
1. Neon Overdrive by Pulse Theory  --  Score: 4.00
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.99)
   - acoustic fit (+0.01)

2. Gym Hero by Max Pulse  --  Score: 1.01
   - energy closeness (+0.98)
   - acoustic fit (+0.03)

3. Storm Runner by Voltline  --  Score: 1.01
   - energy closeness (+0.96)
   - acoustic fit (+0.05)

4. Iron Throne by Black Cathedral  --  Score: 1.00
   - energy closeness (+0.98)
   - acoustic fit (+0.02)

5. Rooftop Lights by Indigo Parade  --  Score: 0.99
   - energy closeness (+0.81)
   - acoustic fit (+0.17)
```

```
=== Dead-Center Energy ===
Profile: jazz / relaxed / energy 0.5 / likes acoustic: no

Top 5 recommendations
------------------------------------------------------------
1. Coffee Shop Stories by Slow Stereo  --  Score: 3.93
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.87)
   - acoustic fit (+0.05)

2. Velvet Hours by Sable June  --  Score: 1.28
   - energy closeness (+0.98)
   - acoustic fit (+0.30)

3. Block Party Anthem by Marcus Vale  --  Score: 1.16
   - energy closeness (+0.72)
   - acoustic fit (+0.44)

4. Night Drive Loop by Neon Echo  --  Score: 1.14
   - energy closeness (+0.75)
   - acoustic fit (+0.39)

5. Island Breeze by Sunny Roots  --  Score: 1.12
   - energy closeness (+0.86)
   - acoustic fit (+0.26)
```

---

## Experiments You Tried

### Intuition check: Deep Intense Rock

For the rock / intense / 0.92 profile, the top result feels right and the rest is mixed:

1. Storm Runner (rock, intense) scores 4.44. This is correct.
2. Gym Hero (pop, intense) scores 2.46. It is intense and high energy, but it is pop.
3. Neon Overdrive (EDM) scores 1.45.
4. Iron Throne (metal, angry) scores 1.43.

The surprise is that metal ranks below EDM and pop for a rock fan. Genre is an exact match, so "metal" is as far from "rock" as any other genre. The system cannot see that two genres are close.

Why Storm Runner ranks first (4.44 out of a possible 4.50):

- genre match: +2.00
- mood match: +1.00
- energy closeness: +0.99 (song 0.91 vs target 0.92)
- acoustic fit: +0.45 (acousticness 0.10, and this user does not like acoustic)

Gym Hero gets no genre points, so it falls to 2.46 even though its energy is almost perfect (+0.99).

### Experiment: remove the mood check

I set `MOOD_WEIGHT = 0.0` temporarily, ran all seven profiles, then restored it to 1.0. The maximum score drops from 4.5 to 3.5, so scores are only comparable within a single run.

| Profile | #1 before | #1 after | Verdict |
|---|---|---|---|
| High-Energy Pop | Sunrise City (4.33) | **Gym Hero (3.44)**, Sunrise City second (3.33) | Less accurate |
| Chill Lofi | Library Rain (4.38) | Focus Flow (3.39), with a near tie for the top three | Just different |
| Deep Intense Rock | Storm Runner (4.44) | Storm Runner (3.44), but Gym Hero's lead over EDM almost vanishes | Same top pick, weaker ordering |
| Genre Not in Catalog | Sunrise City (2.39) | Block Party Anthem (1.42) | Less accurate |
| Sad but Energetic, Acoustic EDM, Dead-Center Energy | unchanged #1 | unchanged #1 | No effect |

Takeaway: removing mood made the results different, and for happy pop it made them worse. The intense workout song (Gym Hero) beats the happy pop song (Sunrise City) for someone who asked for "happy." Mood is the only thing separating those two, so the original weights were better. The mood check matters most when genre alone cannot choose between songs.

Side note: with the weight at 0, the explanation text still printed "mood match (+0.00)". The reasons are still correct, but a zero-weight match should probably be hidden in a future version.

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