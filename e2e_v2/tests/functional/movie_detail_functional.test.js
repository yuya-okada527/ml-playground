const { it, describe, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";

describe("映画詳細ページ 機能テスト", () => {
  describe("画面遷移", () => {
    it("映画詳細に遷移", async ({ page }) => {
      await page.goto(BASE_PAGE);

      // 検索条件なしで、検索実行
      await page.click('button:has-text("Search")');

      // 検索後、一番最初に出てきた映画に遷移
      await page.click("[data-test=search-result-list] li:nth-child(1)");

      // パスで確認
      expect(await page.url()).toContain("movies");
    });
    it("映画詳細から再検索が実行できる", async ({ page }) => {
      await page.goto(BASE_PAGE);

      // 検索条件なしで、検索実行
      await page.click('button:has-text("Search")');

      // 検索後、一番最初に出てきた映画に遷移
      await page.click("[data-test=search-result-list] li:nth-child(1)");

      // 再検索
      await page.click('button:has-text("Search")');

      // Homeに戻れていることを検証
      expect(await page.title()).toBe("ML Playground");

      // 検索条件なしで検索実行できていることを検証
      // 検索条件なしで検索実行していることを検証
      const searchResultKeyword = await page.textContent(
        "data-test=search-result-keyword"
      );
      expect(searchResultKeyword).toBe("Results for ALL");
    });

    it("類似映画から遷移できることを検証", async ({ page }) => {
      await page.goto(BASE_PAGE);

      // 検索条件なしで、検索実行
      await page.click('button:has-text("Search")');

      // 検索後、一番最初に出てきた映画に遷移
      await page.click("[data-test=search-result-list] li:nth-child(1)");

      // 類似映画の一番最初に出てきた映画に遷移
      await page.click("[data-test=similar-movie-list] li:nth-child(1)");
    });
  });
});
