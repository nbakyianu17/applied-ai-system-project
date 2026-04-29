# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

I wanted something that sounded like it actually does something. It finds vibes. That's it.

---

## 2. Goal / Task

The goal is simple: given a user's music preferences, find the songs in a small catalog that match best.

It does not learn over time. It does not know your history. You tell it what you like upfront — genre, mood, energy level — and it scores every song in the catalog against those preferences. Then it returns the top 5.

Think of it like asking a friend who has memorized a playlist of 20 songs: "Hey, I want something chill and instrumental right now." The friend goes through every song in their head, picks the five that fit, and explains why.

---

## 3. Data Used

The catalog is a CSV file with 20 songs. I started with 10 (that came with the project) and added 10 more myself to cover genres that weren't there.

Each song has 13 attributes:
- **Genre** — like lofi, pop, rock, jazz, metal, classical, etc.
- **Mood** — like happy, chill, focused, melancholic, aggressive, peaceful, etc.
- **Energy** — a number from 0 to 1. Low energy = sleepy, high energy = hype.
- **Valence** — how happy or dark the song sounds. High = bright, low = sad.
- **Tempo** — how fast it is in beats per minute.
- **Acousticness** — is it guitar-and-piano or electronic beats?
- **Bass level** — how heavy the bass hits.
- **Instrumentalness** — how much of it is just music with no singing.
- **Speechiness** — how much rapping or talking is in it.
- **Danceability** — can you dance to it? (I ended up not using this in scoring.)

**Limits of the data:**
- 20 songs is tiny. Real platforms have millions.
- Most genres only have one song. So if you like classical, you always get the same #1 no matter what.
- The catalog is mostly English-language western music. Afrobeats, K-pop, Bollywood — not here.
- I made up some of the numeric values myself. They are educated guesses, not real audio analysis.

---

## 4. Algorithm Summary

Here is how it works in plain English, no code.

Every song gets a score out of **7 points total**. The scoring has two parts:

**Part 1 — Does it match the category?**
- If the genre matches what the user wants: **+2 points**
- If the mood matches: **+1 point**
- If either one is wrong: **zero points for that feature**

No in-between. It either matches or it doesn't.

**Part 2 — How close are the numbers?**
For features like energy, valence, and tempo, the system checks the gap between what the user wants and what the song actually has. The smaller the gap, the more points. A perfect match gets full points. A huge gap gets almost nothing.

- Energy: up to **+1.0 points**
- Valence: up to **+0.75 points**
- Instrumentalness: up to **+0.75 points**
- Acousticness: up to **+0.50 points**
- Tempo: up to **+0.50 points** (after normalizing the BPM to a 0–1 scale)
- Bass level: up to **+0.25 points**
- Speechiness: up to **+0.25 points**

Once every song has a score, the system sorts them highest to lowest and returns the top 5.

I chose to weight genre the most (2 points) because I felt like being in the wrong genre immediately ruins a recommendation, no matter how good the other features are. If I'm in the mood for jazz, getting a pop song — even a soft, chill pop song — is still wrong.

---

## 5. Observed Behavior and Biases

Honestly this was the most eye-opening part of the project.

