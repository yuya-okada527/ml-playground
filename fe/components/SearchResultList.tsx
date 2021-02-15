import React from "react";
import {
  createStyles,
  Grid,
  List,
  ListItem,
  makeStyles,
  Paper,
  Theme,
  Typography,
} from "@material-ui/core";
import Image from "material-ui-image";
import Pagination from "@material-ui/lab/Pagination";
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
      transition: "0.3s",
      "&:hover": {
        backgroundColor: "#eee",
        opacity: 0.8,
      },
    },
    paginationRoot: {
      textAlign: "center",
      "& > * + *": {
        marginTop: theme.spacing(2),
      },
    },
    pagination: {
      display: "inline-block",
    },
  })
);

const makeSearchTermView = (searchTerm: string) => {
  if (searchTerm) {
    return `"${searchTerm}"`;
  }

  return "ALL";
};

type SearchResultProps = {
  movies: Movie[];
  searchedTerm: string;
  page: number;
  pageCount: number;
  handlePageChange: (event: React.ChangeEvent<unknown>, page: number) => void;
};

const SearchResultList = ({
  movies,
  searchedTerm,
  page,
  pageCount,
  handlePageChange,
}: SearchResultProps) => {
  const classes = useStyles();
  return (
    <>
      <div className={classes.underSearch} />
      <Typography>Results for {makeSearchTermView(searchedTerm)}</Typography>
      <List>
        {movies.map((movie: Movie) => (
          <Link href={`/movies/${movie.movie_id}`} key={movie.movie_id}>
            <a className={classes.link}>
              <ListItem
                className={classes.searchResultItem}
                key={movie.movie_id}
              >
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
                      <Typography
                        className={classes.movieCardTitle}
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
      <div className={classes.paginationRoot}>
        <Pagination
          count={pageCount}
          page={page}
          color="primary"
          className={classes.pagination}
          onChange={handlePageChange}
        />
      </div>
    </>
  );
};

export default SearchResultList;
