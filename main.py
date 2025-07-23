import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = "7208455886:AAFxWj68GO1JV0MuX72G2oxVDFFqrDubiCY"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    welcome = State()
    experience = State()
    about_you = State()
    product = State()
    offer = State()
    ask_phone = State()
    confirmation = State()

TEXTS = {
    "welcome": (
        "Привет, солнце! ☀️ Я - Alfy.\n"
        "Мама двоих малышей и успеваю всё — даже запускать по 10-100 видео в день всего за час-два.\n\n"
        "Хочешь узнать, как сделать свой контент и бизнес лёгким, красивым и... без лишней суеты?"
    ),
    "experience": (
        "🙅‍♀️ Не нужно краситься перед съемкой, когда совсем не до этого\n"
        "🌸 Можно записывать видео хоть из детской, хоть с кухни — идеальный фон не нужен\n"
        "✨ Даже если нет настроения или сил, мой AI всегда готов работать за меня\n\n"
        "А ты уже пробовала создавать своих AI-аватаров? Или только присматриваешься к этой теме? 😊"
    ),
    "about_you": (
        "Отлично, ты умничка! 🤗\n"
        "С радостью поделюсь своим секретом — как мне удалось создать такого реалистичного аватара, что он теперь продаёт вместо меня 😍\n\n"
        "Но давай сначала расскажи о себе:\n"
        "Ты хочешь создавать аватара для себя, чтобы облегчить свою жизнь, или больше интересует создание контента для клиентов?\n"
        "Очень интересно узнать твои планы! 😊"
    ),
    "product": (
        "Мы с тремя экспертами протестировали сотни фишек, чтобы твой AI-аватар был живым и продавал на русском, как профи 🤯✨\n"
        "В PDF всё не влезает — поэтому мы создали уютный 7-дневный тренинг.\n\n"
        "За неделю ты:\n"
        "- создашь своего реалистичного AI-аватара\n"
        "- запустишь маркетинговые связки, которые действительно приносят доход 💸\n\n"
        "В первом потоке всего 10 мест — у каждого будет персональный разбор от нашей команды 🌷\n\n"
        "Сейчас цена для своих — всего 9 922₽ вместо 14 222₽!\n"
        "Хочешь в первую волну?"
    ),
    "offer": (
        "Что тебя ждёт? 🍌\n"
        "✅ В мини-группе ты создашь своих реалистичных AI-аватаров\n"
        "✅ Будешь отрабатывать проверенные маркетинговые связки, которые приносят не только охваты, но и настоящий доход 🤑\n"
        "👌🏻 Всё разделено на 5 простых блоков — только нужные шаги, лайфхаки и секретики для русскоязычных аватаров, чтобы получилось красиво и по-настоящему живо!\n"
        "🎥 Все уроки останутся у тебя навсегда — можешь возвращаться к ним в любое время, даже с чашкой чая на кухне ☕️\n\n"
        "Хочешь успеть в первый набор? Жми на кнопку и забирай своё место — их всего 10!"
    ),
    "ask_phone": (
        "Чтобы забронировать своё место в первом потоке по спец условиям, просто напиши свой номер WhatsApp в ответ на это сообщение — я пришлю тебе подтверждение и держу место за тобой!\n\n"
        "Успей попасть в команду первых — жду твой номер! 🙌✨"
    ),
    "confirmation": (
        "Поздравляю, твоё место в первом потоке уже забронировано до конца дня! 😇\n\n"
        "Чтобы подтвердить участие, просто перейди по ссылке и внеси оплату.\n"
        "Если появятся вопросы — пиши, я всегда на связи! 🙌"
    ),
}

def kb_welcome():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add("😁 Хочу")

def kb_experience():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Немного")
    kb.add("🔥 Хороший опыт")
    kb.add("😇 Нет еще")
    return kb

def kb_about_you():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("👌🏻 Для себя")
    kb.add("🚀 Для клиентов")
    kb.add("Оба варианта")
    return kb

def kb_product():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔥 Забрать место")
    kb.add("😁 Хочу подробнее")
    return kb

def kb_offer():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔥 Занять место")
    return kb

def kb_confirm():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("✅ Подтвердить")
    return kb

def kb_remove():
    return types.ReplyKeyboardRemove()

@dp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await Form.welcome.set()
    await state.reset_data()
    await message.answer(TEXTS["welcome"], reply_markup=kb_welcome())

@dp.message_handler(lambda m: m.text == "😁 Хочу", state=Form.welcome)
async def step_welcome(message: types.Message, state: FSMContext):
    await Form.experience.set()
    await message.answer(TEXTS["experience"], reply_markup=kb_experience())

@dp.message_handler(lambda m: m.text in ["Немного", "🔥 Хороший опыт", "😇 Нет еще"], state=Form.experience)
async def step_experience(message: types.Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await Form.about_you.set()
    await message.answer(TEXTS["about_you"], reply_markup=kb_about_you())

@dp.message_handler(lambda m: m.text in ["👌🏻 Для себя", "🚀 Для клиентов", "Оба варианта"], state=Form.about_you)
async def step_about_you(message: types.Message, state: FSMContext):
    await state.update_data(about=message.text)
    await Form.product.set()
    await message.answer(TEXTS["product"], reply_markup=kb_product())

@dp.message_handler(lambda m: m.text in ["🔥 Забрать место", "😁 Хочу подробнее"], state=Form.product)
async def step_product(message: types.Message, state: FSMContext):
    await state.update_data(product_choice=message.text)
    await Form.offer.set()
    await message.answer(TEXTS["offer"], reply_markup=kb_offer())

@dp.message_handler(lambda m: m.text == "🔥 Занять место", state=Form.offer)
async def step_offer(message: types.Message, state: FSMContext):
    await Form.ask_phone.set()
    await message.answer(TEXTS["ask_phone"], reply_markup=kb_remove())

@dp.message_handler(state=Form.ask_phone, content_types=types.ContentTypes.TEXT)
async def step_ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await Form.confirmation.set()
    await message.answer(TEXTS["confirmation"], reply_markup=kb_confirm())

@dp.message_handler(lambda m: m.text == "✅ Подтвердить", state=Form.confirmation)
async def step_confirm(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Спасибо! Если возникнут вопросы — напиши мне в любой момент.", reply_markup=kb_remove())

@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def fallback_handler(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, используйте кнопки для ответа или введите требуемую информацию.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
