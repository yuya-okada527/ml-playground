import { Movie } from "src/interfaces";

const emptyMovie = (): Movie => {
  return {
    movie_id: 0,
    original_title: "",
    japanese_title: "",
    overview: "",
    tagline: "",
    poster_url: "",
    backdrop_url: "",
    popularity: 0,
    vote_average: 0,
    release_date: "",
    release_year: 0,
    genre_labels: [],
    genres: [],
  };
};

export { emptyMovie };
