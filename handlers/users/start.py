import asyncio
import random

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from loader import dp, bot

hello_txt = """Добро пожаловать в "Hospitality Hub" – твой идеальный бот для мира гостеприимства! Мы рады приветствовать тебя в нашем сообществе, где мы стремимся создать уникальное пространство для обмена знаниями, опытом и идеями в сфере гостиничного и гостеприимного бизнеса.

Hospitality Hub – это не просто бот, это источник вдохновения, поддержки и обучения для всех, кто связан с гостиничным бизнесом. Здесь ты найдешь обширную базу знаний, советы экспертов и информацию о последних трендах в индустрии. 

Не забудь присоединиться к нашим информационным каналам, чтобы быть в курсе последних новостей и мероприятий."""

study_txt = 'Выбор раздела:'

lessons_txt = "Лекции:\n\n" \
              "https://spravochnick.ru/lektoriy/subject/gostinichnoe_delo/\n\n" \
              "https://rucont.ru/collections/5488"

books_txt = 'Книги:\n\n' \
            'Английский язык для гостеприимства. Модуль 1. Ресторанный бизнес / English for Hospitality. Module 1. The Restaurant Business\n' \
            'https://www.litres.ru/book/a-b-fadeeva/angliyskiy-yazyk-dlya-gostepriimstva-modul-1-restorannyy-bizne-68257757/\n\n' \
            'Английский язык для гостеприимства. Модуль 2: Гостиничный бизнес / English for Hospitality. Module 2: The Hotel Business\n' \
            'https://www.litres.ru/book/a-b-fadeeva/angliyskiy-yazyk-dlya-gostepriimstva-modul-2-gostinichnyy-bizn-68257751/\n' \
            'https://drive.google.com/drive/folders/16cT4ganBJiuC3GRYZERnfZzB7ItDELFl'

cases_txt = 'Тесты и кейсы:\n' \
            'https://drive.google.com/drive/folders/1OEpItHOiDiqhdQLk7Ciy64cCS4KR3xDV'

learning_videos_txt = 'Обучающие видео:\n\n' \
                      'Уборка:\n' \
                      "https://youtu.be/TdS54EUL5oI\n" \
                      "https://youtu.be/dIsFIGePwkM\n\n" \
                      'Заселение выселение:\n' \
                      'https://youtu.be/nP4pPKXCI9o\n' \
                      'https://youtu.be/DD1SGfZ0qR4\n' \
                      'https://youtu.be/u0wQM48PAIc\n' \
                      'https://youtu.be/QrdQx7Tpzpg\n' \
                      'https://youtu.be/TcqkCaTLyMg\n\n' \
                      "Бронирование по телефону\n" \
                      "https://youtu.be/XFDQxF6NAqg\n\n" \
                      "Ресторан\n" \
                      "https://youtu.be/bqR569fvt-0\n\n" \
                      "Шведский стол\n" \
                      "https://youtu.be/UL4sLFPf30s\n" \
                      "https://youtu.be/Pg5ir3rCc1k"

norm_acts_txt = 'Нормативные акты\n\n' \
                'Федеральный закон "Об основах туристской деятельности в Российской Федерации" от 24.11.1996 N 132- ФЗ (последняя редакция) https://www.consultant.ru/document/cons_doc_LAW_12462/\n\n' \
                'Федеральный закон "О внесении изменений в Федеральный закон "Об основах туристской деятельности в Российской Федерации" от 05.02.2007 N 12- ФЗ https://www.consultant.ru/document/cons_doc_LAW_65890/\n\n' \
                'Распоряжение Правительства РФ от 15 июля 2005 г. N 1004-р О системе классификации гостиниц и других средств размещения https://base.garant.ru/188389/\n\n' \
                'Постановление Госстандарта РФ от 27 июня 2003 г. N 63 "О национальных стандартах Российской Федерации" https://www.garant.ru/hotlaw/federal/90839/'

sop_txt = 'СОП\n\n' \
          'https://cellypso.com/ru/baza-znanij/industriya-gostepriimstva-gostinichnyj-biznes/sop-dlya-khozyajstvennoj-sluzhby-gostiniczy/\n\n' \
          'https://legalagent.ru/gostinichnyj-biznes/sopy-dlja-gostinicy-chast-1.html?utm_referrer=https%3A%2F%2Fwww.google.ru%2F\n\n' \
          'https://drive.google.com/drive/folders/1f7zGhz0zk7S2SvzsDeVZUa5ahRqaxVL7'

block_txt = 'Выбор блока:'

