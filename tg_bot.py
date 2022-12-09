from aiogram.dispatcher import Dispatcher
from aiogram.utils.markdown import hbold, hlink
from aiogram.utils import executor
from aiogram import Bot, types
from config import TOKEN
from Globals import is_abilities, is_passive, is_enemy_tips, is_ally_tips, is_found, Globals
from get_data import collect_data
from get_data import champions_list
from io import BytesIO
import json
import nest_asyncio


nest_asyncio.apply()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcoming_process(message: types.Message):
    await message.reply("Hi! This bot allows to help you with the rune choice.\n"
                        "If you have any questions, type /help.")
    chat.id = message.from_user.id

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("This bot allows to peak at different aspects of a LOL champions.\n"
                        "The list of commands:\n"
                        "/Champions - the list of all current champions\n"
                        "/Enemy_tips , /Ally_tips - tips will pop up\n"
                        "/Passive - passive ability will pop up\n"
                        "/Abilities - abilities won't pop up\n"
                        "/Stop_enemy_tips , /Stop_Ally_tips - tips won't pop up\n"
                        "/Stop_passive - passive ability won't pop up\n"
                        "/Stop_abilities - abilities won't pop up\n"
                        )

@dp.message_handler(commands=['Enemy_tips'])
async def process_help_command(message: types.Message):
    is_enemy_tips.change(True)
    await message.reply("Now showing enemy tips")

@dp.message_handler(commands=['Stop_enemy_tips'])
async def process_help_command(message: types.Message):
    is_enemy_tips.change(False)
    await message.reply("No enemy tips showing from now on")

@dp.message_handler(commands=['Ally_tips'])
async def process_help_command(message: types.Message):
    is_ally_tips.change(True)
    await message.reply("Now showing ally tips")

@dp.message_handler(commands=['Stop_ally_tips'])
async def process_help_command(message: types.Message):
    is_ally_tips.change(False)
    await message.reply("No ally tips showing from now on")

@dp.message_handler(commands=['Passive'])
async def process_help_command(message: types.Message):
    is_passive.change(True)
    await message.reply("Now showing passive ability")

@dp.message_handler(commands=['Stop_passive'])
async def process_help_command(message: types.Message):
    is_passive.change(False)
    await message.reply("No passsive ability showing from now on")

@dp.message_handler(commands=['Abilities'])
async def process_help_command(message: types.Message):
    is_abilities.change(True)
    await message.reply("Now showing abilities")

@dp.message_handler(commands=['Stop_abilities'])
async def process_help_command(message: types.Message):
    is_abilities.change(False)
    await message.reply("No abilities showing from now on")

@dp.message_handler(commands=['Champions'])
async def process_help_command(message: types.Message):
    list_of_champions = champions_list()
    champ_list_output = ""
    for champ in list_of_champions:
        champ_list_output = champ_list_output + str(champ["name"]) + "\n"
    await message.reply(champ_list_output)

async def SendPhotosOfAbilities(chat_id, message):
    if is_abilities.is_info:
        data = collect_data(message.text)
        abilities_list = data.get("spells")
        qz = abilities_list[0]
        wz = abilities_list[1]
        ez = abilities_list[2]
        rz = abilities_list[3]
        Q = ""
        W = ""
        E = ""
        R = ""
        Q = Q + str(qz["key"]) + ": " + str(qz["name"]) + ". " + str(qz["description"])
        W = W + str(wz["key"]) + ": " + str(wz["name"]) + ". " + str(wz["description"])
        E = E + str(ez["key"]) + ": " + str(ez["name"]) + ". " + str(ez["description"])
        R = R + str(rz["key"]) + "(Ultimate): " + str(rz["name"]) + ". " + str(rz["description"])
        await bot.send_photo(chat_id=chat_id, photo=str(qz["image_url"]), caption=Q)
        await bot.send_photo(chat_id=chat_id, photo=str(wz["image_url"]), caption=W)
        await bot.send_photo(chat_id=chat_id, photo=str(ez["image_url"]), caption=E)
        await bot.send_photo(chat_id=chat_id, photo=str(rz["image_url"]), caption=R)

@dp.message_handler()
async def champion_select(message: types.Message):
    chat_id = message.from_user.id
    data = collect_data(message.text)
    ally_tip = enemy_tip = ""
    if len(data) != 0:
        is_found.change(True)
    if is_found.is_info:
        await bot.send_photo(chat_id=chat_id, photo=data.get("image_url"), caption=message.text)
        if is_passive.is_info:
            passive_list = data.get("passive")
            await message.reply(str(passive_list["name"]) + " - " + str(passive_list["description"]))
        if is_enemy_tips.is_info:
            tips_list = data.get("enemy_tips")
            for item in tips_list:
                enemy_tip = enemy_tip + item + " "
            await message.reply(enemy_tip)
        if is_ally_tips.is_info:
            tips_list = data.get("ally_tips")
            for item in tips_list:
                ally_tip = ally_tip + item + " "
            await message.reply(ally_tip)
        await SendPhotosOfAbilities(chat_id, message)

