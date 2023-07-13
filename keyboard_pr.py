from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


smiles = {
    "Clear": "Ясно🌞☀",
    "Clouds": "Облачно🌥☁",
    "Rain": "Дождь🌧💧",
    "Thunderstorm": "Гроза🌩⚡",
    "Snow": "Снег🌨❄",
    "Mist": "Туман🌫"}

smiles_for_plans = ["👻", "👽", "👾", "🤖", "😺", "🙉", "👀", "🐶", "🦁", "🦊", "🐯", "🐹", "🐸"]

documentation = "Документация:\n" \
                "weather - узнать погоду в любом городе/стране\n" \
                "plans - написать/переписать список дел\n" \
                "add - добавить что-то одно в список\n" \
                "delete - удалить что-то одно из списка\n" \
                "show - показать список"

phrases = ["В любой момент у нас есть два варианта: сделать шаг вперёд к росту или вернуться в безопасное место",
           "Впереди нас ждут гораздо лучшие вещи, чем те, что мы оставляем позади",
           "Возможности не приходят сами — вы создаете их",
           "Успех обычно приходит к тем, кто слишком занят, чтобы его просто ждать",
           "Чтобы достичь успеха, перестаньте гнаться за деньгами, гонитесь за мечтой",
           "Даже если вы проходите через ад, продолжайте идти",
           "Не бойтесь пожертвовать хорошим ради еще лучшего",
           "Многие люди терпят неудачу только потому, что сдаются в двух шагах от успеха",
           "Одна победа не ведет к успеху, в отличие от постоянного желания побеждать",
           "Пока у тебя есть попытка – ты не проиграл",
           "Я этого хочу. Значит, это будет",
           "Делай сегодня то, что другие не хотят, завтра будешь жить так, как другие не могут",
           "Лучший способ взяться за что-то — перестать говорить и начать делать",
           "Многое кажется невозможным, пока ты этого не сделаешь",
           "Чтобы дойти до цели, человеку нужно только одно. Идти",
           "Если ты не собираешься идти до конца, зачем ты вообще это делаешь?",
           "Учитесь на своих ошибках, признайте их и двигайтесь дальше",
           "Великие дела нужно совершать, а не обдумывать их бесконечно",
           "Поверьте, что сможете, и полпути уже пройдено"]

button_weather = InlineKeyboardButton("weather", callback_data='weather')
button_plans = InlineKeyboardButton("plans", callback_data='plans')
button_add = InlineKeyboardButton("add", callback_data='add')
button_delete = InlineKeyboardButton("delete", callback_data='delete')
button_show = InlineKeyboardButton("show", callback_data='show')
button_help = InlineKeyboardButton("help", callback_data='help')


keyboard = InlineKeyboardMarkup().insert(button_weather).insert(button_help).add(button_plans).insert(button_show)


button_back = InlineKeyboardButton("Вернуться назад", callback_data='back')
back_keyboard = InlineKeyboardMarkup().add(button_back)

back_keyboard_add_delete = InlineKeyboardMarkup().insert(button_add).insert(button_delete).add(button_back)
