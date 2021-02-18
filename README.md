# Скачивание фотографий из SpaceX/Hubble API и автопубликация их в Instagram.

Скрипт скачивает фотографии последних запусков SpaceX, а также снимки телескопа Hubble коллекции `stsci_gallery` 
через [API SpaceX ](https://documenter.getpostman.com/view/2025350/RWaEzAiG#bc65ba60-decf-4289-bb04-4ca9df01b9c1) и 
[API Hubble](http://hubblesite.org/api/documentation) в папку `images`, имена фотографий соответствуют объекту съёмки. 
Затем проверяет фотографии по стандартам Instagram (соотношение сторон и длинну), обрезает под стандарт 1.91 и ужимает 
до 1080px на бо’льшую сторону с сохранением пропорций. Загружает фотографии в Instagram, записывая название загруженных 
фоток в файл `posted_imgs.txt`, в корне программы (создаётся автоматически), в последствии сверяясь с данным списком 
(названия фоток из этого списка не будут загружены при последующих запусках), подпись формируется из названия 
фотографий. После загрузки фотографий в Instagram, скрипт удаляет загруженные фотографии из папки `images` 
(только те, кои удалось загрузить).


## Настройки

Необходимо зарегистрироваться на сайте [Instagram](https://www.instagram.com/).
Затем создать файл `.env` в корневой папке с кодом и записать туда логин и пароль к Instagram, в формате:
```
INSTAGRAM_USERNAME=ВАШ_ЛОГИН
INSTAGRAM_PASSWORD=ВАШ_ПАРОЛЬ
```

## Запуск

Для запуска библиотеки у вас уже должен быть установлен 
[Python 3](https://www.python.org/downloads/release/python-379/).

- Скачайте код.
- Установите зависимости командой:
```
pip install -r requirements.txt
```
- Запустите скрипт командой: 
```
python main.py
```


