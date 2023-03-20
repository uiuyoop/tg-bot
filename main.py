# Импортируем библиотеки и модули
import requests
from bs4 import BeautifulSoup
import json

# Пишем функцию получения элементов
def get_promo():
    # Забираем хедер запроса 
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    # Назначаем URL страницы для парсинга
    url = "https://uiuyoop.github.io/for-parser/"
    # Пишем запрос на получения от страницы
    request = requests.get(url=url, headers=headers)
    # Используем bs4 и lxml для парсинга страницы
    soup = BeautifulSoup(request.text, "lxml")
    # Парсим все элементы "a" с нужным классом
    articles_card = soup.find_all("a", class_="article-card")
    # Создаем список для записи элементов
    promo_dict = {}
    # Проводим цикл по всем "a" и находим нужные элементы для отправики в чат
    for article in articles_card:
        # Заголовки
        article_title = article.find("h2", class_="article-card-title").text.strip()
        # Описание
        article_desc = article.find("p").text.strip()
        # Гиперссылку на страницу
        article_url = f'https://uiuyoop.github.io/for-parser/{article.get("href")}'
        # Пробегаем по id с последнего места
        article_id = article_url.split("/")[-1]
        # Делаем срез
        article_id = article_id[:-4]
        # Заносим спарсенные элементы в список JSON форматом
        promo_dict[article_id] = {
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }
    # Записываем JSON файл
    with open("tg-bot/promo_dict.json", "w") as file:
        json.dump(promo_dict, file, indent=4, ensure_ascii=False)

# Пишем функцию для проверки новых акций
def check_promo_update():
    # Загружаем, записанный JSON файл
    with open("tg-bot/promo_dict.json") as file:
        promo_dict = json.load(file)
    
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    url = "https://uiuyoop.github.io/for-parser/"
    request = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(request.text, "lxml")
    articles_card = soup.find_all("a", class_="article-card")
    # Вводим новый список, свежих акций
    fresh_promo = {}
    # Проходим циклом по id элементам
    for article in articles_card:
        article_url = f'https://uiuyoop.github.io/for-parser/{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]
        # Пишем условие, если такой id есть в списке, пропускаем
        if article_id in promo_dict:
            continue
        # Если нет, то парсим новый элемент
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()
            # Записываем id элементов в промо список
            promo_dict[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
            # Записываем id элементов в свежий промо список
            fresh_promo[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }
    # Записываем JSON файл
    with open("tg-bot/promo_dict.json", "w") as file:
        json.dump(promo_dict, file, indent=4, ensure_ascii=False)
    # Возвращаем список свещих акций
    return fresh_promo
# Запускаем функцию для получения акций
def main():
    get_promo()
# Запускаем код
if __name__ == '__main__':
    main()