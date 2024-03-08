from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import Entry, Label, Button, StringVar, Toplevel
from selenium.common.exceptions import NoSuchElementException
import tkinter.messagebox as msgbox
import time
# 設置 browser driver 路徑
from webdriver_manager.chrome import ChromeDriverManager
class DataInput:
    def __init__(self, root):
        self.root = root
        self.root.title('Zuvio 登錄')

        # 帳號
        Label(root, text='帳號:').grid(row=0, column=0, padx=10, pady=10)
        self.username_var = StringVar()
        Entry(root, textvariable=self.username_var).grid(row=0, column=1, padx=10, pady=10)

        # 密碼
        Label(root, text='密碼:').grid(row=1, column=0, padx=10, pady=10)
        self.password_var = StringVar()
        Entry(root, textvariable=self.password_var, show='*').grid(row=1, column=1, padx=10, pady=10)

        # 課程ID
        Label(root, text='課程名稱:').grid(row=2, column=0, padx=10, pady=10)
        self.course_id_var = StringVar()
        Entry(root, textvariable=self.course_id_var).grid(row=2, column=1, padx=10, pady=10)

        # 提交按鈕
        Button(root, text='提交', command=self.submit).grid(row=3, column=0, columnspan=2, pady=20)

    def submit(self):
        self.username = self.username_var.get()
        self.password = self.password_var.get()
        self.course_id = self.course_id_var.get()
        self.root.destroy()


root = tk.Tk()
data_input = DataInput(root)
root.mainloop()
# 設置模擬的經緯度
latitude = 25.04336
longitude = 121.5338
#設置帳號密碼
account=data_input.username
password=data_input.password
course_name_to_search = data_input.course_id
#print(account)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.geolocation": 1,  # 允許地理位置訪問
    "profile.default_content_settings.popups": 0
})
chrome_options.add_argument("--disable-notifications")  # 禁止彈出式通知

# 使用設置的選項啟動瀏覽器
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# 使用 execute_script 方法設置地理位置
browser.execute_cdp_cmd("Emulation.setGeolocationOverride", {
    "latitude": latitude,
    "longitude": longitude,
    "accuracy": 100  # 設置精確度
})
#print(account)

# 打開 Zuvio 登錄頁面
browser.get('https://irs.zuvio.com.tw/irs/login')
username_elem = browser.find_element(By.ID, 'email')
# 填入您的帳號和密碼
username_elem.send_keys(account)
password_elem = browser.find_element(By.ID, 'password')
password_elem.send_keys(password)

# 按下登錄按鈕
login_btn = browser.find_element(By.ID,'login-btn')
login_btn.click()
    
try:
    course_element = browser.find_element(By.XPATH, f'//div[@class="i-m-p-c-a-c-l-c-b-t-course-name" and text()="{course_name_to_search}"]')
except NoSuchElementException:
    msgbox.showerror("錯誤","帳號或密碼錯誤，或者找不到該課程名稱。")
    browser.quit()

# JavaScript 代碼來獲取經緯度並輸出到 console
'''
javascript_code = """
navigator.geolocation.getCurrentPosition(function(position) {
    console.log('Latitude:', position.coords.latitude);
    console.log('Longitude:', position.coords.longitude);
});
"""

# 使用 Selenium 執行 JavaScript
browser.execute_script(javascript_code)
'''
course_id = course_element.get_attribute('data-course-id')
course_elem = browser.find_element(By.XPATH, f'//div[@data-course-id="{course_id}"]')
course_elem.click()

# 嘗試找到 "點名簽到" 的按鈕
rollcall_button = browser.find_element(By.XPATH, '//div[@data-type="rollcall"]')

# 點擊該按鈕
rollcall_button.click()

# 嘗試找到 "我到了" 的按鈕
try:
    arrived_button = browser.find_element(By.ID, 'submit-make-rollcall')
except NoSuchElementException:
    msgbox.showerror("錯誤","目前未開放簽到")
    browser.quit()

# 點擊該按鈕
arrived_button.click()
# 若需要，保持瀏覽器打開，否則直接關閉瀏覽器
time.sleep(10)
browser.quit()
