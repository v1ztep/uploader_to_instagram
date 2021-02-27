import os
import shutil
import time
from os.path import splitext
from pathlib import Path
from urllib.parse import urlsplit

import requests
import urllib3
from PIL import Image
from dotenv import load_dotenv
from instabot import Bot


def download_image(url, image_name, images_folder='images'):
    response = get_response(url)

    image_path = Path(f'{images_folder}/{image_name}')
    with open(image_path, 'wb') as file:
        file.write(response.content)


def fix_size_extension_images(images_folder):
    images_paths = Path(images_folder).glob('*')
    for image_path in images_paths:
        recomended_ratio = 1.91
        maximum_side = 1080

        image = Image.open(image_path)
        width, height = image.size
        ratio = width / height

        if ratio > recomended_ratio:
            image = trim_to_ratio(image, width, height, recomended_ratio)

        if width > maximum_side or height > maximum_side:
            image.thumbnail((maximum_side, maximum_side), Image.ANTIALIAS)

        new_file_path = Path(image_path.parent, f'{image_path.stem}.jpg')
        image.save(new_file_path)

        if new_file_path != image_path:
            image_path.unlink()


def trim_to_ratio(image, width, height, recomended_ratio):
    new_width = int(height * recomended_ratio)
    left = int((width - new_width) / 2)
    top = 0
    right = int((width + new_width) / 2)
    bottom = height
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image


def get_extension(url):
    url_path = urlsplit(url).path
    extension = splitext(url_path)[-1]
    return extension


def get_response(url, params=None):
    response = requests.get(url, params, verify=False)
    response.raise_for_status()
    return response


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v4/launches/latest'
    spacex_response = get_response(url)

    launch_details = spacex_response.json()
    image_links = launch_details['links']['flickr']['original']
    payloads_name = launch_details['name']

    for num, image_url in enumerate(image_links, 1):
        image_name = f'{payloads_name}_{num}.jpg'
        download_image(image_url, image_name)


def fetch_image_hubble(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    hubble_response = get_response(url)
    image_details = hubble_response.json()

    last_image_details = image_details['image_files'][-1]
    last_image_link = urlsplit(last_image_details['file_url'])
    image_url = last_image_link._replace(scheme='https').geturl()

    photo_name = image_details['name']
    extension = get_extension(image_url)

    image_name = f'{photo_name}{extension}'
    download_image(image_url, image_name)


def get_hubble_image_ids(collection_name):
    url = 'http://hubblesite.org/api/v3/images'
    params = {'page': 'all', 'collection_name': {collection_name}}
    response = get_response(url, params=params)
    image_details = response.json()

    image_ids = [image['id'] for image in image_details]
    return image_ids


def upload_to_instagram(images_folder, username, password, timeout,
                        posted_imgs):
    bot = Bot()
    bot.login(username=username, password=password)

    images_paths = Path(images_folder).glob('*.jpg')

    if images_paths:
        images_names = {path.name for path in images_paths}
        posted_names = set(posted_imgs)
        unpublished_names = images_names.difference(posted_names)

        for name in unpublished_names:
            caption = name.split('.')[0]
            bot.upload_photo(Path(f'{images_folder}/{name}'),
                             caption=caption)
            print(f'upload: {name}')

            if bot.api.last_response.status_code != 200:
                print(bot.api.last_response)
                break

            with open('posted_imgs.txt', 'a', encoding='utf8') as file:
                file.write(f'{name}\n')

            time.sleep(timeout)


def remove_uploaded(images_folder):
    images_paths = Path(images_folder).glob('*.REMOVE_ME')
    for image_path in images_paths:
        image_path.unlink()


def main():
    load_dotenv()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    timeout = 10
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')

    images_folder = 'images'
    Path(images_folder).mkdir(parents=True, exist_ok=True)

    try:
        with open('posted_imgs.txt', 'r', encoding='utf8') as file:
            posted_imgs = file.read().splitlines()
    except FileNotFoundError:
        posted_imgs = []

    fetch_spacex_last_launch()

    hubble_images_ids = get_hubble_image_ids('stsci_gallery')
    for image_id in hubble_images_ids:
        fetch_image_hubble(image_id)

    fix_size_extension_images(images_folder)

    try:
        upload_to_instagram(images_folder, username, password, timeout,
                            posted_imgs)
    finally:
        remove_uploaded(images_folder)
        if Path('config').exists():
            shutil.rmtree('config')


if __name__ == '__main__':
    main()
