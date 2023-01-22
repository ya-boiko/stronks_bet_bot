import time
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils.markdown import text, bold, italic, code, pre, hunderline, hbold

import callbacks
from callbacks import clb_names
from db.Db import Db
from db.DbQuery import DbQuery
from settings import TOKEN, DB_NAME


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Db(DB_NAME)
queries = DbQuery(DB_NAME)
prev = {}
def_prev = {i: str() for i in range(0, 10)}
btn_back_name = " < Назад"


@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    global prev
    if str(message.chat.id) not in prev:
        prev.update({
            str(message.chat.id): {i: str() for i in range(0, 10)}
        })
        prev[str(message.chat.id)][0] = callbacks.start_menu_clb

    # await message.delete()

    show_start_menu = get_start_menu()
    await message.answer(
        text=f"STRONKS BET \nЗалупенди жб",
        reply_markup=show_start_menu,
        parse_mode=ParseMode.MARKDOWN
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
        reply_markup=show_start_menu,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.tours_clb)
async def callback_show_tour_stages(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    tour_id = callback_query.data.replace(clb_names.get("tour"), "")
    tour_stages = queries.get_active_tour_stages_by_tour_id(tour_id)

    list_btn_tour_stages = []
    tour_name = False
    for tour_stage in tour_stages:
        if not tour_name:
            tour_name = tour_stage.get("tour_name")
        clb = f"{clb_names.get('tour_stages')}{tour_stage.get('tour_stage_id')}"
        btn_tour_stage = InlineKeyboardButton(tour_stage.get("stage_name"), callback_data=clb)
        list_btn_tour_stages.append(btn_tour_stage)

    list_btn_tour_stages.append(bth_back(callback_query, 1))

    show_tour_stages = InlineKeyboardMarkup()
    for button in list_btn_tour_stages:
        show_tour_stages.add(button)
        show_tour_stages.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{tour_name}",
        reply_markup=show_tour_stages,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.tour_stages_clb)
async def callback_show_tour_stage_events(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    tour_stage_id = callback_query.data.replace(clb_names.get("tour_stages"), "")
    events = queries.get_events_by_tour_stage_id(tour_stage_id)

    stage_name = False
    list_btn_events = []
    for event in events:
        if not stage_name:
            stage_name = event.get("stage_name")

        clb = f"{clb_names.get('event')}{event.get('event_id')}"
        event_name = get_event_name(
            event.get("team1_name"),
            event.get("team1_emoji"),
            event.get("team2_name"),
            event.get("team2_emoji"),
        )
        btn_event = InlineKeyboardButton(event_name, callback_data=clb)
        list_btn_events.append(btn_event)

    btn_user_bets = InlineKeyboardButton(
        "Мои ставки 🤙",
        callback_data=f"{clb_names.get('tour_stage_user_bets')}{tour_stage_id}"
    )
    list_btn_events.append(btn_user_bets)

    list_btn_events.append(bth_back(callback_query, 2))

    show_events = InlineKeyboardMarkup()
    for button in list_btn_events:
        show_events.add(button)
        show_events.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"{stage_name}",
        reply_markup=show_events,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.events_clb)
async def callback_show_events_bets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    event_id = callback_query.data.replace(clb_names.get("event"), "")

    user_bet = queries.check_user_bet_on_event(callback_query.from_user.id, event_id)
    list_btn_event_bets = []
    event_name = ""
    event_matches = queries.get_event_matches(event_id)
    matches_text = ""
    first_match_date = datetime.strptime(
        event_matches[0].get("match_day"),
        "%d.%m.%Y"
    )
    today = datetime.today()
    for match in event_matches:
        if match.get("home_team") == 2:
            match_name = get_event_name(
                match.get("team1_name"),
                match.get("team1_emoji"),
                match.get("team2_name"),
                match.get("team2_emoji"),
                match.get("winner")
            )
        else:
            match_name = get_event_name(
                match.get("team2_name"),
                match.get("team2_emoji"),
                match.get("team1_name"),
                match.get("team1_emoji"),
                match.get("winner")
            )

        if match.get("is_over") == 1:
            match_name = get_match_with_result(match_name, match.get("result"))

        matches_text += f"{match.get('match_day')} \n{match_name}\n\n"

    if user_bet:
        event_name += f"Твоя ставка - {user_bet.get('bet_name')}"

        if user_bet.get("bet_won") == 1:
            event_name += bold("\n\nСтавка победила ✅")
        elif user_bet.get("bet_won") == -1:
            event_name += bold("\n\nСтавка проиграла ❌")
        else:
            clb = f"{clb_names.get('drop_bet')}{user_bet.get('bet_id')}"
            btn_change_bet = InlineKeyboardButton("Удалить ставку", callback_data=clb)
            list_btn_event_bets.append(btn_change_bet)
    elif today < first_match_date:
        event_bets = queries.get_bets_by_event_id(event_id)

        for event_bet in event_bets:
            clb = f"{clb_names.get('bet')}{event_bet.get('bet_id')}"
            btn_event_bet = InlineKeyboardButton(event_bet.get('bet_name'), callback_data=clb)
            list_btn_event_bets.append(btn_event_bet)
    else:
        event_name += "Ставки уже не принимаются 😛"

    list_btn_event_bets.append(bth_back(callback_query, 3))

    show_event_bets = InlineKeyboardMarkup()
    for button in list_btn_event_bets:
        show_event_bets.add(button)
        show_event_bets.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=text(f"{matches_text}{event_name}"),
        reply_markup=show_event_bets,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.bets_clb)
