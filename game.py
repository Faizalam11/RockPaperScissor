import sqlite3
import random
import sys
def print_scoreboard(cursor, limit=None):
    if limit == None:
        scoreboard = cursor.execute(f"SELECT * FROM RPS_GAME ORDER BY Score DESC;").fetchall()
    else:
        scoreboard = cursor.execute(f"SELECT * FROM RPS_GAME ORDER BY Score DESC LIMIT {limit};").fetchall()
    for i in range(len(scoreboard)):
        print(f"{i+1}) {scoreboard[i][0]} scored {scoreboard[i][1]}")
conn = sqlite3.connect('RPSgame.db')
c=conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS RPS_GAME(
	'Player_Name' text PRIMARY KEY,
	'Score' Integer
);""")
conn.commit()
map = {
1 : "Rock",
2 : "Paper",
3 : "Scissor",
"r" : 1,
"p" : 2,
"s" : 3 }
name=input('Enter Player name : ')
query = c.execute(f"SELECT * FROM RPS_GAME WHERE Player_Name = '{name}';").fetchone()
if query != None:
    Player_Score = query[1]
else:
    Player_Score = 0
print("\nPress e to exit:\nPress sc to view every player score:\nPress l to view leaderboard:\n")
while True:
    computer = random.randint(1, 3)
    Player = input("Select Rock, Paper or Scissor (r/p/s):")
    if Player == "e":
        if query == None:
            c.execute(f"INSERT INTO RPS_GAME(Player_Name,Score) VALUES ('{name}',{Player_Score});")
        else:
            c.execute(f"UPDATE RPS_GAME SET Score = {Player_Score} where Player_Name = '{name}';")
        conn.commit()
        print("Leaderboard:")
        print_scoreboard(c,10)
        conn.close()
        sys.exit()
    if Player == "l":
        print("Leaderboard:")
        print_scoreboard(c,10)
        continue
    if Player == "sc":
        print("Scoreboard:")
        print_scoreboard(c)
        continue
    if Player not in ['r', 'p', 's']:
        print("[WARNING] Please use correct input!!! [WARNING]")
        continue
    Player = map[Player]
    print(f"{name} uses {map[Player]}!")
    print(f"Computer uses {map[computer]}!")
    if Player == computer:
        print('Match Tied!!!')
    elif (Player == 1 and computer == 3) or (Player == 2 and computer == 1) or (Player == 3 and computer == 2):
        print(f'{name} Wins!')
        Player_Score += 1
        print(f"{name} have scored {Player_Score} points.")
    else:
        print('Computer Wins!')
        Player_Score -= 1
        print(f"{name} have scored {Player_Score} points.")
