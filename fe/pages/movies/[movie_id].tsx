import React from "react";
import {
  Card,
  CardMedia,
  CardContent,
  Container,
  createStyles,
  Grid,
  makeStyles,
  Theme,
  Typography,
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
    cardRoot: {
      display: "flex",
    },
    cardCover: {
      width: 700,
    },
  })
);

const MovieDetail = ({ movie_detail }: MovieDetailProps) => {
  const classes = useStyles();
  return (
    <Card className={classes.cardRoot}>
      <CardMedia
        className={classes.cardCover}
        image={movie_detail.poster_url}
      />
      <CardContent>
        <Typography>{movie_detail.japanese_title}</Typography>
        <p>{movie_detail.overview}</p>
      </CardContent>
    </Card>
  );
};

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
        <Grid container>
          <Grid item xs={8}>
            {movie !== undefined && <MovieDetail movie_detail={movie} />}
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
};

export default DetailPage;
