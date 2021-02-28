import React, { ReactNode } from "react";
import Head from "next/head";
import AppBar from "@material-ui/core/AppBar";
import HomeIcon from "@material-ui/icons/Home";
import InfoIcon from "@material-ui/icons/Info";
import {
  Link,
  Grid,
  createStyles,
  makeStyles,
  Theme,
  Typography,
  List,
  ListItem,
} from "@material-ui/core";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    title: {
      margin: theme.spacing(2),
    },
    offset: {
      marginTop: theme.spacing(11.5),
    },
    sidebarIcon: {
      margin: theme.spacing(1),
    },
    sidebarText: {
      marginTop: theme.spacing(0.5),
    },
    footer: {
      width: "100%",
      position: "absolute",
      bottom: 0,
      borderTop: "1px solid black",
    },
    footerList: {
      paddingTop: theme.spacing(0.5),
    },
    footerListItem: {
      paddingTop: theme.spacing(0.5),
      paddingBottom: theme.spacing(0),
    },
  })
);

type Props = {
  children?: ReactNode;
  title?: string;
};

const Layout: React.FC<Props> = ({
  children,
  title = "This is the default title",
}) => {
  const classes = useStyles();
  return (
    <div>
      <Head>
        <title>{title}</title>
        <meta charSet="utf-8" />
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
        />
      </Head>
      <header>
        <AppBar>
          <Typography variant="h4" component="h1" className={classes.title}>
            ML Playground
          </Typography>
        </AppBar>
      </header>
      <div className={classes.offset} />
      <Grid container>
        <Grid item xs={2}>
          <List>
            <ListItem>
              <Link href="/">
                <Grid container>
                  <HomeIcon className={classes.sidebarIcon} />
                  <Typography className={classes.sidebarText} variant="h6">
                    Home
                  </Typography>
                </Grid>
              </Link>
            </ListItem>
            <ListItem>
              <Link href="/about">
                <Grid container>
                  <InfoIcon className={classes.sidebarIcon} />
                  <Typography className={classes.sidebarText} variant="h6">
                    About
                  </Typography>
                </Grid>
              </Link>
            </ListItem>
          </List>
        </Grid>
        <Grid item xs={10}>
          {children}
        </Grid>
      </Grid>

      <footer className={classes.footer}>
        <Grid container>
          <Grid item xs={7}>
            <List className={classes.footerList}>
              <ListItem className={classes.footerListItem}>
                Contact: yuya.okada527@gmail.com
              </ListItem>
              <ListItem className={classes.footerListItem}>
                Github: https://github.com/yuya-okada527/ml-playground
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </footer>
    </div>
  );
};

export default Layout;
