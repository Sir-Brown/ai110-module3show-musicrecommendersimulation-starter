# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal.** VibeMatch suggests the 5 songs from a small catalog that best fit one person's taste. It does not predict what a real listener will play next. It scores each song against what the user says they like: favorite genre, favorite mood, target energy, and whether they like acoustic music.

**Intended use.**

- Classroom exploration of how a recommender turns data into a ranked list.
- Learning how scoring rules, weights, and ranking work together.
- It assumes the user can describe their taste in one genre, one mood, and one energy level.

**Not intended for.**

- Real listeners or a real music app. The catalog has only 18 songs.
- Judging songs, artists, or genres. A low score means "does not match this profile," not "bad music."
- Any setting where fairness matters. It cannot learn from behavior, and it treats every pair of genres as equally different.

---

## 3. How the Model Works  

Every song gets points for how well it fits the user. Then the songs are sorted, and the top 5 are shown.

- **Genre match:** +2.0 points if the song's genre is the user's favorite.
- **Mood match:** +1.0 point if the song's mood is the user's favorite.
- **Energy closeness:** up to +1.0 point. The closer the song's energy is to what the user wants, the more points. A song that is too loud and a song that is too quiet are both penalized.
- **Acoustic fit:** up to +0.5 points. If the user likes acoustic music, acoustic songs get more. If not, non-acoustic songs get more.

The highest possible score is 4.5. Each point is recorded with a short reason, so every recommendation can explain itself.

Changes from the starter: I added the acoustic score, made genre and mood matching ignore capital letters, and kept all the weights in one place so they are easy to change for experiments.

**Optional extras.** These are all off by default, so the results above do not change unless one is switched on.

- **Scoring modes:** "genre first," "mood first," and "energy focused" change the weights.
- **Diversity penalty:** a song loses points if its artist (1.0) or genre (0.5) is already in the list.
- **Advanced preferences:** a user can also ask for a decade, a detailed mood, a popularity level, instrumental or vocal, and a language.
- **Table view:** results can be printed as a table that includes the reasons.

---

## 4. Data  

- **Size:** 18 songs. The starter had 10, and I added 8.
- **Variety:** 15 genres and 14 moods. Examples are pop, lofi, rock, jazz, hip hop, classical, EDM, metal, reggae, and folk.
- **What each song has:** genre, mood, energy, tempo, valence, danceability, and acousticness. I later added five more: popularity, release decade, a detailed mood tag (like "nostalgic"), instrumentalness, and language. The core scoring uses genre, mood, energy, and acousticness. The new attributes only count when a user asks for them.
- **Limits:** 13 of the 15 genres have only one song. Only 3 songs have middle energy (between 0.43 and 0.74). There is no "sad" mood. There are no lyrics. The numbers, including popularity and decade, are made up for the simulation and were not measured from real audio or real listening.

---

## 5. Strengths  

- Quiet and loud tastes get completely different lists. Chill Lofi and Deep Intense Rock share no songs at all.
- Chill Lofi works very well. All of its top three songs are lofi.
- For Deep Intense Rock, the #1 pick (*Storm Runner*) matched my own intuition.
- Every result comes with plain reasons, such as "genre match (+2.00)," so it is easy to see why a song ranked where it did.

---

## 6. Limitations and Bias 

The system keeps recommending *Gym Hero* to almost everyone who wants high energy. It showed up in the top 5 for 5 of my 7 test profiles, even for a user who asked for "happy pop." Gym Hero is very energetic and not acoustic, so it earns near-full points for energy and for the "not acoustic" bonus, no matter what else the user wants. Genre is worth twice as much as the best energy score, but there is only one rock song and two pop songs, so once the genre match runs out, energy alone fills the list. This creates a small filter bubble: loud, high-energy songs crowd out everything else for anyone who likes energetic music.

Another gap: the catalog has no "sad" mood at all. A user who wants sad songs gets matched on energy only, so the mood they asked for is ignored.

---

## 7. Evaluation  

**Profiles tested.** I tested seven profiles and looked at the top 5 songs for each. The full output is in the README.

- Standard: High-Energy Pop, Chill Lofi, Deep Intense Rock
- Adversarial: Sad but Energetic, Genre Not in Catalog, Acoustic EDM, Dead-Center Energy

I also ran one experiment: I turned the mood weight to 0 and ran all seven profiles again (details in the README). Removing mood made High-Energy Pop put *Gym Hero* ahead of *Sunrise City*, which is worse for someone who asked for "happy." So mood matters, and the original weights were better.

**What surprised me.**

- *Iron Throne* (metal) ranks below EDM and pop for a rock fan. The genre rule only checks for an exact match, so it cannot see that metal is close to rock.
- "Sad but Energetic" gets the same five songs as "Deep Intense Rock," just in a slightly different order. With no genre or mood match, the system just picks the loudest songs.
- The Acoustic EDM user says they like acoustic music, but still gets a song with almost no acoustic sound at #1. The acoustic bonus is too small to matter much.

**Comparing every pair of profiles.** "Shared" is how many of the 5 songs appear in both lists.

