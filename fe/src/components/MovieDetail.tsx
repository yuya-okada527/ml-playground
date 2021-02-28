import React from "react";
import {
  Card,
  CardMedia,
  CardContent,
  createStyles,
  makeStyles,
  Theme,
  Typography,
  Box,
} from "@material-ui/core";
import Image from "next/image";
import { Movie } from "../interfaces";

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
    providerInfo: {
      position: "absolute",
      bottom: 0,
      display: "flex",
      alignItems: "center",
    },
    providerIcon: {
      display: "inline",
    },
    providerComment: {
      fontSize: "13px",
      fontWeight: 300,
      marginRight: theme.spacing(1),
    },
  })
);

const MAX_OVERVIEW_LENGTH = 400;

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

const MovieDetail: React.FC<MovieDetailProps> = ({ movie_detail }) => {
  const classes = useStyles();
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
        <Box className={classes.providerInfo}>
          <Typography variant="subtitle2" className={classes.providerComment}>
            This product uses the TMDb API but is not endorsed or certified by
            TMDb.
          </Typography>
          <Image
            src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_1-5bdc75aaebeb75dc7ae79426ddd9be3b2be1e342510f8202baf6bffa71d7f5c4.svg"
            alt="Logo of Tmdb"
            width={40}
            height={40}
            className={classes.providerIcon}
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default MovieDetail;
