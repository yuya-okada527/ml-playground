import { makeQuery } from "../src/utils/http";

describe("makeQuery", () => {
  it("1対1のクエリ", () => {
    // テストデータ
    const queries = {
      str: "str",
      num: 0,
      bool: true,
    };

    // 検証
    const actual = makeQuery(queries);
    const expected = "str=str&num=0&bool=true";
    expect(actual).toBe(expected);
  });

  it("1対多のクエリ", () => {
    // テストデータ
    const queries = {
      str: ["str1", "str2"],
      num: [0, 1],
      bool: [true, false],
    };

    // 検証
    const actual = makeQuery(queries);
    const expected = "str=str1&str=str2&num=0&num=1&bool=true&bool=false";
    expect(actual).toBe(expected);
  });

  it("空のクエリの場合", () => {
    // テストデータ
    const queries = {};

    // 検証
    expect(makeQuery(queries)).toBe("");
  });
});
