# auto-retranslation

## 概要

Amazon Translate で再翻訳して遊ぶツール

##　使用ライブラリ

* boto3

仮想環境は適当に切ってください。

```
$ pip install boto3
```

## 使い方

### 入力ファイル

`in` ディレクトリに `input.txt` の名前で入力用ファイルを作成します。

```
$ vim ./in/input.txt
```

### 中間ファイル

`tmp/tmp-yyyy-MM-dd-HHmmss.json` の形式です。再翻訳途中の各回の結果が出力されるようになっており、実質ログのようなものです。


### 出力ファイル

`out/result-yyyy-MM-dd-HHmmss.txt` の形式です。入力ファイルの改行を保存した形で、テキストファイルとして出力されます。

### 言語コードファイル

`lang-code.json` に言語名と言語コードの対応表です。ここに記載された言語名が Amazon Translate でサポートされています。

### 2言語間の再翻訳

標準的な再翻訳です。ただし Amazon Translate はよくできているため、あまり変化せずお金の無駄になる可能性があります。

* 「日本語 → 英語 → 日本語」を3回繰り返す

```
$ python one.py 3
```

* 「イタリア語 → フランス語 → イタリア語」を3回繰り返す

```
$ python one.py 3 イタリア語 フランス語
```

中間ファイルは以下のようになります。

```
[
  {
    "no": 何回目の再翻訳かの番号,
    "text": 翻訳結果,
    "from": 翻訳前の言語コード,
    "via": 経由する言語コード
  },
  ...
]
```

### 多言語の再翻訳

「日本語 → A語 → B語 → C語 → 日本語」のように2つ以上の言語を経由して最終的に日本語に戻るような再翻訳です。

最初と最後の言語に日本語以外も指定できます。こちらも短い文だとあまり変化しませんが、ある程度勘を掴むと変な日本語を生成できます。

* 日本語 → アフリカーンス語 → ラトビア語 → 日本語

```
$ python multi.py 日本語 アフリカーンス語 ラトビア語
```

中間ファイルは以下のようになります。

```
[
  {
    "text": 翻訳結果,
    "from": 翻訳前の言語コード,
    "to": 翻訳後の言語コード
  },
  ...
]
```

## 進んだ使い方

入力ファイルを日本語で作成し、入力言語として日本語以外で指定することで1往復の再翻訳でかなりトリッキーな日本語が得られます。


## 参考

* [Amazon Translate](https://aws.amazon.com/jp/translate/)
* [Amazon Translate とは](https://docs.aws.amazon.com/ja_jp/translate/latest/dg/what-is.html)
* [Amazon Translate の料金](https://aws.amazon.com/jp/translate/pricing/)
* [Translate Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/translate.html)
* [再翻訳で遊びたい 〜AWS Translate 編〜（拙ブログ）](https://kesumita.hatenablog.com/entry/2020/05/05/004718)
* [再翻訳で遊びたい 〜AWS Translate 編その2〜（拙ブログ）](https://kesumita.hatenablog.com/entry/2020/05/05/183011)
* [再翻訳で遊びたい 〜AWS Translate 編その3〜（拙ブログ）](https://kesumita.hatenablog.com/entry/2020/05/05/214649)
