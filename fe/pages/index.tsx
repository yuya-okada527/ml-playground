import React, { ChangeEvent } from "react";
import {
  Container,
  createStyles,
  makeStyles,
  Theme,
  Grid,
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
  })
);

const fetchSearchResult = async (searchTerm: string) => {
  const url = config.apiEndpoint + "/v1/movie/search";
  const query = {
    query: searchTerm,
    start: 0,
    rows: 5,
  };
  const response = await callGetApi(url, query);
  return response.results;
};

const IndexPage = () => {
  const classes = useStyles();
  const router = useRouter();
  const [searchTerm, setSearchTerm] = React.useState<string>(
    Array.isArray(router.query.searchTerm)
      ? router.query.searchTerm[0]
      : router.query.searchTerm
  );
  const [searchedTerm, setSearchedTerm] = React.useState(
    Array.isArray(router.query.searchedTerm)
      ? router.query.searchedTerm[0]
      : router.query.searchedTerm
  );
  const [searchResult, setSearchResult] = React.useState<Array<Movie>>([]);

  const handleSearchTermChange = (
    event: ChangeEvent<HTMLInputElement>
  ): void => {
    setSearchTerm(event.target.value);
  };

  const handleSearchButtonClick = React.useCallback(async () => {
    const response = await fetchSearchResult(searchTerm);
    setSearchResult(response);
    setSearchedTerm(searchTerm);
  }, [searchTerm]);

  // 初期化時のみ起動、searchTermパラメータありの場合のみ検索を実行する
  React.useEffect(() => {
    if (searchTerm !== undefined) {
      handleSearchButtonClick();
    }
  }, []);
  return (
    <Layout title="Movie Recommender">
      <Container className={classes.container}>
        <Grid container>
          <Grid item xs={8}>
            <SearchBox
              searchTerm={searchTerm}
              handleSearchTermChange={handleSearchTermChange}
              handleSearchButtonClick={handleSearchButtonClick}
            />
            {searchResult.length > 0 && (
              <SearchResultList
                movies={searchResult}
                searchedTerm={searchedTerm}
                page={1}
              />
            )}
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
};

export default IndexPage;
