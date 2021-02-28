#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./src/app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

FORCE_UPDATE=$1
if [ $FORCE_UPDATE != 1 ]; then
  echo "通常モードで、入稿処理を開始します."
else
  echo "強制アップデートモードで、入稿処理を開始します."
fi

# ジャンルマスタ更新バッチを実行
if [ $FORCE_UPDATE != 1 ]; then
  python src/app/main.py input genre
else
  python src/app/main.py input genre --force-update
fi
if [ $? != 0 ]; then
  exit 1
fi

# ページ1~10で、人気映画情報取得バッチを実行
start=1
end=10
for i in $(seq $start $end); do
  if [ $FORCE_UPDATE != "1" ]; then
    python src/app/main.py input movies --page $i
  else
    python src/app/main.py input movies --page $i --force-update
  fi
  if [ $? != 0 ]; then
    exit 1
  fi
done
if [ $? != 0 ]; then
  exit 1
fi

# レビュー収集バッチを実行
python src/app/main.py input reviews
if [ $? != 0 ]; then
  exit 1
fi

# 類似映画収集バッチを実行
python src/app/main.py input similar_movies
if [ $? != 0 ]; then
  exit 1
fi

echo "入稿処理が正常に終了しました."