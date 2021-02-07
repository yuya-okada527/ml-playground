import React from "react";
import {
  Card,
  Container,
  createStyles,
  makeStyles,
  Theme,
} from "@material-ui/core";
import { useRouter } from "next/router";
import Layout from "../../components/Layout";
import { Movie } from "../../interfaces";
import config from "../../utils/config";
import { callGetApi } from "../../utils/http";

type MovieDetailProps = {
  movie_detail: Movie;
};

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      marginLeft: theme.spacing(2),
      marginRight: theme.spacing(2),
    },
  })
);

const MovieDetail = ({ movie_detail }: MovieDetailProps) => (
  <h2>{movie_detail.japanese_title}</h2>
);

const DetailPage = () => {
  const classes = useStyles();
  const router = useRouter();
  const { movie_id } = router.query;
  const [movie, setMovie] = React.useState<Movie>();

  React.useEffect(() => {
    const initMovieData = async () => {
      const url = config.apiEndpoint + `/v1/movie/search/${movie_id}`;
      const query = {};
      const response = await callGetApi(url, query);
      console.log("initMovieData");
      setMovie(response);
    };
    initMovieData();
  }, []);
  return (
    <Layout title={`Movie_${movie_id}`}>
      <Container className={classes.container}>
        {movie !== undefined && <MovieDetail movie_detail={movie} />}
      </Container>
    </Layout>
  );
};

export default DetailPage;
