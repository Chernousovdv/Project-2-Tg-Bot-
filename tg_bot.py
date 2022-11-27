import json

import nest_asyncio
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from get_data import collect_data
from get_data import champions_list
from Globals import is_abilities, is_passive, is_enemy_tips, is_ally_tips, is_found, Globals
#from PIL import Image
from io import BytesIO


nest_asyncio.apply()
bot = Bot(token="5960492939:AAGt-1ZKNBn7nbETqvLSYu7o5ClQQw9S-4E")
dp = Dispatcher(bot)
# is_enemy_tip = True
# is_ally_tip = True
# is_passive = True
# print("why!!")
# is_abilities = True

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
    rew = champions_list()
    champ_list = ""
    for champ in rew:
        champ_list = champ_list + str(champ["name"]) + "\n"
    await message.reply(champ_list)

@dp.message_handler()
async def champion_select(message: types.Message):
    chat_id = message.from_user.id
    dar = collect_data(message.text)
    is_found.change(False)
    if len(dar) != 0:
        is_found.change(True)
    passive_ability = ""
    ally_tip = ""
    enemy_tip = ""
    Q = ""
    W = ""
    E = ""
    R = ""
    # with open('result.json') as file:
    #     dar = json.load(file)
    if is_enemy_tips.is_smth:
        tips = dar.get("enemy_tips")
        for item in tips:
            enemy_tip = enemy_tip + item + " "
    if is_ally_tips.is_smth:
        tips = dar.get("ally_tips")
        for item in tips:
            ally_tip = ally_tip + item + " "
    if is_passive.is_smth:
        temp = dar.get("passive")
        passive_ability = passive_ability + str(temp["name"])    + " - " + str(temp["description"])
    if is_abilities.is_smth:
        tmp = dar.get("spells")
        qz = tmp[0]
        wz = tmp[1]
        ez = tmp[2]
        rz = tmp[3]
        Q = Q + str(qz["key"]) + ": " + str(qz["name"]) + ". " + str(qz["description"])
        W = W + str(wz["key"]) + ": " + str(wz["name"]) + ". " + str(wz["description"])
        E = E + str(ez["key"]) + ": " + str(ez["name"]) + ". " + str(ez["description"])
        R = R + str(rz["key"]) + "(Ultimate): " + str(rz["name"]) + ". " + str(rz["description"])
    if is_found.is_smth:
        await bot.send_photo(chat_id=chat_id, photo=dar.get("image_url"), caption=message.text)
        if is_passive.is_smth:
            await message.reply(passive_ability)
        if is_enemy_tips.is_smth and is_ally_tips.is_smth:
            enemy_tip = enemy_tip + "\n" + ally_tip
            await message.reply(enemy_tip)
        else:
            if is_enemy_tips.is_smth:
                await message.reply(enemy_tip)
            if is_ally_tips.is_smth:
                await message.reply(ally_tip)
        if is_abilities.is_smth:
            await bot.send_photo(chat_id=chat_id, photo=str(qz["image_url"]), caption=Q)
            await bot.send_photo(chat_id=chat_id, photo=str(wz["image_url"]), caption=W)
            await bot.send_photo(chat_id=chat_id, photo=str(ez["image_url"]), caption=E)
            await bot.send_photo(chat_id=chat_id, photo=str(rz["image_url"]), caption=R)


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()


