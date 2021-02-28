"""メインモジュール

バッチコマンドを定義するモジュール
"""
import typer

from entrypoints.v1 import (input_entrypoints, output_entrypoints,
                            similarity_entrypoints)

# サブコマンドの追加
app = typer.Typer()
app.add_typer(input_entrypoints.app, name="input")
app.add_typer(output_entrypoints.app, name="output")
app.add_typer(similarity_entrypoints.app, name="sim")


if __name__ == "__main__":
    app()
