export type Movie = {
  movie_id: number;
  original_title: string;
  japanese_title: string;
  overview: string;
  tagline: string;
  poster_path: string;
  backdrop_path: string;
  popularity: number;
  vote_average: number;
  genre_labels: string[];
  genres: number[];
};
