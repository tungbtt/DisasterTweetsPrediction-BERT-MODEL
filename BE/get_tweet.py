from selenium import webdriver
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GetTweet:

    class __impl:
        def __init__(self, usr, pas) -> None:
            self.option = Options()
            self.option.add_argument("--headless")  # Chạy ở chế độ ẩn
            self.username = usr
            self.password = pas
            self.start_driver()
            self.login_twitter_account()
        

        def start_driver(self):
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.option)
            sleep(3)

        def login_twitter_account(self):
            self.driver.get("https://twitter.com/")

            # Đặt thời gian chờ tối đa là 20 giây
            wait = WebDriverWait(self.driver, 20)

            # Chờ cho phần tử "Phone, email, or username" hiển thị
            element_username = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label'
                ))
            )

            # nhập username vào ô "Phone, email, or username"
            element_username.send_keys(self.username)

            # click nút "Next"
            self.driver.find_element(
                By.XPATH, 
                '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
            ).click()

            # Chờ cho phần tử "password" hiển thị
            element_password = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label'
                ))
            )

            # nhập password vào ô "password"
            element_password.send_keys(self.password)

            # click nút "Log in"
            self.driver.find_element(
                By.XPATH, 
                '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div'
            ).click()

            # Chờ cho page loading trước khi thoát
            wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]'
                ))
            )

        def get_text_form_tweet(self, link_tweet):
            # mở page bằng link_tweet
            self.driver.get(link_tweet)

            # Đặt thời gian chờ tối đa là 20 giây
            wait = WebDriverWait(self.driver, 20)

            # Chờ cho phần tử "text" hiển thị
            element_text = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH, 
                    '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/section/div/div/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div'
                ))
            )

            # lấy text
            text = element_text.text

            return text
        
        def __del__(self):
            self.driver.quit()

        def spam(self):
            """ Test method, return singleton id """
            return id(self)

    # storage for the instance reference
    __instance = None

    def __init__(self, usr, pas):
        """ Create singleton instance """
        # Check whether we already have an instance
        if GetTweet.__instance is None:
            # Create and remember instance
            GetTweet.__instance = GetTweet.__impl(usr, pas)

        # Store instance reference as the only member in the handle
        self.__dict__['_GetTweet__instance'] = GetTweet.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    
