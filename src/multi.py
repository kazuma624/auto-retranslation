import boto3
import json
import os
import sys

from util import (
    format_file_name,
    get_lang_code_dict,
)

client = boto3.client('translate')


def retranslate(init_text, code_list):
    """
    入力ファイルの内容を指定の言語コードの順に翻訳し、最後に元の言語に戻す
    """
    params = {'Text': init_text}
    result = []
    for i, _ in enumerate(code_list):
        if i == len(lang_list) - 1:
            # 最後に元の言語に戻す
            params['SourceLanguageCode'] = code_list[-1]
            params['TargetLanguageCode'] = code_list[0]
        else:
            params['SourceLanguageCode'] = code_list[i]
            params['TargetLanguageCode'] = code_list[i + 1]

        # 5000 文字の制限は API 実行前に弾いてしまう
        if len(params['Text']) > 5000:
            break

        params = unit_translate(params)
        result.append({
            'text': params['Text'],
            'from': params['SourceLanguageCode'],
            'to': params['TargetLanguageCode'],
        })
    return result


def unit_translate(params):
    """
    翻訳を1回行う
    """
    result = client.translate_text(**params)
    params['Text'] = result['TranslatedText']
    return params


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 3:
        print('length of languages-list is required at least 3.')
        sys.exit()

    lang_list = args[1:]
    wd = os.path.dirname(__file__)
    try:
        with open(os.path.join(wd, '../in/input.txt'), mode='r') as in_f:
            init_text = in_f.read()

        lang_code_dict = get_lang_code_dict()
        code_list = [lang_code_dict[elem] for elem in lang_list]
        result = retranslate(init_text, code_list)
        # 途中経過
        with open(
            os.path.join(wd, f'../tmp/tmp-{format_file_name()}.json'),
            mode='w',
            encoding='utf-8'
        ) as out_f:
            json.dump(result, out_f, indent=2, ensure_ascii=False)

        # 最終結果
        with open(
            os.path.join(wd, f'../out/result-{format_file_name()}.txt'),
            mode='w',
            encoding='utf-8'
        ) as out_f:
            out_f.write(result[-1]['text'])

    except Exception:
        import traceback
        print(traceback.format_exc())
