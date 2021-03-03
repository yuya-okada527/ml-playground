import React from "react";
import { shallow } from "enzyme";
import SearchResultItem from "../src/components/SearchResultItem";
import { emptyMovie } from "./TestUtil";

describe("SearchResultItem", () => {
  it("Snapshot Test", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.movie_id = 0;
    movie.japanese_title = "タイトル";
    movie.poster_url = "http://movie.co.jp/image.png";
    movie.release_year = 2000;
    const searchResultItem = shallow(<SearchResultItem movie={movie} />);

    // 検証
    expect(searchResultItem).toMatchSnapshot();
  });
});
