import { Container, createStyles, makeStyles, Theme } from "@material-ui/core";
import { useRouter } from "next/router";
import Layout from "../../components/Layout";

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

  return (
    <Layout title={`Movie_${movie_id}`}>
      <Container className={classes.container}>
        <h1>Movie ID: {movie_id}</h1>
      </Container>
    </Layout>
  );
};

export default DetailPage;
