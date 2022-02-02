# Asobot~あそびば！専用BOT~
## 概要

discordサーバーのあそびば！専用のbotです。
### コマンドについて  
 ユーザーが使用するコマンドはすべてスラッシュコマンドで実装しています。  
 ただし、管理者のユーザーが使用するコマンドは通常のコマンドを使用します。


## 開発環境構築

**1.Pythonの環境作成**  
-Python3の導入方法については説明しません。  
[pipenv](https://github.com/pypa/pipenv) で環境を作成します。pipenv の使い方は[公式ドキュメント](https://pipenv-ja.readthedocs.io/ja/translate-ja/)を参照してください。  
```shell
pip install pipenv
pipenv install 
```
**2.設定ファイルの作成**  
プロジェクトフォルダーの直下に`config.ini`を作成してください
その中に下記をコピペして必要な個所を埋めてください。  
```INI
[BOT_SETTING]
guild_id= 導入するサーバーID
token = botのトークン
```
**3.Pythonファイルの実行**  
下記コマンドで実行します。
```shell
pipenv run start
```
