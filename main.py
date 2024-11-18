import requests
from bs4 import BeautifulSoup
import time

# Ваши заголовки
headers = {

}

response = requests.get("https://yummyanime.tv/2top-100/")
bs = BeautifulSoup(response.text, "lxml")

def card_links():
    anime_cards = bs.find_all("div", class_="movie-item")
    for anime_card in anime_cards:
        anime_card_link = "https://yummyanime.tv/" + anime_card.find("a", class_="movie-item__link").get("href")
        response_card = requests.get(anime_card_link)
        if response_card.status_code <= 200:
            yield anime_card_link
        else:
            continue
def all_info():
    k = 0
    for link in card_links():

        resp = requests.get(link, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        time.sleep(1)

        title = soup.find("div", class_="inner-page__title").find("h1").text

        director = soup.find("ul", class_="inner-page__list").find_all("li")[2].find_all("span")[1].text

        rating = soup.find("ul", class_="inner-page__list").find_all("li")[3].find_all("span")[1].text + "/10"

        unlinked_array_genres = soup.find("ul", class_="inner-page__list").find_all("li")[4].find_all("a")
        array_genres = [genre.text for genre in unlinked_array_genres]
        genres = ', '.join(array_genres)

        k += 1
        print(f"{k}. {title}\n{director}\n{rating}\n{genres}\n")

all_info()