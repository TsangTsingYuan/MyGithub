'''
#简单用例
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
#打开URL
driver.get("http://www.python.org")
assert "Python" in driver.title
#查询页面中的元素
elem = driver.find_element_by_name("q")
#清除input输入框中的任何预填充的文本
elem.clear()
#输入关键字  特殊的按键可以使用Keys类来输入
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

assert "No results found." not in driver.page_source
driver.close()
'''


#测试用例
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()