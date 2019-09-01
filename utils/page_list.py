class Page(object):

    def __init__(self,current_page,all_count,page=11,data_count=10):
        self.current_page = current_page
        self.all_count = all_count
        self.page = page
        self.data_count = data_count

    def start(self):
        return (self.current_page - 1) * self.data_count

    def end(self):
        return self.current_page * self.data_count

    def list(self):
        from django.utils.safestring import mark_safe
        a = []
        count, y = divmod(self.all_count, 10)
        if y:
            count += 1  # 多少页
        start_index = 1  # 起始页
        end_index = count  # 尾页
        curren_page = 11  # 设置多少页
        if count < curren_page:
            start_index = 1  # 起始页
            end_index = count  # 尾页
        else:
            start_index = self.current_page - 5
            end_index = self.current_page + 5 + 1
            if (self.current_page - 5) <= 1:
                start_index = 1
                end_index = 11 + 1
            if (self.current_page + 5) > count:
                start_index = count - 11 + 1
                end_index = count + 1

        if self.current_page == 1:
            pre = '<a class="page" href="javascript:void(0)">上一页</a>'
        else:
            pre = '<a class="page" href="/home-%s.html">上一页</a>' % (self.current_page - 1)
        a.append(pre)
        for i in range(start_index, end_index+1):
            if i == self.current_page:
                tem = '<a class="page active" href="/home-%s.html">%s</a>' % (i, i)
            else:
                tem = '<a class="page" href="/home-%s.html">%s</a>' % (i, i)
            a.append(tem)
        if self.current_page == count:
            nex = '<a class="page" href="javascript:void(0)">下一页</a>'
        else:
            nex = '<a class="page" href="/home-%s.html">下一页</a>' % (self.current_page + 1)
        a.append(nex)
        #跳页
        # jump = '''
        #         <input type="text"/><a id="jump" onclick="jumpTo(this,'/home-');">GO</a>
        #         <script>
        #             function jumpTo(ths,base){
        #                 var pos = ths.previousSibling.value;
        #                 location.href = base + pos + '.html';
        #             }
        #         </script>
        #     '''
        # a.append(jump)
        a = mark_safe("".join(a))
        return a
