import {
  createStyles,
  Grid,
  List,
  ListItem,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import HomeIcon from "@material-ui/icons/Home";
import InfoIcon from "@material-ui/icons/Info";
import Link from "next/link";
import React from "react";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    root: {
      height: "calc(100vh - 170px)",
    },
    sideBarItem: {
      color: theme.palette.primary.main,
      cursor: "pointer",
      borderRadius: "5px",
      "&:hover": {
        backgroundColor: "#eee",
      },
    },
    sidebarIcon: {
      margin: theme.spacing(1),
    },
    sidebarText: {
      marginTop: theme.spacing(0.5),
    },
  })
);

/**
 * サイドバーを描画する
 */
const SideBar: React.FC = () => {
  const classes = useStyles();
  return (
    <List className={classes.root}>
      <ListItem>
        <Link href="/">
          <Grid container className={classes.sideBarItem}>
            <HomeIcon className={classes.sidebarIcon} />
            <Typography className={classes.sidebarText} variant="h6">
              Home
            </Typography>
          </Grid>
        </Link>
      </ListItem>
      <ListItem>
        <Link href="/about">
          <Grid container className={classes.sideBarItem}>
            <InfoIcon className={classes.sidebarIcon} />
            <Typography className={classes.sidebarText} variant="h6">
              About
            </Typography>
          </Grid>
        </Link>
      </ListItem>
    </List>
  );
};

export default SideBar;
