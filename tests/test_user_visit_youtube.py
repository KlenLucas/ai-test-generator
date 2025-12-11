import pytest
from playwright.async_api import async_playwright, Page

@pytest.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_user_visits_youtube_homepage(page: Page):
    await page.goto("https://youtube.com")
    await page.wait_for_load_state("networkidle")
    
    # Verify YouTube homepage elements
    await page.wait_for_selector("[aria-label='YouTube Home']", timeout=10000)
    title = await page.title()
    assert "YouTube" in title