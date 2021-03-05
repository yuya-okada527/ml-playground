const { it, describe, expect } = require("@playwright/test");

const BASE_PAGE = "http://localhost:3000";

describe("Homeページ ビジュアルテスト", () => {
  it("スクリーンショット", async ({ page, browserName }) => {
    await page.goto(`${BASE_PAGE}`);
    const screenshot = await page.screenshot({
      fullPage: true,
    });
    expect(screenshot).toMatchSnapshot(`home-${browserName}.png`, {
      threshold: 0.2,
    });
  });
});
