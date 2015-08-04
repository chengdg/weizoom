# -*- coding: utf-8 -*-

import unittest
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from test import helper

from account.pageobject.login_page import LoginPage
from test.pageobject.page_frame import PageFrame
from question.pageobject.question_list_page import QuestionListPage


class TestQa(helper.FunctionFilterMixin, unittest.TestCase):
	def setUp(self):
		chrome_options = Options()
		chrome_options.add_argument("--disable-extensions")
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
		self.driver.implicitly_wait(3)
		self.verificationErrors = []


	def tearDown(self):
		page_frame = PageFrame(self.driver)
		page_frame.logout()
		self.driver.quit()


	def __assert_problems(self, expected_problems, actual_problems):
		self.assertEquals(len(expected_problems), len(actual_problems))
		for i in range(len(expected_problems)):
			expected_problem = expected_problems[i]
			actual_problem = actual_problems[i]
			self.assertEquals(expected_problem['title'][0:10], actual_problem['title'][0:10])
			self.assertEquals(expected_problem['right_answer'][0:10], actual_problem['right_answer'][0:10])
			self.assertEquals(expected_problem['right_feedback'][0:10], actual_problem['right_feedback'][0:10])


	def __assert_prizes(self, expected_prizes, actual_prizes):
		self.assertEquals(len(expected_prizes), len(actual_prizes))
		for i in range(len(expected_prizes)):
			expected_prize = expected_prizes[i]
			actual_prize = actual_prizes[i]
			title = '%s - %s' % (expected_prize['right_count_min'], expected_prize['right_count_max'])
			self.assertEquals(title, actual_prize['right_count'])
			length = 20
			if len(expected_prize['content']) < length:
				length = len(expected_prize['content'])
			self.assertEquals(expected_prize['content'][0:length], actual_prize['content'][0:length])


	#==============================================================================
	# test_01_question: 微信问答
	#==============================================================================
	@helper.register('question')
	def test_01_question(self):
		login_page = LoginPage(self.driver)
		login_page.login('test')

		question_list_page = QuestionListPage(self.driver)
		#1. 进入问答列表页面
		question_list_page.load_question()

		#2. 进入添加游戏页面
		edit_question_page = question_list_page.add_question()
		#3. 点击提交，验证错误提示
		edit_question_page.submit_question()
		error_hints = edit_question_page.get_error_hints()
		self.assertEquals(u'内容长度必须在1到10之间，请重新输入', error_hints[0])
		self.assertEquals(u'内容长度必须在1到40之间，请重新输入', error_hints[1])
		self.assertEquals(u'请添加问答题目', error_hints[2])
		self.assertEquals(u'请添加问答奖品', error_hints[3])

		expected_question = {
			'message': {'start_patterns': u'游戏1', 'end_patterns': u'退出 ',
			            'finished_message': u'谢谢参与！！'},
		    'problems': [{
		            'title': u'请选出小米公司第一步手机（A 小米1 B 小米2 C小米3 ）',
		            'right_answer': u'A',
		            'right_feedback': u'恭喜您答对了！',
		            'error_feedback': u'很遗憾，答错了！'
			    },{
				    'title': u'百度创始人（A 李彦宏 B 马云 C 蔡文胜 ） ',
				    'right_answer': u'A',
				    'right_feedback': u'',
				    'error_feedback': u''
		        },{
				    'title': u'小米创始人（A 雷军 B 马云 C 蔡文胜 ）',
				    'right_answer': u'A',
				    'right_feedback': u'恭喜您答对了！',
				    'error_feedback': u''
		        },{
				    'title': u'微众创始人（A 王震 B 马云 C 蔡文胜 ） ',
				    'right_answer': u'A',
				    'right_feedback': u'',
				    'error_feedback': u'很遗憾，答错了！ '
		        },{
				    'title': u'阿里巴巴创始人（A 马云 B 雷军 C 蔡文胜 ） ',
				    'right_answer': u'A',
				    'right_feedback': u'',
				    'error_feedback': u'很遗憾，答错了！ '
		        }],
		    'prizes': [{
			        'right_count_min': '5',
					'right_count_max': '5',
		            'count': '1',
		            'content': u'感谢参与，给你九五折。你可以凭此消息来店消费！'
		        },{
				    'right_count_min': '3',
				    'right_count_max': '3',
				    'count': '1',
				    'content': u'感谢参与，给你九五折。你可以凭此消息来店消费！'
		        },{
	                'right_count_min': '1',
	                'right_count_max': '1',
	                'count': '1',
	                'content': u'感谢参与，给你九五折。你可以凭此消息来店消费！'
		        },{
		            'right_count_min': '0',
		            'right_count_max': '0',
		            'count': '1',
		            'content': u'感谢参与！'
		        }]
		}
		edit_question_page.set_question_info(**expected_question['message'])

		#4. 添加标题
		expected_problems = expected_question['problems']
		for i in range(0,len(expected_problems)):
			edit_question_page.submit_problem(**expected_problems[i])
		#5. 添加奖品
		expected_prizes = expected_question['prizes']
		for i in range(0,len(expected_prizes)):
			edit_question_page.submit_prize(**expected_prizes[i])

		#6. 验证标题和奖品显示
		actual_problems = edit_question_page.get_problems()
		self.__assert_problems(expected_problems, actual_problems)
		actual_prizes = edit_question_page.get_prizes()
		self.__assert_prizes(expected_prizes, actual_prizes)

		#5. 编辑题目5
		expected_question['problems'][4] = {
			'title': u'请你选择出谁是阿里巴巴创始人？？（A 马云 B 雷军 C 蔡文胜 ） ',
			'right_answer': u'A',
			'right_feedback': u'恭喜您答对了！',
			'error_feedback': u''
		}
		edit_question_page.edit_problem(u'阿里巴巴创始人')
		edit_question_page.update_problem(**expected_question['problems'][4])

		#6. 删除第4题，‘微众创始人...’
		edit_question_page.delete_problem(u'微众创始人')

		#7. 删除奖品P3
		edit_question_page.delete_prize(u'1 - 1')

		#8. 编辑题目P2
		expected_question['prizes'][1] = {
			'right_count_min': '2',
			'right_count_max': '3',
			'count': '1',
			'content': u'谢谢你的参与！你可以凭此消息来店消费享受九五折。'
		}
		edit_question_page.edit_prize(u'3 - 3')
		edit_question_page.update_prize(**expected_question['prizes'][1])

		#9. 验证题目和奖品
		expected_problems = [expected_question['problems'][0], expected_question['problems'][1],
		                     expected_question['problems'][2], expected_question['problems'][4]]
		expected_prizes = [expected_question['prizes'][0], expected_question['prizes'][1],
		                   expected_question['prizes'][3]]
		actual_problems = edit_question_page.get_problems()
		self.__assert_problems(expected_problems, actual_problems)
		actual_prizes = edit_question_page.get_prizes()
		self.__assert_prizes(expected_prizes, actual_prizes)


		#10. 提交此游戏
		edit_question_page.submit_question()

		question_list_page = QuestionListPage(self.driver)
		edit_question_page = question_list_page.add_question()

		#11. 验证重复关键词
		edit_question_page.set_question_info(**expected_question['message'])
		edit_question_page.submit_question()
		error_hints = edit_question_page.get_error_hints()
		self.assertEquals(u'本系统已经有一个该关键词的规则，请重新设置一个', error_hints[0])

		#12. 添加游戏2
		expected_question = {
			'message': {'start_patterns': u'游戏2', 'end_patterns': u'退出',
		            'finished_message': u'谢谢参与！！'},
			'problems': [{
	             'title': u'下面哪个是题目1？（ A 小米1 B 题目1 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
            },{
	             'title': u'下面哪个是题目2？（ A 小米1 B 题目2 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
            },{
	             'title': u'下面哪个是题目3？（ A 小米1 B 题目3 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
            },{
	             'title': u'下面哪个是题目4？（ A 小米1 B 题目4 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
            }],
			'prizes': [{
		        'right_count_min': '3',
		        'right_count_max': '3',
		        'count': '1',
		        'content': u'感谢参与，给你八五折。你可以凭此消息来店消费！'
            },{
	            'right_count_min': '2',
	            'right_count_max': '2',
	            'count': '1',
	            'content': u'感谢参与，给你九五折。你可以凭此消息来店消费！'
            },{
	            'right_count_min': '0',
	            'right_count_max': '1',
	            'count': '1',
	            'content': u'感谢参与！'
            }]
		}

		edit_question_page.set_question_info(**expected_question['message'])
		expected_problems = expected_question['problems']
		for i in range(0,len(expected_problems)):
			edit_question_page.submit_problem(**expected_problems[i])
		expected_prizes = expected_question['prizes']
		for i in range(0,len(expected_prizes)):
			edit_question_page.submit_prize(**expected_prizes[i])
		edit_question_page.submit_question()


		#12. 添加‘退出’
		expected_question = {
		'message': {'start_patterns': u'退出', 'end_patterns': u'B',
		            'finished_message': u'谢谢参与！'},
		'problems': [{
				'title': u'下面哪个是题目1？（ A 小米1 B 题目1 C小米3）',
				'right_answer': u'B',
				'right_feedback': u'',
				'error_feedback': u''
			},{
	             'title': u'下面哪个是题目2？（ A 小米1 B 题目2 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
		    },{
	             'title': u'下面哪个是题目3？（ A 小米1 B 题目3 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
		    },{
	             'title': u'下面哪个是题目4？（ A 小米1 B 题目4 C小米3）',
	             'right_answer': u'B',
	             'right_feedback': u'',
	             'error_feedback': u''
		    }],
		'prizes': [{
	           'right_count_min': '3',
	           'right_count_max': '4',
	           'count': '1',
	           'content': u'感谢参与，给你八五折。你可以凭此消息来店消费！'
		    },{
	           'right_count_min': '2',
	           'right_count_max': '2',
	           'count': '1',
	           'content': u'感谢参与！'
		    }]
		}
		question_list_page = QuestionListPage(self.driver)
		edit_question_page = question_list_page.add_question()

		edit_question_page.set_question_info(**expected_question['message'])
		expected_problems = expected_question['problems']
		for i in range(0,len(expected_problems)):
			edit_question_page.submit_problem(**expected_problems[i])
		expected_prizes = expected_question['prizes']
		for i in range(0,len(expected_prizes)):
			edit_question_page.submit_prize(**expected_prizes[i])
		edit_question_page.submit_question()

		#13. 验证列表
		question_list_page = QuestionListPage(self.driver)
		questions = question_list_page.get_questions()
		self.assertEquals(3, len(questions))
		self.assertEquals(u'退出', questions[0]['name'])
		self.assertEquals(u'游戏2', questions[1]['name'])
		self.assertEquals(u'游戏1', questions[2]['name'])

		#14. 删除游戏1
		question_list_page.delete_question(u'游戏1')
		#验证列表
		questions = question_list_page.get_questions()
		self.assertEquals(2, len(questions))
		self.assertEquals(u'退出', questions[0]['name'])
		self.assertEquals(u'游戏2', questions[1]['name'])


def init():
	print 'init db environment for qa'
	from question.models import Problem, Prize, QuestionInfo

	Problem.objects.all().delete()
	Prize.objects.all().delete()
	QuestionInfo.objects.all().delete()


def clear():
	print 'clear db environment for qa'


TestClass = TestQa
def suite(group='all'):
	if group == 'all':
		suite = unittest.makeSuite(TestClass, 'test')
	else:
		suite = unittest.TestSuite()
		for function in TestClass.filter_function_by_group(group):
			suite.addTest(TestClass(function))

	return suite

if __name__ == "__main__":
	unittest.main()