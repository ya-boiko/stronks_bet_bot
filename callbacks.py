from db.DbQuery import DbQuery
from settings import DB_NAME


queries = DbQuery(DB_NAME)

clb_names = {
    "tour": "tour_",
    "tour_stages": "tour_stages_",
    "event": "event_",
    "event_users_bets": "event_users_bets_",
    "bet": "bet_",
    "drop_bet": "drop_bet_",
    "tour_stage_user_bets": "tour_stage_user_bets_",
    "rating": "rating_",
}


start_menu_clb = "start_menu"

# колбэк кнопки турниров
tours = queries.get_all_tours()
tours_clb = []
rating_clb = []
for tour in tours:
    tours_clb.append(f"{clb_names['tour']}{tour['id']}")
    rating_clb.append(f"{clb_names['rating']}{tour['id']}")


# колбэк кнопки стадий турниров и кнопки со ставками пользователя
tour_stages = queries.get_all_tour_stages()
tour_stages_clb = []
tour_stage_user_bets_clb = []
for tour_stage in tour_stages:
    tour_stages_clb.append(f"{clb_names['tour_stages']}{tour_stage['id']}")
    tour_stage_user_bets_clb.append(f"{clb_names['tour_stage_user_bets']}{tour_stage['id']}")


# колбэк кнопки событий стадии турнира
events = queries.get_all_events()
events_clb = []
event_users_bets_clb = []
for event in events:
    events_clb.append(f"{clb_names['event']}{event['id']}")
    event_users_bets_clb.append(f"{clb_names['event_users_bets']}{event['id']}")


# колбэк кнопки ставки пользователя
bets = queries.get_coming_bets()
bets_clb = []
drop_bet_clb = []
for bet in bets:
    bets_clb.append(f"{clb_names['bet']}{bet['id']}")
    drop_bet_clb.append(f"{clb_names['drop_bet']}{bet['id']}")
