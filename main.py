import requests
import os


def main():
    filename = 'hubble.jpeg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    dest_folder = 'media'

    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(dest_folder, exist_ok=True)
    with open(f'media/{filename}', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    main()
