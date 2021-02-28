"""サービス例外モジュール

アプリケーション例外を記述するモジュール
"""


class BaseAppException(Exception):
    """基底例外

    アプリケーション内で明示的に投げられる例外は必ずこの基底クラスを継承する
    """
    pass


class AppWarningException(BaseAppException):
    """アプリケーション警告例外

    アプリケーションの続行可能だが、注意が必要な例外が発生した場合に、投げる
    """
    pass
