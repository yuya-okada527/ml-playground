import React, { ChangeEvent } from "react";
import {
  Container,
  createStyles,
  Grid,
  makeStyles,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Theme,
  Typography,
} from "@material-ui/core";
import { useRouter } from "next/router";
import Layout from "../../components/Layout";
import SearchBox from "../../components/SearchBox";
import MovieDetail from "../../components/MovieDetail";
import { Movie } from "../../interfaces";
import config from "../../utils/config";
import { callGetApi } from "../../utils/http";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      marginLeft: theme.spacing(2),
      marginRight: theme.spacing(2),
    },
  })
);

const DetailPage = () => {
  const classes = useStyles();
  const router = useRouter();
  const { movie_id } = router.query;
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
    const initMovieData = async () => {
      const url = config.apiEndpoint + `/v1/movie/search/${movie_id}`;
      const query = {};
      const response = await callGetApi(url, query);
      setMovie(response);
    };
    const initSimilarMovies = async () => {
      const url = config.apiEndpoint + `/v1/movie/similar/${movie_id}`;
      const query = {
        model_type: "tmdb-sim",
      };
      const response = await callGetApi(url, query);
      setSimilarMovies(response.results);
    };
    initMovieData();
    initSimilarMovies();
  }, []);
  return (
    <Layout title={`Movie_${movie_id}`}>
      <Container className={classes.container}>
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
            <Typography variant="h6">Similar Movies</Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Rank</TableCell>
                    <TableCell>Title</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {similarMovies.map((movie: Movie, index: number) => (
                    <TableRow>
                      <TableCell>{index + 1}</TableCell>
                      <TableCell>{movie.japanese_title}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
};

export default DetailPage;
