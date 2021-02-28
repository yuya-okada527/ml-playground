export type Movie = {
  movie_id: number;
  original_title: string;
  japanese_title: string;
  overview: string;
  tagline: string;
  poster_url: string;
  backdrop_url: string;
  popularity: number;
  vote_average: number;
  release_date: string;
  release_year: number;
  genre_labels: string[];
  genres: number[];
};

export type SearchMoviesResponse = {
  start: number;
  returned_num: number;
  available_num: number;
  results: Movie[];
};

export type SimilarMoviesResponse = {
  target_id: number;
  model_type: string;
  results: Movie[];
};
