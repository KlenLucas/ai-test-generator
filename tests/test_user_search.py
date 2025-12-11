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
async def test_user_performs_a_search(page: Page):
    # Given I am on the search page
    await page.goto("https://example.com/search")
    
    # When I enter "test query" in the search box
    await page.fill('[data-testid="search-input"]', "test query")
    
    # And I click the search button
    await page.click('[data-testid="search-button"]')
    
    # Then I should see search results displayed
    await page.wait_for_selector('[data-testid="search-results"]')
    results = await page.locator('[data-testid="search-results"]').count()
    assert results > 0