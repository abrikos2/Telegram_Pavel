import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from keyboards import keyboardMain
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
PRICE = types.LabeledPrice(label="Подписка", amount=1500*100)
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
    await bot.send_message(message.chat.id, 'Здавствуйте, оплатите подписку, чтобы получить доступ к курсам, стоимость курса 1500р', reply_markup=keyboardMain())
    
    
@dp.callback_query()
async def callback(call: types.CallbackQuery):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(call.message.chat.id, "Тестовый платеж!!!")
    if call.data == 'Купить базовый курс':
        await bot.send_invoice(call.message.chat.id,
                           title="Подписка на базовый курс по английскому языку",
                           description="Активация подписки на курсы по английскому языку ",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           payload="Базовый курс")
    elif call.data == 'Купить расширенный курс':
        await bot.send_invoice(call.message.chat.id,
                        title="Подписка расширенный курс по английскому языку",
                        description="Активация подписки на курсы по английскому языку ",
                        provider_token=PAYMENTS_TOKEN,
                        currency="rub",
                        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                        photo_width=416,
                        photo_height=234,
                        photo_size=416,
                        is_flexible=False,
                        prices=[PRICE],
                        payload="Расширенный курс")
@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
@dp.channel_post()
async def get_channel_id(message: types.Message):
    channel_id = message.chat.id
    print(channel_id)
@dp.message(F.content_type == types.ContentType.SUCCESSFUL_PAYMENT)
async def process_sucessful_payment(message: types.Message):
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

