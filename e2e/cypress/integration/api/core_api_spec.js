const BASE_URL = "localhost:8888/v1";

describe("CoreAPI スナップショットテスト", () => {
  context("映画検索API", () => {
    it("検索条件なし", () => {
      return cy
        .request(`${BASE_URL}/movie/search`)
        .its("body")
        .toMatchSnapshot();
    });

    it("検索条件あり", () => {
      return cy
        .request(`${BASE_URL}/movie/search?query=ゴジラ`)
        .its("body")
        .toMatchSnapshot();
    });
  });

  context("映画取得API", () => {
    it("映画ID=373571", () => {
      return cy
        .request(`${BASE_URL}/movie/search/373571`)
        .its("body")
        .toMatchSnapshot();
    });
  });

  context("類似映画取得API", () => {
    it("映画ID=373571", () => {
      return cy
        .request(`${BASE_URL}/movie/similar/373571?model_type=tmdb-sim`)
        .its("body")
        .toMatchSnapshot();
    });
  });
});
