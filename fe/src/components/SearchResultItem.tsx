/* eslint-disable jsx-a11y/anchor-is-valid */
// TODO 暫定対応
import {
  createStyles,
  Grid,
  ListItem,
  makeStyles,
  Paper,
  Theme,
  Typography,
} from "@material-ui/core";
import Link from "next/link";
import Image from "material-ui-image";
import React from "react";
import { Movie } from "../interfaces";
import { makeTitle } from "./MovieDetail";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    movieCardTitle: {
      margin: theme.spacing(1),
    },
    link: {
      textDecoration: "none",
    },
    searchResultItem: {
      paddingLeft: 0,
      paddingBottom: theme.spacing(1),
      paddingTop: theme.spacing(0),
    },
    searchResultItemPaper: {
      width: "100%",
      transition: "0.2s",
      "&:hover": {
        backgroundColor: "#eee",
        opacity: 0.8,
      },
    },
  })
);

type SearchResultItemProps = {
  movie: Movie;
};

/**
 * 検索結果を描画する
 */
const SearchResultItem: React.FC<SearchResultItemProps> = ({ movie }) => {
  const classes = useStyles();
  return (
    <Link href={`/movies/${movie.movie_id}`}>
      <a className={classes.link}>
        <ListItem className={classes.searchResultItem} key={movie.movie_id}>
          <Paper
            className={classes.searchResultItemPaper}
            variant="outlined"
            square
          >
            <Grid container>
              <Grid item xs={1}>
                <Image src={movie.poster_url} aspectRatio={9 / 12} />
              </Grid>
              <Grid item xs={11}>
                <Typography className={classes.movieCardTitle} variant="h6">
                  {makeTitle(movie)}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </ListItem>
      </a>
    </Link>
  );
};

export default SearchResultItem;
