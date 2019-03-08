import telebot
import requests
import config
from bs4 import BeautifulSoup
from telebot import apihelper

f = open(".teletoken", "r")
token = f.read().strip()
bot = telebot.TeleBot(token)

f = open(".socks5", "r")
socks_url = f.read().strip()
apihelper.proxy = {'https': socks_url}

config.domain = "http://www.ifmo.ru/ru/schedule/0"
week_days = {
    "monday": "1day",
    "tuesday": "2day",
    "wednesday": "3day",
    "thursday": "4day",
    "friday": "5day",
    "saturday": "6day",
    "sunday": "7day"
}


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, week_day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на нужный день недели
    schedule_table = soup.find("table", attrs={"id": week_days[week_day]})
    if schedule_table is None:
        return None, None, None

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
    return times_list, locations_list, lessons_list


@bot.message_handler(commands=week_days.keys())
def get_week_day(message):
    week_day, group = message.text.split()
    week_day = week_day.strip("/")
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page, week_day)

    resp = ''
    if times_lst is not None:
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    else:
        resp = '<b>В этот день нет пар, можете отдохнуть ;)</b>\n'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


# @bot.message_handler(content_types=['text'])
# def echo(message):
#     bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
