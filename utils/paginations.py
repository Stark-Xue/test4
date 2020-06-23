from django.utils.safestring import mark_safe

class Page:
    def __init__(self, current_page, all_count, per_page_count=10, xsys=5):
        self.current_page = current_page
        self.all_count = all_count
        self.per_page_count = per_page_count
        self.xsys = xsys

    def start(self):
        return (self.current_page - 1)*self.per_page_count

    def end(self):
        return self.current_page*self.per_page_count

    @property
    def total_count(self):
        #all_count = len(LIST)
        # way1
        '''if all_count%10 == 0:
            page_num = all_count//10
        else:
            page_num = all_count//10+1'''

        # way2
        v, y = divmod(self.all_count, self.per_page_count) # 计算结果商和余数
        if y:
            v += 1

        print(v)
        return v

    def page_str(self, base_url):
        page_list = []
        if self.total_count<=self.xsys:
            start_index = 1
            end_index = self.total_count
        else:
            if self.current_page <=(self.xsys-1)/2:
                start_index = 1
                end_index = self.xsys+1
            elif self.current_page >=self.total_count-(self.xsys-1)/2:
                start_index = self.total_count-(self.xsys-1)
                end_index = self.total_count+1
            else:
                start_index = self.current_page - (self.xsys-1)/2
                end_index = self.current_page + (self.xsys-1)/2 + 1
        if self.current_page == 1:
            prev_page = '<a class="page" href="javascript:void(0);">上一页</a>'
        else:
            prev_page = '<a class="page" href="http://127.0.0.1:8000%s?p=%s">上一页</a>' % (base_url, self.current_page-1)
        page_list.append(prev_page)
        for i in range(int(start_index),int(end_index)):
            if i == self.current_page:
                temp = '<a class="page active" href="http://127.0.0.1:8000%s?p=%s">%s</a>' % (base_url,i,i)
            else:
                temp = '<a class="page" href="http://127.0.0.1:8000%s?p=%s">%s</a>' % (base_url,i,i)
            page_list.append(temp)
        if self.current_page == self.total_count:
            next_page = '<a class="page" href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a class="page" href="http://127.0.0.1:8000%s?p=%s">下一页</a>' % (base_url,self.current_page+1)
        page_list.append(next_page)

        jump = """
            <input type='text' /><a onclick='jumpTo(this, "%s?p=");' id='ii1'>go</a>
            <script>
                function jumpTo(ths, base){
                    var val = ths.previousSibling.value;
                    location.href = base+val;
                }
            </script>
            """ % (base_url,)
        page_list.append(jump)
        """page_msg = '''
                <a href="http://127.0.0.1:8000/user_list/?p=1">1</a>
                <a href="http://127.0.0.1:8000/user_list/?p=2">2</a>
                <a href="http://127.0.0.1:8000/user_list/?p=3">3</a>
                '''"""
        page_msg = "".join(page_list)

        page_msg = mark_safe(page_msg)
        return page_msg