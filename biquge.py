import requests
import parsel 
import sys
import io
from tqdm import tqdm
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
 
def get_response(html_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(url=html_url, headers=headers)
    if response.status_code != 200: 
        return get_response(html_url)
    response.encoding = response.apparent_encoding 
    return response
 
 
def save(novel_name, title, content):
    """
    保存小说
    :param title: 小说章节标题
    :param content: 小说内容
    :return:
    """
    filename = f'{novel_name}' + '.txt'
    # 一定要记得加后缀 .txt  mode 保存方式 a 是追加保存  encoding 保存编码
    with open(filename, mode='a', encoding='utf-8') as f:
        # 写入标题
        if title:
            f.write(title)
        # 换行
        f.write('\n')
        # 写入小说内容
        f.write(content)
 
 
def get_one_novel(name, novel_url):
    novel_url = 'https://www.22biqu.com'+ novel_url
    # 调用请求网页数据函数
    response = get_response(novel_url)
    # 转行成selector解析对象
    selector = parsel.Selector(response.text)
    # 获取小说标题
    title = selector.css('.reader-main h1::text').get()
    # 获取小说内容 返回的是list
    content_list = selector.css('.content p::text').getall()
    print(content_list, flush=True)
    # ''.join(列表) 把列表转换成字符串
    content_str = ''.join(content_list)
    next_text = selector.css('#next_url::text').get()
    print(next_text, flush=True)
    next_url = selector.css('#next_url::attr(href)').get()
    print(next_url, flush=True)
    if next_text == '没有了': 
        next_url = ''
    save(name, title, content_str) 
    if next_url != '':
        get_one_novel(name, next_url)
    else:
        print('小说下载完成')
        exit()
    

 
def get_all_url(html_url):
    # 调用请求网页数据函数
    response = get_response(html_url)
    # 转行成selector解析对象
    selector = parsel.Selector(response.text)
    # 所有的url地址都在 a 标签里面的 href 属性中
    dds = selector.css('#list dd a::attr(href)').getall() 
    # 小说名字
    novel_name = selector.css('#info h1::text').get()
    for dd in tqdm(dds):
        novel_url = 'https://www.ddyueshu.com/' + dd
        get_one_novel(novel_name, novel_url)
 
 
if __name__ == '__main__': 
    url = f'https://www.ddyueshu.com/0_62/'
    #get_all_url(url)
    get_one_novel('庆余年','/biqu16899/14705862.html')
