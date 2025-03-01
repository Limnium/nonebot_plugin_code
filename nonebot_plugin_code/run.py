# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 14:17
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : run.py
# @Software: PyCharm

# @Time    : 2023/01/23 17:00
# @UpdateBy: Limnium

import re
import httpx

codeType = {
    'py': ['python', 'py'],
    'cpp': ['cpp', 'cpp'],
    'java': ['java', 'java'],
    'php': ['php', 'php'],
    'js': ['javascript', 'js'],
    'c': ['c', 'c'],
    'cs': ['csharp', 'cs'],
    'go': ['go', 'go'],
    'asm': ['assembly', 'asm']
}


async def run(strcode):
    strcode = strcode.replace('&amp;', '&').replace('&#91;', '[').replace('&#93;', ']')
    try:
        # 'c#'似乎不能匹配到，改成'cs'就没问题了，先这样吧
        a = re.match(r'(py|php|java|cpp|js|cs|c|go|asm)\b ?(.*)\n((?:.|\n)+)', strcode)
        lang, stdin, code = a.group(1), a.group(2).replace(' ','\n'), a.group(3)
    except:
        return "输入有误，目前仅支持c/cpp/cs/py/php/go/java/js"
    dataJson = {
        "files": [
            {
                "name": f"main.{codeType[lang][1]}",
                "content": code
            }
        ],
        "stdin": stdin,
        "command": ""
    }
    headers = {"Authorization": "Token 0123456-789a-bcde-f012-3456789abcde",
               "content-type": "application/"}
    async with httpx.AsyncClient() as client:
        res = await client.post(url=f'https://glot.io/run/{codeType[lang][0]}?version=latest', headers=headers, json=dataJson)
    if res.status_code == 200:
        res = res.json()
        res = res['stdout']+('\n---\n'+res['stderr'] if res['stderr'] else '')
        return (res if res else '无输出或报错！')
    else:
        return '响应异常'
