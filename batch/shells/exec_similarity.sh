#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./src/app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

echo "30 sleepします"
sleep 30

echo "類似映画情報作成処理を開始します."

# TMDB-APIに基づく、類似映画情報をセットする
python src/app/main.py sim tmdb-sim
if [ $? -ne 0 ]; then
  exit 1
fi

echo "類似映画情報作成処理を終了."