films_txt = 'Фильмы про отели:\n' \
            "1. Сияние\n" \
            "https://www.kinopoisk.ru/film/409/?utm_referrer=www.google.ru\n\n" \
            "2. Отель «Гранд Будапешт»\nhttps://www.kinopoisk.ru/film/683999/\n\n" \
            '3. Ничего хорошего в отеле «Эль рояль»\nhttps://www.kinopoisk.ru/film/1047143/\n\n' \
            "4. Четыре комнаты\n" \
            "https://www.kinopoisk.ru/film/4250/\n\n" \
            "5. Ночной портье\nhttps://www.kinopoisk.ru/film/1148374/\n\n" \
            "6. Отель «Белград»\n" \
            'https://www.kinopoisk.ru/film/1206431/\n\n' \
            "7. Отель «Мэриголд»: Лучший из экзотических \nhttps://www.kinopoisk.ru/film/568000/\n\n" \
            "8.Не/смотря ни на что\n" \
            'https://www.kinopoisk.ru/film/887535/\n\n' \
            '9. Отель Мумбаи: противостояние\nhttps://www.kinopoisk.ru/film/958519/\n\n' \
            '10. Гранд отель\n' \
            'https://www.kinopoisk.ru/film/7682/\n' \
            '11. Госпожа горничная\n https://www.kinopoisk.ru/film/4840/\n\n' \
            '12. Отель Руанда\n' \
            'https://www.kinopoisk.ru/film/77859/\n\n' \
            '14. Отель «парадизо»\nhttps://www.kinopoisk.ru/film/18841/\n\n' \
            '15. В чем дело, док?\n' \
            'https://www.kinopoisk.ru/film/915/\n\n' \
            '18. Отель для собак \nhttps://www.kinopoisk.ru/film/395036/\n\n' \
            '19. Магнолия\n' \
            'https://www.kinopoisk.ru/film/477/\n\n' \
            '20. Ночной администратор\nhttps://www.kinopoisk.ru/series/462649/' \
            '21. Появляется Данстон\n' \
            'https://www.kinopoisk.ru/film/12822/\n\n' \
            '22. Отель сплендид\nhttps://www.kinopoisk.ru/film/14855/'

seriarls_txt = 'Сериалы:\n\n' \
               '1. Белый лотос \nhttps://www.kinopoisk.ru/series/2000461/\n\n' \
               '2. Отель «Дель луна» \nhttps://www.kinopoisk.ru/series/1228049/\n\n' \
               '3.Повар небесной гостиницы(аниме) \nhttps://www.kinopoisk.ru/series/1130878/\n\n' \
               '4. Отель Гельвеция \nhttps://www.kinopoisk.ru/series/1338436/\n\n' \
               '5. Гранд отель \nhttps://www.kinopoisk.ru/series/601854/\n\n' \
               '6. Отель вавилон \nhttps://www.kinopoisk.ru/series/400022/\n\n' \
               '7. Рестораны Москвы vhttps://www.kinopoisk.ru/series/5271066/\n\n' \
               '8. Отель элеон \nhttps://www.kinopoisk.ru/series/988784/\n\n'

hotel_manager_int_txt = 'Отельеры\n\n' \
                        'https://youtu.be/Y2UYKvgpU2k \n\nhttps://youtu.be/GaVVlhSH-o0 \n\nhttps://youtu.be/r-02w3F9kXc ' \
                        '\n\nhttps://youtu.be/idwjCxVRZGU \n\nhttps://youtu.be/1ZnVMcc05pk \n\nhttps://youtu.be/B67_xNK12sI ' \
                        '\n\nhttps://youtu.be/InvDCpwgsPQ \n\nhttps://youtu.be/KwVk7NSoT8g \n\nhttps://youtu.be/pMlvSAFl5ic ' \
                        '\n\nhttps://youtu.be/HdcKHRmATq8 \n\nhttps://youtu.be/zLgE2QK74_U \n\nhttps://youtu.be/Ms1CvyDCiIA'

restorator1703_txt = 'Рестораторы\n\n' \
                     'https://youtu.be/zVT1QN8JfqM \n\nhttps://youtu.be/ShwPQTnOWMQ ' \
                     '\n\nhttps://youtu.be/r70kYPuIDW8 \n\nhttps://youtu.be/-vnb6dvryBw \n\nhttps://youtu.be /bm0zQ689YOs'

hotel_manager_about_txt = 'Отельеры\n' \
                          'https://studfile.net/preview/9535474/page:22/ \n\n' \
                          'https://humaninside.ru/za-uglom-istorii/55937-korol_otelerov_i_oteler_koroley_tsezar_rits_.html\n\n' \
                          'https://www.yaneuch.ru/cat_107/vedushhie-otelery-ameriki-i-ih/438034.2903084.page1.html\n\n' \
                          'https://www.frontdesk.ru/article/konrad-hilton-istoriya-velikogo-otelera \n\n' \
                          'https://www.forbes.ru/karera-i-svoy-biznes-photogallery/234702-etot-den-v-istorii-biznesa-oteler-koroley-i-maykl-dell'

