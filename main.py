import os
import shutil
import time
from pathlib import Path

import requests
import urllib3
from PIL import Image
from dotenv import load_dotenv
from instabot import Bot


def download_image(url, image_name, images_folder='images'):
    response = get_response(url)

    Path(images_folder).mkdir(parents=True, exist_ok=True)
    image_path = Path(f'{images_folder}/{image_name}')
    with open(image_path, 'wb') as file:
        file.write(response.content)


def resize_image(images_folder):
    images_paths = list(Path(images_folder).glob('*'))
    if images_paths:
        recomended_ratio = 1.91
        maximum_side = 1080
        for image_path in images_paths:
            image = Image.open(image_path)
            width, height = image.size
            ratio = width / height

            if ratio > recomended_ratio:
                image = trim_to_ratio(image, width, height, recomended_ratio)

            if width > maximum_side or height > maximum_side:
                image.thumbnail((maximum_side, maximum_side),
                                Image.ANTIALIAS)

            new_file_path = Path(image_path.parent, f'{image_path.stem}.jpg')
            image.save(new_file_path)

            if new_file_path != image_path:
                Path(image_path).unlink()


def trim_to_ratio(image, width, height, recomended_ratio):
    new_width = int(height * recomended_ratio)
    left = int((width - new_width) / 2)
    top = 0
    right = int((width + new_width) / 2)
    bottom = height
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image


def get_extension(url):
    extension = url.split('.')[-1]
    return extension


def get_response(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    if response.ok:
        return response
    raise requests.HTTPError


def fetch_spacex_last_launch():
    response_spacex = get_response('https://api.spacexdata.com/v4/launches'
                                   '/latest')

    launch_info = response_spacex.json()
    image_links = launch_info['links']['flickr']['original']
    payloads_name = launch_info['name']

    for numb, image_url in enumerate(image_links, 1):
        image_name = f'{payloads_name}_{numb}.jpg'
        download_image(image_url, image_name)


def fetch_image_hubble(image_id):
    response_hubble = get_response(
        f'http://hubblesite.org/api/v3/image/{image_id}')

    hubble_info = response_hubble.json()
    last_image_link = hubble_info['image_files'][-1]
    photo_name = hubble_info['name']

    image_url = last_image_link['file_url'].replace('//', 'https://')
    extension = get_extension(image_url)

    image_name = f'{photo_name}.{extension}'
    download_image(image_url, image_name)


def get_hubble_image_ids(collection_name):
    response = get_response(
        'http://hubblesite.org/api/v3'
        f'/images?page=all&collection_name={collection_name}')
    collection_info = response.json()

    image_ids = []
    for image in collection_info:
        image_ids.append(image['id'])
    return image_ids


def upload_to_instagram(images_folder):
    timeout = 5

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    try:
        with open("posted_imgs.txt", "r", encoding="utf8") as file:
            posted_img_list = file.read().splitlines()
    except Exception:
        posted_img_list = []

    bot = Bot()
    bot.login(username=username, password=password)

    images_paths = list(Path(images_folder).glob('*.jpg'))

    if images_paths:
        images_names = {path.name for path in images_paths}
        posted_names = set(posted_img_list)
        unpublished_names = images_names.difference(posted_names)

        if unpublished_names:
            for name in unpublished_names:
                caption = name.split('.')[0]
                bot.upload_photo(Path(f'{images_folder}/{name}'),
                                 caption=caption)
                print("upload: " + name)

                if bot.api.last_response.status_code != 200:
                    print(bot.api.last_response)
                    break

                with open("posted_imgs.txt", "a", encoding="utf8") as file:
                    file.write(name + "\n")

                time.sleep(timeout)


def remove_uploaded(images_folder):
    images_paths = list(Path(images_folder).glob('*.REMOVE_ME'))
    if images_paths:
        for image_path in images_paths:
            Path(image_path).unlink()


def main():
    load_dotenv()
    timeout = 10
    images_folder = 'images'

    if Path('config').exists():
        shutil.rmtree('config')

    fetch_spacex_last_launch()

    hubble_images_ids = get_hubble_image_ids('stsci_gallery')
    for image_id in hubble_images_ids:
        fetch_image_hubble(image_id)

    resize_image(images_folder)

    # upload_to_instagram(images_folder)

    # time.sleep(timeout)
    # remove_uploaded(images_folder)


if __name__ == '__main__':
    main()
