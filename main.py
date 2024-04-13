import requests
from bs4 import BeautifulSoup
import time

headers = { #Ваши заголовки
    "User-Agent": ""
}

#Стандартный запрос на главную страницу сайта
url = "https://yummyanime.tv/2top-100/"
response = requests.get(url, headers=headers)
bs = BeautifulSoup(response.text, 'lxml')

def card_links():
    anime_cards = bs.find_all("div", class_="movie-item")
    for anime_card in anime_cards:
        anime_card_link = "https://yummyanime.tv" + anime_card.find("a", class_="movie-item__link").get("href")
        yield anime_card_link #Вытаскиваем ссылки на карточки

def all_info():
    for link in card_links():
        k = 0
        resp = requests.get(link, headers=headers) #Запрос на страницу карточки аниме
        soup = BeautifulSoup(resp.text, "lxml")
        time.sleep(1) #Чтобы не нагружать сайт, поставим задержку в 1 секунду

        title = soup.find("div", class_="inner-page__title").find("h1").text #Нашли название аниме

        #Нашли имя режиссёра
        ul = soup.find("ul", class_="inner-page__list")
        li_director = ul.find_all("li")[2]
        director = li_director.find_all("span")[1].text

        #Нашли рейтинг
        li_rating = ul.find_all("li")[3]
        rating = li_rating.find_all("span")[1].text + " / 10"

        #Нашли жанры
        li_genre = ul.find_all("li")[4]
        span_genre = li_genre.find_all("span")[1]
        a_genres = span_genre.find_all("a")
        #Перебираем каждый эллемент в текст, чтобы избавиться от тегов <a> и получить чистый текст
        array_genres = [a_genre.text for a_genre in a_genres]
        genres = ', '.join(array_genres) #Преобразовываем список жанров в строку

        yield title, director, rating, genres

        #print(f"{k}, Название: {title}, Директор: {director}, Рейтинг: {rating}, Жанр: {genres}\n")









