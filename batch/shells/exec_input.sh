#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

echo "入稿処理を開始します."

# ジャンルマスタ更新バッチを実行
python app/main.py input genre
if [ $? != 0 ]; then
  exit 1
fi

# ページ1~10で、人気映画情報取得バッチを実行
start=1
end=10
for i in $(seq $start $end); do
  python app/main.py input movies --page $i
  if [ $? != 0 ]; then
    exit 1
  fi
done
if [ $? != 0 ]; then
  exit 1
fi

# レビュー収集バッチを実行
python app/main.py input reviews
if [ $? != 0 ]; then
  exit 1
fi

echo "入稿処理が正常に終了しました."