**The genre filter bubble is real.**
Because genre is worth 28% of the total score, songs in the wrong genre almost never break into the top 5 — even if everything else about them is a perfect match. I tested a classical music fan profile. The system returned one great result (#1 at 6.96/7.0) and then four random-ish songs from jazz and lofi because no other classical songs existed. The system wasn't broken. The data just wasn't good enough for that user type.

**"Gym Hero" keeps showing up everywhere.**
This song (pop, intense, energy=0.93) appeared in the top 5 for the pop profile AND the rock profile. Not because it's a perfect fit for rock, but because it's the highest-energy song in the catalog and the scoring formula rewards energy closeness. I started calling it the "loud neighbor" — it shows up uninvited because it scores well on numbers, not because it sounds right.

**Mood is too strict.**
"Chill" and "focused" feel very similar to me as a listener — both describe a calm headspace. But the system treats them as completely different. A "chill" song gets zero mood points for a "focused" user. This causes a big drop-off between #1 and #2 in some profiles, which feels unfair.

**The "sad banger" test broke things.**
I tried a profile with high energy (0.90) but a sad/dark mood. The results were all over the place — metal, blues, pop, all in the same top 5. The system wasn't doing anything wrong mathematically, but the output felt incoherent. When preferences conflict, the system gets confused just like a person would.

**Quiet listeners get stuck.**
If your target energy is below 0.35, you will keep seeing the same cluster of ambient, lofi, and classical songs. There is no mechanism to break out of that bubble or introduce something surprising.

---

## 6. Evaluation Process

I tested six user profiles total.

**The three main ones:**
- **High-Energy Pop** — wanted happy, upbeat, fast pop music
- **Chill Lofi** — wanted calm, focused, instrumental music for studying
- **Deep Intense Rock** — wanted heavy, fast, aggressive rock

**The three edge cases I designed to break it:**
- **Sad Bangers** — high energy but dark and melancholic mood (conflicting signals)
- **Classical Fan** — a genre with only one song in the catalog (scarcity test)
- **Perfectly Average** — all numeric targets at 0.5, no strong preferences (ambiguity test)

I also ran one experiment: I cut the genre weight in half (2.0 → 1.0) and doubled the energy weight (1.0 → 2.0). The top-1 results stayed the same across all profiles, but positions 3–5 got messier — songs from the wrong genres started creeping in. That confirmed that the original genre weight was doing important work even when it felt too strict.

What surprised me most was how well the "obvious" profiles worked (lofi, rock) and how badly the system fell apart for edge cases. A real user with unusual taste would have a pretty frustrating experience with this system.

---

## 7. Intended Use and Non-Intended Use

**What this is for:**
- Learning how recommendation algorithms work
- A classroom project exploring content-based filtering
- Experimenting with how weights and features affect results
- Understanding what data a real system might need

**What this is NOT for:**
- Real music discovery. The catalog is 20 songs. You will run out immediately.
- Any user who prefers music outside the genres in the dataset.
- Replacing a real music app. Please do not cancel your Spotify subscription because of this.
- Anything involving actual audio analysis. The numeric values were assigned by hand, not computed from real audio.
- Making decisions about people's taste in a consequential way. This is a toy, not a product.

---

## 8. Ideas for Improvement

**1. Genre families instead of exact genre match.**
Right now "lofi" and "jazz" earn zero points from each other even though many people like both. I'd create genre groups — like "low-key" for lofi, ambient, and jazz — and give partial credit when songs are in the same family. That would reduce the filter bubble without removing genre as a signal.

**2. Mood similarity instead of on/off matching.**
I'd build a small table that shows how similar moods are to each other. "Chill" and "focused" would score 0.8 similarity. "Euphoric" and "melancholic" would score 0.1. Songs with a close-but-not-exact mood would earn partial points instead of zero.

**3. A much bigger catalog and real audio features.**
The biggest limit is 20 songs. With 200 songs per genre and audio features computed from actual sound files (not assigned by hand), the system would produce meaningfully different results for different users in the same genre. Right now it often feels like the system recommends "the only option available" rather than "the best match."

---

## 9. Responsible AI Reflection

### Limitations and Biases

The most significant bias in this system is structural: genre carries 28% of the total score (2.0 out of 7.0 points), which means a song from the "wrong" genre almost never appears in the top 5 even if every other feature is a near-perfect match. This creates a filter bubble by design. A lofi listener will never discover a jazz track that feels identical in practice — the label mismatch alone buries it.

Mood compounds this. "Chill" and "focused" are treated as completely different categories with no partial credit, even though most listeners experience them as nearly interchangeable. The result is that the system's top-5 lists feel coherent for common taste profiles (pop, lofi, rock) and hollow for anyone whose preferences don't map cleanly onto the genre/mood taxonomy the catalog was built around.

The catalog itself carries a deeper bias: 20 songs, mostly English-language Western music, with numeric feature values assigned by hand rather than computed from actual audio. The system's taste was shaped by whoever built the catalog and chose those values — which in this case was one person. There is no Afrobeats, K-pop, Bollywood, or regional genre representation. A listener whose musical identity sits outside the catalog's frame is not an edge case; they are simply invisible.

Finally, the system assumes preference stability. It applies the same profile every time, with no way to account for context — the same person might want something completely different at 7am versus 11pm, while working versus commuting. That context-blindness is a known limitation of static content-based filtering.

---

### Could This AI Be Misused?

This specific system is low-stakes — it recommends songs from a 20-track catalog. Direct harm is unlikely. But the design patterns it uses appear in higher-stakes systems, and those patterns carry real misuse risks worth naming.

**Filter bubble amplification.** A recommender that over-weights categorical features (genre, mood) and ignores cross-genre discovery will, at scale, narrow what people hear rather than expand it. Applied to news, job listings, or social content, the same logic actively limits what people encounter and can reinforce existing preferences in ways that are hard to detect or reverse.

**Catalog bias as silent exclusion.** If the underlying data doesn't represent a group, the system won't serve that group — and it won't announce that failure. It will just quietly return worse results. At scale and in higher-stakes domains, this becomes discriminatory in effect even without discriminatory intent.

**Preventing misuse in this system:** The explainability built into the scoring (every recommendation includes a feature-by-feature breakdown) is the most important safeguard. Users can see exactly why a result ranked where it did, which makes the system's assumptions auditable. For a production system, I would add: explicit catalog diversity monitoring, a mechanism to surface when a user's preferences are underrepresented in the data, and human review of recommendations for any new genre or demographic the system hasn't been evaluated against.

---

### What Surprised Me During Reliability Testing

Two things stood out.

First, the three "normal" profiles (pop, lofi, rock) scored between 6.75 and 6.92 out of 7.0 — almost perfect — while the edge cases dropped sharply to around 5.74 (Sad Bangers) and 4.97 (Perfectly Average). I expected the edge cases to score lower, but not by that much. The gap revealed how dependent the system is on having strong, consistent preference signals. When genre, mood, and energy all point in the same direction, the engine becomes highly confident very quickly. When they conflict or flatten out, it almost has nothing to work with.

Second, the "Perfectly Average" profile — all numeric targets at 0.5 and a genre with only one song in the catalog — produced a 71% confidence score on its top result, but positions 2 through 5 were essentially arbitrary. The confidence score looks reasonable at the top level, but it masks how meaningless the rest of the list is. That's a subtle reliability problem: aggregate metrics can look fine while the system's actual usefulness for that user type has already collapsed. In a real product, that user would churn without ever knowing why.

---

### AI Collaboration on This Project

I used Claude throughout this project — for coding help, debugging, writing, and working through design decisions. The collaboration was genuinely useful, but not uniformly so.

**A helpful suggestion:** When I was designing the scoring formula, I asked Claude whether tempo should be scored on its raw BPM value or normalized. Claude pointed out that without normalization, a tempo target of 128 BPM and a song at 80 BPM would score a raw gap of 48 — far larger than any gap possible on the 0–1 features — and that this would let tempo dominate the result in a way that had nothing to do with its intended weight. It suggested normalizing tempo to a 0–1 scale using the catalog's BPM range before applying the proximity formula. That was the right call, and it's now part of the final implementation. Without that, the scoring would have been silently broken in a way that was hard to spot just by reading the code.

**A flawed suggestion:** At one point Claude proposed using `danceability` as a scored feature alongside energy and valence. It generated a plausible-sounding justification — that danceability captures something distinct from energy, specifically the rhythmic regularity of a beat. When I tested it, adding danceability as a scored feature produced almost no change in the top-1 results across all six profiles but increased score noise in positions 3–5, making weaker matches appear more similar than they actually were. The feature was adding weight without adding signal. I removed it from scoring and kept it as a stored attribute only. The lesson: AI suggestions that sound well-reasoned still need to be tested empirically. A convincing rationale is not the same as a working feature.

---

## 10. Personal Reflection

Honestly, I came into this project pretty confused. I understood conceptually that Spotify "learns what you like," but I had no idea what that actually meant in terms of code. Watching a simple list of numbers turn into what feels like a recommendation — that was the click moment for me.

The biggest thing I learned is that every recommendation system is really just a series of choices someone made. Someone decided genre should matter more than tempo. Someone decided mood should be an exact match instead of a spectrum. Those choices seem small when you're writing them, but when you run the system against six different user types, you start to see exactly who wins and who loses based on those decisions. The system I built works great for pop and lofi listeners, and it basically fails classical and country listeners. That's not random — it's a direct consequence of the choices I made and the data I included.

Using AI tools (Claude and Copilot) genuinely helped me move faster than I expected. When I got stuck on the CSV loading logic or wasn't sure how to structure the scoring function, I could describe what I wanted in plain English and get working code back. But I had to double-check a lot of it. A few times the AI gave me code that looked right but had a subtle bug — like the tempo normalization producing values slightly above 1.0 for tempos above 160 BPM. If I'd just trusted it and moved on I wouldn't have caught that.

What surprised me most was how quickly the system started *feeling* like real recommendations even though the logic is incredibly simple. When Focus Flow showed up at 6.91/7.0 for the study session profile, I actually thought "yeah, that tracks." It wasn't magic — it was just math that matched the numbers I put in. But it felt like the computer understood something. That gap between "it's just math" and "it feels like understanding" is probably what makes AI seem so mysterious to most people, and now I feel like I have a slightly better handle on where that feeling comes from.

If I kept going, I'd want to try collaborative filtering — building a second version that recommends based on what similar users listened to rather than song attributes. I'd also want to add a "surprise me" mode that intentionally introduces one song per session that doesn't quite fit the profile, just to see if the user discovers something new. That's what I always hope Spotify will do for me, and it almost never does.
