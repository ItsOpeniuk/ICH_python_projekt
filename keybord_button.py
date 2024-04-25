from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from search_methods import all_genres, all_years


class ButtonText:
    GENRES = 'Genres'
    YEARS = 'Years'
    RATING = 'Rating'
    ACTOR = 'Actors'
    KEYWORDS = 'Keywords'
    HISTORY = 'History'


def start_buttons():
    button_genres = KeyboardButton(text=ButtonText.GENRES)
    button_year = KeyboardButton(text=ButtonText.YEARS)
    button_rating = KeyboardButton(text=ButtonText.RATING)
    button_actor = KeyboardButton(text=ButtonText.ACTOR)
    button_keyword = KeyboardButton(text=ButtonText.KEYWORDS)
    button_history = KeyboardButton(text=ButtonText.HISTORY)
    buttons_row_1 = [button_genres, button_year, button_rating]
    buttons_row_2 = [button_actor, button_keyword, button_history]
    keyboard = ReplyKeyboardMarkup(keyboard=[buttons_row_1, buttons_row_2], resize_keyboard=True)
    return keyboard


def get_genres_kb():
    genres = all_genres()
    builder = ReplyKeyboardBuilder()
    for genre in genres:
        builder.button(text=genre)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=False)


def get_years_kb():
    years = all_years()
    builder = ReplyKeyboardBuilder()
    for year in years:
        builder.button(text=str(year))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=False)
