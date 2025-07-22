import csv
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep
from lxml import etree


def main(url):
    driver.get(url)
    res = driver.page_source
    tree = etree.HTML(res)
    title = tree.xpath('//h1/text()')[0].strip()
    user = tree.xpath('//div[@class="post_info"]/a/text()')[0]
    date = tree.xpath('//div[@class="post_info"]/text()')[0].strip().replace('鏉ユ簮:', '')
    html = etree.tostring(tree.xpath('//div[@class="post_body"]')[0]).decode('utf-8')
    content = '\n'.join([i.strip() for i in tree.xpath('//div[@class="post_body"]//text()') if i.strip()])
    img = '\n'.join(tree.xpath('//div[@class="post_body"]//img/@src'))
    data = [tag, url, title, user, date, html, content, img]
    print(date, '\t', title)
    csv.writer(open('data.csv', 'a', encoding='utf-8-sig', newline='')).writerow(data)


if __name__ == '__main__':
    tag = 'www.163.com'
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=options)
    js = open('stealth.min.js').read()
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': js})
    driver.execute_script('window.open();')
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    rows = open('urls.txt', encoding='utf-8').readlines()
    for row in rows:
        if 'https://www.163.com/dy/article/' in row:
            try:
                main(row.strip())
                sleep(5)
            except Exception as e:
                print('error:', e)
    driver.quit()
