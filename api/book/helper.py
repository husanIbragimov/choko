from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
from datetime import datetime
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        if self.request.query_params.get('page_size'):
            page_size = self.request.query_params.get('page_size')
        else:
            page_size = 10
        return Response(OrderedDict([
            ('server_time', datetime.now()),
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('page', self.page.number),
            ('page_size', int(page_size)),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
