# Geo_TgBot

Бот доступен по ссылке: https://t.me/geojson_bot

Для работы с API телеграма была выбрана библиотека [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) из-за того, что она позволяет легко хэндлить разные виды файлов и облегчает процесс запросов к официальному API.

Для инциализации бота я получил токен с помощью бота @botfather, после чего начал разработку локально (создав для этого виртуальное окружение с помощью virtualenv). Для каждого типа сообщения (Video, Text, etc) был поставлен свой хэндлер. Для отправки данных используется механизм long polling, который позволяет нам отвечать на запросы клиента, когда у нас уже есть готовая информация. Учитывая то, что нам нужно обрабатывать только файлы, в ответ на все сообщения, которые не являются объектами Document, бот отвечает требованием прислать файл.

Если же сообщение является файлом, мы загружаем его в переменную и пытаемся декодировать с помощью официальной библиотеки json для python'а (т.к geojson файл - это простой json со специальной структурой). Очевидно, что если файл не является json-файлом (PDF, doc, etc), поднимется исключение ValueError, которое мы ловим и просим пользователя прислать файл нужного типа.

Если все прошло хорошо, то мы получаем словарь, который передаем в функцию подсчета геометрических объектов. Мы знаем, что geojson должен иметь ключ type, и если его нет, поднимается KeyError, который мы также ловим и возвращаем сообщение об ошибке. Дальше идет рекурсивный подсчет нужных нам геометрических объектов (они бывают 6 типов). Если ключ type принимает значение, отличное от FeatureCollection, Feature и это значение не является геометрическим типом, geojson не валиден - возвращается сообщение об ошибке. Если все хорошо, то мы возвращаем словарь в виде строки.

Также были написаны тесты, которые тестируют функции обработки файлов - в вопросах запросов и обработки других типов сообщений мы полагаемся на библиотеку, которая также покрыта тестами.

Затем бот был задеплоен на сервисе [pythonanywhere](https://www.pythonanywhere.com), который имеет необходимое окружение для python и подходит для проектов небольшого и среднего размера. На сайте я настроил таск, который перезапускает бот в случае проблем, не зависящих от бота - к примеру, по какой-то внешней причине отключился скрипт. Данные о работе бота логируются в директории .logs с помощью средств библиотеки logging. Для того, чтобы не превысить лимит по занятому пространству на диске, настроена ротация логов с помощью RotatingFileHandler, который перезаписывает логи, если их размер превышает 10 мегабайт.