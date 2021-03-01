import React from "react";
import Head from "next/head";
import theme from "../utils/theme";

type MetaDataProps = {
  title: string;
};

/**
 * headタグを記述する
 *
 * @param title タイトル
 */
const MetaData: React.FC<MetaDataProps> = ({ title }) => (
  <Head>
    <title>{title}</title>
    <meta charSet="utf-8" />
    <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    <meta name="theme-color" content={theme.palette.primary.main} />
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"
    />
    <link rel="preconnect" href="https://fonts.gstatic.com" />
    <link
      href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP&display=swap"
      rel="stylesheet"
    />
  </Head>
);

export default MetaData;
