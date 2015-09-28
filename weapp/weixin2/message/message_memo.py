# -*- coding: utf-8 -*-


from weixin2 import export
from core import resource
from core.jsonresponse import create_response

COUNT_PER_PAGE = 20
FIRST_NAV = export.WEIXIN_HOME_FIRST_NAV

class MessageMemo(resource.Resource):
    """
    表示消息加星标的状态
    """
    app = 'new_weixin'
    resource = 'message_memo'

    def api_get(request):
        return create_response(200).get_response()

    def api_post(request):
        """
        更新消息的备注信息
        """
        #print("POST: {}".format(request.POST))
        assert 'msg_id' in request.POST
        assert 'text' in request.POST
        #print(request.POST['fans_id'])

        return create_response(200).get_response()
