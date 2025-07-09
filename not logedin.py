
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

USERNAME = "your_username"
PASSWORD = "your_password"
POST_URL = "https://www.instagram.com/p/POST_ID/"

DM_MESSAGE_FOLLOWER = "سلام! اینم لینکی که قولش رو داده بودم: https://your-link.com"
DM_MESSAGE_NONFOLLOWER = "سلام رفیق! اول منو فالو کن لطفاً تا بتونم لینکت رو بفرستم 😉"

def human_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

driver = uc.Chrome()
driver.get("https://www.instagram.com/accounts/login/")
human_sleep(5, 7)

# لاگین
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)
human_sleep(7, 10)

# رد کردن نوتیفیکیشن
try:
    driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]").click()
    human_sleep(3, 5)
except:
    pass

# رفتن به پست
driver.get(POST_URL)
human_sleep(5, 7)

# لود کردن کامنت‌ها
for _ in range(5):
    try:
        driver.find_element(By.XPATH, '//button[contains(text(),"View all")]').click()
        human_sleep(3, 5)
    except:
        break

# گرفتن کامنت‌های با عدد ۴
comments = driver.find_elements(By.XPATH, '//ul[contains(@class, "_a9ym")]/div/li')
qualified_users = []

for comment in comments:
    try:
        text = comment.find_element(By.XPATH, './/span').text.strip()
        if text == "4":
            username = comment.find_element(By.XPATH, './/h3').text.strip()
            if username not in qualified_users:
                qualified_users.append(username)
    except:
        continue

# ارسال دایرکت به کاربران واجد شرایط
sent_users = set()

for user in qualified_users:
    if user in sent_users:
        continue

    driver.get(f"https://www.instagram.com/{user}/")
    human_sleep(4, 6)

    is_follower = False
    try:
        driver.find_element(By.XPATH, '//button[contains(text(), "Following")]')
        is_follower = True
    except:
        is_follower = False

    message_to_send = DM_MESSAGE_FOLLOWER if is_follower else DM_MESSAGE_NONFOLLOWER
    print(f"{'✅' if is_follower else '⚠️'} در حال ارسال پیام به {user}...")

    try:
        driver.get("https://www.instagram.com/direct/inbox/")
        human_sleep(6, 8)

        # دکمه "ارسال پیام"
        driver.find_element(By.XPATH, '//div[contains(text(),"Send message")]').click()
        human_sleep(3, 5)

        # جستجوی یوزر
        search_box = driver.find_element(By.NAME, "queryBox")
        search_box.send_keys(user)
        human_sleep(3, 4)

        # انتخاب یوزر
        driver.find_element(By.XPATH, f'//div[text()="{user}"]').click()
        human_sleep(2, 3)

        # زدن دکمه Next
        driver.find_element(By.XPATH, '//div[text()="Next"]').click()
        human_sleep(3, 4)

        # نوشتن پیام
        text_box = driver.find_element(By.TAG_NAME, "textarea")
        text_box.send_keys(message_to_send)
        text_box.send_keys(Keys.ENTER)
        print(f"📤 پیام به {user} ارسال شد.")
        sent_users.add(user)

        human_sleep(8, 12)

    except Exception as e:
        print(f"❌ خطا در ارسال به {user}: {e}")
        continue

driver.quit()

