import React from "react";
import {
  Box,
  createStyles,
  makeStyles,
  Paper,
  List,
  Theme,
  Typography,
  ListItem,
  Grid,
} from "@material-ui/core";
import Image from "material-ui-image";
import Link from "next/link";
import { Movie } from "../interfaces";

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

const SimilarMovies = ({ similarMovies, movieTitle }: SimilarMoviesProps) => {
  const classes = useStyles();
  return (
    <Box className={classes.root}>
      <Paper className={classes.similarMoviesHeader} variant="outlined">
        <Typography className={classes.similarMoviesHeaderText} variant="h6">
          "{movieTitle}" が好きなあなたにおすすめ
        </Typography>
      </Paper>
      <List>
        {similarMovies.map((movie: Movie) => (
          <Link href={`/movies/${movie.movie_id}`} key={movie.movie_id}>
            <a className={classes.link}>
              <ListItem
                className={classes.similarMovieItem}
                key={movie.movie_id}
              >
                <Paper
                  className={classes.similarMovieItemPaper}
                  variant="outlined"
                  square
                >
                  <Grid container>
                    <Grid item xs={2}>
                      <Image src={movie.poster_url} aspectRatio={9 / 12} />
                    </Grid>
                    <Grid item xs={10}>
                      <Typography
                        className={classes.similarMovieTitle}
                        variant="h6"
                      >
                        {movie.japanese_title
                          ? movie.japanese_title
                          : movie.original_title}
                        {movie.release_year
                          ? " (" + movie.release_year + ") "
                          : ""}
                      </Typography>
                    </Grid>
                  </Grid>
                </Paper>
              </ListItem>
            </a>
          </Link>
        ))}
      </List>
    </Box>
  );
};

export default SimilarMovies;
