const { it, describe, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";

describe("Aboutページ ビジュアルテスト", () => {
  it("スクリーンショット", async ({ page, browserName }) => {
    await page.goto(`${BASE_PAGE}/about`);
    const screenshot = await page.screenshot({
      fullPage: true,
    });
    expect(screenshot).toMatchSnapshot(`about-${browserName}.png`, {
      threshold: 0.2,
    });
  });
});
