from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def keyboardMain():
    '''builder = ReplyKeyboardBuislder()
    builder.button('Купить базовый курс')
    builder.button('Купить расширенный курс')
    return builder.as_markup'''
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Купить базовый курс', callback_data='Купить базовый курс'),
        InlineKeyboardButton(text='Купить расширенный курс', callback_data='Купить расширенный курс')
                ]])
    

