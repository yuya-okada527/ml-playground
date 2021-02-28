import React, { ChangeEvent } from "react";
import { Grid } from "@material-ui/core";
import { useRouter } from "next/router";
import Layout from "../../components/Layout";
import SearchBox from "../../components/SearchBox";
import MovieDetail from "../../components/MovieDetail";
import SimilarMovies from "../../components/SimilarMovies";
import { Movie, SimilarMoviesResponse } from "../../interfaces";
import config from "../../utils/config";
import { callGetApi } from "../../utils/http";

const DetailPage: React.FC = () => {
  const router = useRouter();
  const [movieId, setMovieId] = React.useState("");
  const [movie, setMovie] = React.useState<Movie>();
  const [searchTerm, setSearchTerm] = React.useState("");
  const [similarMovies, setSimilarMovies] = React.useState<Array<Movie>>([]);

  const handleSearchTermChange = (
    event: ChangeEvent<HTMLInputElement>
  ): void => {
    setSearchTerm(event.target.value);
  };

  const handleSearchButtonClick = async () => {
    router.push({
      pathname: "/",
      query: { searchTerm: searchTerm },
    });
  };

  React.useEffect(() => {
    // idがqueryで利用可能になったら処理される
    if (router.asPath !== router.route) {
      setMovieId(
        Array.isArray(router.query.movie_id)
          ? router.query.movie_id[0]
          : router.query.movie_id
      );
    }
  }, [router]);

  React.useEffect(() => {
    if (!movieId) {
      return;
    }
    const initMovieData = async () => {
      const url = config.apiEndpoint + `/v1/movie/search/${movieId}`;
      const query = {};
      const response = await callGetApi<Movie>(url, query);
      setMovie(response);
    };
    const initSimilarMovies = async () => {
      const url = config.apiEndpoint + `/v1/movie/similar/${movieId}`;
      const query = {
        model_type: "tmdb-sim",
      };
      const response = await callGetApi<SimilarMoviesResponse>(url, query);
      setSimilarMovies(response.results);
    };
    initMovieData();
    initSimilarMovies();
  }, [movieId]);
  return (
    <Layout title={`Movie Recommend ${movieId}`}>
      <Grid container>
        <Grid item xs={8}>
          <SearchBox
            searchTerm={searchTerm}
            handleSearchTermChange={handleSearchTermChange}
            handleSearchButtonClick={handleSearchButtonClick}
          />
          {movie !== undefined && <MovieDetail movie_detail={movie} />}
        </Grid>
        <Grid item xs={4}>
          <SimilarMovies
            similarMovies={similarMovies}
            movieTitle={movie ? movie.japanese_title : ""}
          />
        </Grid>
      </Grid>
    </Layout>
  );
};

export default DetailPage;
