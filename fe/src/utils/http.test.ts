import { makeQuery } from "./http";

describe("テスト: makeQuery", () => {
  it("単一値のクエリ", () => {
    // テストデータ
    const queries = {
      keyString: "str",
      keyNumber: 0,
      keyBoolean: true,
    };

    // 検証
    const actual = makeQuery(queries);
    const expected = "keyString=str&keyNumber=0&keyBoolean=true";
    expect(actual).toBe(expected);
  });
});