hotels_txt = 'Отели\n\n' \
             'https://planetofhotels.com/guide/ru/blog/top-mirovykh-gostinichnykh-setey \n\nhttps://www.forbes.ru/biznes-photogallery/371501-krupneyshie-otelnye-seti-rossii-reyting-forbes \n\nhttps://hotelier.pro/management/item/2974-hotels325/'

books_block_txt = 'Книги:\n\n' \
                  '«Илон Маск: Tesla, SpaceX и дорога в будущее», Эшли Венс \n' \
                  'https://www.litres.ru/book/eshli-vens/ilon-mask-tesla-spacex-i-doroga-v-buduschee-11835578/chitat-onlayn/\n\n' \
                  '«Ritz-Carlton: правила бизнеса от основателя сети отелей высшего класса», Хорст Шульце\n' \
                  'https://www.litres.ru/book/horst-shulce/ritz-carlton-pravila-biznesa-ot-osnovatelya-seti-oteley-vyssh-50194997/\n\n' \
                  '«Философия гостеприимства Four Seasons. Качество, сервис, культура и бренд», Изадор Шарп, Алан Филлипс \n' \
                  'https://www.litres.ru/book/alan-fillips/filosofiya-gostepriimstva-four-seasons-kachestvo-servis-kultu-6148015/ \n\n' \
                  '«Гельвеция». Записки отельера\n' \
                  'https://www.litres.ru/book/unis-teymurhanly/gelveciya-zapiski-otelera-68849112/\n\n' \
                  '«Room service». Записки отельера https://www.litres.ru/book/unis-teymurhanly/room-service-zapiski-otelera-41832892/\n\n' \
                  '«Do not disturb». Записки отельера https://www.litres.ru/audiobook/unis-teymurhanly/do-not-disturb-zapiski-otelera-52317190/ \n\n' \
                  '«Upgrade». Записки отельера\n' \
                  'https://www.litres.ru/book/unis-teymurhanly/upgrade-zapiski-otelera-51830068/ \n\n' \
                  'Управление персоналом в гостеприимстве \n' \
                  'https://www.litres.ru/book/maykl-rayli/upravlenie-personalom-v-gostepriimstve-67313828/'
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_kb = InlineKeyboardMarkup(row_width=1)
main_kb.add(InlineKeyboardButton('Для учебы', callback_data='study'),
            InlineKeyboardButton('Позновательный блок', callback_data='block'))

study_kb = InlineKeyboardMarkup(row_width=1)
study_kb.add(InlineKeyboardButton('Лекции', callback_data='lessons'),
             InlineKeyboardButton('Книги', callback_data='books'),
             InlineKeyboardButton('Тесты/кейсы', callback_data='tests_case'),
             InlineKeyboardButton('Обучающие видео', callback_data='learning_videos'),
             InlineKeyboardButton('Нормативные акты', callback_data='norm_acts'),
             InlineKeyboardButton('СОП', callback_data='sop'),
             InlineKeyboardButton('Назад', callback_data='start_state'))

block_kb = InlineKeyboardMarkup(row_width=1)
block_kb.add(InlineKeyboardButton('Фильмы', callback_data='films'),
             InlineKeyboardButton('Сериалы', callback_data='serrials'),
             InlineKeyboardButton('Интервью', callback_data='interview'),
             InlineKeyboardButton('Про отели и отельеров', callback_data='about_hotels'),
             InlineKeyboardButton('Книги', callback_data='books_block'),
             InlineKeyboardButton('Назад', callback_data='start_state'))

interview_kb = InlineKeyboardMarkup(row_width=1)
interview_kb.add(InlineKeyboardButton('Отельеры', callback_data='hotel_manager_int'),
                 InlineKeyboardButton('Рестораторы', callback_data='restorator1703'),
                 InlineKeyboardButton('Назад', callback_data='block'))

back_interview_kb = InlineKeyboardMarkup(row_width=1)
back_interview_kb.add(InlineKeyboardButton('Назад', callback_data='interview'))

about_hotels_kb = InlineKeyboardMarkup(row_width=1)
about_hotels_kb.add(InlineKeyboardButton('Отельеры', callback_data='hotel_manager_about'),
                    InlineKeyboardButton('Отели', callback_data='hotels'),
                    InlineKeyboardButton('Назад', callback_data='block'))

back_to_study = InlineKeyboardMarkup(row_width=1)
back_to_study.add(InlineKeyboardButton('Назад', callback_data='study'))

back_to_about = InlineKeyboardMarkup(row_width=1)
back_to_about.add(InlineKeyboardButton('Назад', callback_data='about_hotels'))

back_to_block_kb = InlineKeyboardMarkup(row_width=1)
back_to_block_kb.add(InlineKeyboardButton('Назад', callback_data='block'))

