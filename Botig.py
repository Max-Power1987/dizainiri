from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database

TOKIN = '5732148878:AAEOUtD1xxcbrxmqfIrmlQTcR3PAuOF8f6k'
bot = Bot(token=TOKIN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('dizainiri.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('В каком городе будем искать дизайнеров интерьера?')

@dp.message_handler()
async def serch(message: types.Message):
    result = await db.search_citi('%' + str.title(message.text))
    name = result[0].get('Имя')
    tel = result[0].get('Телефон')
    portfol = result[0].get('Порфолио')
    all_page = result[1]
    if len(name) == 0 and len(tel) == 0 and len(portfol) == 0:
        await message.answer(f'Чета не чего не нашел')
    elif len(name) == 1:
        await message.answer(f'{name[0]}  +{tel[0]}  {portfol[0]}')
    else:
        await message.answer(f'{name[0]}  +{tel[0]}  {portfol[0]}',
                             reply_markup=makeKeyboard( 1, all_page) )
        pages = {'page': 0,
                'all_page': result[1],
                }
        await storage.set_data(chat=message.from_user.id, data=result[0])
        await storage.update_bucket(chat=message.from_user.id, bucket=pages)

@dp.callback_query_handler(lambda callback: callback.data == 'btnup')
async def btn(callback: types.CallbackQuery):
    data = await storage.get_data(chat=callback.from_user.id)
    pages = await storage.get_bucket(chat=callback.from_user.id)
    name = data.get('Имя')
    tel = data.get('Телефон')
    portfol = data.get('Порфолио')
    all_page = pages['all_page']
    page = pages['page'] + 1
    if page < all_page:
        pages = {'page': page
                 }
        await callback.message.edit_text(f'{name[page]} телепон +{tel[page]} портфолио {portfol[page]}',reply_markup=makeKeyboard(page + 1, all_page))
        await storage.update_bucket(chat=callback.from_user.id, bucket=pages)
    else:
        pass

@dp.callback_query_handler(lambda callback: callback.data == 'btndown')
async def btn(callback: types.CallbackQuery):
    data = await storage.get_data(chat=callback.from_user.id)
    pages = await storage.get_bucket(chat=callback.from_user.id)
    name = data.get('Имя')
    tel = data.get('Телефон')
    portfol = data.get('Порфолио')
    all_page = pages['all_page']
    page = pages['page'] - 1
    if page >= 0:
        pages = {'page': page
                 }
        await callback.message.edit_text(f'{name[page]} телепон +{tel[page]} портфолио {portfol[page]}',
                                         reply_markup=makeKeyboard(page + 1, all_page))
        await storage.update_bucket(chat=callback.from_user.id, bucket=pages)
    else:
        pass




def makeKeyboard(page, all_page):
    markup = types.InlineKeyboardMarkup(resize_keyboard = True)
    btndown = types.InlineKeyboardButton(text=f'<---Назад', callback_data='btndown')
    btnup = types.InlineKeyboardButton(text='Вперед --->', callback_data='btnup')
    count = types.InlineKeyboardButton(text=f'Страница {page} из {all_page}', callback_data='_')
    markup.insert(btndown)
    markup.insert(count)
    markup.insert(btnup)
    return markup


if __name__ == '__main__':
    executor.start_polling(dp)