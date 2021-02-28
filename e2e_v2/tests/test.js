const chromium = require("playwright").chromium;

/** @type {import('playwright').Browser} */
let browser;
/** @type {import('playwright').Page} */
let page;

beforeAll(async () => {
  browser = await chromium.launch({ headless: false });
});

beforeAll(async () => {
  browser = await chromium.launch({ headless: false });
});

describe("LOGIN", () => {
  beforeAll(async () => {
    page = await browser.newPage();
    await page.goto("http://localhost:3000");
  });

  it("Title is valid", async () => {
    expect(await page.title()).toBe("ML Playground");
  });
});

afterAll(async () => {
  await browser.close();
});
