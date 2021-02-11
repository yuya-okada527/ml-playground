import React, { ChangeEvent } from "react";
import {
  Container,
  createStyles,
  makeStyles,
  Theme,
  Grid,
  Typography,
} from "@material-ui/core";
import { useRouter } from "next/router";

import Layout from "../components/Layout";
import SearchBox from "../components/SearchBox";
import SearchResultList from "../components/SearchResultList";
import { Movie } from "../interfaces/index";
import { callGetApi } from "../utils/http";
import config from "../utils/config";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      marginLeft: theme.spacing(2),
      marginRight: theme.spacing(2),
    },
    underSearch: {
      marginBottom: theme.spacing(2),
    },
  })
);

const IndexPage = () => {
  const classes = useStyles();
  const router = useRouter();
  const [searchTerm, setSearchTerm] = React.useState<string>(
    Array.isArray(router.query.searchTerm)
      ? router.query.searchTerm[0]
      : router.query.searchTerm
  );
  const [searchedTerm, setSearchedTerm] = React.useState(
    router.query.searchTerm
  );
  const [searchResult, setSearchResult] = React.useState<Array<Movie>>([]);

  // const [searchResult, dispatchSearchResult] = React.useReducer()

  const handleSearchTermChange = (
    event: ChangeEvent<HTMLInputElement>
  ): void => {
    setSearchTerm(event.target.value);
  };

  const handleSearchButtonClick = async () => {
    const url = config.apiEndpoint + "/v1/movie/search";
    const query = {
      query: searchTerm,
      start: 0,
      rows: 5,
    };
    const response = await callGetApi(url, query);
    setSearchResult(response.results);
    setSearchedTerm(searchTerm);
  };
  return (
    <Layout title="Movie Recommeder">
      <Container className={classes.container}>
        <Grid container>
          <Grid item xs={8}>
            <Typography variant="h6" component="h2">
              Search Your Favorite Movies!!
            </Typography>
            <SearchBox
              searchTerm={searchTerm}
              handleSearchTermChange={handleSearchTermChange}
              handleSearchButtonClick={handleSearchButtonClick}
            />
            {searchResult.length > 0 && (
              <>
                <div className={classes.underSearch} />
                <Typography>Results for "{searchedTerm}"</Typography>
                <SearchResultList movies={searchResult} />
              </>
            )}
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
};

export default IndexPage;
