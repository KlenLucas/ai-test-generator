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
    # Given I navigate to "https://example.com"
    await page.goto("https://example.com")
    
    # When the page loads
    await page.wait_for_load_state("networkidle")
    
    # Then I should see "Example Domain" in the page
    assert await page.locator("text=Example Domain").is_visible()