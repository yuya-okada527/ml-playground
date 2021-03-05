import React from "react";
import { shallow } from "enzyme";
import SimilarMovieItem from "../src/components/SimilarMovieItem";
import { emptyMovie } from "./TestUtil";

describe("SimilarMovieItem", () => {
  it("Snapshot Test", () => {
    const movie = emptyMovie();
    const similarMovieItem = shallow(<SimilarMovieItem movie={movie} />);
    expect(similarMovieItem).toMatchSnapshot();
  });
});
