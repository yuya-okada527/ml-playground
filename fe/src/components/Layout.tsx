import React, { ReactNode } from "react";
import { Grid, createStyles, makeStyles, Theme } from "@material-ui/core";
import Footer from "./Footer";
import Header from "./Header";
import SideBar from "./SideBar";
import MetaData from "./MetaData";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    offset: {
      marginTop: theme.spacing(11.5),
    },
  })
);

type LayoutProps = {
  children?: ReactNode;
  title?: string;
};

/**
 * ページの全体構造を提供する
 * このコンポーネントでページ要素をラップして、ページを作る
 */
const Layout: React.FC<LayoutProps> = ({
  children,
  title = "This is the default title",
}) => {
  const classes = useStyles();
  return (
    <>
      {/* ヘッダー要素 */}
      <MetaData title={title} />
      <Header />
      <div className={classes.offset} />

      {/* メイン要素 */}
      <Grid container>
        <Grid item xs={2}>
          <SideBar />
        </Grid>
        <Grid item xs={10}>
          {children}
        </Grid>
      </Grid>

      {/* フッター要素 */}
      <Footer />
    </>
  );
};

export default Layout;
