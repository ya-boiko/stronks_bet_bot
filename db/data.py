from Db import Db
from settings import DB_NAME


db = Db(DB_NAME)

# db.insert("INSERT INTO teams(id, name, code, emoji) VALUES (?, ?, ?, ?);",
#           [
#               (1, 'Реал', 'real', '🇪🇸'),
#               (2, 'ПСЖ', 'paris', '🇫🇷'),
#               (3, 'Айнтрахт Ф', 'aintraht_f', '🇩🇪'),
#               (4, 'Наполи', 'napoli', '🇮🇹'),
#               (5, 'Боруссия Д', 'borussia_d', '🇩🇪'),
#               (6, 'Челси', 'chelsi', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
#               (7, 'Ливерпуль', 'liverpool', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
#               (8, 'Милан', 'milan', '🇮🇹'),
#               (9, 'Тоттенхэм', 'tottenham_h', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
#               (10, 'Интер', 'inter', '🇮🇹'),
#               (11, 'Порту', 'porto', '🇵🇹'),
#               (12, 'Бавария', 'bavaria', '🇩🇪'),
#               (13, 'РБ Лейпциг', 'rb_leipzig', '🇩🇪'),
#               (14, 'Манчестер Сити', 'man_city', '🏴󠁧󠁢󠁥󠁮󠁧󠁿'),
#               (15, 'Брюгге', 'brugge', '🇧🇪'),
#               (16, 'Бенфика', 'benfika', '🇵🇹'),
#           ])
#
#
# db.insert("INSERT INTO events(id, team_id_1, team_id_2, tour_stage_id) VALUES (?, ?, ?, ?);",
#           [
#               (1, 13, 14, 1),
#               (2, 15, 16, 1),
#               (3, 7, 1, 1),
#               (4, 8, 9, 1),
#               (5, 3, 4, 1),
#               (6, 5, 6, 1),
#               (7, 10, 11, 1),
#               (8, 2, 12, 1)
#           ])
#
# db.insert("INSERT INTO matches(id, event_id, home_team, day) VALUES (?, ?, ?, ?);",
#           [
#               (1, 1, 1, '14.02.2023'),
#               (2, 2, 1, '14.02.2023'),
#               (3, 3, 1, '14.02.2023'),
#               (4, 4, 1, '14.02.2023'),
#               (5, 5, 1, '14.02.2023'),
#               (6, 6, 1, '14.02.2023'),
#               (7, 7, 1, '14.02.2023'),
#               (8, 8, 1, '14.02.2023'),
#               (9, 1, 2, '07.03.2023'),
#               (10, 2, 2, '07.03.2023'),
#               (11, 3, 2, '07.03.2023'),
#               (12, 4, 2, '07.03.2023'),
#               (13, 5, 2, '07.03.2023'),
#               (14, 6, 2, '07.03.2023'),
#               (15, 7, 2, '07.03.2023'),
#               (16, 8, 2, '07.03.2023'),
#           ])
#
# db.insert("INSERT INTO tours(id, name) VALUES (?, ?);",
#           [
#               (1, "Лига чемпионов (сезон 2022-2023)"),
#           ])
#
# db.insert("INSERT INTO stages(id, name) VALUES (?, ?);",
#           [
#               (1, "1/8 финала"),
#               (2, "1/4 финала"),
#               (3, "1/2 финала"),
#               (4, "Финал"),
#           ])
#
# db.insert("INSERT INTO tour_stages(id, tour_id, stage_id, is_active) VALUES (?, ?, ?, ?);",
#           [
#               (1, 1, 1, 1),
#               (2, 1, 2, 0),
#               (3, 1, 3, 0),
#               (4, 1, 4, 0),
#           ])


def create_event_bets(db):
    events = db.query("""
        SELECT e.id, t1.name, t2.name, t1.emoji, t2.emoji FROM events e
        join teams t1 on t1.id = e.team_id_1
        join teams t2 on t2.id = e.team_id_2
        WHERE e.winner = -1 AND e.id NOT IN (SELECT event_id FROM bets);
    """)

    bet_id = 1

    params = []
    for event in events:
        for i in [1, 2]:
            bet = (
                bet_id,
                event[0],
                None,
                f"Пройдет {event[i]} {event[i+2]}",
                i,
                None
            )
            params.append(bet)
            bet_id += 1

    db.insert("INSERT INTO bets(id, event_id, match_id, name, who_winner, bet_won) VALUES (?, ?, ?, ?, ?, ?);",
              params)


create_event_bets(db)
