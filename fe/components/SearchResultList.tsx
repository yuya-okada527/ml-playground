import React from "react";
import {
  createStyles,
  List,
  ListItem,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import Link from "next/link";
import { Movie } from "../interfaces/index";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    movieCardTitle: {
      margin: theme.spacing(1),
    },
  })
);

type SearchResultProps = {
  movies: Movie[];
};

const SearchResultList = ({ movies }: SearchResultProps) => {
  const classes = useStyles();
  return (
    <List>
      {movies.map((movie: Movie) => (
        <Link href={`/movies/${movie.movie_id}`} key={movie.movie_id}>
          <a>
            <ListItem key={movie.movie_id}>
              <Typography className={classes.movieCardTitle} variant="h6">
                {movie.japanese_title
                  ? movie.japanese_title
                  : movie.original_title}
              </Typography>
            </ListItem>
            <hr />
          </a>
        </Link>
      ))}
    </List>
  );
};

export default SearchResultList;