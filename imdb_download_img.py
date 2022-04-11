import os
import requests
from bs4 import BeautifulSoup

IMDB_LINK = 'https://www.imdb.com/chart/top/'
headers = {'Accept-Language': 'en-US,en;q=0.8'}
SAVE_FOLDER = 'images-imdb'


def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()


def download_images():
    print('Start searching...')
    response = requests.get(IMDB_LINK, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    # results = soup.findAll('td', {'class': 'posterColumn'})
    image_links = [result['src'] for result in soup.select('td.posterColumn a img')]
    print(f'Found {len(image_links)} images')
    print('Start downloading...')

    for idx, image in enumerate(image_links):
        # open image link and save as file
        res = requests.get(image)
        image_name = SAVE_FOLDER + '/' + str(idx + 1) + '.jpg'
        # wb = write & binary. good for jpg file
        with open(image_name, 'wb') as file:
            file.write(res.content)
    print('Done')


if __name__ == '__main__':
    main()
