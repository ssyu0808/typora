import time
import requests
import sys
import base64
import os
import uuid
#{update.py} ${filename}
from urllib import parse


def file2base64(abspath) -> str:
    content = open(abspath, 'rb').read()
    if content:
        return base64.b64encode(content).decode(encoding='utf8')
    return None


def upload2github(path, abspath):
    content = file2base64(abspath)
    if content == None:
        return None
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": "token [token]"}
    data = {"message": "Typora auto update @ {0:0>4}-{1:0>2}-{2:0>2} {3:0>2}:{4:0>2}:{5:0>2}".format(*(time.localtime())),
            "content": content}
    user = "ssyu0808"
    repo = "typora"
    path = parse.quote("images/"+path, encoding='utf8')
    file = str(uuid.uuid4()).replace('-', '')+'.'+abspath.split('.')[-1]
    response = requests.put(f"https://api.github.com/repos/{user}/{repo}/contents/{path}/{file}",
                            headers=headers,
                            json=data)
    if response.status_code == 201:
        return f"https://cdn.jsdelivr.net/gh/{user}/{repo}@main/{path}/{file}"
    else:
        return None
    # print(response.status_code)


if __name__ == '__main__':
    path = sys.argv[1]
    imgs = sys.argv[2:]
    outline = []
    for img in imgs:
        result = upload2github(path, img)
        if result:
            outline.append(result)
        else:
            exit()
    print('\n'.join(outline))
