from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def keyboardMain():
    '''builder = ReplyKeyboardBuislder()
    builder.button('Купить базовый курс')
    builder.button('Купить расширенный курс')
    return builder.as_markup'''
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Описание курсов', callback_data='Описание курсов')],[
        InlineKeyboardButton(text='Часто задаваемые вопросы(FAQ)', callback_data='FAQ'),
        InlineKeyboardButton(text='Отзывы', callback_data='Отзывы')],[
        InlineKeyboardButton(text='Контактная информация', callback_data='Контактная информация')
                ]])
def keyboardPay():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Базовый курс', callback_data='базовый курс'),
        InlineKeyboardButton(text='Расширенный курс', callback_data='расширенный курс')],[
        InlineKeyboardButton(text='Назад', callback_data='Назад')]])

def keyboardMenu():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='Купить', callback_data='buy')],[
        InlineKeyboardButton(text='Меню', callback_data='menu')]])
    

