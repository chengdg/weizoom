"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from core.jsonresponse import decode_json_str


class QuestionTest(TestCase):
	def setUp(self):
		self.client = Client()

	#获取response对象中的json数据
	def get_json(self, response):
		#去掉头部信息，截取返回的json字符串
		data_str = str(response).split('\n\n')[1].strip()
		#解析json字符串，返回json对象
		return decode_json_str(data_str)

	def create_question(self, data=None):
		if data:
			return self.client.post('/question/api/question/create/', data)
		else:
			return self.client.get('/question/editor/create/')

	def delete_question(self, question_id, http_referer):
		return self.client.get('/question/editor/delete/%d/' % question_id, {}, HTTP_REFERER=http_referer)

	def test_question(self):
		#test用户登录
		self.client.login(username='test', password='test')

		#
		#测试: 没有 游戏
		#
		response = self.client.get('/question/editor/questions/')
		self.assertEquals('marketing_tool', response.context['nav_name'])
		self.assertEquals(0, len(response.context['questions']))

		#
		#进入：添加界面
		#
		response = self.create_question()
		self.assertEquals('marketing_tool', response.context['nav_name'])

		question_content = {
			'start_patterns': u'游戏1',
			'end_patterns': u'退出',
			'finished_message': u'/微笑谢谢参与！！',
			'problems': """[
			        {"id":-103,"right_answer":"A","title":"阿里巴巴创始人（A 马云 B 雷军 C 蔡文胜 ）","right_feedback":"","error_feedback":"","title_content":"<p>阿里巴巴创始人（A 马云 &nbsp;B 雷军 &nbsp;C 蔡文胜 ）</p>","right_feedback_content":"","error_feedback_content":""},
			        {"id":-100,"right_answer":"A","title":"表情 + 百度创始人（A 李彦宏 B 马云 C 蔡文胜 ）","right_feedback":"","error_feedback":"","title_content":"<p>表情 + 百度创始人（A 李彦宏 &nbsp;B 马云 &nbsp;C 蔡文胜 ）</p>","right_feedback_content":"","error_feedback_content":""},
			        {"id":-101,"right_answer":"A","title":"小米创始人（A 雷军 B 马云 C 蔡文胜 ）","right_feedback":"恭喜您答对了！","error_feedback":"","title_content":"<p>小米创始人（A 雷军 &nbsp;B 马云 &nbsp;C 蔡文胜 ）</p>","right_feedback_content":"<p>恭喜您答对了！</p>","error_feedback_content":""},
			        {"id":-102,"right_answer":"A","title":"微众创始人（A 王震 B 马云 C 蔡文胜 ）","right_feedback":"","error_feedback":"很遗憾，答错了！","title_content":"<p>微众创始人（A 王震 &nbsp;B 马云 &nbsp;C 蔡文胜 ）</p>","right_feedback_content":"","error_feedback_content":"<p>很遗憾，答错了！</p>"},
			        {"id":-99,"right_answer":"A","title":"请选出小米公司第一步手机（A 小米1 B 小米2 C小米3 ）","right_feedback":"恭喜您答对了！","error_feedback":"很遗憾，答错了！","title_content":"请选出小米公司第一步手机（A 小米1 &nbsp;B 小米2 &nbsp;C小米3 ）","right_feedback_content":"恭喜您答对了！","error_feedback_content":"很遗憾，答错了！"}
			    ]""",
			'prizes': """[
			        {"id":-98,"right_count_min":"5","right_count_max":"5","content":"感谢参与，给你九五折。你可以凭此消息来店消费！","count":"1","content_content":"感谢参与，给你九五折。你可以凭此消息来店消费！"},
			        {"id":-97,"right_count_min":"3","right_count_max":"3","content":"感谢参与，给你九五折。你可以凭此消息来店消费！","count":"1","content_content":"<p>感谢参与，给你九五折。你可以凭此消息来店消费！</p>"},
			        {"id":-96,"right_count_min":"1","right_count_max":"1","content":"感谢参与，给你九五折。你可以凭此消息来店消费！","count":"1","content_content":"<p>感谢参与，给你九五折。你可以凭此消息来店消费！</p>"},
			        {"id":-95,"right_count_min":"0","right_count_max":"0","content":"感谢参与！","count":"1","content_content":"<p>感谢参与！</p>"}
			    ]"""
		}

		#
		# 创建一条游戏
		#
		self.create_question(question_content)

		#测试: 有一个 游戏
		response = self.client.get('/question/editor/questions/')
		self.assertEquals('marketing_tool', response.context['nav_name'])
		questions = response.context['questions']
		self.assertEquals(1, len(questions))
		question = questions[0]
		self.assertEquals(u'游戏1', question.start_patterns)

		#
		# 测试，验证游戏名是否存在
		#
		response = self.client.post('/question/api/pattern/check_duplicate/', {'patterns': u'游戏1'})
		json = self.get_json(response)
		self.assertEquals(601, json['code'])
		self.assertEquals(u'本系统已经有一个该关键词的规则，请重新设置一个', json['errMsg'])

		#
		# 创建第二条游戏
		#
		question_content['start_patterns'] = u'游戏2'
		self.create_question(question_content)

		#测试: 有二个 游戏
		response = self.client.get('/question/editor/questions/')
		self.assertEquals('marketing_tool', response.context['nav_name'])
		questions = response.context['questions']
		self.assertEquals(2, len(questions))
		question = questions[0]
		self.assertEquals(u'游戏2', question.start_patterns)
		question = questions[1]
		self.assertEquals(u'游戏1', question.start_patterns)

		# 停用游戏1
		self.client.get('/question/editor/update_status/%d/' % questions[0].id)

		# 删除 游戏1
		self.delete_question(questions[0].id, '/question/editor/questions/')

		#测试: 有一个 游戏
		response = self.client.get('/question/editor/questions/')
		self.assertEquals('marketing_tool', response.context['nav_name'])
		questions = response.context['questions']
		self.assertEquals(1, len(questions))
		question = questions[0]
		self.assertEquals(u'游戏1', question.start_patterns)

		#
		#翻页测试：正好一页，20条数据
		#
		for i in range(3,22):
			question_content['start_patterns'] = u'游戏%d' % i
			self.create_question(question_content)

		response = self.client.get("/question/editor/questions/")
		questions = response.context['questions']
		self.assertEquals(20, len(questions))
		response = self.client.get("/question/editor/questions/?page=2")
		questions = response.context['questions']
		self.assertEquals(0, len(questions))

		#
		#翻页测试：多于一页，21条数据
		#
		question_content['start_patterns'] = u'游戏23'
		self.create_question(question_content)

		response = self.client.get("/question/editor/questions/?page=1")
		questions = response.context['questions']
		self.assertEquals(20, len(questions))
		response = self.client.get("/question/editor/questions/?page=2")
		questions = response.context['questions']
		self.assertEquals(1, len(questions))
		response = self.client.get("/question/editor/questions/?page=3")
		questions = response.context['questions']
		self.assertEquals(0, len(questions))


from test.app_test_suites_loader import *

test_cases = [
	QuestionTest,
]

def suite():
	test_suites_in_cur_file = build_test_suite_from(test_cases)
	test_suites_in_all_others = load_testsuits_from_app('question')

	test_suites_in_all_others.addTests(test_suites_in_cur_file)
	return test_suites_in_all_others