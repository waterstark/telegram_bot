from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from service.user import get_user_by_tg_id

from payment_system import payment, check_payment

import kb
import text
import sys
import os

sys.path.append(os.path.dirname("service"))

router = Router()


class Bot(StatesGroup):
    menu = State()
    business_direction = State()
    bot_platform = State()
    budget = State()
    phone_number = State()
    purchase_of_goods = State()
    payment_for_the_goods = State()


buttons_business_direction = [
    button[0].text for button in kb.business_direction.inline_keyboard
]
buttons_bot_platform = [button[0].text for button in kb.bot_platform.inline_keyboard]
the_quantity_of_goods_on_the_buyer_account = 0.00


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    get_user_by_tg_id(message.from_user.id)
    await state.update_data(
        the_quantity_of_goods_on_the_buyer_account=the_quantity_of_goods_on_the_buyer_account
    )
    await message.answer(
        text.greet.format(name=message.from_user.full_name), reply_markup=kb.menu
    )
    await state.set_state(Bot.menu)


@router.callback_query(Bot.menu, F.data.in_("Оставить заявку"))
async def business_direction(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(the_button_selected_by_the_user=callback.data.lower())
    await callback.message.answer(
        "Спасибо. Теперь, пожалуйста, ответьте:\nКакое направление вашего бизнеса?",
        reply_markup=kb.business_direction,
    )
    await state.set_state(Bot.business_direction)
    await callback.answer()


@router.callback_query(Bot.menu, F.data.in_("Купить товар"))
async def Buy_a_product(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(the_button_selected_by_the_user=callback.data.lower())
    await callback.message.answer(
        "Спасибо. Выберите желаемое кол-во товара",
        reply_markup=kb.purchase_of_goods,
    )
    await state.set_state(Bot.purchase_of_goods)
    await callback.answer()


@router.callback_query(F.data.in_("Мой баланс"))
async def buyer_balance(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(the_button_selected_by_the_user=callback.data.lower())
    data = await state.get_data()
    balance = data["the_quantity_of_goods_on_the_buyer_account"]
    await callback.message.answer(f"Ваш баланс равен: {balance}")
    await callback.answer()


@router.callback_query(Bot.purchase_of_goods, F.data.in_("Купить 1 раз"))
async def purchase_of_one_product(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(quantity_of_goods_to_purchase=callback.data.lower())
    payment_data = payment(1, "Платеж за 1 товар")
    link_for_payment = payment_data["confirmation"]["confirmation_url"]
    await callback.message.answer(
        f"Спасибо. Пожалуйста, перейдите по ссылке ниже, для оплаты вашего заказа.\n{link_for_payment}"
    )
    payment_result = await check_payment(payment_data["id"])
    if payment_result:
        await callback.message.answer("Платеж прошел успешно, спасибо!")
        await state.update_data(
            the_quantity_of_goods_on_the_buyer_account=the_quantity_of_goods_on_the_buyer_account
            + float(payment_data["amount"]["value"])
        )
        await state.set_state(Bot.payment_for_the_goods)
    else:
        await callback.message.answer("Ошибка платежа, пожалуйста, попробуйте еще раз.")


@router.callback_query(Bot.purchase_of_goods, F.data.in_("Купить 2 раза"))
async def purchase_of_two_goods(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(quantity_of_goods_to_purchase=callback.data.lower())
    payment_data = payment(2, "Платеж за 2 товара")
    link_for_payment = payment_data["confirmation"]["confirmation_url"]
    await callback.message.answer(
        f"Спасибо. Пожалуйста, перейдите по ссылке ниже, для оплаты вашего заказа.\n{link_for_payment}"
    )
    payment_result = await check_payment(payment_data["id"])
    if payment_result:
        await callback.message.answer("Платеж прошел успешно, спасибо!")
        await state.update_data(
            the_quantity_of_goods_on_the_buyers_account=the_quantity_of_goods_on_the_buyer_account
            + float(payment_data["amount"]["value"])
        )
        await state.set_state(Bot.payment_for_the_goods)
    else:
        await callback.message.answer("Ошибка платежа, пожалуйста, попробуйте еще раз.")


@router.callback_query(Bot.business_direction, F.data.in_(buttons_business_direction))
async def business_direction(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(business_direction=callback.data.lower())
    await callback.message.answer(
        "Спасибо. Теперь, пожалуйста, ответьте:\nНа какой платформе вы хотите разработать чат-бот?",
        reply_markup=kb.bot_platform,
    )
    await state.set_state(Bot.bot_platform)
    await callback.answer()


@router.callback_query(Bot.bot_platform, F.data.in_(buttons_bot_platform))
async def business_direction(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(platform_for_writing_a_bot=callback.data.lower())
    await callback.message.answer(
        "Спасибо. Теперь, пожалуйста, ответьте:\nКакой у вас бюджет? От … До …",
    )
    await state.set_state(Bot.bot_platform)
    await callback.answer()


@router.message(F.text, Bot.bot_platform)
async def bot_platform(message: types.Message, state: FSMContext):
    try:
        range_budget = message.text.split(" ")
        if isinstance(int(range_budget[0]), int) and isinstance(
            int(range_budget[1]), int
        ):
            await state.update_data(
                min_budget=range_budget[0], max_budget=range_budget[1]
            )
            await message.answer(
                "Спасибо. Последний вопрос, укажите, пожалуйста, свой номер телефона:"
            )
            await state.set_state(Bot.budget)
    except (IndexError, ValueError):
        await message.answer(
            "Пожалуйста, введите два числа через пробел.\nПример: 10000 100000 "
        )


@router.message(F.text, Bot.budget)
async def budget(message: types.Message, state: FSMContext):
    try:
        data = {"phone_number": "<N/A>"}
        for item in message.entities:
            if item.type in data.keys():
                data[item.type] = item.extract_from(message.text)
        await state.update_data(phone=message.text)
        await message.answer("На этом все, спасибо, что выбираете нас!")
        await state.set_state(Bot.phone_number)
        await state.bot.send_message("483700323", str(await state.get_data()))
        await state.clear()
    except TypeError as e:
        print(e)
        await message.answer("Пожалуйста, введите корректный номер телефона")