async def callback_add_user_bet(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    bet_id = callback_query.data.replace(clb_names.get("bet"), "")
    queries.add_user_bet(callback_query.from_user.id, bet_id)

    show_btn = InlineKeyboardMarkup()
    show_btn.add(bth_back(callback_query, 4))
    show_btn.row()

    bet_name = queries.get_bet_name_by_id(bet_id)
    await bot.send_message(
        callback_query.from_user.id,
        text=f"{bet_name} - ставка сделана!",
        reply_markup=show_btn,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.drop_bet_clb)
async def callback_drop_user_bet(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    bet_id = callback_query.data.replace(clb_names.get("drop_bet"), "")
    queries.del_user_bet(callback_query.from_user.id, bet_id)

    show_btn = InlineKeyboardMarkup()
    show_btn.add(bth_back(callback_query, 4))
    show_btn.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=f"Cтавка успешно удалена",
        reply_markup=show_btn,
        parse_mode=ParseMode.MARKDOWN
    )


@dp.callback_query_handler(text=callbacks.tour_stage_user_bets_clb)
async def callback_show_tour_stage_user_bets(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    time.sleep(0.25)
    await callback_query.message.delete()

    tour_stage_id = callback_query.data.replace(clb_names.get("tour_stage_user_bets"), "")
    user_bets = queries.get_user_bets_on_tour_stage(callback_query.from_user.id, tour_stage_id)

    user_bets_text = ""
    if not user_bets:
        user_bets_text += "Ставок на эту стадию еще нет\n"

    count = 0
    for bet in user_bets:
        count += 1

        if user_bets_text == "":
            user_bets_text = f"{bet.get('tour_name')}\n"
            user_bets_text += f"{bet.get('stage_name')}\n\n"

        event_name = get_event_name(
            team1_name=bet.get('team1_name'),
            team1_emoji=bet.get('team1_emoji'),
            team2_name=bet.get('team2_name'),
            team2_emoji=bet.get('team2_emoji'),
            winner=bet.get("winner")
        )

        user_bets_text += f"{count}. {event_name}\n"

        bet_won = ""
        if bet.get("bet_won") == 1:
            bet_won += bold("✅ ")
        elif bet.get("bet_won") == -1:
            bet_won += bold("❌ ")

        bet_name = hunderline(bet.get('bet_name'))
        user_bets_text += f"{bet_won}{bet_name}\n\n"

    show_btn = InlineKeyboardMarkup()
    show_btn.add(bth_back(callback_query, 3))
    show_btn.row()

    await bot.send_message(
        callback_query.from_user.id,
        text=user_bets_text,
        reply_markup=show_btn,
        parse_mode=ParseMode.HTML
    )


def get_team_name(team1_name: str, team1_emoji: str) -> str:
    return f"{team1_name} {team1_emoji}"


def get_event_name(team1_name, team1_emoji, team2_name, team2_emoji, winner = 0):
    home = get_team_name(team1_name, team1_emoji)
    guest = get_team_name(team2_name, team2_emoji)
    if winner == 1:
        home = text(bold(home))
    elif winner == 2:
        home = text(bold(guest))

    return f"{home} - {guest}"


def get_match_with_result(match_name: str, result: str) -> str:
    return match_name.replace(" - ", f" {result} ")


def bth_back(callback, lvl):
    global prev
    user_id = str(callback.from_user.id)

    if user_id not in prev:
        prev.update({
            user_id: {i: str() for i in range(0, 10)}
        })
        prev[user_id][0] = callbacks.start_menu_clb

        btn_back = InlineKeyboardButton(
            btn_back_name,
            callback_data=prev[user_id][0]
        )
    else:
        btn_back = InlineKeyboardButton(
            btn_back_name,
            callback_data=prev[user_id][lvl - 1]
        )

    prev[str(callback.from_user.id)][lvl] = callback.data

    return btn_back


def get_start_menu():
    # кнопка турниров
    tours = queries.get_all_tours()

    list_btn_tours = []
    for tour in tours:
        clb = f"{clb_names.get('tour')}{tour.get('id')}"
        btn_tour = InlineKeyboardButton(tour.get("name"), callback_data=clb)
        list_btn_tours.append(btn_tour)

    show_start_menu = InlineKeyboardMarkup()
    for button in list_btn_tours:
        show_start_menu.add(button)
        show_start_menu.row()

    return show_start_menu


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
