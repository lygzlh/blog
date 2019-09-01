from bs4 import BeautifulSoup

def filter(content):
    soup = BeautifulSoup(content,'html.parser')

    # tem = {
    #     'ul':['id','class'],
    #     'p':['id','class'],
    #     'div':['id','class'],
    #     'span':['id','class'],
    # }
    tem = ['script']  #过滤tem中的标签
    for tag in soup.find_all():
        if tag.name not in tem:
            pass
        else:
            tag.clear()
            tag.hidden = True
            continue
        #过滤属性
        # input_attr = tag.attrs
        # vail_attr = tem[tag.name]
        # for k in list(input_attr.keys()):
        #     if k in vail_attr:
        #         pass
        #     else:
        #         del tag.attrs[k]
    content = soup.decode()
    return content
