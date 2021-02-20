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

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    cardRoot: {
      display: "flex",
      marginTop: theme.spacing(5),
      height: "450px",
      width: "98%",
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

const MAX_OVERVIEW_LENGTH = 450;

const cutLongOverview = (overview?: string) => {
  if (!overview) {
    return overview;
  }

  if (overview.length > MAX_OVERVIEW_LENGTH) {
    return overview.substr(0, MAX_OVERVIEW_LENGTH) + "...";
  }

  return overview;
};

type MovieDetailProps = {
  movie_detail: Movie;
};

const MovieDetail = ({ movie_detail }: MovieDetailProps) => {
  const classes = useStyles();
  console.log(JSON.stringify(movie_detail));
  return (
    <Card className={classes.cardRoot}>
      <CardMedia
        className={classes.posterImage}
        image={movie_detail.poster_url}
      />
      <CardContent className={classes.movieDescription}>
        <Typography variant="h6" className={classes.movieTitle}>
          {movie_detail.japanese_title}
          {movie_detail.release_year
            ? " (" + movie_detail.release_year + ") "
            : ""}
        </Typography>
        <Typography variant="body1">
          {cutLongOverview(movie_detail.overview)}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MovieDetail;
