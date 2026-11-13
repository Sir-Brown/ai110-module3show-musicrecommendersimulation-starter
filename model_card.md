# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  