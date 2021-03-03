import React from "react";
import { shallow } from "enzyme";
import MovieDetail, {
  makeOverview,
  makeTitle,
} from "../src/components/MovieDetail";
import { emptyMovie } from "./TestUtil";

describe("makeOverview", () => {
  it("シナリオが空", () => {
    // テストデータ
    const overview = "";

    // 検証
    expect(makeOverview(overview)).toBe("");
  });

  it("シナリオがnull", () => {
    // テストデータ
    let overview;

    // 検証
    expect(makeOverview(overview)).toBe("");
  });

  it("シナリオの文字数 < 400", () => {
    // テストデータ
    const overview = "1234567890";

    // 検証
    expect(makeOverview(overview)).toBe(overview);
  });

  it("シナリオの文字列 > max_length", () => {
    // テストデータ
    const overview = "1234567890";
    const max_length = 5;

    // 検証
    const actual = makeOverview(overview, max_length);
    const expected = "12345...";
    expect(actual).toBe(expected);
  });
});

describe("makeTitle", () => {
  it("タイトルが無い場合", () => {
    // テストデータ
    const movie = emptyMovie();

    // 検証
    const actual = makeTitle(movie);
    const expected = "申し訳ありません。タイトルが表示できません。";
    expect(actual).toBe(expected);
  });

  it("日本語タイトルあり オリジナルタイトルなし 公開年なし", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.japanese_title = "日本語タイトル";

    // 検証
    expect(makeTitle(movie)).toBe(movie.japanese_title);
  });

  it("日本語タイトルあり オリジナルタイトルあり 公開年あり", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.japanese_title = "日本語タイトル";
    movie.original_title = "original title";
    movie.release_year = 2020;

    // 検証
    const actual = makeTitle(movie);
    const expected = "日本語タイトル (2020)";
    expect(actual).toBe(expected);
  });

  it("日本語タイトルなし オリジナルタイトルあり 公開年なし", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.original_title = "original title";

    // 検証
    expect(makeTitle(movie)).toBe(movie.original_title);
  });

  it("日本語タイトルなし オリジナルタイトルあり 公開年あり", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.original_title = "original title";
    movie.release_year = 2020;

    // 検証
    const actual = makeTitle(movie);
    const expected = "original title (2020)";
    expect(actual).toBe(expected);
  });
});

describe("MovieDetail", () => {
  it("Snapshot Test", () => {
    // テストデータ
    const movie = emptyMovie();
    movie.japanese_title = "タイトル";
    movie.overview = "シナリオ";
    movie.poster_url = "https://image_url.png";

    // 検証
    const movieDetail = shallow(<MovieDetail movie_detail={movie} />);
    expect(movieDetail).toMatchSnapshot();
  });
});
