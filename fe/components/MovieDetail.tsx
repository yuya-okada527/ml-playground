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
      height: "400px",
      width: "98%",
    },
    posterImage: {
      flex: 1.2,
    },
    movieDescription: {
      flex: 2,
    },
  })
);

type MovieDetailProps = {
  movie_detail: Movie;
};

const MovieDetail = ({ movie_detail }: MovieDetailProps) => {
  const classes = useStyles();
  return (
    <Card className={classes.cardRoot}>
      <CardMedia
        className={classes.posterImage}
        image={movie_detail.poster_url}
      />
      <CardContent className={classes.movieDescription}>
        <Typography>
          {movie_detail.japanese_title}
          {movie_detail.release_year
            ? " (" + movie_detail.release_year + ") "
            : ""}
        </Typography>
        <p>{movie_detail.overview}</p>
      </CardContent>
    </Card>
  );
};

export default MovieDetail;
