import json
import os

from datetime import datetime

def get_lang_code_dict():
    with open(
        os.path.join(os.path.dirname(__file__), './lang-code.json'),
        mode='r',
        encoding='utf-8'
    ) as f:
        lang_dict = json.load(f)
    return lang_dict

def format_file_name():
    """
    適当なファイル名を作るためのやつ
    """
    return datetime.now().strftime('%Y-%m-%d-%H%M%S')
