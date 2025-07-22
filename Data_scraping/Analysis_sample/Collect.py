# 微博搜索

import requests
from lxml import etree
import time
from urllib import parse
import pandas as pd


def collect(k):
    resLs = []
    for page in range(10):
        time.sleep(2)
        page += 1
        url = f'https://s.weibo.com/weibo?q={parse.quote(k)}&xsort=hot&suball=1&Refer=g&page={page}'
        print(url)
        print(k, page)
        headers = {
            'Cookie': ck,
            'User-Agent': ua,
            'Referer': url
        }
        while True:
            try:
                res = requests.get(url=url, headers=headers, timeout=(5, 5)).content.decode('utf-8', errors='ignore')
                break
            except:
                time.sleep(2)
        if f'<p>抱歉，未找到“{k}”相关结果。</p>' in res:
            break
        tree = etree.HTML(res)
        for li in tree.xpath('//div[@action-type="feed_list_item"]'):
            name = li.xpath('.//a[@class="name"]/text()')[0]
            date = li.xpath('.//div[@class="from"]/a/text()')[0].strip()
            cbox = li.xpath('.//p[@node-type="feed_list_content_full"]')
            cbox = li.xpath('.//p[@node-type="feed_list_content"]')[0] if not cbox else cbox[0]
            cont = '\n'.join(cbox.xpath('./text()')).strip()
            tran = li.xpath('.//div[@class="card-act"]/ul/li[1]/a//text()')[1].strip()
            try:
                tran = eval(tran)
            except:
                tran = 0
            comm = li.xpath('.//div[@class="card-act"]/ul/li[2]/a//text()')[0].strip()
            try:
                comm = eval(comm)
            except:
                comm = 0
            like = li.xpath('.//div[@class="card-act"]//span[@class="woo-like-count"]/text()')[0].strip()
            try:
                like = eval(like)
            except:
                like = 0
            ID = li.xpath('./@mid')[0]
            dic = {
                '昵称': name,
                '时间': date,
                '内容': cont,
                '转发': tran,
                '评论': comm,
                '点赞': like,
                '链接': f'https://m.weibo.cn/detail/{ID}',
                'ID': ID
            }
            resLs.append(dic)
            print(dic)
        df = pd.DataFrame(resLs)
        df.to_excel('微博搜索1.xlsx', index=False)


if __name__ == '__main__':
    ck = 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWuN-OnmkaCviarbyST164z5JpX5KzhUgL.Fo-NS0Bfeo.NS0M2dJLoIpHKIsHEdsvoIEHhebHFSXpfqcLJ9Pzt;SCF=ApguU9iL0n9QTEr9aFTbqLa4YgEzacVQQpnvu51_2nWpnQyIm1hl1AbjcCwsVfDEqZYAKy9WGRZ8pssTrq-ZMHQ.;_s_tentry=passport.weibo.com;SUB=_2A25FB83WDeRhGeNJ7FYU8ifLzDuIHXVmfU8erDV8PUNbmtANLRihkW9NS7EPhg3VElUmUMg8rT6gXcOy5i1zIwTR;Apache=7159674714967.061.1745075592844;ALF=02_1747667590;SINAGLOBAL=7159674714967.061.1745075592844;ULV=1745075592845:1:1:1:7159674714967.061.1745075592844:'
    ua = 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/91.0.4472.106Safari/537.36'
    collect('特朗普关税')
