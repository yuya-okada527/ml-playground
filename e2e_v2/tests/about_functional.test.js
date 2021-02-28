const { it, describe, beforeEach, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";

describe("Aboutページ 機能テスト", () => {
  describe("Aboutページへの画面遷移", () => {
    it("Topページから遷移", async ({ page }) => {
      await page.goto(BASE_PAGE);
      await page.click("text=About");
      expect(await page.title()).toBe("About This Site");
    });
    it("URLで直接遷移", async ({ page }) => {
      await page.goto(`${BASE_PAGE}/about`);
      expect(await page.title()).toBe("About This Site");
    });
  });

  describe("Aboutページからの画面遷移", () => {
    beforeEach(async ({ page }) => {
      await page.goto(`${BASE_PAGE}/about`);
    });
    it("Homeボタンで遷移", async ({ page }) => {
      await page.click("text=Home");
      expect(await page.title()).toBe("ML Playground");
    });
    it("映画推薦リンクで遷移", async ({ page }) => {
      await page.click("text=映画推薦");
      expect(await page.title()).toBe("ML Playground");
    });
  });
});
