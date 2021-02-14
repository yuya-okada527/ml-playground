import re

import pandas as pd


def concatenate_reviews(reviews: pd.DataFrame) -> pd.DataFrame:

    # スペース区切りで、レビューを結合
    concatenated_reviews = (reviews.groupby("movie_id")["review"]
        .apply(list)
        .apply(" ".join)
    )

    return pd.DataFrame({
        "movie_id": concatenated_reviews.index,
        "review": concatenated_reviews
    })


def normalize_reviews(concatenated_reviews: pd.DataFrame) -> pd.DataFrame:

    # 改行コードを除去
    concatenated_reviews["review"] = concatenated_reviews["review"].apply(_remove_line_separator)

    # タブを除去
    concatenated_reviews["review"] = concatenated_reviews["review"].apply(_remove_tab)

    # 連続したスペースを除去
    concatenated_reviews["review"] = concatenated_reviews["review"].apply(_remove_duplicate_space)

    return concatenated_reviews


def _remove_line_separator(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")


def _remove_tab(text: str) -> str:
    return text.replace("\t", " ")


def _remove_duplicate_space(text: str) -> str:
    return re.sub("[ 　]+", " ", text)
