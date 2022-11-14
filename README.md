# ![KeibaBot Logo](https://github.com/Domzou-kun/discord_bot_KeibaVote/blob/master/logos/bot_banner_logo.png)

---


# 競馬予想集計bot

このプログラムは、discordのサーバー上にて中央競馬または地方競馬若しくはその両方の予想を投票、集計、予想新聞風に出力することが出来るbotです。
日本人の使用を想定して、日本語を主に対象言語として居ます。

# Caution
このプログラムで使用するデータはnetkeiba様のサイトより、スクレイピングによって取得します。
データに対してアクセスする場合、必ず5秒以上の時間を空けてスクレイピングを行っており、一時的に大量のリクエストを行わないように配慮しております。
本プログラムを利用、もしくは参考にされる際必ずこのスクレイピングに関しては細心の注意を払い利用を行ってください。
また、本データは自動でレコードファイルなどの生成、削除を行います。予期しない動作による、利用者の個人的なファイルの削除やPCに対する事故等には責任を負いかねますのでご注意ください。


## Description

基本的な機能としては以下のようになっています。
- 競馬のレース予想の投票及び集計
- 競馬新聞風に自動で予想の出力
- 投票者の予想のレコード
- 投票レースの自動取得
- ゲーム機能

---

## Getting Started

### Installing

このbotはserverなどに登録されておらず、使用時はローカルでプログラムを実行して起動する必要があります。
よって、このリポジトリにアップロードされているプログラム全てをローカルにダウンロードする必要があります。

---

## Usage

###  Operating environment
本プログラムは、以下の環境にて動作を確認、想定しています。
- windows 10/11
- Python 3.9.4

以上の環境以外では動作を確認しておりません。

### Token
本プログラムを実行するには、Discordのbot用tokenの取得が必要になります。
Discord Developer portalへの登録が必要となります。
tokenは、[ac_key.json](https://github.com/Domzou-kun/discord_bot_KeibaVote/blob/master/voted_bot/keiba_vote_prog/ac_key.json)へ記述してください。

### Python
本プログラムは、Python 3.9.4でのみ動作が可能となっています。それ以外のVersionについては動作の検証を行っておりません。
検証や実際の動作の際には、Python 3.9.4をお使いください。

### requirement
必要なモジュールは全て、[requirement.txt](https://github.com/Domzou-kun/discord_bot_KeibaVote/blob/master/voted_bot/bot_run/requirements.txt)にまとめております。
以下にて、Python 3.9.4環境にインストールを行ってください。

```Python
pip install -r requirement.txt
```
またdiscordのAPIには、discord.pyを使用していますが、バージョンが特殊なためご注意ください。


### Start-up
本プログラムはwindows環境での使用を想定しております。よって、起動メニューを[batファイルにて簡易的に実装](https://github.com/Domzou-kun/discord_bot_KeibaVote/blob/master/voted_bot/bot_run/keiba_prog_starter.bat)しております。
競馬botの一連のプログラムには、こちらのbatファイルを直接実行、もしくはショートカットなどを作成して実行してください。

メニュー項目
- 投票レースのデータ取得プログラムの起動
- 本botの起動
- 投票モードのみの起動
- ゲームモードのみの起動
- テスト（検証）モードでの起動
- メニュー画面の終了

### others
投票や、レースデータの取得を行うと、レコードデータが自動で蓄積されます。
また、本botを導入したサーバーでは、bot利用者の以下の情報を記録するため、利用にはご注意ください。
- Discord id
- Discord user name
- user icon

---

## Mode

### Race data mode
レースデータを取得するモードです。
本プログラムでは、netkeiba様のサイトより、スクレイピングによって取得します。
中央競馬、地方競馬の寮データの取得が可能です。（海外競馬は対応不可）

### Vote mode
取得したレースデータを用いて、discord上で投票を行えるモードです。

### Game mode
2種類のミニゲームを実装しております。
- Umadle(wordleのウマ娘に登場するキャラクター版)
- Uma Quiz(競走馬に関する制限時間120秒の早押しクイズ)

---

## Version History

* 1.0
    * Development version
* 1.1.1
    * Release version
* 1.1.2
    * github version
    
## Authors

Domzou



