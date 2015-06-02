#coding=utf-8
#合并原模版r6865
#1.module=mall > module=apps:weshop:mall
#2.products.html 中 修改商品链接
#	./?webapp_owner_id={{request.webapp_owner_id}}&module=apps:weshop:mall&model=product&resource=product&action=get&workspace_id=apps:&rid={{product.id}}
#2.去支付 > 微众卡支付
