import {
  createStyles,
  List,
  ListItem,
  makeStyles,
  Theme,
} from "@material-ui/core";
import React from "react";

const MAIL_ADDRESS = "yuya.okada527@gmail.com";
const GITHUB_URL = "https://github.com/yuya-okada527/ml-playground";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
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

/**
 * フッターを描画する
 */
const Footer: React.FC = () => {
  const classes = useStyles();
  return (
    <footer className={classes.footer}>
      <List className={classes.footerList}>
        <ListItem className={classes.footerListItem}>
          Contact: {MAIL_ADDRESS}
        </ListItem>
        <ListItem className={classes.footerListItem}>
          Github: {GITHUB_URL}
        </ListItem>
      </List>
    </footer>
  );
};

export default Footer;
