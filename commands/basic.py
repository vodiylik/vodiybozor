# Queries
from queries.users import user_exists
from queries.users import insert_user
from queries.users import deactivate_user
from queries.users import get_admins

# Helpers
from utils.helpers import format_text

# Misc
import json


async def process_start_command(chat, match, logger):
    has_last_name = lambda u: u.get('last_name', '') != ''
    first_name = chat.sender.get('first_name')
    fullname = first_name

    if has_last_name(chat.sender):
        fullname = first_name + ' ' + chat.sender.get('last_name')

    greeting = format_text('''
    Ассалому алайкум {name}!
    Водий бозорга хуш келибсиз.
    ''')

    await insert_user(chat.bot.pg_pool, chat.sender)

    if not await user_exists(chat.bot.pg_pool, chat.sender):
        logger.info('New user %s requested /start', chat.sender)
        await chat.send_text(greeting.format(name=fullname))


async def process_menu_command(chat, match, logger):
    info = format_text('''
    *МЕНЮ*

    /ads - эълонлар
    /sub - обуна
    /rules - канал қоидалари
    /contact - админлар билан боғланиш
    /stop - ботни тўхтатиш

    [Канал манзили](https://t.me/vodiybozor)
    ''')
    logger.info('%s menu requested by', chat.sender)
    await chat.send_text(info, parse_mode='Markdown', disable_web_page_preview=True)


async def process_rules_command(chat, match, logger):
    info = format_text('''
    *ХИЗМАТ* *ШАРТЛАРИ* *ВА* *ҚОИДАЛАР*

    1. Бир кунда бир тур бўйича биттадан ортиқ эълон бериш мумкин эмас.
    ''')
    logger.info('%s eula requested by', chat.sender)
    await chat.send_text(info, parse_mode='Markdown', disable_web_page_preview=True)


async def process_contact_command(chat, match, logger):
    logger.info('%s contact requested by', chat.sender)

    contacts = format_text('''
    *Админлар:*

    {admins}
    ''')

    admins = []
    for admin in await get_admins(chat.bot.pg_pool):
        admins.append('@' + admin)

    text = contacts.format(admins=admins).replace('\'', '')

    await chat.send_text(text, parse_mode='Markdown', disable_web_page_preview=True)


async def process_stop_command(chat, match, logger):
    farewell = format_text('''
    Қизиқиш учун раҳмат, {name}.
    [Каналимизни](https://t.me/vodiybozor) кузатишда давом этинг.
    ''')
    await deactivate_user(chat.bot.pg_pool, chat.sender)
    logger.info('%s deactivated', chat.sender)
    await chat.send_text(
        farewell.format(name=chat.sender['first_name']),
        parse_mode='Markdown',
        disable_web_page_preview=True)


async def process_unknown_command(chat, match, logger):
    question = format_text('''
    {name}, қизиқиш билдирганингиз учун раҳмат.

    Ҳозирда бу бўлим дастурлаштириляпти.
    ''')
    # question = format_text('''
    # {name}, мен ботман. Бунақа гапларни тўғриси тушунмайман. Мен фақат чой дамлайман холос. 😃

    # Балки, админларга бирор гапингиз бордир?
    # ''')
    # keyboard = [
    #     ['👮🏻 Админ керак', '📃 Менюни кўрмоқчиман'],
    # ]
    # reply_keyboard_markup = {
    #     'keyboard': keyboard,
    #     'resize_keyboard': True,
    #     'one_time_keyboard': True
    # }

    logger.info('%s unknown requested by', chat.sender)
    await chat.send_text(
        question.format(name=chat.sender['first_name']),
        parse_mode='Markdown',
        disable_web_page_preview=True)
        # reply_markup=json.dumps(reply_keyboard_markup))
