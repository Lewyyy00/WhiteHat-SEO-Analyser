from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class PageLoadTimerAnaylyser:
    def __init__(self):
        options = Options()
        options.add_argument("--incognito")
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service)
    
    def measure_webiste_load_time(self, url):
        start_time = time.time()
        self.driver.get(url)
        
        while self.driver.execute_script("return document.readyState") != "complete":
            time.sleep(0.1)  
   
        end_time = time.time()
        load_time = end_time - start_time
        return load_time
    
    def open_page(self, url):
        self.driver.get(url)
        time.sleep(5)

    def is_each_file_loaded(self, url):
        logs = self.driver.get_log("performance")
        loaded = True

        for log in logs:
            message = log['message']
            if "Network.responseReceived" in message:
                if '"status":404' in message or '"status":500' in message:
                    loaded = False
                    print ('not loaded file')
                    break
        
        return loaded

    def close_browser(self):
        self.driver.quit()


if __name__ == "__main__":
    timer = PageLoadTimerAnaylyser()
    url = 'https://www.screamingfrog.co.uk/seo-spider/user-guide/tabs/#pagespeed'
    """load_time = timer.is_each_file_loaded(url)
    print(f"time needed to load the webiste: {load_time:.2f} sec")
    timer.close_browser()"""

    
    timer.open_page(url)
    timer.close_browser()