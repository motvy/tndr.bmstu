# -*- coding: utf-8 -*-

"""
1 - en
2 - ru
"""

def tr(lang, key, *args):
	msg = messages.get(key, {1: 'No translated', 2: 'Не переведено'})
	return msg.get(lang, msg.get(2)).format(*args)

def language(lang):
	return langs.get(lang, 2)

def language_scode(lang):
	return lang_scodes.get(lang, 'en')


langs = {
	1: 'English'
,	2: 'Русский'
}

lang_scodes = {
	1: 'en'
,	2: 'ru'
}

messages = {
    'email_html_text': {
        1: """\
<html>
    <body style="background-color: #dbc5d5">
        <center>
            <!-- <img src="https://fikiwiki.com/uploads/posts/2022-02/1644855676_21-fikiwiki-com-p-kartinki-khd-kachestva-21.jpg" /> -->
            <strong>Hello, {}!</strong>
            <p>Confirmation code:<br>
                <strong>{}</strong>
            </p>
            <p><i>This code is only use for varification of your registration at BMSTU.TINDER. It is no needed for anything else.
                Do not share this code with anyone, even if it is requested from Telegram.
            </i></p>
            <p>If you did not request confirmation code, please ignore this message.</p>
            <strong>Respectfully,<br>BMSTU.TNDR team</strong>
        </center>  
    </body>
</html>
""",
        2: """\
<html>
    <body style="background-color: #dbc5d5">
        <center>
            <!-- <img src="https://fikiwiki.com/uploads/posts/2022-02/1644855676_21-fikiwiki-com-p-kartinki-khd-kachestva-21.jpg" /> -->
            <strong>Привет, {}!</strong>
            <p>Код подтверждения:<br>
                <strong>{}</strong>
            </p>
            <p><i>Этот код используется только для подтверждения регистрации в BMSTU.TNDR. Он не нужен для чего-то еще. 
                Никому не давайте код, даже если его требуют от имени Telegram.
            </i></p>
            <p>Если вы не запрашивали код подтверждения, проигнорируйте это сообщение.</p>
            <strong>С уважением,<br>Команда BMSTU.TNDR</strong>
        </center>  
    </body>
</html>
"""
    },
    'start_msg': {
        1: 'Start message',
        2: 'Стартовое сообщение',
    },
    'received_email': {
        1: 'Email received',
        2: 'Почта получена',        
    },
    'received_code': {
        1: 'Code received',
        2: 'Код получен',
    },
    'invalid_email': {
        1: 'Something wrong with your email.\nEnter yours corporation email with bmstu.ru domain.',
        2: 'С твоей почтой что-то не так.\nВведи свою корпоративную почту в домене bmstu.ru.',
    },
    'about': {
        1: 'About',
        2: 'О боте',
    },
    'help': {
        1: 'Help',
        2: 'Помощь',
    },
    'waiting_email': {
        1: 'Enter yours corporation email with bmstu.ru domain.',
        2: 'Введи свою корпоративную почту в домене bmstu.ru.',
    },
    'waiting_code_query': {
        1: '''We have sent a confirmation code to {}. Write it as a reply to this post.
The code should arrive within a minute - if it does not happen, try again with /code command.''',
        2: '''Мы отправили код для подтверждения аккаунта на {}. Напиши его в ответ на это сообщение.
Код должен прийти в течение минуты — если этого не произошло, попробуй ещё раз, выполнив команду /code''',
    },
    'valid_code': {
        1: 'Your account has been verified!\nTo create profile use /profile command.',
        2: 'Твой аккаунт подтвержден!\nДля создания профиля воспользуйся командой /profile',
    },
    'invalid_code': {
        1: 'Code is invalid or expired. Try again with /code command',
        2: 'Код неверный или истекло время ожидания. Попробуй ещё раз, выполнив команду /code',
    },
    'contact_support': {
        1: 'Contact [support]({})',
        2: 'Обратиться в [службу поддержки]({})',        
    },
    'cancel_command': {
        1: 'Cancel /cancel',
    	2: 'Отмена /cancel',
    },
    'canceled_login': {
        1: 'Account verification canceled.',
        2: 'Подтверждение аккаунта отменено',
    },
    'question_code_invalid' : {
        1: 'Enter your email with bmstu.ru domain first through /login command. Then you will be able to request a code.',
    	2: 'Сначала введи имейл в домене bmstu.ru, с помощью команды /login. После этого ты сможешь запросить код.',
    },
    'question_delete_account' : {
        1: '''Are you sure that you want to delete your BMSTU.TNDR account?
Your profile will be also deleted''',
    	2: '''Ты уверен, что хочешь удалить аккаунт BMSTU.TNDR?
Твоя анкета также будет удалена''',
    },
    'delete_btn': {
        1: 'Delete',
        2: 'Да, удалить',
    },
    'cancel_btn': {
        1: 'Cancel',
        2: 'Отмена',
    },
    'user_for _delete_not_found': {
        1: 'There is no confirmed account for deleting',
        2: 'Нет потдвержденного аккаунта для удаления',
    },
    'delete_success': {
        1: 'Your account was deleted successfully. Для его восстановления воспользуйся командой /login',
        2: 'Твой аккаунт BMSTU.TNDR удален. Для его восстановления воспользуйся командой /login',
    },
    'delete_canceled': {
        1: 'Account deleting was canceled',
        2: 'Удаление аккаунта отменено',
    },
    'lang_question': {
        1: 'Choose your language',
        2: 'Выбери язык для общения с ботом',
    },
    'ru_lang': {
        1: 'Русский',
        2: 'Русский',
    },
    'en_lang': {
        1: 'English',
        2: 'English',
    },
    'select_ru_lang': {
        1: 'Язык изменен на русский',
        2: 'Язык изменен на русский',
    },
    'select_en_lang': {
        1: 'Language changed to English',
        2: 'Language changed to English',
    },
    'profile_empty': {
        1: '_Blank profile_',
        2: '_Анкета пуста_',
    },
    'has_no_login': {
        1: 'To use this command, you have to authorise in chat with /login command first',
        2: 'Для выполнения этой команды необходимо авторизоваться в чате при помощи команды /login',
    },
    'ask_name': {
        1: 'Enter your name',
        2: 'Введи имя',
    },
    'incorrect_name': {
        1: 'Enter correct name without numbers and special characters',
        2: 'Введи корректное имя без цифр и спецсимволов',
    },
    'cancelled_name': {
        1: 'Name input canceled',
        2: 'Ввод имени отменен',
    },
    'ask_date_of_birth': { # DD.MM.YYYY 
        1: 'Enter your birth date (DD.MM.YYYY)',
        2: 'Введи дату рождения (ДД.ММ.ГГГГ)',
    },
    'incorrect_date': {
        1: 'Enter correct date of birth in format DD.MM.YYYY',
        2: 'Введи корректную дату рождения в формате ДД.ММ.ГГГГ',
    },
    'cancelled_date': {
        1: 'Birth date input canceled',
        2: 'Ввод даты рождения отменен',
    },
    'ask_photo': {
        1: 'Send profile photo',
        2: 'Отправь свое фото',
    },
    'cancelled_photo': {
        1: 'Set profile photo canceled',
        2: 'Установка фото отменена',
    },
    'ask_gender': {
        1: 'Choose gender:',
        2: 'Давай определимся, кто ты:',
    },
    'men_select': {
        1: 'Male',
        2: 'Парень',
    },
    'women_select': {
        1: 'Female',
        2: 'Девушка',
    },
    'ask_about': {
        1: 'Tell about yourself',
        2: 'Расскажи немного о себе',
    },
    'incorrect_about': {
        1: 'Tell about yourself from 50 to 500 symbols\nYou entered: {} ({})',
        2: 'Расскажи о себе от 50 до 500 символов\nТы ввел: {} ({})',
    },
    'cancelled_about': {
        1: 'Profile information input canceled',
        2: 'Ввод информации о себе отменен',
    },
    'ask_voice': {
        1: 'Send voice message',
        2: 'Отправь голосовое сообщение',
    },
    'ask_study_group': {
        1: 'Enter your study group (ИУ6-54Б)',
        2: 'Введи учебную группу (ИУ6-54Б)',
    },
    'incorrect_study_group': {
        1: 'Enter correct group number in ИУ6-54Б format',
        2: 'Введи корректную группу в формате ИУ6-54Б',
    },
    'ask_vk_link': {
        1: 'Enter your vk link (https://vk.com/username)',
        2: 'Отправь ссылку на свою страницу вк (https://vk.com/username)',
    },
    'incorrect_vk_link': {
        1: 'Enter corrcet vk link in https://vk.com/username format',
        2: 'Отправь корректную ссылку на свою страницу вк в формате https://vk.com/username',
    },
    'not_unique_vk_link': {
        1: '''Someone has already specified {} as their.
If this is your page, please [contact support]({}).
Or enter corrcet vk link in https://vk.com/username format''',
        2: '''Кто-то уже укаказал {} как свою.
Если это твоя страница, пожалуйста, свяжись со [службой поддержки]({}).
Или отправь корректную ссылку на свою страницу вк в формате https://vk.com/username''',
    },
    'ask_tags': {
        1: 'Chose from the list',
        2: 'Выберите из списка',
    },
    'empty_profile': {
        1: '_Blank Profile_',
        2: '_Анкета пуста_',
    },
    'without_name': {
        1: 'No name',
        2: 'Без имени',
    },
    'name_info': {
        1: '*Name*: {}',
        2: '*Имя:* {}',
    },
    'date_info': {
        1: '*Date of birth:* {}',
        2: '*Дата рождения:* {}',
    },
    'about_info': {
        1: '*About me:* {}',
        2: '*О себе:* {}',
    },
    'gender_info': {
        1: '*Gender:* {}',
        2: '*Пол:* {}',
    },
    'vk_link_info': {
        1: '*VK link:* {}',
        2: '*Ссылка на вк:* {}',
    },
    'study_group_info': {
        1: '*Study group:* {}',
        2: '*Учебная группа:* {}',
    },
    'tags_info': {
        1: '*Tags:* {}',
        2: '*Интересы:* {}'
    },
    'none_info': {
        1: '_Empty_',
        2: '_Пусто_',
    },
    'it': {
        1: '💻IT',
        2: '💻IT',
    },
    'anime': {
        1: '🦹Anime',
        2: '🦹Аниме',
    },
    'sport': {
        1: '💪sport',
        2: '💪спорт',
    },
    'study': {
        1: '🎓study',
        2: '🎓ботать',
    },
    'music': {
        1: '🎶music',
        2: '🎶музыка',
    },
    'party': {
        1: '🍾party',
        2: '🍾тусы',
    },
    'books': {
        1: '📚books',
        2: '📚книги',
    },
    'games': {
        1: '🎮games',
        2: '🎮игры',
    },
    'science': {
        1: '🔭science',
        2: '🔭наука',
    },
    'films': {
        1: '🍿films',
        2: '🍿кино',
    },
    'food': {
        1: '🥦food',
        2: '🥦еда',
    },
    'languages': {
        1: '🇬🇧languages',
        2: '🇬🇧языки',
    },
    'finance': {
        1: '💵finance',
        2: '💵финансы',
    },
    'history': {
        1: '🦖history',
        2: '🦖история',
    },
    'medicine': {
        1: '💊medicine',
        2: '💊медицина',
    },
    'name': {
        1: 'Name',
        2: 'Имя',
    },
    'gender': {
        1: 'Gender',
        2: 'Пол',
    },
    'age': {
        1: 'Age',
        2: 'Возраст',
    },
    'photo': {
        1: 'Photo',
        2: 'Фото',
    },
    'about': {
        1: 'About me',
        2: 'О себе',
    },
    'tags': {
        1: 'Tags',
        2: 'Интересы',
    },
    'vk_link': {
        1: 'Vk link',
        2: 'Ссылка на вк',
    },
    'view': {
        1: 'Profile for others',
        2: 'Как мой профиль видят другие',
    },
    'group': {
        1: 'Study group',
        2: 'Учебная группа',
    },
    'clear': {
        1: 'Clear',
        2: 'Очистить',
    },
    'save': {
        1: 'Save',
        2: 'Сохранить',
    },
    'no': {
        1: 'No',
        2: 'Нет',
    },
    'no_vk': {
        1: "I don't have vk page",
        2: 'У меня нет страницы вк'
    },
    'not_full_profile': {
        1: 'To start swapping, you need to fill out the profile completely with command /profile',
        2: 'Чтобы начать свапать, необходимо полностью заполнить профиль при помощи команды /profile',
    },
    'go_swipe': {
        1: 'Use button to go to the main application.\n\nP.S. ou can always come back to set up your profile',
        2: 'Используйте кнопку для перехода в основное приложение.\n\nP.S. Ты всегда можешь вернуться для настройки своего профиля',
    },
    'swipe_btn': {
        1: 'Go swipe',
        2: 'Свайпать',
    },
    'setting_btn': {
        1: 'English Настроить профиль',
        2: 'Настроить профиль',
    },
    'menu_msg': {
        1: 'Menu',
        2: 'Меню',
    },
    'profiles_end': {
        1: 'English Анкеты закончились, попробуйте зайти позже',
        2: 'Анкеты закончились, попробуйте зайти позже',
    },
    'go_swipe_btn': {
        1: 'English Смотреть анкеты',
        2: 'Смотреть анкеты',
    },
    'show_fans_btn': {
        1: 'English Посмотреть кому ты нравишься',
        2: 'Посмотреть кому ты нравишься',
    },
    'show_match_btn': {
        1: 'English Посмотреть взаимные лайки',
        2: 'Посмотреть взаимные лайки',
    },
    'show_profile_btn': {
        1: 'My profile',
        2: 'Мой профиль',
    },
    'to_menu_btn': {
        1: 'To menu',
        2: 'В меню',
    },
    'no_likes': {
        1: 'English Ты просмотрел всех, кто лайкнул тебя',
        2: 'Ты просмотрел всех, кто лайкнул тебя',
    },
    'fuck_you': {
        1: 'Кому ты нахуй нужен?',
        2: 'Кому ты нахуй нужен?',
    },
    'hide': {
        1: 'English Скрыть',
        2: 'Скрыть',
    },
    'send_msg': {
        1: 'English Написать',
        2: 'Написать',
    },
    'end_match': {
        1: 'English Ты просмотрел все взаимные лайки',
        2: 'Ты просмотрел все взаимные лайки',
    },
    'schedule': {
        1: 'English Посмотреть учебное расписание',
        2: 'Посмотреть учебное расписание',
    },
    'places': {
        1: 'English Получить рекомендацию по местам встречи',
        2: 'Получить рекомендацию по местам встречи',
    },
    'get_time': {
        1: 'English Общее время свободное от занятий',
        2: 'Общее время свободное от занятий',
    },
    'back_btn': {
        1: 'Back',
        2: 'Назад',
    },
    'edit_centre': {
        1: 'English Изменить центр',
        2: 'Изменить центр',
    },
    'edit_radius': {
        1: 'English Изменить радиус',
        2: 'Изменить радиус',
    },
    'edit_tags': {
        1: 'English Изменить теги',
        2: 'Изменить теги',
    },
    'places_menu': {
        1: 'English Получить рекомендации',
        2: 'Получить рекомендации',
    },
    'get_place': {
        1: 'English Смотреть места',
        2: 'Смотреть места',
    },
    'lang_btn': {
        1: 'English Изменить язык',
        2: 'Изменить язык',
    },
    'delete_profile': {
        1: 'English Удалить профиль',
        2: 'Удалить профиль',
    },
    'my_profile': {
        1: 'English Мой профиль',
        2: 'Мой профиль',
    },
}