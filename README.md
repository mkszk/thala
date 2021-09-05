Thala
====

このライブラリは
動画素材へ簡単に解説字幕・ナレーションを追加するものです。

## Description

現在の機能は以下の３点です。

 - 解説字幕の追加
 - ナレーションの追加
 - 再生速度の調整

### 解説字幕の追加

字幕はMoviePy経由でImageMagickの文字入力を利用します。

字幕とナレーションはcsvファイルで一括入力します。
これにより編集の手間が小さくなっています。

csvファイルの中身は「処理開始秒数,再生速度,字幕・ナレーションの内容」です。
字幕とナレーションの異なる箇所は青空文庫のルビ記法を採用しました。
具体的には「｜字幕の内容《ナレーションの内容》」と記載します。
ナレーションの読み上げ内容が意図に合わない場合に使用します。


### ナレーションの追加
ナレーションはOpenJTalkまたはVOICEVOXを利用します。。

OpenJTalkの音響モデルはMMDAgentのMeiです。
Creative Commons — 表示 – 3.0 非移植 — CC BY 3.0
Copyright 2009-2013 Nagoya Institute of Technology (MMDAgent Accessory “NIT Menu”)

VOICEVOXはVoice:四国めたんです。
https://zunko.jp/guideline.html

字幕とナレーションはcsvファイルで一括入力します。
これにより編集の手間が小さくなっています。

csvファイルの中身は「処理開始秒数,再生速度,字幕・ナレーションの内容」です。
字幕とナレーションの異なる箇所は青空文庫のルビ記法を採用しました。
具体的には「｜字幕の内容《ナレーションの内容》」と記載します。
ナレーションの読み上げ内容が意図に合わない場合に使用します。

### 語源

Thalaは『指輪物語』のエルフ語で映像という意味だそうです。

## Demo

https://youtu.be/gesoM7o9D7s

## Requirement

依存先のソフトウェアは以下の通りです。

 - MoviePy (2.0.0.dev2 or upper)
     - ImageMagick
     - FFmpeg
 - Pydub
 - pyopenjtalk or VoiceVox

## Usage

 1. 実行パスにImageMagickとFFmpegを含めるか、
    環境変数にImageMagickとFFmpegを指定してください。
    これはMoviePyでの依存先の指定法に従っています。
 2. python example.py

### VOICEVOX(Windows/Linux共通)

VOICEVOXを使う場合はrun.exeを起動しておいてください。
```
run.exe
```

## Install

zipをダウンロードして適当に配置してください。

## Contribution

 1. フォークする（http://github.com/mkszk/voicedub）
 2. Featureブランチを作る（git checkout -b my-new-feature）
 3. コミットする（git commit -am 'Add some feature'）
 4. 公開リポジトリにプッシュする（git push origin my-new-feature）
 5. プルリクエストを送る

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[mkszk](https://github.com/mkszk)

