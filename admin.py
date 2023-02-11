import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from db.Db import Db
from db.AdminDbQuery import AdminDbQuery
from settings import ADMIN_TOKEN, DB_NAME, ADMINS

import admin_commands
from admin_commands import add_text, clb_names

bot = Bot(token=ADMIN_TOKEN)
dp = Dispatcher(bot)
db = Db(DB_NAME)
queries = AdminDbQuery(DB_NAME)


def get_chunks(items: list, size: int) -> list:
    for i in range(0, len(items), size):
        yield items[i:i+size]


def check_admin(tg_id: str) -> bool:
    return True if tg_id in ADMINS else False


async def stop_bitch(message):
    await message.answer(
        text=f"куда ты лезешь..."
    )


def table_buttons(table: str):
    buttons = [
        "add",
        "update",
        "remove"
    ]
    list_btn = []
    for button in buttons:
        btn_tour_stage = InlineKeyboardButton(f"{button}_{table}")
        list_btn.append(btn_tour_stage)

    show_buttons = ReplyKeyboardMarkup()
    for btn in list_btn:
        show_buttons.add(btn)

    return show_buttons


@dp.message_handler(commands=['tables'])
async def tables(message: types.Message):
    if not check_admin(str(message.chat.id)):
        await stop_bitch(message)
        return

    all_tables = queries.get_all_tables()

    list_btn_tour_stages = []
    for table in all_tables:
        btn_tour_stage = InlineKeyboardButton(table['name'])
        list_btn_tour_stages.append(btn_tour_stage)

    show_tables = ReplyKeyboardMarkup()
    for buttons in get_chunks(list_btn_tour_stages, 2):
        show_tables.add(*buttons)

    await bot.send_message(
        message.chat.id,
        text="Таблицы",
        reply_markup=show_tables
    )


@dp.message_handler(text=admin_commands.tables_names)
async def table(message: types.Message):
    if not check_admin(str(message.chat.id)):
        await stop_bitch(message)
        return

    await bot.send_message(
        message.chat.id,
        text=f"Таблица '{message.text}'",
        reply_markup=table_buttons(message.text)
    )


@dp.message_handler(text=admin_commands.add_to_table)
async def add_to_table(message: types.Message):
    if not check_admin(str(message.chat.id)):
        await stop_bitch(message)
        return

    table_name = message.text.split("_")[-1]

    await bot.send_message(
        message.chat.id,
        text=f"last_id = {queries.max_id_tours().get('max_id')}"
    )

    await bot.send_message(
        message.chat.id,
        text=json.dumps(add_text.get(table_name))
    )


@dp.message_handler(text=)
async def add_command(message: types.Message):
    if not check_admin(str(message.chat.id)):
        await stop_bitch(message)
        return

    fields = json.loads(message.text)
    table_name = fields.get("table")

    add_fields = {}
    for key in fields:
        if key not in ["table", "command"]:
            add_fields.update({
                key: fields.get(key)
            })

    function_add = f"add_{table_name}"
    queries.add_to_(table_name, add_fields)

    await bot.send_message(
        message.chat.id,
        text=f"Данные добавлены в '{table_name}'"
    )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
