import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd
import json
import threading
df = pd.read_csv("docs/assignment/furniture stores pages.csv")

if True:
    def saver(idx_str, status, text_json:str):
        with open(f"data/crawled_texts/idx_{idx_str}_s_{status}.json", 'wt+') as f:
            f.write(text_json)
    
    def helper(link_to_page, idx_str):
        attempts = 10
        while attempts >0:
            try:
                chrome_options = webdriver.ChromeOptions()
                prefs = {"profile.managed_default_content_settings.images": 2, 'profile.managed_default_content_settings.javascript': 2}                
                chrome_options.add_experimental_option("prefs", prefs)
                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
                driver.set_page_load_timeout(20)
                try:
                    driver.get(link_to_page)
                    try:
                        main = driver.find_element(By.XPATH, "//main")
                    except Exception as e:
                        main = driver.find_element(By.XPATH, "//body")
                    
                    result_str = main.text
                    result_json = {link_to_page:result_str}
                    result_json["status"] = 0
                    if len(result_str) > 0 and not ("404" in result_str or "403" in result_str):
                        result_json["status"] = 1
                    saver(idx_str, result_json["status"], json.dumps(result_json))
                except Exception as e:
                    print(39, e)
                    pass
                break
            except Exception as e:
                print("42", e)
                time.sleep(1)
                attempts -=1
    indexes = list(range(len(df)))
    for idx in range(len(indexes)//5):
        partial_df = df.iloc[idx*5:(idx+1)*5]
        ts = []
        for i in range(len(partial_df)):            
            link_to_page = partial_df.iloc[i].values[0]
            t = threading.Thread(target=helper, args=[link_to_page, f"{idx}_{i}"])
            t.start()
            ts.append(t)
            
            print(f"idx={idx}", link_to_page)
            if(len(ts) > 5):
                break
        for t in ts:
            t.join()
        print()

else:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_page_load_timeout(20)
    driver.get("https://dunlin.com.au/products/beadlight-cirrus")
    # driver.maximize_window()

    headers = driver.find_element(By.XPATH, "//body")
    import pdb;pdb.set_trace()
