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
    },
    cardCover: {
      width: 700,
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
        className={classes.cardCover}
        image={movie_detail.poster_url}
      />
      <CardContent>
        <Typography>{movie_detail.japanese_title}</Typography>
        <p>{movie_detail.overview}</p>
      </CardContent>
    </Card>
  );
};

export default MovieDetail;
