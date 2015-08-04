# -*- coding: utf-8 -*-

import mongoengine as models

#Demo Class
'''
class Planet(models.Document):
	name = models.StringField(max_length=100) #星球名称
	suitable_for_living = models.BooleanField(verbose_name='是否适合居住')
	distance = models.IntField(verbose_name='与地球的距离，单位为光年')
	has_advanced_species = models.BooleanField(verbose_name='是否有高级物种')
	created_at = models.DateTimeField()

	meta = {
		'collection': 'star_wars_planets'
	}
'''
	