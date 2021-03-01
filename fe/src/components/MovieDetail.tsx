import React from "react";
import {
  Card,
  CardMedia,
  CardContent,
  createStyles,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import { Movie } from "../interfaces";
import ProviderInfo from "./ProviderInfo";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    cardRoot: {
      display: "flex",
      marginTop: theme.spacing(5),
      height: "450px",
      width: "98%",
      position: "relative",
    },
    posterImage: {
      flex: 1.2,
    },
    movieDescription: {
      flex: 2,
    },
    movieTitle: {
      marginBottom: theme.spacing(2),
    },
  })
);

const MAX_OVERVIEW_LENGTH = 400;

/**
 * 省略済シナリオを作成する
 *
 * @param overview シナリオ
 * @param max_length 最大文字列サイズ
 */
const makeOverview = (
  overview?: string,
  max_length = MAX_OVERVIEW_LENGTH
): string => {
  if (!overview) {
    return "";
  }

  if (overview.length <= max_length) {
    return overview;
  }

  return overview.substr(0, max_length) + "...";
};

/**
 * 表示用タイトルを作成する.
 *
 * @param movie 映画詳細
 */
const makeTitle = (movie: Movie): string => {
  // タイトル
  const title = movie.japanese_title
    ? movie.japanese_title
    : movie.original_title;
  if (!title) {
    return "申し訳ありません。タイトルが表示できません。";
  }

  // 公開年がある場合は、タイトルの後ろに公開年を付加する
  if (movie.release_year) {
    return `${title} (${movie.release_year})`;
  }

  return title;
};

type MovieDetailProps = {
  movie_detail: Movie;
};

/**
 * 映画詳細を描画する
 *
 * @param movie_detail 映画詳細
 */
const MovieDetail: React.FC<MovieDetailProps> = ({ movie_detail }) => {
  const classes = useStyles();
  return (
    <Card className={classes.cardRoot}>
      {/* ポスターイメージ */}
      <CardMedia
        className={classes.posterImage}
        image={movie_detail.poster_url}
      />
      <CardContent className={classes.movieDescription}>
        {/* タイトル */}
        <Typography variant="h6" className={classes.movieTitle}>
          {makeTitle(movie_detail)}
        </Typography>
        {/* シナリオ */}
        <Typography variant="body1">
          {makeOverview(movie_detail.overview)}
        </Typography>
        {/* 提供情報 */}
        <ProviderInfo />
      </CardContent>
    </Card>
  );
};

export default MovieDetail;
export { makeOverview, makeTitle };
