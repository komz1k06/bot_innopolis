from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

bEUR = KeyboardButton("EUR (Евро)")
bUSD = KeyboardButton("USD (Доллар США)")
bGEL = KeyboardButton("GEL (Грузинский лари)")
bKZT = KeyboardButton("KZT (Казахстанских тенге)")
bCNY = KeyboardButton("CNY (Китайский юань)")
bTRY = KeyboardButton("TRY (Турецких лир)")

choose_chat_type_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).insert(bEUR).insert(bUSD).insert(bGEL).add(bKZT).insert(bCNY).insert(bTRY)