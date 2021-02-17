#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

echo "全バッチ処理の実行を開始します."

# 入稿処理を開始
sh shells/exec_input.sh
if [ $? != 0 ]; then
  exit 1
fi

# 出稿処理を開始
sh shells/exec_output.sh
if [ $? != 0 ]; then
  exit 1
fi

# 類似データフィード処理を開始
sh shells/exec_similarity.sh
if [ $? != 0 ]; then
  exit 1
fi

echo "全バッチの実行が完了しました."
