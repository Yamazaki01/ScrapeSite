
import re
from html import unescape
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import ssl

# coding:utf-8

def scraping(target_url, headers, wait_sec, re_str):
    headers = headers_format_recreate(headers)
    # temp_headers ={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
    req = Request(url=target_url, headers=headers)
    # ssl._create_default_https_context = ssl._create_unverified_context
    try:
        f = urlopen(req)
    except HTTPError as e:
        error = 'The Sever could''t fulfill the request.\r\nError cod:', e.code
        return error
    except URLError as e:
        error = 'We faild to reach a server.\r\nReason:', e.code
        return error
    else:
        encoding = f.info().get_content_charset(failobj="utf-8")
        html = f.read().decode(encoding)
    # re.fideall()を使って、書籍1冊に相当する部分のHTMLを取得する
    # *?は*と同様だが、なるべく短い文字列にマッチする(non-greedyである)ことをあらわすメタ文字。
    validate_results = []
    for partial_html in re.findall(re_str, html, re.DOTALL):
        # 書籍のURLは、itemprop="url" という属性をもつa要素のhref属性から取得する
        #url = re.serch(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        #url = 'https://gihyo.jp' + url  # / で始まっているのでドメイン名などを追加する
        # item_url = re.search(r'<a itemprop="url" href="(.*?)">', partial_html).group(1)
        # item_url = url + item_url
        #
        # # 書籍のタイトルは、improp="name"　という属性を持つp要素から取得する
        # # item_title = re.search('<p itemprop="name".*?</p>', partial_html).group(0)
        # item_title = item_title.replace('<br/>', ' ') # <br/>タグをスペースに置き換える。str.replace()は文字列を置換する
        # item_title= re.sub(r'<.*?>', '', item_title) # タグを取り除く
        # item_title = unescape(item_title)
        validate_results.append(partial_html)
        print(partial_html)
    if len(validate_results) == 0:
        validate_results = ['No mache!']
        return validate_results
    return validate_results
def headers_format_recreate(headers):
    re_split_str = re.split(r',', re.sub((r'\r\n|:'), r',', headers))
    key = []
    val = []
    for i, v in enumerate(re_split_str):
        ++i
        if i % 2:
            val.append(v)
        else:
            key.append(v)

    headers_dic = {}
    for k, v in zip(key, val):
        headers_dic[k] = v

    return headers_dic