import logging
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from db import Db
from queries import DbQuery
from settings import TOKEN, DB_NAME

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Db(DB_NAME)
queries = DbQuery(DB_NAME)
prev = {i: "" for i in range(0, 10)}
btn_back_name = " < Назад"

# колбэк кнопки турниров
tours = queries.get_all_tours()
list_btn_tours_clb = []
for tour in tours:
    list_btn_tours_clb.append(f"tour_{tour['id']}")


# колбэк кнопки стадий турниров
tour_stages = db.query("""
    SELECT id as id FROM tour_stages;
""")
list_btn_tour_stages_clb = []
for tour_stage in tour_stages:
    list_btn_tour_stages_clb.append(f"tour_stages_{tour_stage['id']}")


# колбэк событий стадии турнира
events = db.query("""
    SELECT id as id FROM events;
""")
list_btn_events_clb = []
for event in events:
    list_btn_events_clb.append(f"event_{event['id']}")


# колбэк ставки пользователя
bets = db.query("""
    SELECT b.id as id FROM bets b
    WHERE b.bet_won IS NULL;
""")
list_btn_bets_clb = []
list_btn_drop_bet_clb = []
for bet in bets:
    list_btn_bets_clb.append(f"bet_{bet['id']}")
    list_btn_drop_bet_clb.append(f"drop_bet_{bet['id']}")

@dp.message_handler(commands=['start'])
async def show_tours(message: types.Message):
    # кнопка турниров
    tours = queries.get_all_tours()

    list_btn_tours = []
    for tour in tours:
        btn_tour = InlineKeyboardButton(tour["name"], callback_data=f"tour_{tour['id']}")
        list_btn_tours.append(btn_tour)

    show_tours = InlineKeyboardMarkup()
    for button in list_btn_tours:
        show_tours.add(button)
        show_tours.row()

    await message.answer(
        text=f"STRONKS BET",
        reply_markup=show_tours
    )


@dp.callback_query_handler(text=list_btn_tours_clb)
async def callback_show_tour_stages(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    tour_id = callback_query.data.replace("tour_", "")
    tour_stages = queries.get_active_tour_stages_by_tour_id(tour_id)

    list_btn_tour_stages = []
    tour_name = False
    for tour_stage in tour_stages:
        if not tour_name:
            tour_name = tour_stage["tour_name"]
        btn_tour_stage = InlineKeyboardButton(tour_stage["stage_name"],
                                              callback_data=f"tour_stages_{tour_stage['tour_stage_id']}")
        list_btn_tour_stages.append(btn_tour_stage)

    bth_back(callback_query.data, 1)

    show_tour_stages = InlineKeyboardMarkup()
    for button in list_btn_tour_stages:
        show_tour_stages.add(button)
        show_tour_stages.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{tour_name}",
        reply_markup=show_tour_stages
    )


@dp.callback_query_handler(text=list_btn_tour_stages_clb)
async def callback_show_tour_stage_events(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    tour_stage_id = callback_query.data.replace("tour_stages_", "")
    events = queries.get_events_by_tour_stage_id(tour_stage_id)

    stage_name = False
    list_btn_events = []
    for event in events:
        if not stage_name:
            stage_name = event["stage_name"]

        clb = f"event_{event['event_id']}"
        home = f"{event['team1_name']} {event['team1_emoji']}"
        guest = f"{event['team2_name']} {event['team2_emoji']}"
        event_name = f"{home} - {guest}"
        btn_event = InlineKeyboardButton(event_name, callback_data=clb)
        list_btn_events.append(btn_event)

    list_btn_events.append(bth_back(callback_query.data, 2))

    show_events = InlineKeyboardMarkup()
    for button in list_btn_events:
        show_events.add(button)
        show_events.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{stage_name}",
        reply_markup=show_events
    )


@dp.callback_query_handler(text=list_btn_events_clb)
async def callback_show_events_bets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    event_id = callback_query.data.replace("event_", "")

    user_bet = queries.check_user_bet_on_event(callback_query.from_user.id, event_id)
    list_btn_event_bets = []
    if user_bet:
        event_bet = queries.get_event_by_id(event_id)
        home = f"{event_bet['team1_name']} {event_bet['team1_emoji']}"
        guest = f"{event_bet['team2_name']} {event_bet['team2_emoji']}"
        event_name = f"{home} - {guest}\n\nТвоя ставка - {user_bet.get('event_name')}"

        clb = f"drop_bet_{user_bet['bet_id']}"
        btn_change_bet = InlineKeyboardButton("Удалить ставку", callback_data=clb)
        list_btn_event_bets.append(btn_change_bet)
    else:
        event_bets = queries.get_bets_by_event_id(event_id)
        event_name = False
        for event_bet in event_bets:
            if not event_name:
                home = f"{event_bet['team1_name']} {event_bet['team1_emoji']}"
                guest = f"{event_bet['team2_name']} {event_bet['team2_emoji']}"
                event_name = f"{home} - {guest}"

            clb = f"bet_{event_bet['bet_id']}"
            btn_event_bet = InlineKeyboardButton(event_bet['bet_name'], callback_data=clb)
            list_btn_event_bets.append(btn_event_bet)

    list_btn_event_bets.append(bth_back(callback_query.data, 3))

    show_event_bets = InlineKeyboardMarkup()
    for button in list_btn_event_bets:
        show_event_bets.add(button)
        show_event_bets.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{event_name}",
        reply_markup=show_event_bets
    )


@dp.callback_query_handler(text=list_btn_bets_clb)
async def callback_add_user_bet(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    bet_id = callback_query.data.replace("bet_", "")
    queries.add_user_bet(callback_query.from_user.id, bet_id)

    show_btn = InlineKeyboardMarkup()
    show_btn.add(bth_back(callback_query.data, 4))
    show_btn.row()

    bet_name = queries.get_bet_name_by_id(bet_id)
    await bot.send_message(
        callback_query.from_user.id,
        text=f"{bet_name} - ставка сделана!",
        reply_markup=show_btn
    )


@dp.callback_query_handler(text=list_btn_drop_bet_clb)
async def callback_drop_user_bet(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    bet_id = callback_query.data.replace("drop_bet_", "")
    queries.del_user_bet(callback_query.from_user.id, bet_id)

    show_btn = InlineKeyboardMarkup()
    show_btn.add(bth_back(callback_query.data, 4))
    show_btn.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"Cтавка успешно удалена",
        reply_markup=show_btn
    )


def bth_back(callback_data, lvl):
    global prev
    btn_back = InlineKeyboardButton(btn_back_name, callback_data=prev[lvl-1])
    prev[lvl] = callback_data
    return btn_back


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
