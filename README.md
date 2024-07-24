# ポートフォリオ用のDjangoで作成したアンケートWEBサイト

## 概要

Djangoで作成したアンケートWEBサイトです。

## 使用技術

- Python
- Django

## デモ

### 自動生成ドキュメント

![デモ画像](images/ReadMeDemoImage.png)

### 自動テストの実行

![デモ画像](images/ReadMeDemoImageTest.png)

## 動作確認方法

ローカル環境で動作確認可能です。

### ローカル環境

ローカル環境で動作確認する場合は、以下の手順で動作確認できます。  
Pythonがインストールされていることを前提として説明します。

1. コマンドプロンプトを起動します。
2. プロジェクトフォルダの`src`ディレクトリに移動します。
3. `poetry install`を実行して、パッケージをインストールします。
4. `poetry run src/manage.py makemigrations`を実行して、マイグレーションファイルを作成します。
5. `poetry run src/manage.py migrate`を実行して、データベース構造を作成します。
6. `poetry run src/manage.py runserver`を実行して、サーバーを起動します。
7. ブラウザで `http://localhost:8000` にアクセスして、アンケートを表示します。
8. 停止したい場合は、`Ctrl + C`を実行してください。