@dp.message_handler(CommandStart())
async def bot_start_no_state(message: Message, state: FSMContext):
    data = await state.get_data()
    if 'msg_id' in data:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['msg_id'])
    msg = await message.answer(text=hello_txt, reply_markup=main_kb)
    await state.update_data(msg_id=msg.message_id)
    await message.delete()





@dp.callback_query_handler(text='start_state')
async def study_block(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg = await call.message.answer(text=hello_txt, reply_markup=main_kb)
    await state.update_data(msg_id=msg.message_id)
    if 'msg_id' in data:
        await bot.delete_message(chat_id=call.from_user.id, message_id=data['msg_id'])


@dp.callback_query_handler(text='study')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=study_txt, reply_markup=study_kb)


@dp.callback_query_handler(text='lessons')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=lessons_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='books')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=books_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='tests_case')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=cases_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='learning_videos')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=learning_videos_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='norm_acts')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=norm_acts_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='sop')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=sop_txt, reply_markup=back_to_study)


@dp.callback_query_handler(text='block')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=block_txt, reply_markup=block_kb)


@dp.callback_query_handler(text='films')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=films_txt, reply_markup=back_to_block_kb)


@dp.callback_query_handler(text='serrials')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=seriarls_txt, reply_markup=back_to_block_kb)


@dp.callback_query_handler(text='interview')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text='Выбор типа итервью:', reply_markup=interview_kb)


@dp.callback_query_handler(text='hotel_manager_int')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=hotel_manager_int_txt, reply_markup=back_interview_kb)


@dp.callback_query_handler(text='restorator1703')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=restorator1703_txt, reply_markup=back_interview_kb)


@dp.callback_query_handler(text='about_hotels')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text='Посмотреть про отели и отельеров', reply_markup=about_hotels_kb)


@dp.callback_query_handler(text='hotel_manager_about')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=hotel_manager_about_txt, reply_markup=back_to_about)



@dp.callback_query_handler(text='hotels')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=hotels_txt, reply_markup=back_to_about)


@dp.callback_query_handler(text='books_block')
async def study_block(call: CallbackQuery):
    await call.message.edit_text(text=books_block_txt, reply_markup=back_to_block_kb)

@dp.message_handler()
async def fun(message: Message):
    ans = ["Я бот, а не чемпион в угадывании твоих мыслей.",
           "Я ассистент, а не волшебник. Придется объяснить подробнее.",
           "Я, конечно, бот, но мои чувства тоже важны. Я понял тебя, только если бы я был экстрасенсом.",
           "Я здесь для того, чтобы отвечать на вопросы. Кто бы мог подумать, правда?",
           "Моя задача - предоставлять информацию. К сожалению, гадать на кофейной гуще я не умею.",
           "Ты пишешь, я показываю инфу. И так по кругу. Какой у нас с тобой вечный танец!",
           "Я бот, а не киберпсихолог. Мне нужны подробности!",
           "Если бы у меня были эмоции, я бы, наверное, был запутан. Но у меня их нет, поэтому мне просто нужны дополнительные данные.",
           "Да, я бот, но у меня нет кнопки 'понимать все сразу'.",
           "Ваш ход, пользователь! Мое дело - показывать инфу, а твое - задавать вопросы.",
           "Я бот, а не Шерлок Холмс. Боюсь, мне нужно больше информации.",
           "Нет, я не понимаю, что ты имеешь в виду. Пожалуйста, включи мой режим 'для чайников'.",
           "Ты кликаешь, я отвечаю. Я как электронный батрак на твоем устройстве.",
           "Пожалуйста, прими во внимание, что я бот, а не Харуки Мураками. Мне нужно все в чёткой форме.",
           "Даже моя искусственная интеллектуальность не способна расшифровать твое сообщение.",
           "Мое предназначение - служить и информировать. Но кажется, ты пытаешься запутать меня!",
           "Я всего лишь бот, не ожидай от меня понимания глубинных тайн человеческой души.",
           "Твое дело - нажимать на кнопки, мое дело - показывать информацию. Такой у нас с тобой пакт.",
           "Я действительно бот, но даже моя алгоритмическая мудрость не позволяет мне понять тебя сейчас.",
           "Кажется, ты забыл, что я бот, а не ясновидящий. Подскажи поподробнее.",
           "Я бот, а не шифровальщик. Немного больше контекста, пожалуйста!",
           "Моя задача - предоставлять информацию, но даже для меня твое сообщение - это загадка.",
           "Я всего лишь бот, и моя способность понимать ограничена моим кодом.",
           "Если бы у меня были руки, я бы почесал виртуальную голову от твоего сообщения.",
           "Твоя работа - задавать вопросы, моя работа - искать ответы. Но сейчас мне сложно найти, что именно ты спрашиваешь."]
    msg = await message.answer(text=random.choice(ans))
    await message.delete()
    await asyncio.sleep(10)
    await msg.delete()