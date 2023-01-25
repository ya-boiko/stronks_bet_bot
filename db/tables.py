from Db import Db


db = Db("stronks_bot.db")

# таблица "Команды"
db.execute("""
    CREATE TABLE IF NOT EXISTS teams(
        id INT,
        name TEXT DEFAULT '',
        emoji TEXT DEFAULT '',
        code TEXT DEFAULT ''
    );
""")

# таблица "События"
db.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INT,
        team_id_1 INT,
        team_id_2 INT,
        tour_stage_id INT,
        winner INT DEFAULT -1
    );
""")

# таблица "Матчи"
db.execute("""
    CREATE TABLE IF NOT EXISTS matches(
        id INT,
        event_id INT,
        home_team INT DEFAULT 1,
        result TEXT DEFAULT '0:0',
        day TEXT,
        is_over INT DEFAULT 0,
        winner INT DEFAULT -1
    );
""")

# таблица "Турниры"
db.execute("""
    CREATE TABLE IF NOT EXISTS tours(
        id INT,
        name TEXT
    );
""")

# таблица "Стадии"
db.execute("""
    CREATE TABLE IF NOT EXISTS stages(
        id INT,
        name TEXT
    );
""")

# таблица "Стадии турнира"
db.execute("""
    CREATE TABLE IF NOT EXISTS tour_stages(
        id INT,
        tour_id INT,
        stage_id INT,
        is_active INT DEFAULT 0 
    );
""")

# таблица "Ставки"
db.execute("""
    CREATE TABLE IF NOT EXISTS bets(
        id INT,
        event_id INT DEFAULT NULL,
        match_id INT DEFAULT NULL,
        name TEXT DEFAULT '',
        who_winner INT DEFAULT NULL, 
        bet_won INT DEFAULT NULL 
    );
""")

# таблица "Ставки пользователя"
db.execute("""
    CREATE TABLE IF NOT EXISTS user_bets(
        user_id INT,
        bet_id INT DEFAULT NULL
    );
""")

# таблица "Ставки пользователя"
db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        tg_id TEXT,
        login TEXT DEFAULT '',
        name TEXT DEFAULT '',
        surname TEXT DEFAULT ''
    );
""")
