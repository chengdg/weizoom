# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from core import paginator
import json

from models import *

QUESTION_NAV_NAME = 'marketing_tool'

COUNT_PER_PAGE = 20

def list_tools(request):
	c = RequestContext(request, {
		'nav_name': QUESTION_NAV_NAME,
	})
	return render_to_response('question/list_tools.html', c)


########################################################################
# list_questions: 显示问答列表
########################################################################
@login_required
def list_questions(request):
	#获取当前页数
	cur_page = int(request.GET.get('page', '1'))
	#获取每页个数
	count = int(request.GET.get('count', COUNT_PER_PAGE))

	questions = QuestionInfo.objects.filter(owner=request.user,is_deleted=False).order_by('-created_at')
	pageinfo, questions = paginator.paginate(questions, cur_page, count, query_string=request.META['QUERY_STRING'])

	c = RequestContext(request, {
		'nav_name': QUESTION_NAV_NAME,
		'questions': questions,
		'pageinfo': json.dumps(paginator.to_dict(pageinfo))
	})
	return render_to_response('question/list_questions.html', c)


########################################################################
# add_question: 添加问答
########################################################################
@login_required
def add_question(request):
	if request.POST:
		QuestionInfo.objects.create(
			owner = request.user,
			name = request.POST['name'],
			pic_url = request.POST.get('pic_url', '')
		)
		return HttpResponseRedirect('/question/questions/')
	else:
		c = RequestContext(request, {
			'nav_name': QUESTION_NAV_NAME
		})
		return render_to_response('question/edit_question.html', c)


########################################################################
# update_question: 更新问答
########################################################################
@login_required
def update_question(request, question_id):
	if request.POST:
		QuestionInfo.objects.filter(owner=request.user, id=question_id).update(
			name = request.POST['name'],
			pic_url = request.POST.get('pic_url', '')
		)

		return HttpResponseRedirect('/question/questions/')
	else:
		question = QuestionInfo.objects.get(owner=request.user, id=question_id)
		c = RequestContext(request, {
			'nav_name': QUESTION_NAV_NAME,
			'question': question
		})
		return render_to_response('question/edit_question.html', c)


########################################################################
# delete_question: 删除问答
########################################################################
@login_required
def delete_question(request, question_id):
	QuestionInfo.objects.filter(id=question_id).update(is_active=False, is_deleted=True)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


########################################################################
# update_question_status: 修改状态
########################################################################
def update_question_status(request, question_id):
	question = QuestionInfo.objects.get(owner=request.user, id=question_id)
	question.is_active = False if question.is_active else True
	question.save()

	return HttpResponseRedirect('/question/editor/questions/')

