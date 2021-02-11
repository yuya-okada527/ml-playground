describe("検索エンジン スナップショットテスト", () => {
  it("全検索条件がマッチすること", () => {
    return cy
      .request("http://localhost:8983/solr/movies/select?q=*:*")
      .its("body")
      .its("response")
      .its("docs")
      .toMatchSnapshot();
  });
});
