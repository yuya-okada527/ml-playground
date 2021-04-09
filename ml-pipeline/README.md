# ML Playground ML Pipeline

## 使用技術

- 言語: Python3.8
- フレームワーク:
  - ワークフロー管理: kedro
  - 実験管理: mlflow tracking
- 主要ライブラリ
  - numpy
  - pandas
  - spaCy (自然言語処理)
  - Annoy (近似最近傍探索)

## コマンド

```bash
# 仮想環境起動
source .venv/bin/activate
# 仮想環境無効化
deactivate
# 実行(準備)
cd movie-recommender-ml-pipeline
# Kedro起動
kedro run
# jupyter notebook起動
kedro jupyter notebook
# kedro viz起動
kedro viz
```

## パイプライン概要

<img src="https://github.com/yuya-okada527/ml-playground/blob/develop/docs/phase1/%20image/kedro_viz.png" width="480">

## コマンド

```bash
# ローカル用
$ kedro run
# k8s上
$ kedro run --env k8s
```
