from aiogram import Bot, Dispatcher, executor, types
from config import token
import json
from main import check_promo_update
from aiogram.dispatcher.filters import Text
# Иницииурем бота
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
# Создаем команду старт
@dp.message_handler(commands="start")
async def start(message: types.Message):
    # Создаем кнопки
    start_buttons = ["Все промо акции", "Последние 3 промо акции", "Свежие промо акции"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Добавляем кнопку старт в бота
    keyboard.add(*start_buttons)
    await message.answer("Летна промо акций", reply_markup=keyboard)    
# Создаем кнопку и логику получения всех акций с сайта
@dp.message_handler(Text(equals="Все промо акции"))
async def get_all_promo(message: types.Message):
    # Загрузаем JSON файл
    with open("tg-bot/promo_dict.json") as file:
        promo_dict = json.load(file)
    # Проводим цикл по списку
    for k, v in promo_dict.items():
        promo = f"<u>{v['article_title']}</u>\n" \
                f"<code>{v['article_desc']}</code>\n" \
                f"{v['article_url']}"
        # Выводим ответом в UI 
        await message.answer(promo)
# Создаем кнопку и логику получения трех последних акций с сайта
@dp.message_handler(Text(equals="Последние 3 промо акции"))
async def get_last_three_promo(message: types.Message):
    with open("tg-bot/promo_dict.json") as file:
        promo_dict = json.load(file)

    for k, v in sorted(promo_dict.items())[-3:]:
        promo = f"<u>{v['article_title']}</u>\n" \
                f"<code>{v['article_desc']}</code>\n" \
                f"{v['article_url']}"
        
        await message.answer(promo)
# Создаем кнопку и логику получения новых акций с сайта
@dp.message_handler(Text(equals="Свежие промо акции"))
async def get_fresh_promo(message: types.Message):
    fresh_promo = check_promo_update()
    # Создаем условия, при которых, если в списке fresh_promo добавляется 1 и больше элементов, то проходим цикллом по ним и отправляем ответ в бота
    if len(fresh_promo) >= 1:
        for k, v in sorted(fresh_promo.items()):
            promo = f"<u>{v['article_title']}</u>\n" \
                f"<code>{v['article_desc']}</code>\n" \
                f"{v['article_url']}"
        
        await message.answer(promo)
    else:
        # Если нет, то отправляем сообщение
        await message.answer("Пока что нет свежих промо акций...")

if __name__ == "__main__":
    # Запускаем бота
    executor.start_polling(dp)