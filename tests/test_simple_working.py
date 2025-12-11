import pytest
from playwright.async_api import async_playwright, Page

@pytest.fixture
async def browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=300  # Para ver las acciones
        )
        yield browser
        await browser.close()

@pytest.fixture
async def page(browser):
    page = await browser.new_page()
    yield page
    await page.close()

@pytest.mark.asyncio
async def test_visit_playwright_website(page: Page):
    """User Story: Visit Playwright website and verify title"""
    print("🌐 Navegando a Playwright.dev...")
    await page.goto("https://playwright.dev")
    
    print("✅ Verificando título...")
    title = await page.title()
    assert "Playwright" in title, f"Título no contiene 'Playwright': {title}"
    
    print("📸 Tomando screenshot...")
    await page.screenshot(path="playwright_simple.png")
    
    print("🎉 ¡Test completado exitosamente!")