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
async def test_user_visits_example_com_and_sees_content(page: Page):
    await page.goto("https://example.com")
    await page.wait_for_load_state("networkidle")
    content = await page.text_content("body")
    assert "Example Domain" in content