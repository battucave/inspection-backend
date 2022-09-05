from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination 
from rest_framework.response import Response





class CustomSuccessPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        datum = OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])
        return Response({"success":True,"error":False,"msg":"","data":datum})
