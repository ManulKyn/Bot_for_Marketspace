from aiogram import types
from dispatcher import dp
import json
import html_parser
from bot import BotDB

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if (not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id, message.from_user.username)
    await message.bot.send_message(
        message.from_user.id,
        f'Приветствую, {message.from_user.username}!\n' +
        'Я могу отслеживать стоимость видеокарт и др. товаров.\n' +
        'Команда для отслеживания товара /follow\n' +
        'To get help press /help.'
  )


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    keyboard = {
            "inline_keyboard": [[{"text": "Message the developer", "url": "telegram.me/ManulKyn"},]]
    }

    await message.bot.send_message(
        message.from_user.id,
        'Основные функции бота:\n' +
        '1) Получить информацию о товаре \n' +
        '2) Добавлять товары в список, для дальнейшего отслеживания цены/наличия',
        reply_markup=json.dumps(keyboard)
    )


@dp.message_handler(commands=['follow'])
async def info_command(message: types.Message):
    if (not BotDB.user_follow_exists(message.from_user.id)):
        await message.bot.send_message(
            message.from_user.id,
            'Для добавления товара в список отслеживаемых товаров\n' +
            'пришли ссылку на него (пока только из Ситилинка).',
        )
    else:
        follow_goods_list = BotDB.get_follow(message.from_user.id)
        answer = ''
        for index, goods in enumerate(follow_goods_list):
            answer = answer + f'{index + 1}. ' + f'{goods[0]}\n' + 'Текущая цена: ' + f'{goods[1]}\n\n'

        goods_url = BotDB.get_follow_url(message.from_user.id)
        keyboard = InlineKeyboardMarkup(row_width=2)
        for index,url in enumerate(goods_url):
            keyboard.add(InlineKeyboardButton(text=f'{index+1}', url=url[0]))

        await message.bot.send_message(
            message.from_user.id,
            answer,
            reply_markup=keyboard,
        )


@dp.message_handler(content_types=['text'])
async def send_text(message: types.Message):
    if message.text.lower() == 'привет':
        await message.bot.send_message(message.from_user.id, 'Ещё раз привет!')
    elif message.text.lower() == 'пока':
        await message.bot.send_message(message.from_user.id, 'Пока!')

    if '://www' in message.text:
        numbers_of_goods = int(BotDB.count_follows(message.from_user.id))
        if numbers_of_goods <= 4:
            await message.bot.send_chat_action(message.from_user.id, 'typing')
            url = message.text
            answer = html_parser.get_data(url)
            if answer != 'Ничего не найдено' or answer != 'Странница не найдена':
                BotDB.add_follow(message.from_user.id, answer['goods_name'], answer['goods_price'],message.text)
            await message.bot.send_message(message.from_user.id, 'Товар добавлен')
        else:
            await message.bot.send_message(message.from_user.id, 'Нельзя добавлять больше 4 товаров в список отслеживания')
