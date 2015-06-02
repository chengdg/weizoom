# -*- coding: utf-8 -*-

from core import paginator
from weixin2 import export
from core import resource
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.MESSAGE_FIRST_NAV

class MessageSearch(resource.Resource):
    """
    消息搜索
    """
    app = 'new_weixin'
    resource = 'message_search'

    def api_get(request):
        """
        搜索消息
        """
        assert 'start_at' in request.GET
        assert 'end_at' in request.GET

        searched_messages = [{
            "id": 1,
            "name": "樱桃小丸子",
            "text": "这是一条微信消息。这是一条微信消息。这是一条微信消息。这是一条微信消息。这是一条微信消息。",
            "created_at": "2015-04-15 10:11:12",
            "is_starred": False,
            "is_received": True, # True表示是收到的消息
            "memo": "这是备注信息。"
        }, {
            "id": 2,
            "name": "米琦尔",
            "text": "【自动回复】感谢购买米琦尔大米！",
            "created_at": "2015-04-15 10:11:12",
            "is_starred": False,
            "is_received": False, # True表示是收到的消息
            "memo": "这是备注信息。这是由微信公众号发出的信息。"
        }]

        # 复用realtime_messages页面
        count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
        cur_page = int(request.GET.get('page', '1'))
        pageinfo, searched_messages = paginator.paginate(searched_messages, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
        response = create_response(200)
        response.data = {
            'items': searched_messages,
            'pageinfo': paginator.to_dict(pageinfo),
            'sortAttr': '-id',
            'data': {}
        }
        return response.get_response()
