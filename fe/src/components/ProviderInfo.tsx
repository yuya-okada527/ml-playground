import React from "react";
import {
  Box,
  createStyles,
  makeStyles,
  Theme,
  Typography,
} from "@material-ui/core";
import Image from "next/image";

const useStyles = makeStyles((theme: Theme) =>
  createStyles({
    providerInfo: {
      position: "absolute",
      bottom: 0,
      display: "flex",
      alignItems: "center",
    },
    providerIcon: {
      display: "inline",
    },
    providerComment: {
      fontSize: "13px",
      fontWeight: 300,
      marginRight: theme.spacing(1),
    },
  })
);

/**
 * 提供情報を描画する
 */
const ProviderInfo: React.FC = () => {
  const classes = useStyles();
  return (
    <Box className={classes.providerInfo}>
      <Typography variant="subtitle2" className={classes.providerComment}>
        This product uses the TMDb API but is not endorsed or certified by TMDb.
      </Typography>
      <Image
        src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_1-5bdc75aaebeb75dc7ae79426ddd9be3b2be1e342510f8202baf6bffa71d7f5c4.svg"
        alt="TMDB Logo"
        width={40}
        height={40}
        className={classes.providerIcon}
      />
    </Box>
  );
};

export default ProviderInfo;
