import { createMuiTheme } from "@material-ui/core/styles";
import { red } from "@material-ui/core/colors";

// TODO パッケージ構成再考
// Create a theme instance.
const theme = createMuiTheme({
  typography: {
    fontFamily: [
      "'Roboto'",
      "'Helvetica Neue'",
      "Arial",
      "'Noto Sans JP'",
      "'Hiragino Kaku Gothic ProN'",
      "'Hiragino Sans'",
      "Meiryo",
      "sans-serif",
    ].join(","),
  },
  palette: {
    secondary: {
      main: "#19857b",
    },
    error: {
      main: red.A400,
    },
    background: {
      default: "#fff",
    },
  },
});

export default theme;
