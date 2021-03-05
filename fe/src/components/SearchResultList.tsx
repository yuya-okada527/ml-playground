import React from "react";
import {
  createStyles,
  List,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import { Movie } from "../interfaces/index";
import SearchResultPagination from "./SearchResultPagination";
import SearchResultItem from "./SearchResultItem";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    underSearch: {
      marginBottom: theme.spacing(2),
    },
  })
);

const makeSearchTermView = (searchTerm: string): string => {
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

/**
 * 検索結果リストを描画する
 */
const SearchResultList: React.FC<SearchResultProps> = ({
  movies,
  searchedTerm,
  page,
  pageCount,
  handlePageChange,
}) => {
  const classes = useStyles();
  return (
    <>
      <div className={classes.underSearch} />
      <Typography data-test="search-result-keyword">
        Results for {makeSearchTermView(searchedTerm)}
      </Typography>
      <List data-test="search-result-list">
        {movies.map((movie: Movie) => (
          <SearchResultItem key={movie.movie_id} movie={movie} />
        ))}
      </List>
      <SearchResultPagination
        totalPageCount={pageCount}
        currentPage={page}
        handlePageChange={handlePageChange}
      />
    </>
  );
};

export default SearchResultList;
export { makeSearchTermView };
