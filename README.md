# DarGameProcessor
Categorizes sports games for MLB, NHL, NBA, NCAAB, NFL

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Git (for cloning the repository)

### Installation Steps

1. Clone the repository:

```bash
git clone git@github.com:ArminRezz/DarGameProcessor.git
cd DarGameProcessor
```

2. Create a virtual environment:
```bash
python -m venv dar_game_python_env
```

3. Activate the virtual environment:

**On macOS/Linux:**
```bash
source dar_game_python_env/bin/activate
```

**On Windows:**
```bash
dar_game_python_env\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

### Verify Installation
1. Confirm you're in the virtual environment:
- Your terminal prompt should show `(dar_game_python_env)`
- Run `which python` (Unix) or `where python` (Windows) to verify it points to the virtual environment

2. Test the installation:
```bash
python gui.py
```

### Common Issues
If you encounter `ModuleNotFoundError`:
1. Ensure your virtual environment is activated
2. Try reinstalling dependencies:
```bash
pip install -r requirements.txt
```

### Deactivating the Environment
When you're done working:
```bash
deactivate
```

### Rules Framework for Labeling

##### NBA (National Basketball Association)

_Applies to daily games, typically between 7 PM - 10 PM ET:_
- **Monday (Public Day)** – First game is Vegas, then alternates (7 PM same slots are all Vegas).
- **Tuesday (Vegas Day)** – First game is Public, then alternates.
- **Wednesday (Public Day)** – First game is Vegas, then alternates.
- **Thursday (Vegas Day)** – First game is Public, then alternates.
- **Friday (Public Day)** – First game is Vegas, then alternates.
- **Saturday (Vegas Day)** – First game is Public, then alternates.
- **Sunday (Vegas Day)** – First game is Public, then alternates.

✔ Back-to-back games impact line movement.  
✔ Late games (West Coast) often favor Vegas movements.

---

##### NFL (National Football League)

_Weekly games, different schedule from daily sports like NBA/NHL:_
- **Thursday Night Football (Vegas Day)** – Short prep week, favors Vegas lines.
- **Sunday 1 PM (Public Games)** – Heavy casual bettor action, public sides stronger.
- **Sunday 4 PM (Vegas Games)** – Sharper betting movement, more line shifts.
- **Sunday Night Football (Vegas Game)** – Prime-time, sharp money shapes late action.
- **Monday Night Football (Public Game)** – Standalone, public teams get more money.

✔ Public bets favor favorites, overs, and big-name teams.  
✔ Sharp action usually hits Sunday morning and before prime-time games.

---

##### NHL (National Hockey League)

_Follows a similar structure to NBA due to daily games:_
- **Monday (Public Day)** – First game Vegas, then alternates.
- **Tuesday (Vegas Day)** – First game Public, then alternates.
- **Wednesday (Public Day)** – First game Vegas, then alternates.
- **Thursday (Vegas Day)** – First game Public, then alternates.
- **Friday (Public Day)** – First game Vegas, then alternates.
- **Saturday (Vegas Day)** – First game Public, then alternates.
- **Sunday (Vegas Day)** – First game Public, then alternates.

✔ Low-scoring nature makes puck lines important.  
✔ Public tends to overbet favorites and overs.

---

##### MLB (Major League Baseball)

_162-game season, many games per day, different start times:_
- **Monday:** Public Day
- **Tuesday:** Vegas Day
- **Wednesday:** Hybrid (first half public, 5:40 PM CST Vega ====> aka 6:40 PM EST)
- **Thursday:** Vegas Day
- **Friday:** Public Day
- **Saturday:** Vegas Day
- **Sunday:** Vegas Day

✔ Early games (1 PM - 4 PM) tend to favor Vegas betting trends.  
✔ Public loads up on big-name pitchers & home teams.  
✔ Late games often have sharper movement.

---

##### NCAAF (College Football)

_Mostly played on Thursdays, Fridays, and Saturdays, with some weekday games:_
- **Thursday Games (Vegas Day)** – Short rest, favors Vegas oddsmakers.
- **Friday Games (Vegas Day)** – Smaller slate, sharper betting impact.
- **Saturday Early Games (Public Games)** – Heavy action on ranked teams.
- **Saturday Afternoon (Vegas Games)** – Line movements are sharpest here.
- **Saturday Night (Mixed Vegas/Public Games)** – Public bets build, but sharp money moves lines.

✔ Public heavily bets ranked teams and favorites.  
✔ Vegas adjusts heavily for injury news and motivation factors.

---

##### NCAAB (College Basketball)

_Follows a daily game schedule but varies during March Madness:_
- **Monday (Public Day)** – First game Vegas, then alternates.
- **Tuesday (Vegas Day)** – First game Public, then alternates.
- **Wednesday (Public Day)** – First game Vegas, then alternates.
- **Thursday (Vegas Day)** – First game Public, then alternates.
- **Friday (Public Day)** – First game Vegas, then alternates.
- **Saturday (Vegas Day)** – First game Public, then alternates.
- **Sunday (Vegas Day)** – First game Public, then alternates.

✔ March Madness shifts betting patterns (huge public influence).  
✔ Public overbets favorites and overs.  
✔ Vegas adjustments are sharpest in the second half of the season.