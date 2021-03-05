import React from "react";
import {
  Box,
  createStyles,
  makeStyles,
  Paper,
  List,
  Theme,
  Typography,
} from "@material-ui/core";
import { Movie } from "../interfaces";
import SimilarMovieItem from "./SimilarMovieItem";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      marginTop: theme.spacing(2),
      marginRight: theme.spacing(2),
    },
    similarMoviesHeader: {
      padding: theme.spacing(1),
      marginBottom: theme.spacing(1),
      backgroundColor: theme.palette.primary.main,
      color: "white",
      height: 70,
      display: "flex",
      alignItems: "center",
    },
    similarMoviesHeaderText: {
      fontSize: "1rem",
      fontWeight: 400,
    },
    link: {
      textDecoration: "none",
    },
    similarMovieItem: {
      paddingLeft: 0,
      paddingRight: 0,
      paddingBottom: theme.spacing(1),
      paddingTop: theme.spacing(0),
    },
    similarMovieItemPaper: {
      width: "100%",
      transition: "0.3s",
      "&:hover": {
        backgroundColor: "#eee",
        opacity: 0.8,
      },
    },
    similarMovieTitle: {
      margin: theme.spacing(1),
    },
  })
);

type SimilarMoviesProps = {
  similarMovies: Movie[];
  movieTitle: string;
};

/**
 * 類似映画リストを描画する
 */
const SimilarMovies: React.FC<SimilarMoviesProps> = ({
  similarMovies,
  movieTitle,
}) => {
  const classes = useStyles();
  return (
    <Box className={classes.root}>
      <Paper className={classes.similarMoviesHeader} variant="outlined">
        <Typography className={classes.similarMoviesHeaderText} variant="h6">
          &quot;{movieTitle}&quot; が好きなあなたにおすすめ
        </Typography>
      </Paper>
      <List data-test="similar-movie-list">
        {similarMovies.map((movie: Movie) => (
          <SimilarMovieItem key={movie.movie_id} movie={movie} />
        ))}
      </List>
    </Box>
  );
};

export default SimilarMovies;
