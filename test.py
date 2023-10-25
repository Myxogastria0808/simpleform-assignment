from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.wise-agent.com/database/")
    page.get_by_role("link", name="【IN GROUPE】高林イツキに関する情報提供").nth(1).click()
    page.get_by_text("情報商材 2021.04.08 【IN GROUPE】高林イツキに関する情報提供 詐欺種別 情報商材 名称等 IN GROUPE LUC888&evolutio").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
