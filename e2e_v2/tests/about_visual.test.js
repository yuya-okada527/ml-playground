const { it, describe, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";
const IMAGE_BASE = "__snapshots__";

describe("Aboutページ ビジュアルテスト", () => {
  it("スクリーンショット", async ({ page }) => {
    await page.goto(`${BASE_PAGE}/about`);
    const screenshot = await page.screenshot({
      fullPage: true,
    });
    expect(screenshot).toMatchSnapshot("test-about", {
      threshold: 0.2,
    });
  });
});
