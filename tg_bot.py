import asyncio  # Для работы с асинхроными методами
from aiogram import F, Bot, Dispatcher, types, html  # Создание бота, диспетчера бота, а так же анотация типов сообщений
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from config_file import TG_BOT_TOKEN as TOKEN  # Мой токен находиться в переменных окружения
import logging  # Логи для просмотра корректной работы бота
from aiogram.filters import CommandStart, Command  # Декораторы для обработки команд в боте
import search_methods
import keybord_button as kb

AVAILABLE_GENRES = search_methods.all_genres()
AVAILABLE_YEARS = search_methods.all_years()
dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)


class Form(StatesGroup):
    genres = State()
    years = State()
    rating = State()
    actors = State()
    keywords = State()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer_photo(photo=f'https://assets-global.website-files.com/61a91fef5f705a0369d2ae2a/'
                                     f'62965c1882cb34abda41f311_62963461d572564315259287_10-movies-that-'
                                     f'changed-the-visual-effects-industry-forever-vanas.jpeg',
                               caption=f'Привет, {message.from_user.full_name}, Я бот который найдет тебе фильм на '
                                       f'вечер!\n\n'
                                       f'Используй меню снизу экрана для поиска по заданным критериям',
                               reply_markup=kb.start_buttons())


@dp.message(Command('genres'))
@dp.message(F.text == kb.ButtonText.GENRES)
async def handle_genres(message: types.Message, state: FSMContext):
    await message.answer(text=f'Поиск по фильма жанру',
                         reply_markup=kb.get_genres_kb())
    await state.set_state(Form.genres)


@dp.message(Form.genres)
async def handle_genre(message: types.Message, state: FSMContext):
    await state.update_data(genre=message.text)
    search_methods.write_history(f'Genre: {message.text}', message.from_user.id)
    result = search_methods.search_mv_by_genres(f'{html.quote(message.text)}')
    for row in result:
        await message.answer_photo(photo=row[0],
                                   caption=f'Name - {row[1]}\nRating imdb {row[2]}\nYear - {row[3]}\n'
                                           f'Genre - {row[4]}\nRuntime - {row[5]}\nDescription - {row[6]}',
                                   reply_markup=ReplyKeyboardRemove())
    await state.clear()


@dp.message(Command('year'))
@dp.message(F.text == kb.ButtonText.YEARS)
async def handle_years(message: types.Message, state: FSMContext):
    await message.answer(text=f'Поиск фильма по году выпуска!',
                         reply_markup=kb.get_years_kb())
    await state.set_state(Form.years)


@dp.message(Form.years)
async def handle_year(message: types.Message, state: FSMContext):
    await state.update_data(year=message.text)
    search_methods.write_history(f'Year: {message.text}', message.from_user.id)
    result = search_methods.search_mv_by_year(int(html.quote(message.text)))
    for row in result:
        await message.answer_photo(photo=row[0],
                                   caption=f'Name - {row[1]}\nRating imdb {row[2]}\nYear - {row[3]}\n'
                                           f'Genre - {row[4]}\nRuntime - {row[5]}\nDescription - {row[6]}',
                                   reply_markup=ReplyKeyboardRemove())
    await state.clear()


@dp.message(Command('rating'))
@dp.message(F.text == kb.ButtonText.RATING)
async def handle_ratings(message: types.Message, state: FSMContext):
    await message.answer(text='Топ 10 фильмов по рейтингу!', reply_markup=ReplyKeyboardRemove())
    search_methods.write_history(f'Rating: {message.text}', message.from_user.id)
    result = search_methods.search_mv_by_rating()
    for row in result:
        await message.answer_photo(photo=row[0],
                                   caption=f'Name - {row[1]}\nRating imdb {row[2]}\nYear - {row[3]}\n'
                                           f'Genre - {row[4]}\nRuntime - {row[5]}\nDescription - {row[6]}')
    await state.clear()


@dp.message(Command('actors'))
@dp.message(F.text == kb.ButtonText.ACTOR)
async def handle_actors(message: types.Message, state: FSMContext):
    await message.answer(text=f'Поиск фильма по Актеру!\n'
                              f'Введите имя актера в чат.',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.actors)


@dp.message(Form.actors)
async def handle_actor(message: types.Message, state: FSMContext):
    await state.update_data(actor=message.text)
    search_methods.write_history(f'Actor: {message.text}', message.from_user.id)
    result = search_methods.search_mv_by_actor(html.quote(message.text.title()))
    if len(result) == 0:
        return await message.answer(text=f'Фильмов с актером {html.quote(message.text)} не найдено!')
    for row in result:
        await message.answer_photo(photo=row[0],
                                   caption=f'Name - {row[1]}\nRating imdb {row[2]}\nYear - {row[3]}\n'
                                           f'Genre - {row[4]}\nRuntime - {row[5]}\nDescription - {row[6]}')
    await state.clear()


@dp.message(Command('keyword'))
@dp.message(F.text == kb.ButtonText.KEYWORDS)
async def handle_keywords(message: types.Message, state: FSMContext):
    await message.answer(text='Дя поиска Фильма по ключевому слову введите слово в чат!',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.keywords)


@dp.message(Form.keywords)
async def handle_keyword(message: types.Message, state: FSMContext):
    await state.update_data(keyword=message.text)
    search_methods.write_history(f'Keyword: {message.text}', message.from_user.id)
    result = search_methods.search_mv_by_keyword(html.quote(message.text.title()))
    if len(result) == 0:
        return await message.answer('Фильм по заданному слову не найден! Пожалуйста повторите попітку')
    for row in result:
        await message.answer_photo(photo=row[0],
                                   caption=f'Name - {row[1]}\nRating imdb {row[2]}\nYear - {row[3]}\n'
                                           f'Genre - {row[4]}\nRuntime - {row[5]}\nDescription - {row[6]}')
    await state.clear()


@dp.message(Command('history'))
@dp.message(F.text == kb.ButtonText.HISTORY)
async def search_most_common(message: types.Message):
    await message.answer(text='Самые популярные запросы!')
    result = search_methods.search_history()
    if len(result) == 0:
        await message.answer(text='История поиска пуста...')
    for row in result:
        await message.answer(f'{row[0]} - Count: {row[1]}')


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
