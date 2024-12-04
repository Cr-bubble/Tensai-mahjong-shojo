from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # 測試 WebDriver 初始化
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://game.maj-soul.com")
    time.sleep(10)  # 等待頁面完全加載
    print("Game page loaded successfully.")

    driver.quit()
except Exception as e:
    print(f"An error occurred: {e}")