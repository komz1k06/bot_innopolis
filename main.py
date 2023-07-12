import math
from config import TOKEN
from keyboard_pr import choose_chat_type_keyboard
import time
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

smiles = {
    "Clear": "Ясно🌞☀",
    "Clouds": "Облачно🌥☁",
    "Rain": "Дождь🌧💧",
    "Thunderstorm": "Гроза🌩⚡",
    "Snow": "Снег🌨❄",
    "Mist": "Туман🌫"
}

documentation = "Документация:\n" \
                "/weather - узнать погоду в любом городе/стране\n" \
                "/exitweather - выйти из /weather\n" \
                "/rate - узнать курс доллара/евро/грузинского лари/казахстанского тенге/китайского юаня/турецких лира\n" \
                "/exitrate - выйти из /weather"


@dp.message_handler(commands=["start"], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer(f"Привет,{message.from_user.first_name} !")
    time.sleep(1)
    await message.answer("Чтобы узнать про меня побольше введите /help")


@dp.message_handler(commands=["help"], state="*")
async def help_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{documentation}")


@dp.message_handler(commands=["weather"], state="*")
async def weather_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, напиши мне название города и я пришлю сводку погоды")
    await state.set_state("get_weather")


@dp.message_handler(commands="exitweather", state="*")
async def exit_weather_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, до скорой встречи)")


@dp.message_handler(state="get_weather")
async def get_weather_handler(message: types.message, state: FSMContext):
    city = message.text
    city = city.lower()
    await state.update_data({"name": city})
    try:
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&units=metric&appid=cc6d20e9665c2daf3845b0b3b127aa40")
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
        await message.reply(f"Погода в {cityy}\nТемпература: {temp}℃ {wd}\nВлажность: {wet}%\n"
                            f"Давление: {math.ceil(pressure / 1.333)} мм.рт.ст.\n"
                            f"Ветер: {wind} м/c\nХорошего дня!❤")
    except:
        await message.reply("Введите название города корректно!")


@dp.message_handler(commands=["rate"], state="*")
async def rate_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, выбери валюту", reply_markup=choose_chat_type_keyboard)
    await state.set_state("get_rate")


@dp.message_handler(commands="exitrate", state="*")
async def exit_rate_handler(message: types.Message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, до скорой встречи)", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state="get_rate")
async def get_rate_handler(message: types.message, state: FSMContext):
    text = message.text
    course = text[:3]
    await state.update_data({"course": course})
    response_rate = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    dataa = response_rate.json()
    await message.answer(f"1 {dataa['Valute'][course]['Name']} = {dataa['Valute'][course]['Value']} рублей")


@dp.message_handler(commands="plans")
async def plans_handler(message: types.message, state: FSMContext):
    await message.answer(f"Напиши мне свои планы на день\n"
                         f"Например:\n"
                         f"Погулять c собакой\n"
                         f"Приготовить ужин\n"
                         f"Убраться в комнате\n")
    await state.set_state("get_plans")


@dp.message_handler(state="get_plans")
async def get_plans_handler(message: types.message, state: FSMContext):
    #await state.update_data(plans=message.text)
    #data = await state.get_data()
    #data["plans"] = data['plans'].lower()
    #data["plans"] = data["plans"].split("\n")
    #print(data["plans"])
    pl = message.text
    pl = pl.split("\n")
    print(pl)
    await message.answer(f"Чтобы пополнить свой список введите /add, а чтобы удалить что-то введите /delete")
    await state.set_state("add")


@dp.message_handler(commands="add", state="add")
async def plans_handler(message: types.message, state: FSMContext):
    await message.answer(f"{message.from_user.first_name}, напиши что-то и я пополню твой список!")
    await state.set_state("get_add")


@dp.message_handler(state="get_add")
async def get_add_handler(message: types.message, state: FSMContext):
    #await state.update_data(new=message.text)
    #data = await state.get_data()
    #print(data)
    print(get_plans_handler)


executor.start_polling(dp, skip_updates=True)
