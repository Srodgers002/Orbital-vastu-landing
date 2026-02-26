from playwright.async_api import async_playwright


async def scrape_article(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.locator('article').inner_text()
        await browser.close()
        return content
