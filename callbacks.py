from db.DbQuery import DbQuery
from settings import DB_NAME


queries = DbQuery(DB_NAME)

clb_names = {
    "tour": "tour_",
    "tour_stages": "tour_stages_",
    "event": "event_",
    "bet": "bet_",
    "drop_bet": "drop_bet_",
}


start_menu_clb = "start_menu"

# колбэк кнопки турниров
tours = queries.get_all_tours()
tours_clb = []
for tour in tours:
    tours_clb.append(f"{clb_names['tour']}{tour['id']}")


# колбэк кнопки стадий турниров
tour_stages = queries.get_all_tour_stages()
tour_stages_clb = []
for tour_stage in tour_stages:
    tour_stages_clb.append(f"{clb_names['tour_stages']}{tour_stage['id']}")


# колбэк кнопки событий стадии турнира
events = queries.get_all_events()
events_clb = []
for event in events:
    events_clb.append(f"{clb_names['event']}{event['id']}")


# колбэк кнопки ставки пользователя
bets = queries.get_coming_bets()
bets_clb = []
drop_bet_clb = []
for bet in bets:
    bets_clb.append(f"{clb_names['bet']}{bet['id']}")
    drop_bet_clb.append(f"{clb_names['drop_bet']}{bet['id']}")
