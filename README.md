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

- **`Song`**: `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`, plus optional advanced fields (`popularity`, `release_decade`, `detailed_mood`, `instrumentalness`, `language`; see Optional Extensions)
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

## Optional Extensions

All four optional challenges are implemented. The default run (`python -m src.main`) is unchanged, so every output above is still correct. Each extension is switched on with a command-line option.

```bash
python -m src.main --mode genre_first      # Challenge 2: pick a ranking strategy
python -m src.main --diverse               # Challenge 3: penalize repeat artists and genres
python -m src.main --table                 # Challenge 4: print results as a table
python -m src.main --advanced              # Challenge 1: also run the advanced-feature profiles
python -m src.main --profile "chill"       # only run profiles whose name contains "chill"
```

Options can be combined, for example `python -m src.main --advanced --diverse --table`.

### Challenge 1: Advanced song features

`data/songs.csv` has five new columns: `popularity` (0-100), `release_decade`, `detailed_mood` (for example "nostalgic", "aggressive", "euphoric"), `instrumentalness` (0-1), and `language`. A user profile can now optionally say what it wants for each one. If a profile leaves a preference out, that feature adds nothing, so the original profiles score exactly as before.

| Preference in the profile | Scoring rule | Max points |
|---|---|---|
| `preferred_decade` | exact decade match, or half points one decade away | 0.5 |
| `preferred_detailed_mood` | match | 0.75 |
| `target_popularity` | closeness to the target, like energy | 0.5 |
| `prefers_instrumental` | instrumentalness if true, 1 minus it if false | 0.25 |
| `preferred_language` | match | 0.25 |

`python -m src.main --advanced --profile "dreamy"` shows a profile that wants dreamy, instrumental 2020s lofi:

```
=== Dreamy Instrumental Study ===
Profile: lofi / chill / energy 0.35 / likes acoustic: yes
Also wants: decade 2020, detailed mood dreamy, popularity 55, instrumental True

Top 5 recommendations
------------------------------------------------------------
1. Library Rain by Paper Lanterns  --  Score: 6.39
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+1.00)
   - acoustic fit (+0.43)
   - decade match (+0.50)
   - detailed mood match (+0.75)
   - popularity closeness (+0.48)
   - instrumental fit (+0.23)

2. Midnight Coding by LoRoom  --  Score: 6.20
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.93)
   - acoustic fit (+0.35)
   - decade match (+0.50)
   - detailed mood match (+0.75)
   - popularity closeness (+0.46)
   - instrumental fit (+0.21)

3. Focus Flow by LoRoom  --  Score: 4.54
   - genre match (+2.00)
   - energy closeness (+0.95)
   - acoustic fit (+0.39)
   - decade match (+0.50)
   - popularity closeness (+0.47)
   - instrumental fit (+0.22)

4. Spacewalk Thoughts by Orbit Bloom  --  Score: 3.31
   - mood match (+1.00)
   - energy closeness (+0.93)
   - acoustic fit (+0.46)
   - nearby decade (+0.25)
   - popularity closeness (+0.43)
   - instrumental fit (+0.24)

5. Moonlit Sonata Remix by Elena Marchetti  --  Score: 2.24
   - energy closeness (+0.87)
   - acoustic fit (+0.47)
   - nearby decade (+0.25)
   - popularity closeness (+0.40)
   - instrumental fit (+0.24)
```

A second profile, "Nostalgic Throwback," wants 1990s nostalgic country:

```
=== Nostalgic Throwback ===
Profile: country / nostalgic / energy 0.5 / likes acoustic: yes
Also wants: decade 1990, detailed mood nostalgic, popularity 50, instrumental False, language en

Top 5 recommendations
------------------------------------------------------------
1. Dusty Road Home by Wade Harlan  --  Score: 6.60
   - genre match (+2.00)
   - mood match (+1.00)
   - energy closeness (+0.98)
   - acoustic fit (+0.41)
   - decade match (+0.50)
   - detailed mood match (+0.75)
   - popularity closeness (+0.47)
   - instrumental fit (+0.25)
   - language match (+0.25)

2. Coffee Shop Stories by Slow Stereo  --  Score: 2.92
   - energy closeness (+0.87)
   - acoustic fit (+0.45)
   - detailed mood match (+0.75)
   - popularity closeness (+0.49)
   - instrumental fit (+0.11)
   - language match (+0.25)

3. Autumn Letters by Willow & Pine  --  Score: 2.21
   - energy closeness (+0.81)
   - acoustic fit (+0.47)
   - popularity closeness (+0.44)
   - instrumental fit (+0.24)
   - language match (+0.25)

4. Island Breeze by Sunny Roots  --  Score: 2.03
   - energy closeness (+0.86)
   - acoustic fit (+0.24)
   - nearby decade (+0.25)
   - popularity closeness (+0.45)
   - instrumental fit (+0.24)

5. Rooftop Lights by Indigo Parade  --  Score: 1.84
   - energy closeness (+0.74)
   - acoustic fit (+0.17)
   - popularity closeness (+0.43)
   - instrumental fit (+0.24)
   - language match (+0.25)
```

### Challenge 2: Multiple scoring modes

