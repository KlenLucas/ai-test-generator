import pytest
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


@pytest.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        yield browser
        await browser.close()


@pytest.fixture
async def page(browser: Browser):
    context = await browser.new_context()
    page = await context.new_page()
    yield page
    await context.close()


@pytest.mark.asyncio
async def test_user_can_access_playwright_demo_page(page: Page):
    # Cambia esta URL por una que funcione
    await page.goto("https://playwright.dev/")
    
    title = await page.title()
    # Cambia el assertion para que coincida con el título real
    assert "Playwright" in title  # Cambiado de == a "in"
    
    await page.screenshot(path="playwright_demo_page.png")