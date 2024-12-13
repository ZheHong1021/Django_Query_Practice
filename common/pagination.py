from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


# 建立自訂的分頁器 (繼承 PageNumberPagination)
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30 # 每頁顯示的數量 (預設值: 30)
    page_size_query_param = 'page_size' # 允許客戶端通過該參數自定義每頁大小 (page_size=10: 代表每頁10筆資料)
    max_page_size = 200 # 可以限制每頁最大顯示的數量 (預設值: 200)

    def paginate_queryset(self, queryset, request, view=None):
        # 找尋 request.query_params中有無帶入 page_size 參數 (如果沒有就使用預設值)
        page_size = request.query_params.get(self.page_size_query_param, self.page_size)
    
        if page_size == "-1": # 如果有帶且又是給 "-1" => 代表一頁帶入全部數據
            self.page_size = len(queryset) # 將 page_size 設定為 queryset 的長度
        else: # 如果有帶且不是給 "-1" => 代表客戶端有自定義每頁顯示的數量
            self.page_size = int(page_size)
        return super().paginate_queryset(queryset, request, view)
    
    def get_paginated_response(self, data):
        return Response({
            # 下一頁的頁數
            'next': self.page.next_page_number() if self.page.has_next() else None,

            # 上一頁的頁數
            'previous': self.page.previous_page_number() if self.page.has_previous() else None,

            # 總共的數量
            'count': self.page.paginator.count,

            # 總頁數
            'total_pages': self.page.paginator.num_pages,

            # 當前頁數的資料
            'data': data,

            # 當前頁碼
            'page': self.page.number,
        })