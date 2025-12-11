"""
Prueba del validador con código CORRECTO
"""

from src.validators import CodeValidator

# Código correcto (sin problemas)
test_code_good = """
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
async def test_example(page: Page):
    await page.goto("https://example.com")
    title = await page.title()
    assert "Example" in title
"""

# Código malo (con problemas)
test_code_bad = """
import pytest

async def test_example(page):
    page.goto("https://example.com")
    title = page.title()
    assert "Example" in title
"""

def main():
    validator = CodeValidator()
    
    print("🧪 PRUEBA 1: CÓDIGO MALO")
    print("=" * 60)
    result_bad = validator.validate_code(test_code_bad)
    print(result_bad)
    print()
    
    print()
    print("🧪 PRUEBA 2: CÓDIGO BUENO")
    print("=" * 60)
    result_good = validator.validate_code(test_code_good)
    print(result_good)
    print()

if __name__ == "__main__":
    main()