import requests
import os


def download_image(url, image_name, dest_folder='images'):
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(dest_folder, exist_ok=True)
    with open(f'{dest_folder}/{image_name}', 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    image_name = 'hubble.jpeg'

    download_image(url, image_name)


if __name__ == '__main__':
    main()
