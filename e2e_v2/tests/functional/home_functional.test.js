const { it, describe, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";

describe("Homeページ 機能テスト", () => {
  describe("検索", () => {
    it("キーワードなし", async ({ page }) => {
      await page.goto(BASE_PAGE);

      // 検索条件なしで、検索実行
      await page.click('button:has-text("Search")');

      // 検索条件なしで検索実行していることを検証
      const searchResultKeyword = await page.textContent(
        "data-test=search-result-keyword"
      );
      expect(searchResultKeyword).toBe("Results for ALL");

      // 検索結果が5件表示されていることを検証
      const searchResultLength = await page.$$eval(
        "[data-test=search-result-list] li",
        (items) => items.length
      );
      expect(searchResultLength === 5).toBeTruthy();
    });
    it("キーワードあり", async ({ page }) => {
      await page.goto(`${BASE_PAGE}`);

      // 検索条件ありで、検索実行
      const keyword = "ワンダー";
      await page.fill('input[type="search"]', keyword);
      await page.click('button:has-text("Search")');

      // 指定検索条件で検索実行していることを検証
      const searchResultKeyword = await page.textContent(
        "data-test=search-result-keyword"
      );
      expect(searchResultKeyword).toBe(`Results for "${keyword}"`);

      // ワンダーウーマンが検索結果にあることを確認
      expect(await page.isVisible("ワンダーウーマン"));
    });
  });

  describe("ページネーション", () => {
    it("検索後 1ページ目であること", async ({ page }) => {
      await page.goto(`${BASE_PAGE}`);

      // 検索実行
      await page.click('button:has-text("Search")');

      // 1ページ目が現在のページであることを検証
      const current = await page.getAttribute(
        '[aria-label="page 1"]',
        "aria-current"
      );
      expect(current).toBeTruthy();
    });

    it("検索後 2ページ目に遷移", async ({ page }) => {
      await page.goto(`${BASE_PAGE}`);

      // 検索実行
      await page.click('button:has-text("Search")');

      // 2ページ目に遷移
      await page.click('[aria-label="Go to page 2"]');
      const current = await page.getAttribute(
        '[aria-label="page 2"]',
        "aria-current"
      );
      expect(current).toBeTruthy();
    });

    it("検索後 次のページに遷移", async ({ page }) => {
      await page.goto(`${BASE_PAGE}`);

      // 検索実行
      await page.click('button:has-text("Search")');

      // 次のページに遷移
      await page.click('[aria-label="Go to next page"]');
      const current = await page.getAttribute(
        '[aria-label="page 2"]',
        "aria-current"
      );
      expect(current).toBeTruthy();
    });

    it("検索後 前のページに遷移", async ({ page }) => {
      await page.goto(`${BASE_PAGE}`);

      // 検索実行
      await page.click('button:has-text("Search")');

      // 次のページに遷移、前のページに戻る
      await page.click('[aria-label="Go to next page"]');
      await page.click('[aria-label="Go to previous page"]');
      const current = await page.getAttribute(
        '[aria-label="page 1"]',
        "aria-current"
      );
      expect(current).toBeTruthy();
    });
  });
});
