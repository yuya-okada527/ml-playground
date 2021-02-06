import React from "react";
import {
  Button,
  Container,
  createStyles,
  makeStyles,
  TextField,
  Theme,
  Grid,
  Typography,
} from "@material-ui/core";
import Layout from "../components/Layout";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    container: {
      marginLeft: theme.spacing(2),
      marginRight: theme.spacing(2),
    },
    searchButton: {
      marginTop: theme.spacing(1),
      marginLeft: theme.spacing(2),
    },
  })
);

const IndexPage = () => {
  const classes = useStyles();
  return (
    <Layout title="Movie Recommeder">
      <Container className={classes.container}>
        <Grid container>
          <Grid item xs={9}>
            <Typography variant="h6" component="h2">
              Search Your Favorite Movies!!
            </Typography>
            <Grid container>
              <Grid item xs={8}>
                <TextField
                  id="search-movie"
                  label="Search Movies!!"
                  type="search"
                  fullWidth
                />
              </Grid>
              <Grid item xs={4}>
                <Button
                  variant="contained"
                  color="primary"
                  className={classes.searchButton}
                >
                  Search
                </Button>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Container>
    </Layout>
  );
};

export default IndexPage;