Each mode is a small `ScoringMode` object holding four weights, and `score_song` takes the mode as a parameter (a simple Strategy pattern). Adding a new strategy means adding one line to `MODES` in `src/recommender.py`.

| Mode | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| `balanced` (default) | 2.0 | 1.0 | 1.0 | 0.5 |
| `genre_first` | 3.0 | 0.75 | 0.5 | 0.25 |
| `mood_first` | 1.0 | 3.0 | 1.0 | 0.5 |
| `energy_focused` | 0.75 | 0.5 | 3.0 | 0.5 |

Top 5 for the High-Energy Pop profile in each mode:

| Mode | Top 5 |
|---|---|
| `balanced` | Sunrise City, Gym Hero, Rooftop Lights, Storm Runner, Neon Overdrive |
| `genre_first` | Sunrise City, Gym Hero, Rooftop Lights, Storm Runner, Iron Throne |
| `mood_first` | Sunrise City, Rooftop Lights, Gym Hero, Storm Runner, Neon Overdrive |
| `energy_focused` | Sunrise City, Gym Hero, Storm Runner, Rooftop Lights, Neon Overdrive |

The #1 song is the same in every mode here. The modes mostly reorder the middle of the list: `mood_first` pulls the happy *Rooftop Lights* above *Gym Hero*, and `energy_focused` pulls the loud *Storm Runner* above *Rooftop Lights*.

### Challenge 3: Diversity penalty

With `--diverse`, the top results are picked one at a time. Before each pick, a song loses **1.0 point** if its artist is already in the list and **0.5 points** if its genre is already in the list. The penalty shows up in the song's reasons.

| Profile | Without `--diverse` | With `--diverse` |
|---|---|---|
| Chill Lofi | Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories | Library Rain, Midnight Coding, Spacewalk Thoughts, Focus Flow, Coffee Shop Stories |
| Deep Intense Rock | Storm Runner, Gym Hero, Neon Overdrive, Iron Throne, Sunrise City | Storm Runner, Gym Hero, Neon Overdrive, Iron Throne, Block Party Anthem |
| Genre Not in Catalog | Sunrise City, Rooftop Lights, Block Party Anthem, Gym Hero, Night Drive Loop | Sunrise City, Rooftop Lights, Block Party Anthem, Storm Runner, Neon Overdrive |

For Genre Not in Catalog, *Gym Hero* (pop, like the already-chosen *Sunrise City*) is replaced by *Storm Runner*, and *Night Drive Loop* (same artist, Neon Echo, as *Sunrise City*) is replaced by *Neon Overdrive*. That weakens the Gym Hero filter bubble described in the model card. For Chill Lofi, the second LoRoom song (*Focus Flow*) drops from #3 to #4 behind a different artist.

### Challenge 4: Visual summary table

`--table` prints a table with rank, title, artist, score, and the reasons for each score. It uses plain ASCII formatting (no extra library to install). Here it is combined with `--diverse` so the penalty reasons are visible:

```
=== Chill Lofi ===
Profile: lofi / chill / energy 0.4 / likes acoustic: yes
Mode: balanced | diversity penalty: on

Top 5 recommendations
------------------------------------------------------------
+---+---------------------+----------------+-------+-------------------------------------------+
| # | Title               | Artist         | Score | Reasons                                   |
+---+---------------------+----------------+-------+-------------------------------------------+
| 1 | Library Rain        | Paper Lanterns | 4.38  | genre match (+2.00)                       |
|   |                     |                |       | mood match (+1.00)                        |
|   |                     |                |       | energy closeness (+0.95)                  |
|   |                     |                |       | acoustic fit (+0.43)                      |
+---+---------------------+----------------+-------+-------------------------------------------+
| 2 | Midnight Coding     | LoRoom         | 3.83  | genre match (+2.00)                       |
|   |                     |                |       | mood match (+1.00)                        |
|   |                     |                |       | energy closeness (+0.98)                  |
|   |                     |                |       | acoustic fit (+0.35)                      |
|   |                     |                |       | diversity penalty (-0.50): genre already  |
|   |                     |                |       |   recommended                             |
+---+---------------------+----------------+-------+-------------------------------------------+
| 3 | Spacewalk Thoughts  | Orbit Bloom    | 2.34  | mood match (+1.00)                        |
|   |                     |                |       | energy closeness (+0.88)                  |
|   |                     |                |       | acoustic fit (+0.46)                      |
+---+---------------------+----------------+-------+-------------------------------------------+
| 4 | Focus Flow          | LoRoom         | 1.89  | genre match (+2.00)                       |
|   |                     |                |       | energy closeness (+1.00)                  |
|   |                     |                |       | acoustic fit (+0.39)                      |
|   |                     |                |       | diversity penalty (-1.00): artist already |
|   |                     |                |       |   recommended                             |
|   |                     |                |       | diversity penalty (-0.50): genre already  |
|   |                     |                |       |   recommended                             |
+---+---------------------+----------------+-------+-------------------------------------------+
| 5 | Coffee Shop Stories | Slow Stereo    | 1.42  | energy closeness (+0.97)                  |
|   |                     |                |       | acoustic fit (+0.45)                      |
+---+---------------------+----------------+-------+-------------------------------------------+
```

More detail on how these were built, and how I checked them, is in [ai_interactions.md](ai_interactions.md).

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