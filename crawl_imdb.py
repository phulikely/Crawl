import random
import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/chart/top/'
headers = {'Accept-Language': 'en-US,en;q=0.8'}


def main():
    response = requests.get(url=url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    movie_tags = soup.select('td.titleColumn')
    total_movies = len(movie_tags)
    print(f'total movies here :{total_movies}')
    inner_movie_tags = soup.select('td.titleColumn a')
    # rating_tags = soup.find_all(attrs={'class': 'ratingColumn'})
    rating_tags = soup.find_all(attrs={'class': 'imdbRating'})
    # rating_tags_0 = rating_tags[0]
    # rating_tags_0_split = rating_tags_0.text.split()
    # print(rating_tags_0_split[0]) #9.2

    def get_year(movie_tag):
        movie_split = movie_tag.text.split()
        year = movie_split[-1]
        year = year.replace('(', '').replace(')', '')
        return int(year)

    years = [get_year(tag) for tag in movie_tags]
    actors = [tag['title'] for tag in inner_movie_tags]
    titles = [tag.text for tag in inner_movie_tags]
    ratings = [float(tag.text.split()[0]) for tag in rating_tags]

    while 1:
        # for idx in range(0, total_movies):
        #     if years[idx] >= 2020:
        #         print(f'{titles[idx]} | {years[idx]} | rating: {ratings[idx]} | starring: {actors[idx]}\n')
        idx = random.randrange(0, total_movies)
        print(f'{titles[idx]} | {years[idx]} | rating: {ratings[idx]} | starring: {actors[idx]}\n')
        user_input = input('Do you want another movie (y/[n])?')
        if user_input != 'y':
            break


if __name__ == '__main__':
    main()
