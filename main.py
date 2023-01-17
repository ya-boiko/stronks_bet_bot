import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import callbacks
from callbacks import clb_names
from db.Db import Db
from db.DbQuery import DbQuery
from settings import TOKEN, DB_NAME


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Db(DB_NAME)
queries = DbQuery(DB_NAME)
prev = {i: str() for i in range(0, 10)}
prev[0] = callbacks.start_menu_clb
btn_back_name = " < Назад"
reply_markup = types.ReplyKeyboardRemove()


@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    await message.delete()

    show_start_menu = get_start_menu()
    await message.answer(
        text=f"STRONKS BET \nЗалупенди жб",
        reply_markup=show_start_menu
    )


@dp.callback_query_handler(text=callbacks.start_menu_clb)
async def callback_start_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    show_start_menu = get_start_menu()
    await bot.send_message(
        callback_query.from_user.id,
        text=f"STRONKS BET \nЗалупенди жб",
        reply_markup=show_start_menu
    )


@dp.callback_query_handler(text=callbacks.tours_clb)
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
        clb = f"{clb_names['tour_stages']}{tour_stage['tour_stage_id']}"
        btn_tour_stage = InlineKeyboardButton(tour_stage["stage_name"], callback_data=clb)
        list_btn_tour_stages.append(btn_tour_stage)

    list_btn_tour_stages.append(bth_back(callback_query.data, 1))

    show_tour_stages = InlineKeyboardMarkup()
    for button in list_btn_tour_stages:
        show_tour_stages.add(button)
        show_tour_stages.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{tour_name}",
        reply_markup=show_tour_stages
    )


@dp.callback_query_handler(text=callbacks.tour_stages_clb)
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

        clb = f"{clb_names['event']}{event['event_id']}"
        event_name = get_event_name(
            event["team1_name"],
            event["team1_emoji"],
            event["team2_name"],
            event["team2_emoji"],
        )
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


@dp.callback_query_handler(text=callbacks.events_clb)
async def callback_show_events_bets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    event_id = callback_query.data.replace("event_", "")

    user_bet = queries.check_user_bet_on_event(callback_query.from_user.id, event_id)
    list_btn_event_bets = []
    if user_bet:
        event_bet = queries.get_event_by_id(event_id)

        event_name = get_event_name(
            event_bet["team1_name"],
            event_bet["team1_emoji"],
            event_bet["team2_name"],
            event_bet["team2_emoji"],
        )
        event_name += f"\n\nТвоя ставка - {user_bet.get('event_name')}"

        clb = f"{clb_names['drop_bet']}{user_bet['bet_id']}"
        btn_change_bet = InlineKeyboardButton("Удалить ставку", callback_data=clb)
        list_btn_event_bets.append(btn_change_bet)
    else:
        event_bets = queries.get_bets_by_event_id(event_id)
        event_name = False
        for event_bet in event_bets:
            if not event_name:
                event_name = get_event_name(
                    event_bet["team1_name"],
                    event_bet["team1_emoji"],
                    event_bet["team2_name"],
                    event_bet["team2_emoji"],
                )

            clb = f"{clb_names['bet']}{event_bet['bet_id']}"
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


@dp.callback_query_handler(text=callbacks.bets_clb)
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


@dp.callback_query_handler(text=callbacks.drop_bet_clb)
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


def get_event_name(team1_name, team1_emoji, team2_name, team2_emoji):
    home = f"{team1_name} {team1_emoji}"
    guest = f"{team2_name} {team2_emoji}"
    return f"{home} - {guest}"


def bth_back(callback_data, lvl):
    global prev
    btn_back = InlineKeyboardButton(btn_back_name, callback_data=prev[lvl-1])
    prev[lvl] = callback_data
    return btn_back


def get_start_menu():
    # кнопка турниров
    tours = queries.get_all_tours()

    list_btn_tours = []
    for tour in tours:
        clb = f"{clb_names['tour']}{tour['id']}"
        btn_tour = InlineKeyboardButton(tour["name"], callback_data=clb)
        list_btn_tours.append(btn_tour)

    show_start_menu = InlineKeyboardMarkup()
    for button in list_btn_tours:
        show_start_menu.add(button)
        show_start_menu.row()

    return show_start_menu


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
