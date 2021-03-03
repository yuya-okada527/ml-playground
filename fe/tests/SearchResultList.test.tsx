import { makeSearchTermView } from "../src/components/SearchResultList";

describe("makeSearchTermView", () => {
  it("searchTerm exists", () => {
    // テストデータ
    const searchTerm = "test";

    // 検証
    expect(makeSearchTermView(searchTerm)).toBe('"test"');
  });

  it("searchTerm does not exist", () => {
    // テストデータ
    const searchTerm = "";

    // 検証
    expect(makeSearchTermView(searchTerm)).toBe("ALL");
  });
});
