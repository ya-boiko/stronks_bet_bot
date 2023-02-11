import datetime

from db.Db import Db


class DbQuery(Db):
    def get_all_tours(self):
        return self.query("""
            SELECT t.id AS id, 
                   t.name AS name
            FROM tours t;
        """)

    def get_all_tour_stages(self):
        return self.query("""
            SELECT ts.id AS id, 
                   ts.tour_id AS tour_id,
                   ts.stage_id AS stage_id,
                   ts.is_active AS is_active
            FROM tour_stages ts;
        """)

    def get_all_events(self):
        return self.query("""
            SELECT e.id AS id, 
                   e.team_id_1 AS team_id_1,
                   e.team_id_2 AS stage_id,
                   e.tour_stage_id AS tour_stage_id,
                   e.winner AS winner
            FROM events e;
        """)

    def get_coming_bets(self):
        return self.query("""
            SELECT b.id as id,
                   b.event_id as event_id, 
                   b.match_id as match_id, 
                   b.name as name,
                   b.bet_won as bet_won
            FROM bets b
            WHERE b.bet_won IS NULL;
        """)

    def get_active_tour_stages_by_tour_id(self, tour_id):
        return self.query("""
            SELECT ts.id AS tour_stage_id,
                   t.name AS tour_name,
                   s.name AS stage_name
            FROM tour_stages ts
             JOIN tours t ON t.id = ts.tour_id
             JOIN stages s ON s.id = ts.stage_id
            WHERE ts.tour_id = {0} AND ts.is_active = 1;
        """.format(tour_id))

    def get_events_by_tour_stage_id(self, tour_stage_id):
        return self.query("""
            SELECT ev.id AS event_id,
                   t1.code AS team1_code,
                   t1.name AS team1_name,
                   t1.emoji AS team1_emoji,
                   t2.code AS team2_code,
                   t2.name AS team2_name,
                   t2.emoji AS team2_emoji,
                   s.name  AS stage_name,
                   ev.winner as winner
            FROM events ev
             JOIN teams t1 ON t1.id = ev.team_id_1
             JOIN teams t2 ON t2.id = ev.team_id_2
             JOIN tour_stages ts ON ts.id = ev.tour_stage_id
             JOIN stages s ON s.id = ts.stage_id
            WHERE ev.tour_stage_id = {0};
        """.format(tour_stage_id))

    def get_bets_by_event_id(self, event_id):
        return self.query("""
            SELECT b.id AS bet_id,
                   b.name AS bet_name,
                   t1.name AS team1_name,
                   t1.emoji AS team1_emoji,
                   t2.name AS team2_name,
                   t2.emoji AS team2_emoji
            FROM bets b
             JOIN events ev ON ev.id = b.event_id
             JOIN teams t1 ON t1.id = ev.team_id_1
             JOIN teams t2 ON t2.id = ev.team_id_2
            WHERE b.event_id = {0};
        """.format(event_id))

    def add_user_bet(self, user_id, bet_id):
        query = """
            INSERT INTO user_bets (user_id, bet_id)
            VALUES (?, ?)
        """
        self.insert(
            query,
            [(user_id, bet_id)]
        )

    def get_bet_name_by_id(self, bet_id):
        return self.query_fetchone("""
            SELECT b.name AS name
            FROM bets b
            WHERE b.id = {0};
        """.format(bet_id)).get("name")

    def check_user_bet_on_event(self, user_id, event_id):
        return self.query_fetchone("""
            SELECT ub.user_id as user_id,
                   ub.bet_id as bet_id,
                   b.event_id as event_id,
                   b.match_id as match_id,
                   b.name as bet_name,
                   b.bet_won as bet_won
            FROM user_bets ub
            JOIN bets b on b.id = ub.bet_id
            WHERE ub.user_id = {0}
            AND b.event_id = {1};
        """.format(user_id, event_id))

    def get_event_by_id(self, event_id):
        return self.query_fetchone("""
            SELECT ev.id AS event_id,
                   t1.code AS team1_code,
                   t1.name AS team1_name,
                   t1.emoji AS team1_emoji,
                   t2.code AS team2_code,
                   t2.name AS team2_name,
                   t2.emoji AS team2_emoji,
                   s.name  AS stage_name
            FROM events ev
             JOIN teams t1 ON t1.id = ev.team_id_1
             JOIN teams t2 ON t2.id = ev.team_id_2
             JOIN tour_stages ts ON ts.id = ev.tour_stage_id
             JOIN stages s ON s.id = ts.stage_id
            WHERE ev.id = {0};
        """.format(event_id))

    def del_user_bet(self, user_id, bet_id):
        query = """
            DELETE FROM user_bets
            WHERE user_id = ?
            AND bet_id = ?;
        """
        self.insert(
            query,
            [(user_id, bet_id)]
        )

    def get_event_matches(self, event_id):
        return self.query("""
            SELECT m.id AS match_id,
                   ev.id AS event_id,
                   t1.code AS team1_code,
                   t1.name AS team1_name,
                   t1.emoji AS team1_emoji,
                   t2.code AS team2_code,
                   t2.name AS team2_name,
                   t2.emoji AS team2_emoji,
                   m.day AS match_day,
                   m.home_team AS home_team,
                   m.result AS result,
                   m.is_over AS is_over,
                   m.winner AS winner,
                   s.id  AS stage_id,
                   s.name  AS stage_name
            FROM matches m
             JOIN events ev ON ev.id = m.event_id
             JOIN teams t1 ON t1.id = ev.team_id_1
             JOIN teams t2 ON t2.id = ev.team_id_2
             JOIN tour_stages ts ON ts.id = ev.tour_stage_id
             JOIN stages s ON s.id = ts.stage_id
            WHERE ev.id = {0}
            ORDER BY m.id;
        """.format(event_id))

    def get_user_bets_on_tour_stage(self, user_id, tour_stage_id):
        return self.query("""
            SELECT ub.user_id as user_id,
                   ub.bet_id as bet_id,
                   b.event_id as event_id,
                   b.match_id as match_id,
                   b.name as bet_name,
                   b.bet_won as bet_won,
                   t1.name as team1_name,
                   t1.emoji as team1_emoji,
                   t2.name as team2_name,
                   t2.emoji as team2_emoji,
                   e.winner as winner,
                   s.name as stage_name,
                   t.name as tour_name
            FROM user_bets ub
            JOIN bets b on b.id = ub.bet_id
            JOIN events e on e.id = b.event_id
            JOIN teams t1 on t1.id = e.team_id_1
            JOIN teams t2 on t2.id = e.team_id_2
            JOIN tour_stages ts on ts.id = e.tour_stage_id
            JOIN tours t on t.id = ts.tour_id
            JOIN stages s on s.id = ts.stage_id
            WHERE ub.user_id = {0}
            AND e.tour_stage_id = {1}
            ORDER BY b.event_id;
        """.format(user_id, tour_stage_id))

    def add_user(self, tg_id, login, name, surname):
        query = """
            INSERT INTO users (tg_id, login, name, surname)
            VALUES (?, ?, ?, ?)
        """
        self.insert(
            query,
            [(tg_id, login, name, surname)]
        )

    def get_users(self):
        return self.query("""
            SELECT u.tg_id as tg_id,
                   u.login as login,
                   u.name as name,
                   u.surname as surname
            FROM users u;
        """)

    def get_user_by_tg_id(self, tg_id):
        return self.query_fetchone("""
            SELECT u.tg_id as tg_id,
                   u.login as login,
                   u.name as name,
                   u.surname as surname
            FROM users u
            WHERE u.tg_id = {0};
        """.format(tg_id))

    def get_users_bets_on_event(self, event_id):
        return self.query("""
            SELECT ub.user_id as user_id,
                   ub.bet_id as bet_id,
                   b.event_id as event_id,
                   b.match_id as match_id,
                   b.name as bet_name,
                   b.bet_won as bet_won,
                   t1.name as team1_name,
                   t1.emoji as team1_emoji,
                   t2.name as team2_name,
                   t2.emoji as team2_emoji,
                   e.winner as winner,
                   u.login as user_login,
                   u.name as user_name,
                   u.surname as user_surname
            FROM user_bets ub
            JOIN bets b on b.id = ub.bet_id
            JOIN events e on e.id = b.event_id
            JOIN teams t1 on t1.id = e.team_id_1
            JOIN teams t2 on t2.id = e.team_id_2
            JOIN users u on ub.user_id = u.tg_id
            WHERE b.event_id = {0}
            ORDER BY b.event_id;
        """.format(event_id))

    def update_match_info(self, match_id, result, is_over, winner):
        query = """
            UPDATE matches
            SET result = ?,
                is_over = ?,
                winner = ?
            WHERE id = ?;
        """
        self.update(
            query,
            [(result, is_over, winner, match_id)]
        )

    def get_today_matches(self):
        day = datetime.datetime.today()
        today = day.strftime("%d.%m.%Y")
        tomorrow = (day + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
        return self.query("""
            SELECT m.id AS match_id,
                   m.day AS match_day,
                   m.home_team AS home_team,
                   m.result AS result,
                   m.is_over AS is_over,
                   m.winner AS winner,
                   m.link AS link,
                   m.start_time AS start_time,
                   ev.id AS event_id,
                   t1.code AS team1_code,
                   t1.name AS team1_name,
                   t1.emoji AS team1_emoji,
                   t2.code AS team2_code,
                   t2.name AS team2_name,
                   t2.emoji AS team2_emoji,
                   s.id  AS stage_id,
                   s.name  AS stage_name,
                   t.id  AS tour_id,
                   t.name  AS tour_name
            FROM matches m
             JOIN events ev ON ev.id = m.event_id
             JOIN teams t1 ON t1.id = ev.team_id_1
             JOIN teams t2 ON t2.id = ev.team_id_2
             JOIN tour_stages ts ON ts.id = ev.tour_stage_id
             JOIN stages s ON s.id = ts.stage_id
             JOIN tours t ON t.id = ts.tour_id
            WHERE m.day IN ('{0}', '{1}') AND
                  m.is_over = 0;
        """.format(today, tomorrow))