| Pair | Shared | What changed, and why it makes sense |
|--------------------------------|---|-----------------|
| High-Energy Pop vs. Chill Lofi | 0 | Loud pop turns into quiet lofi. The energy targets are 0.5 apart and the genre is different. |
| High-Energy Pop vs. Deep Intense Rock | 4 | Both want loud songs. Only the #1 changes (Sunrise City vs. Storm Runner). Gym Hero is #2 for both: for pop it matches the genre, for rock it matches "intense." |
| High-Energy Pop vs. Sad but Energetic | 4 | The sad profile has no genre or mood match, so loudness picks the songs. Pop gets Rooftop Lights (a "happy" match); the sad profile gets Iron Throne (louder). |
| High-Energy Pop vs. Genre Not in Catalog | 3 | With no pop to match, scores drop from about 4.3 to 2.4. But "happy" and energy 0.8 still bring up Sunrise City and Rooftop Lights, which is a sensible fallback. |
| High-Energy Pop vs. Acoustic EDM | 4 | Both want very loud songs, so the lists are alike. The EDM profile just puts Neon Overdrive first because of its genre match. |
| High-Energy Pop vs. Dead-Center Energy | 0 | Energy 0.9 vs. 0.5, and pop vs. jazz. Nothing overlaps, which is correct. |
| Chill Lofi vs. Deep Intense Rock | 0 | Opposites: quiet acoustic songs vs. loud intense ones. This is the clearest proof that the scoring separates "chill" from "intense." |
| Chill Lofi vs. Sad but Energetic | 0 | Quiet songs vs. the loudest songs in the catalog. Energy is the main reason. |
| Chill Lofi vs. Genre Not in Catalog | 0 | Energy 0.4 vs. 0.8 and "chill" vs. "happy," so the lists do not meet. |
| Chill Lofi vs. Acoustic EDM | 0 | Both say they like acoustic music, yet the lists share nothing. Energy outweighs the acoustic preference, which shows how small that bonus is. |
| Chill Lofi vs. Dead-Center Energy | 1 | Both want lower energy and share Coffee Shop Stories. Lofi has three matching songs, so its top 3 are all lofi. Jazz has only one, so its list drops off after #1. |
| Deep Intense Rock vs. Sad but Energetic | 5 | Same five songs. "Rock/intense" gets Storm Runner first because it matches genre and mood. "Blues/sad" matches nothing, so Gym Hero (loudest) goes first. |
| Deep Intense Rock vs. Genre Not in Catalog | 2 | Both like high energy, but the k-pop profile wants 0.8 and "happy," so it shifts toward Sunrise City and Rooftop Lights. They share only Gym Hero and Sunrise City. |
| Deep Intense Rock vs. Acoustic EDM | 4 | Very similar energy targets (0.92 and 0.95). The only real difference is which genre match comes first: Storm Runner or Neon Overdrive. |
| Deep Intense Rock vs. Dead-Center Energy | 0 | Energy 0.92 vs. 0.5, and rock vs. jazz. They want different music. |
| Sad but Energetic vs. Genre Not in Catalog | 2 | Neither matches a genre. The sad profile ranks by energy 0.9, the k-pop profile also uses "happy," so only Gym Hero and Sunrise City overlap. |
| Sad but Energetic vs. Acoustic EDM | 4 | Both want very loud songs. The EDM profile has one genre and mood match (Neon Overdrive) and the rest of the list looks the same. |
| Sad but Energetic vs. Dead-Center Energy | 0 | Energy 0.9 vs. 0.5. Nothing is shared, which is expected. |
| Genre Not in Catalog vs. Acoustic EDM | 2 | Energy 0.8 vs. 0.95 and "happy" vs. "euphoric." They share only Rooftop Lights and Gym Hero. |
| Genre Not in Catalog vs. Dead-Center Energy | 2 | They share Block Party Anthem and Night Drive Loop. With no genre match, or only one, both lists fill up with songs near the energy target. |
| Acoustic EDM vs. Dead-Center Energy | 0 | Energy 0.95 vs. 0.5, EDM vs. jazz. Opposite tastes. |

---

## 8. Future Work  

1. **Smarter genre matching.** Treat close genres as partly matching, so metal counts as near rock instead of being treated like any other genre.
2. **Learn from behavior.** Use skips, replays, and playlists instead of only what the user says they like, so the weights can be tuned from real feedback.
3. **A bigger, more balanced catalog.** Add many more songs, more middle-energy songs, and missing moods such as "sad."

(I already added a diversity penalty as an optional extra. It helps, but it only swaps songs in the top 5. It cannot fix a catalog that is too small.)

---

## 9. Personal Reflection  

**Biggest learning moment.** I learned how a system can turn preferences into recommendations. My version only uses what the user *says* they like. Real apps also watch what people actually do, such as skips, replays, and playlists, and learn from that. That gap between stated taste and observed behavior was the biggest thing I took away.

**How AI helped, and when I double-checked it.** AI helped me plan the scoring rules, write the code, and find weak spots. But I did not trust the numbers on their own. I recalculated scores by hand and compared them to the program's output. I also caught problems that the AI had not predicted. For example, running `main.py` directly from my editor gave a `FileNotFoundError`, because the data path depended on where I ran it from. Some editor warnings were also out of date, so I checked by actually running the code and the tests.

**What surprised me.** A handful of simple rules produced lists that felt like real recommendations. Chill Lofi looked just right. But the same simple rules also made *Gym Hero* show up for almost every high-energy user. It looks like taste, but it is just arithmetic. That is how a small bias can look like a personal recommendation.

**What I would try next.** I went on to try all four optional challenges: more song features, different scoring modes, a diversity rule, and a clearer results table. They helped, but they did not fix the deeper limits: the catalog is tiny, and genre is matched exactly. Next I would try smarter genre matching, a much bigger catalog, and a version that learns from what a user actually plays or skips.
