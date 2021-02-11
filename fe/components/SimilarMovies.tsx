import React from "react";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@material-ui/core";
import { Movie } from "../interfaces";

type SimilarMoviesProps = {
  similarMovies: Movie[];
};

const SimilarMovies = ({ similarMovies }: SimilarMoviesProps) => (
  <>
    <Typography variant="h6">Similar Movies</Typography>
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Rank</TableCell>
            <TableCell>Title</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {similarMovies.map((movie: Movie, index: number) => (
            <TableRow>
              <TableCell>{index + 1}</TableCell>
              <TableCell>{movie.japanese_title}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  </>
);

export default SimilarMovies;