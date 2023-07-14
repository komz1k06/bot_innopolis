import asyncio
import math
import random
from config import TOKEN
from keyboard_pr import smiles, smiles_for_plans, documentation, phrases, keyboard, back_keyboard, back_keyboard_add_delete,  ReplyKeyboardRemove
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def spam_start(user_id: int):
    await asyncio.sleep(1800)

    while True:
        await bot.send_message(user_id, f"{phrases[random.randint(0, 18)]}\n"
                                        f"Не забывай про свой список дел, если такой имеется)")
        await asyncio.sleep(1800)


spam_targets = set()

main_menu = {
    'text' : "Чтобы узнать про меня побольше об этих командах нажмите help",
    'reply_markup' : keyboard
}


@dp.message_handler(commands=["start"], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    user_id = message.from_id
    if user_id not in spam_targets:
        spam_targets.add(user_id)
        asyncio.create_task(spam_start(user_id))
    await message.answer(f"Привет,{message.from_user.first_name} !", reply_markup=ReplyKeyboardRemove())
    await message.answer(**main_menu)


@dp.callback_query_handler(lambda c: c.data == 'help', state="*")
async def help_handler(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(f"{documentation}", reply_markup=back_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def process_back(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.edit_text(**main_menu)


@dp.callback_query_handler(lambda c: c.data == 'weather', state='*')
async def weather_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(f"Напиши мне название города и я пришлю сводку погоды",
                                           reply_markup=back_keyboard)
    await state.set_state("get_weather")


@dp.callback_query_handler(lambda c: c.data == 'add', state='*')
async def add_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    try:
        await state.update_data()
        data = await state.get_data()
        if len(data["plans"]) != 0:
            await callback_query.message.answer(f"Если что, вот твой список:")
            await callback_query.message.answer('\n'.join(data["plans"]))
            await callback_query.message.edit_text(f"Напиши что-то и я пополню твой список")
            await state.set_state("get_add")
    except:
        await callback_query.message.edit_text(f"Твой список пуст, чтобы его заполнить введите /plans", reply_markup=back_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'delete', state='*')
async def delete_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    try:
        await state.update_data()
        data = await state.get_data()
        if len(data["plans"]) != 0:
            await callback_query.message.answer(f"Если что, вот твой список:")
            await callback_query.message.answer('\n'.join(data["plans"]))
            await callback_query.message.edit_text(f"Напиши мне что-то из своего списка и я удалю это")
            await state.set_state("get_delete")
    except:
        await callback_query.message.edit_text(f"Твой список пуст, из него нечего удалять, чтобы его заполнить нажмите plans", reply_markup=back_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'show', state='*')
async def show_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    try:
        await state.update_data()
        data = await state.get_data()
        if len(data["plans"]) > 0:
            await callback_query.message.answer(f"Вот твой список:")
            await callback_query.message.answer('\n'.join(data["plans"]), reply_markup=back_keyboard_add_delete)
    except:
        await callback_query.message.edit_text(f"Твой список пуст, чтобы его заполнить нажмите plans", reply_markup = back_keyboard)


@dp.callback_query_handler(lambda c: c.data == 'plans', state='*')
async def plans_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.edit_text(f"Напиши мне свои планы на день в таком формате\n"
                         f"Например:\n"
                         f"Погулять c собакой\n"
                         f"Приготовить ужин\n"
                         f"Убраться в комнате\n")
    await state.set_state("get_plans")


@dp.message_handler(state="get_weather")
async def get_weather_handler(message: types.message, state: FSMContext):
    city = message.text
    city = city.lower()
    await state.update_data({"name": city})
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=cc6d20e9665c2daf3845b0b3b127aa40")
        data = response.json()
        cityy = data["name"]
        temp = data["main"]["temp"]
        wet = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        weather_description = data["weather"][0]["main"]
        if weather_description in smiles:
            wd = smiles[weather_description]
        else:
            wd = "Я не могу подобрать слов, чтобы описать эту погоду"
        await message.answer(f"Погода в {cityy}\nТемпература: {temp}℃\n{wd}\nВлажность: {wet}%\n"
                            f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст.\n"
                            f"Ветер: {wind} м/c\nХорошего дня!❤", reply_markup=back_keyboard)
    except:
        await message.answer("Введите название города корректно!", reply_markup=back_keyboard)


@dp.message_handler(state="get_plans")
async def get_plans_handler(message: types.message, state: FSMContext):
    await state.update_data(plans=message.text.split("\n"))
    data = await state.get_data()
    await message.answer(f"Если что, вот твой список:")
    for line in data["plans"]:
        await message.answer(f"{smiles_for_plans[random.randint(0, 10)]}{line}")
    await message.answer(f"Удачи!", reply_markup=back_keyboard_add_delete)


@dp.message_handler(state="get_add")
async def get_add_handler(message: types.message, state: FSMContext):
    data = await state.get_data()
    data["plans"].append(message.text)
    await state.update_data(plans=data["plans"])
    await message.answer(f"Твой список успешно пополнился, вот он:")
    for line in data["plans"]:
        if line == data["plans"][-1]:
            await message.answer(f"{smiles_for_plans[random.randint(0, 12)]}{line}", reply_markup=back_keyboard)
        else:
            await message.answer(f"{smiles_for_plans[random.randint(0, 12)]}{line}")


@dp.message_handler(state="get_delete")
async def get_delete_handler(message: types.message, state: FSMContext):
    data = await state.get_data()
    try:
        data["plans"].remove(message.text)
        await state.update_data(plans=data["plans"])
        await message.answer(f"Твой список уменьшился, так держать")
        if len(data["plans"]) !=0:
            for line in data["plans"]:
                if line == data["plans"][-1]:
                    await message.answer(f"{smiles_for_plans[random.randint(0, 12)]}{line}", reply_markup=back_keyboard)
                else:
                    await message.answer(f"{smiles_for_plans[random.randint(0, 12)]}{line}")
        else:
            await message.answer("Твой список пуст", reply_markup=back_keyboard)
    except:
        await message.answer("Такого нет в твоем списке", reply_markup=back_keyboard)


executor.start_polling(dp, skip_updates=True)
