#!/bin/sh

# main.pyが存在するか確認
if [ ! -e "./app/main.py" ]; then
  echo "main.py does not exist!"
  exit 1
fi

echo "main.py exists"
