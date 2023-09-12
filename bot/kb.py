from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [
        InlineKeyboardButton(
            text="Оставить заявку",
            callback_data="Оставить заявку",
            data="submit_application",
        ),
    ],
    [
        InlineKeyboardButton(
            text="Купить товар", callback_data="Купить товар", data="buy_product"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Мой баланс", callback_data="Мой баланс", data="balance"
        ),
    ],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)

business_direction = [
    [
        InlineKeyboardButton(
            text="Продажа",
            callback_data="Продажа",
            data="sale",
        ),
    ],
    [
        InlineKeyboardButton(
            text="Производство", callback_data="Производство", data="production"
        ),
    ],
    [
        InlineKeyboardButton(
            text="Оказание услуг",
            callback_data="Оказание услуг",
            data="provision of services",
        ),
    ],
]

business_direction = InlineKeyboardMarkup(inline_keyboard=business_direction)

bot_platform = [
    [
        InlineKeyboardButton(
            text="Телеграмм",
            callback_data="Телеграмм",
            data="telegram",
        ),
    ],
    [
        InlineKeyboardButton(text="Ватсап", callback_data="Ватсап", data="whatsapp"),
    ],
    [
        InlineKeyboardButton(
            text="Вайбер",
            callback_data="Вайбер",
            data="viber",
        ),
    ],
]

bot_platform = InlineKeyboardMarkup(inline_keyboard=bot_platform)

purchase_of_goods = [
    [
        InlineKeyboardButton(
            text="Купить 1 раз",
            callback_data="Купить 1 раз",
            data="buy_once",
        ),
    ],
    [
        InlineKeyboardButton(
            text="Купить 2 раза", callback_data="Купить 2 раза", data="buy_twice"
        ),
    ],
]

purchase_of_goods = InlineKeyboardMarkup(inline_keyboard=purchase_of_goods)
