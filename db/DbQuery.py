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
                   b.who_winner as who_winner, 
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
                   s.name  AS stage_name
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
                   b.name as event_name,
                   b.who_winner as who_winner,
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
