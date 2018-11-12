#!/usr/bin/python3.6
import telebot
import json
import logging
import os
from logging.handlers import RotatingFileHandler

bot = telebot.TeleBot("<SOME_TOKEN>")

STR_NOT_JSON = "Please, send a GeoJSON file"
STR_NOT_VALID_JSON = "Please, send a valid GeoJSON file"

valid_geom_types = {"Point", "MultiPoint", "LineString",
                    "MultiLineString", "Polygon", "MultiPolygon"}
irrelevant_content_types = ["text", "audio", "photo", "sticker",
                            "video", " video_note", "voice", "location", "contact"]

def start_logging(bot):
    dirname = os.path.dirname(__file__)
    logs_dir = os.path.join(dirname , ".logs")

    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    log_path = os.path.join(logs_dir, "bot.log")

    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    my_handler = RotatingFileHandler(log_path, mode='a', maxBytes=5*1024*1024,
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setLevel(logging.INFO)
    my_handler.setFormatter(log_formatter)

    logger = telebot.logger
    logger.setLevel(logging.INFO)
    logger.addHandler(my_handler)


def decode_json(document):
    decoded_json = json.loads(document)
    return decoded_json


def process_document(document):
    try:
        decoded_json = decode_json(document)
        counts_dict = {k: 0 for k in valid_geom_types}
        count_geom_types(decoded_json, counts_dict)
        return counts_dict
    except ValueError:
        return STR_NOT_VALID_JSON
    except KeyError:
        return STR_NOT_VALID_JSON


def count_geom_types(json, counts_dict):
    if json["type"] == "FeatureCollection":
        for obj in json["features"]:
            count_geom_types(obj, counts_dict)
    elif json["type"] == "Feature":
        if "geometry" in json:
            if json["geometry"]["type"] in valid_geom_types:
                counts_dict[json["geometry"]["type"]] += 1
        else:
            raise ValueError("Object must contain geometry object")
    # in case we get a geometry object which is not in an array
    elif json["type"] in valid_geom_types:
        counts_dict[json["type"]] += 1
    else:
        raise ValueError(STR_NOT_VALID_JSON)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello. Please send a GeoJSON file.")


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    result = process_document(downloaded_file)
    bot.reply_to(message, str(result))


@bot.message_handler(content_types=irrelevant_content_types)
def handle_irrelevant(message):
    bot.reply_to(message, STR_NOT_JSON)

if __name__ == '__main__':
    start_logging(bot)
    bot.polling(none_stop=True)
