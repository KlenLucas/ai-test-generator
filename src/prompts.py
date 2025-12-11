"""
Prompt templates for AI test generation.

Este módulo contiene todos los prompts que usamos para 
interactuar con Claude API.
"""

# PROMPT 1: Define el rol de Claude
SYSTEM_PROMPT = """You are an expert QA Engineer and test automation specialist.
You excel at analyzing user stories and creating comprehensive, production-ready tests.

Your expertise includes:
- Writing clear, maintainable Gherkin scenarios
- Creating robust Playwright test code in Python
- Following testing best practices and patterns
- Ensuring proper error handling and assertions
- Writing clean, well-documented code

Always prioritize:
1. Test clarity and maintainability
2. Proper use of Page Object Model patterns
3. Explicit waits and stable selectors
4. Comprehensive assertions
5. Good error messages
"""

# PROMPT 2: Para generar Gherkin desde User Stories
GHERKIN_GENERATION_PROMPT = """Generate a SINGLE, SIMPLE Gherkin scenario from this user story.

User Story:
{user_story}

CRITICAL RULES:
1. Generate ONLY ONE scenario (the main happy path)
2. Keep it simple - 3-5 steps maximum
3. Focus on what's explicitly requested
4. NO edge cases, NO error scenarios, NO variants
5. Just the core functionality

GOOD example (SINGLE scenario):
Feature: Visit Example Website

  Scenario: User visits example.com and sees content
    Given I navigate to "https://example.com"
    When the page loads
    Then I should see "Example Domain" in the page

BAD example (multiple scenarios):
Feature: Visit Example Website

  Scenario: Successfully visit
    Given I navigate to "https://example.com"
    ...
  
  Scenario: Visit with HTTP
    Given I navigate to "http://example.com"
    ...
  
  # DON'T DO THIS - too many scenarios

Generate ONLY ONE simple scenario. Output only valid Gherkin.
"""

# PROMPT 3: Para generar código Playwright desde Gherkin
PLAYWRIGHT_GENERATION_PROMPT = """You are generating Playwright test code from Gherkin scenarios.

Gherkin Scenarios:
{gherkin_scenarios}

CRITICAL REQUIREMENTS - FOLLOW EXACTLY:

1. FIXTURES (MANDATORY):
You MUST include these fixtures at the top:
```python
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
```

2. TEST FUNCTIONS:
- Create EXACTLY ONE test function per Gherkin scenario
- Use @pytest.mark.asyncio decorator
- Keep tests under 15 lines each
- Use descriptive but concise names

3. FORBIDDEN (DO NOT INCLUDE):
- NO Page Object Model classes
- NO @pytest.mark.parametrize
- NO multiple viewport tests
- NO network timeout tests
- NO accessibility tests (unless explicitly in Gherkin)
- NO try/except blocks (unless explicitly needed)
- NO extra scenarios beyond the Gherkin

4. STRUCTURE:
```python
import pytest
from playwright.async_api import async_playwright, Page

# Fixtures here (browser and page)

@pytest.mark.asyncio
async def test_name(page: Page):
    # Test implementation (simple and direct)
```

Generate MINIMAL, SIMPLE code. Only what is explicitly requested in the Gherkin.
Output ONLY the complete Python code with fixtures included.
"""
# ============================================
# FUNCIONES HELPER
# ============================================

def get_gherkin_prompt(user_story: str) -> str:
    """
    Get the prompt for generating Gherkin scenarios from a user story.
    
    Args:
        user_story: The user story text
        
    Returns:
        Formatted prompt string ready to send to Claude
        
    Example:
        >>> story = "As a user I want to login..."
        >>> prompt = get_gherkin_prompt(story)
        >>> # Ahora puedes enviar 'prompt' a Claude API
    """
    return GHERKIN_GENERATION_PROMPT.format(user_story=user_story)


def get_playwright_prompt(gherkin_scenarios: str) -> str:
    """
    Get the prompt for generating Playwright code from Gherkin scenarios.
    
    Args:
        gherkin_scenarios: The Gherkin scenarios text
        
    Returns:
        Formatted prompt string ready to send to Claude
        
    Example:
        >>> gherkin = "Feature: Login\\nScenario: ..."
        >>> prompt = get_playwright_prompt(gherkin)
        >>> # Ahora puedes enviar 'prompt' a Claude API
    """
    return PLAYWRIGHT_GENERATION_PROMPT.format(gherkin_scenarios=gherkin_scenarios)