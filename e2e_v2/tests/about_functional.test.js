const chromium = require("playwright").chromium;

/** @type {import('playwright').Browser} */
let browser;
/** @type {import('playwright').Page} */
let page;

const BASE_PAGE = "http://localhost:3000";

beforeAll(async () => {
  browser = await chromium.launch({ headless: false, slowMo: 1000 });
});

describe("Aboutページ", () => {
  beforeAll(async () => {
    page = await browser.newPage();
  });

  describe("Aboutページへの画面遷移", () => {
    it("Topページから遷移", async () => {
      await page.goto(BASE_PAGE);
      await page.click("text=About");
      expect(await page.title()).toBe("About This Site");
    });
    it("URLで直接遷移", async () => {
      await page.goto(`${BASE_PAGE}/about`);
      expect(await page.title()).toBe("About This Site");
    });
  });

  describe("Aboutページからの画面遷移", () => {
    beforeEach(async () => {
      await page.goto(`${BASE_PAGE}/about`);
    });
    it("Homeボタンで遷移", async () => {
      await page.click("text=Home");
      expect(await page.title()).toBe("ML Playground");
    });
    it("映画推薦リンクで遷移", async () => {
      await page.click("text=映画推薦");
      expect(await page.title()).toBe("ML Playground");
    });
  });
});

afterAll(async () => {
  await browser.close();
});
