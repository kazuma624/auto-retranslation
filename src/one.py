import boto3
import json
import os
import sys

from util import (
    format_file_name,
    get_lang_code_dict,
)

client = boto3.client('translate')


def retranslate(init_text, src='ja', via='en', cnt=0):
    """
    入力ファイルの内容を指定の回数再翻訳する
    """
    params = {
        'text': init_text,
        'src': src,
        'via': via
    }
    result = []
    for i in range(cnt):
        # 5000 文字の制限は API 実行前に弾いてしまう
        if len(params['text']) > 5000:
            break

        params = unit_retranslate(params)
        result.append({
            'no': i + 1,
            'text': params['text'],
            'from': src,
            'via': via
        })
    return result


def unit_retranslate(params):
    """
    再翻訳を1回行う
    """
    # 翻訳
    tmp_result = client.translate_text(
        Text=params['text'],
        SourceLanguageCode=params['src'],
        TargetLanguageCode=params['via']
    )
    # 再翻訳
    result = client.translate_text(
        Text=tmp_result['TranslatedText'],
        SourceLanguageCode=params['via'],
        TargetLanguageCode=params['src']
    )
    params['text'] = result['TranslatedText']
    return params


if __name__ == '__main__':
    args = sys.argv
    if not (len(args) == 2 or len(args) == 4):
        print('Specify int number OR int number, source language and destination language.')
        sys.exit()

    wd = os.path.dirname(__file__)
    try:
        with open(os.path.join(wd, '../in/input.txt'), mode='r') as in_f:
            init_text = in_f.read()

        lang_code_dict = get_lang_code_dict()
        if len(args) == 2 and args[1].isdigit():
            result = retranslate(init_text, cnt=int(args[1]))
        elif len(args) == 4 and args[1].isdigit():
            result = retranslate(
                init_text,
                src=lang_code_dict[args[2]],
                via=lang_code_dict[args[3]],
                cnt=int(args[1])
            )
        else:
            print('Specified args are something wrong.')
            sys.exit()

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
