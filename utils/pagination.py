# Author: 73

from django.utils.safestring import mark_safe

class Page:
    def __init__(self, current_page, all_count, per_page_count=20, total_html_count=9):
        self.current_page = current_page
        self.all_count = all_count
        self.per_page_count = per_page_count
        self.total_html_count = total_html_count

    @property
    def total_page_count(self):
        x, y = divmod(self.all_count, self.per_page_count)  # 商和余数
        if y:
            x += 1
        print(x)
        return x
    @property
    def start(self):
        start = (self.current_page - 1) * self.per_page_count
        return start
    @property
    def end(self):
        end = self.current_page * self.per_page_count
        return end

    def page_str(self):
        if self.total_page_count < self.total_html_count:  # 总页数<能显示的页数
            start_index = 1
            end_index = self.total_page_count + 1
        else:
            if self.current_page <= (self.total_html_count + 1) / 2:  # 当前页<=能显示的页数+1的一半
                start_index = 1
                end_index = self.total_html_count + 1
            else:
                if self.current_page + (self.total_html_count - 1) / 2 > self.total_page_count:  # 当前页+能显示的页数-1的一半 > 总页数
                    start_index = self.total_page_count - self.total_html_count + 1
                    end_index = self.total_page_count + 1
                else:
                    start_index = self.current_page - (self.total_html_count - 1) / 2
                    end_index = self.current_page + (self.total_html_count + 1) / 2
        print(start_index, end_index)

        page_list = []
        if self.current_page - 1 < 1:
            prev = "<a class='page' href='/usr_list/?p=1'>上一页</a>"
        else:
            prev = "<a class='page' href='/usr_list/?p=%s'>上一页</a>" % str(self.current_page - 1)
        page_list.append(prev)
        for i in range(int(start_index), int(end_index)):
            if self.current_page == i:
                temp = "<a class='page active' href='/usr_list/?p=%s'>%s</a>" % (i, i)
            else:
                temp = "<a class='page' href='/usr_list/?p=%s'>%s</a>" % (i, i)
            page_list.append(temp)

        if self.current_page + 1 > self.total_page_count:
            nex = "<a class='page' href='/usr_list/?p=%s'>下一页</a>" % self.total_page_count
        else:
            nex = "<a class='page' href='/usr_list/?p=%s'>下一页</a>" % str(self.current_page + 1)
        page_list.append(nex)

        jump = """<input type='text' /> <a onclick="jumpTo(this, '/usr_list/?p=');">Go</a>
                    <script>
                        function jumpTo(ths, base){
                            var val = ths.previousElementSibling.value;
                            location.href = base + val;
                        }
                    </script>
            """
        page_list.append(jump)
        page_str = "".join(page_list)
        page_str = mark_safe(page_str)

        return page_str