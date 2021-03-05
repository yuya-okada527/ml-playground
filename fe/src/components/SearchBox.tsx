import React, { ChangeEvent } from "react";
import {
  Button,
  createStyles,
  makeStyles,
  TextField,
  Theme,
  Typography,
  Grid,
} from "@material-ui/core";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    searchButton: {
      marginTop: theme.spacing(1.5),
      marginLeft: theme.spacing(3),
    },
  })
);

type SearchBoxProps = {
  searchTerm: string;
  handleSearchTermChange: (event: ChangeEvent<HTMLInputElement>) => void;
  handleSearchButtonClick: (_event?: React.MouseEvent<unknown>) => void;
};

/**
 * 検索ボックスを描画する
 */
const SearchBox: React.FC<SearchBoxProps> = ({
  searchTerm,
  handleSearchTermChange,
  handleSearchButtonClick,
}) => {
  const classes = useStyles();
  return (
    <>
      <Typography variant="h6" component="h2">
        Search Your Favorite Movies!!
      </Typography>
      <Grid container>
        <Grid item xs={10}>
          <TextField
            id="search-movie"
            label="Search Movies!!"
            type="search"
            fullWidth
            value={searchTerm}
            onChange={handleSearchTermChange}
          />
        </Grid>
        <Grid item xs={2}>
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
    </>
  );
};

export default SearchBox;
