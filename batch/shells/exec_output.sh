#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./src/app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

echo "出稿処理を開始します."

# 検索スキーマ更新バッチを実行
python src/app/main.py output schema
if [ $? -ne 0 ]; then
  exit 1
fi

# 検索インデックス構築バッチを実行
python src/app/main.py output index
if [ $? -ne 0 ]; then
  exit 1
fi

echo "出稿処理が正常に終了しました."