# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:

#     browser = p.chromium.launch(headless=False)

#     page = browser.new_page()

#     page.goto("https://example.com")

#     print(page.title())

#     browser.close()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://www.google.com")

    page.fill('textarea[name="q"]', "Python tutorial")

    page.press('textarea[name="q"]', "Enter")

    page.wait_for_timeout(5000)

    browser.close()