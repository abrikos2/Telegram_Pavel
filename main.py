import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
from aiogram.filters import Command
from keyboards import keyboardMain, keyboardPay, keyboardMenu
import datetime
import json
API_TOKEN = ""
PAYMENTS_TOKEN= ""
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")) as f:
    data = json.load(f)
    API_TOKEN = data["API_TOKEN"]
    PAYMENTS_TOKEN = data["PAYMENTS_TOKEN"]
dp = Dispatcher()
bot = Bot(API_TOKEN)
PRICE_BASE = types.LabeledPrice(label="Подписка", amount=35000*100)
PRICE_PRO = types.LabeledPrice(label="Подписка", amount=45000*100)
async def logger(message: types.Message):
    try:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt"), "a+", encoding="utf-8") as log:
            log.write(f"{datetime.datetime.now()} @{message.chat.username} ==> {message.text if message.text != None else "Оплатил подписку на базовый курс "if message.successful_payment.invoice_payload == "Базовый курс"  else "Оплатил подписку на расширенный курс " if message.successful_payment.invoice_payload == "Расширенный курс"else message.text}\n")
            log.close()
    except FileNotFoundError:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt"), "a+", encoding="utf-8") as log:
            log.write(f"{datetime.datetime.now()} @{message.chat.username} ==>  {message.text if message.text != None else "Оплатил подписку на базовый курс "if message.successful_payment.invoice_payload == "Базовый курс"  else "Оплатил подписку на расширенный курс " if message.successful_payment.invoice_payload == "Расширенный курс"else message.text}\n")
            log.close()

        
@dp.message(F.text, Command("start"))
async def buy(message: types.Message):
    await logger(message)
    await bot.send_message(message.chat.id, "Привет! 👋 Добро пожаловать в мир видеомонтажа!\
    Здесь вы сможете научиться английскому языку, вне зависимости от вашего уровня и опыта.\
    Выберите курс, который подходит именно вам:\
    Готовы начать? Нажмите кнопку ниже!", reply_markup=keyboardMain())
    
    
    
@dp.callback_query()
async def callback(call: types.CallbackQuery):
    #if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
    #    await bot.send_message(call.message.chat.id, "Тестовый платеж!!!")
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == 'базовый курс':
        await bot.send_photo(call.message.chat.id, photo=FSInputFile("photo_base.jpg"))
        await bot.send_invoice(call.message.chat.id,
                           title="Подписка на базовый курс по английскому языку",
                           description="Активация подписки на курсы по английскому языку ",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE_BASE],
                           payload="Базовый курс"
                           )
    elif call.data == 'расширенный курс':
        await bot.send_photo(call.message.chat.id, photo=FSInputFile("photo_pro.jpg"))
        await bot.send_invoice(call.message.chat.id,
                        title="Подписка расширенный курс по английскому языку",
                        description="Активация подписки на курсы по английскому языку ",
                        provider_token=PAYMENTS_TOKEN,
                        currency="rub",
                        is_flexible=False,
                        prices=[PRICE_PRO],
                        payload="Расширенный курс")
    elif call.data == 'Описание курсов':
        await bot.send_message(call.message.chat.id, "Данные курсы предназначены для всех уровней сложности.Вы можете выбрать начальный уровень или продвинутый.В зависимости от ваших знаний и умений на текущей момент.Во всех видео роликах детально разбираются все необходимые моменты по теме в среднем темпе.Поэтому информацию легко усвоить вне зависимости от возраста или пола.Данные курсы подойдут как для тех,кто еще не знаком с этой тематикой,так и тем у кого уже имеются кое-какие навыки,но недостает знаний для выполнения более сложных и лучше оплачиваемых работ.По завершению базового курса студент будет знать основные принципы работы в программе и главные методики и способы реализации монтажа видео.В продвинутом курсе будет добавлены элементы профессионального монтажа,который применяется для работы над музыкальными клипами и даже кино", reply_markup=keyboardPay())
    elif call.data == 'FAQ':
        await bot.send_message(call.message.chat.id, "Здесь будут часто задаваемые вопросы")
    elif call.data == "Отзывы":
        await bot.send_message(call.message.chat.id, "Здесь будет ссылка на канал с отзывами")
    elif call.data == "Контактная информация": 
        await bot.send_message(call.message.chat.id, "Здесь будет контанкт для связи")
    elif call.data == "Назад" or "menu":
        await buy(call.message)

@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.channel_post()
async def get_channel_id(message: types.Message):
    channel_id = message.chat.id
    print(channel_id)

@dp.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_sucessful_payment(message: types.Message):
    await bot.delete_messages(message.chat.id, [message.message_id, message.message_id-1, message.message_id-2])
    await bot.send_message(message.chat.id, "Данный бот не имеет доступа к генерации ссылок")
    if message.successful_payment.invoice_payload == "Базовый курс":
        await logger(message)
        invite_link = await bot.create_chat_invite_link(chat_id=-1002168428229, member_limit=1)
        await bot.send_message(message.chat.id, f"{invite_link.invite_link}")
    if message.successful_payment.invoice_payload == "Расширенный курс":
        await logger(message)
        invite_link = await bot.create_chat_invite_link(chat_id=-1002285663690, member_limit=1)
        await bot.send_message(message.chat.id, f"{invite_link.invite_link}")


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())

