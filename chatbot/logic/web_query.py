# pip install selenium
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("https://www.mayoclinic.org/diseases-conditions/migraine/symptoms-causes/syc-20360201")
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
desc = soup.find("div", class_="css-0 e1oc5a60")
print(desc.get_text() if desc else "Không tìm thấy.")
driver.quit()
