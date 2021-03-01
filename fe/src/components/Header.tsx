import {
  AppBar,
  createStyles,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import React from "react";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    title: {
      margin: theme.spacing(2),
    },
  })
);

/**
 * ヘッダーを描画する
 */
const Header: React.FC = () => {
  const classes = useStyles();
  return (
    <header>
      <AppBar>
        <Typography variant="h4" component="h1" className={classes.title}>
          ML Playground
        </Typography>
      </AppBar>
    </header>
  );
};

export default Header;
