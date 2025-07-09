import time
import random
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

# آدرس پروفایل کروم شما
user_data_dir = r"C:\\Users\\Ariasb\\AppData\\Local\\Google\\Chrome\\User Data"
profile_dir = "Default"

POST_URL = "https://www.instagram.com/p/POST_ID/"
DM_MESSAGE_FOLLOWER = "سلام! اینم لینکی که قولش رو داده بودم: https://your-link.com"
DM_MESSAGE_NONFOLLOWER = "سلام رفیق! اول منو فالو کن لطفاً تا بتونم لینکت رو بفرستم 😉"
SENT_USERS_FILE = "sent_users.csv"

def human_sleep(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

def load_sent_users(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, newline='', encoding='utf-8') as f:
        return set(row[0] for row in csv.reader(f))

def save_sent_user(file_path, username):
    with open(file_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([username])

# کروم با پروفایل شخصی
options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile_dir}")

driver = uc.Chrome(options=options)

# شروع
driver.get("https://www.instagram.com/")
human_sleep(5, 7)

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

# لود کاربران قبلاً ارسال‌شده
sent_users = load_sent_users(SENT_USERS_FILE)

# ارسال دایرکت به کاربران واجد شرایط
for user in qualified_users:
    if user in sent_users:
        print(f"⏩ کاربر {user} قبلاً پیام دریافت کرده، رد شد.")
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

        # دکمه ارسال پیام (تغییر بده اگر زبان مرورگر فارسیه)
        driver.find_element(By.XPATH, '//div[contains(text(),"Send message")]').click()
        human_sleep(3, 5)

        # جستجوی یوزر
        search_box = driver.find_element(By.NAME, "queryBox")
        search_box.send_keys(user)
        human_sleep(3, 4)

        # انتخاب یوزر
        driver.find_element(By.XPATH, f'//div[text()="{user}"]').click()
        human_sleep(2, 3)

        # دکمه Next
        driver.find_element(By.XPATH, '//div[text()="Next"]').click()
        human_sleep(3, 4)

        # نوشتن پیام
        text_box = driver.find_element(By.TAG_NAME, "textarea")
        text_box.send_keys(message_to_send)
        text_box.send_keys(Keys.ENTER)
        print(f"📤 پیام به {user} ارسال شد.")
        save_sent_user(SENT_USERS_FILE, user)
        human_sleep(15, 25)  # فاصله بین پیام‌ها برای امنیت

    except Exception as e:
        print(f"❌ خطا در ارسال به {user}: {e}")
        continue

driver.quit()
