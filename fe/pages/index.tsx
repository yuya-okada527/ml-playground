import React, { ChangeEvent } from "react";
import {
  Button,
  Card,
  Container,
  createStyles,
  List,
  ListItem,
  makeStyles,
  TextField,
  Theme,
  Grid,
  Typography,
  CardContent,
} from "@material-ui/core";
import Layout from "../components/Layout";
import { Movie } from "../interfaces/index";
import { callGetApi } from "../utils/http";
import config from "../utils/config";

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
    underSearch: {
      marginBottom: theme.spacing(2),
    },
    movieCard: {
      width: "75%",
      padding: theme.spacing(0),
    },
    movieCardContent: {
      padding: theme.spacing(0),
    },
    movieCardTitle: {
      margin: theme.spacing(1),
    },
  })
);

type SearchResultProps = {
  movies: Movie[];
};

const SearchResultList = ({ movies }: SearchResultProps) => {
  const classes = useStyles();
  return (
    <List>
      {movies.map((movie: Movie) => (
        <ListItem>
          <Card className={classes.movieCard}>
            <CardContent className={classes.movieCardContent}>
              <Typography className={classes.movieCardTitle} variant="h6">
                {movie.japanese_title
                  ? movie.japanese_title
                  : movie.original_title}
              </Typography>
            </CardContent>
          </Card>
        </ListItem>
      ))}
    </List>
  );
};

const IndexPage = () => {
  const classes = useStyles();
  const [searchTerm, setSearchTerm] = React.useState("");
  const [searchedTerm, setSearchedTerm] = React.useState("");
  const [searchResult, setSearchResult] = React.useState<Array<Movie>>([]);

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
                  value={searchTerm}
                  onChange={handleSearchTermChange}
                />
              </Grid>
              <Grid item xs={4}>
                <Button
                  variant="contained"
                  color="primary"
                  className={classes.searchButton}
                  onClick={handleSearchButtonClick}
                >
                  Search
                </Button>
              </Grid>
            </Grid>
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
