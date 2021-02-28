import { ParsedUrlQuery } from "querystring";
import React, { ChangeEvent } from "react";
import { Grid } from "@material-ui/core";
import { useRouter } from "next/router";

import Layout from "../components/Layout";
import SearchBox from "../components/SearchBox";
import SearchResultList from "../components/SearchResultList";
import { Movie, SearchMoviesResponse } from "../interfaces/index";
import { callGetApi } from "../utils/http";
import config from "../utils/config";

const fetchSearchResult = async (
  searchTerm: string,
  page?: number
): Promise<SearchMoviesResponse> => {
  const url = config.apiEndpoint + "/v1/movie/search";
  const query = {
    query: searchTerm,
    start: page ? (page - 1) * 5 : 0,
    rows: 5,
  };

  const response = await callGetApi<SearchMoviesResponse>(url, query);
  return response;
};

const parsePageQuery = (query: ParsedUrlQuery) => {
  const pageStr = Array.isArray(query.page) ? query.page[0] : query.page;
  // 指定なしの場合、1
  if (!pageStr) {
    return 1;
  }

  return Number(pageStr);
};

const calcTotalPage = (hitNum: number) => {
  if (hitNum % 5 == 0) {
    return Math.floor(hitNum / 5);
  }

  return Math.floor(hitNum / 5) + 1;
};

const IndexPage: React.FC = () => {
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
  const [page, setPage] = React.useState<number>(parsePageQuery(router.query));
  const [totalPage, setTotalPage] = React.useState<number>(0);

  const handleSearchTermChange = (
    event: ChangeEvent<HTMLInputElement>
  ): void => {
    setSearchTerm(event.target.value);
  };

  const handleSearchButtonClick = React.useCallback(
    async (_event?: React.MouseEvent<unknown>, pageParam?: number) => {
      const response = await fetchSearchResult(searchTerm, pageParam);
      const hitNum: number = response.available_num;
      setSearchResult(response.results);
      setSearchedTerm(searchTerm);
      setPage(pageParam ? pageParam : 1);
      setTotalPage(calcTotalPage(hitNum));
    },
    [searchTerm, page]
  );

  const handlePageChange = (
    _event: React.ChangeEvent<unknown>,
    page: number
  ): void => {
    handleSearchButtonClick(undefined, page);
  };

  // 初期化時のみ起動、searchTermパラメータありの場合のみ検索を実行する
  React.useEffect(() => {
    if (searchTerm !== undefined) {
      handleSearchButtonClick(undefined);
    }
  }, []);
  return (
    <Layout title="ML Playground">
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
              page={page}
              pageCount={totalPage}
              handlePageChange={handlePageChange}
            />
          )}
        </Grid>
      </Grid>
    </Layout>
  );
};

export default IndexPage;
