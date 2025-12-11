import pytest
from playwright.async_api import async_playwright, Page, Browser, BrowserContext


class TestLogin:
    
    @pytest.fixture
    async def browser(self):
        """Setup and teardown browser instance"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            yield browser
            await browser.close()
    
    @pytest.fixture
    async def page(self, browser: Browser):
        """Setup and teardown page instance"""
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()
        yield page
        await context.close()
    
    async def test_user_login_success(self, page: Page):
        """Test successful user login with valid credentials"""
        
        # Navigate to the login page
        await page.goto("https://the-internet.herokuapp.com/login")
        
        # Wait for the login form to be visible
        await page.wait_for_selector("#username", state="visible")
        
        # Enter username in the username field
        await page.fill("#username", "tomsmith")
        
        # Enter password in the password field
        await page.fill("#password", "SuperSecretPassword!")
        
        # Click the Login button
        await page.click("button[type='submit']")
        
        # Wait for the success message to appear
        success_message_selector = ".flash.success"
        await page.wait_for_selector(success_message_selector, state="visible")
        
        # Verify the success message is displayed
        success_message = await page.text_content(success_message_selector)
        assert "You logged into a secure area!" in success_message, \
            f"Expected success message not found. Actual message: {success_message}"
        
        # Verify the URL contains "/secure"
        current_url = page.url
        assert "/secure" in current_url, \
            f"Expected URL to contain '/secure'. Actual URL: {current_url}"
        
        # Additional verification: Check if logout button is present (indicates successful login)
        logout_button = await page.wait_for_selector("a[href='/logout']", state="visible")
        assert logout_button is not None, "Logout button should be visible after successful login"