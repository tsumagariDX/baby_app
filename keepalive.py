from playwright.sync_api import sync_playwright

URL = "https://babyapp-jtbow68yqwfehs54qdbhzk.streamlit.app/"

def wake_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, timeout=60000)
        page.wait_for_timeout(5000)

        try:
            button = page.get_by_text("get this app back up")
            if button.is_visible():
                button.click()
                page.wait_for_timeout(10000)
                print("アプリを起こしました")
            else:
                print("アプリは起きています")
        except Exception:
            print("アプリは起きています")

        browser.close()

if __name__ == "__main__":
    wake_app()