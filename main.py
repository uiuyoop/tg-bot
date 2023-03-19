import requests
from bs4 import BeautifulSoup
import json

def get_promo():

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    url = "https://uiuyoop.github.io/for-parser/"
    request = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(request.text, "lxml")

    articles_card = soup.find_all("a", class_="article-card")

    promo_dict = {}
    for article in articles_card:
        article_title = article.find("h2", class_="article-card-title").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = f'https://uiuyoop.github.io/for-parser/{article.get("href")}'

        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        promo_dict[article_id] = {
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }

    with open("tg-bot/promo_dict.json", "w") as file:
        json.dump(promo_dict, file, indent=4, ensure_ascii=False)


def check_promo_update():

    with open("tg-bot/promo_dict.json") as file:
        promo_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    url = "https://uiuyoop.github.io/for-parser/"
    request = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(request.text, "lxml")
    articles_card = soup.find_all("a", class_="article-card")

    fresh_promo = {}
    for article in articles_card:
        article_url = f'https://uiuyoop.github.io/for-parser/{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in promo_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()

            promo_dict[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_promo[article_id] = {
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

    with open("tg-bot/news_dict.json", "w") as file:
        json.dump(promo_dict, file, indent=4, ensure_ascii=False)

    return fresh_promo

def main():
    get_promo()


if __name__ == '__main__':
    main()