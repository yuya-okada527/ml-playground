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
    underSearch: {
      marginBottom: theme.spacing(2),
    },
  })
);

type SearchResultProps = {
  movies: Movie[];
  searchedTerm: string;
};

const SearchResultList = ({ movies, searchedTerm }: SearchResultProps) => {
  const classes = useStyles();
  console.log(movies);
  return (
    <>
      <div className={classes.underSearch} />
      <Typography>Results for "{searchedTerm}"</Typography>
      <List>
        {movies.map((movie: Movie) => (
          <Link href={`/movies/${movie.movie_id}`} key={movie.movie_id}>
            <a>
              <ListItem key={movie.movie_id}>
                <Typography className={classes.movieCardTitle} variant="h6">
                  {movie.japanese_title
                    ? movie.japanese_title
                    : movie.original_title}
                  {movie.release_year ? " (" + movie.release_year + ") " : ""}
                </Typography>
              </ListItem>
              <hr />
            </a>
          </Link>
        ))}
      </List>
    </>
  );
};

export default SearchResultList;
