# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource

import models as app_models
import export

FIRST_NAV = 'apps'
COUNT_PER_PAGE = 20

class voteStatistic(resource.Resource):
	app = 'apps/vote'
	resource = 'vote_statistic'
	
	@login_required
	def get(request):
		"""
		响应GET
		"""
		if 'id' in request.GET:
			all_participances = app_models.voteParticipance.objects(belong_to=request.GET['id'])
			total_count = all_participances.count()
			titles_list = []
			title2itemCount = {}
			title_valid_dict = {}
			for p in all_participances:
				for title, data in p.termite_data.items():
					if data['type'] == 'appkit.selection':
						is_valid = False
						for item, value in data['value'].items():
							if value['isSelect']:
								is_valid = True
							if title2itemCount.has_key(title):
								if title2itemCount[title].has_key(item):
									title2itemCount[title][item] += 1 if value['isSelect'] else 0
								else:
									title2itemCount[title][item] = 1 if value['isSelect'] else 0
							else:
								title2itemCount[title] = {}
								title2itemCount[title][item] = 1 if value['isSelect'] else 0
						if is_valid:
							if title_valid_dict.has_key(title):
								title_valid_dict[title] += 1
							else:
								title_valid_dict[title] = 1

			for title, title_value in reversed(title2itemCount.items()):
				single_title_dict = {}
				single_title_dict['title_name'] = title
				single_title_dict['title_valid_count'] = title_valid_dict[title]
				single_title_dict['title_value'] = []
				for item, item_value in title_value.items():
					single_item_value = {}
					single_item_value['item_name'] = item
					single_item_value['counter'] = item_value
					single_item_value['percent'] = '%d%s' % (item_value / float(title_valid_dict[title]) * 100, '%')
					single_title_dict['title_value'].append(single_item_value)

				titles_list.append(single_title_dict)

			project_id = 'new_app:vote:%s' % request.GET.get('related_page_id', 0)
		else:
			total_count = 0
			titles_list = None
			project_id = 'new_app:vote:0'
		
		c = RequestContext(request, {
			'first_nav_name': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav_name': 'votes',
			'titles': titles_list,
			'total_count': total_count,
			'project_id': project_id,
		})
		
		return render_to_response('vote/templates/editor/vote_statistic.html', c)