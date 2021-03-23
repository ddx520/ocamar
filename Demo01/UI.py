from selenium import webdriver

driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 设置超时时间
driver.maximize_window()  # 窗口最大化显示

driver.get("http://www.baidu.com/")

search_field = driver.find_element_by_id("kw")  # 找到输入框
search_field.clear()  # 清空当前输入内容

search_field.send_keys("铜钱贯")  # 重新这是搜索关键字
search_field.submit()  # 提交进行搜索

products = driver.find_elements_by_xpath("//div[contains(@class, 'c-abstract')]")

print("Found " + str(len(products)) + "products:")

for product in products:
    print(product.text)


# driver.quit()