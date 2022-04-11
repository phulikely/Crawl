"""
Unfortunately Google changed its html structure, so this exact code won't work anymore(still working in 2020)
"""
import os
import json
import requests #to sent GET requests
from bs4 import BeautifulSoup #to parse HTML

# user can input a topic and a number
# download first n images from google image search

# GOOGLE_IMAGE = 'https://images.google.com/'
GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string
# that allows the network protocol peers to identify the application type,
# operating system, and software version of the requesting software user agent.
# needed for google search
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
}

SAVE_FOLDER = 'images'


def main():
    if not os.path.exists(SAVE_FOLDER):
        os.mkdir(SAVE_FOLDER)
    download_images()


def download_images():
    # ask for user input
    data = input('What are you looking for? ')
    n_images = int(input('How many images do you want? '))

    print('Start searching...')

    # get url query string
    search_url = GOOGLE_IMAGE + 'q=' + data
    print(search_url)

    response = requests.get(search_url, headers=usr_agent)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('div', {'class': 'rg_meta'}, limit=n_images)

    # extract the link from the div tag
    imagelinks = []
    for re in results:
        text = re.text  # this is a valid json string
        text_dict = json.loads(text)  # deserialize json to a Python dict
        link = text_dict['ou']
        # image_type = text_dict['ity']
        imagelinks.append(link)

    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open image link and save as file
        response = requests.get(imagelink)

        imagename = SAVE_FOLDER + '/' + data + str(i + 1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == '__main__':
    main()
