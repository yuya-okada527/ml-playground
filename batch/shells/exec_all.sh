#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./src/app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

FORCE_UPDATE=$1
if [ $FORCE_UPDATE != 1 ]; then
  echo "通常モードで、全処理を開始します."
else
  echo "強制アップデートモードで、全処理を開始します."
fi

# 入稿処理を開始
sh shells/exec_input.sh ${FORCE_UPDATE}
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
