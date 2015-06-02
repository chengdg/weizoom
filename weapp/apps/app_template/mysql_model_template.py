class {{class_name}}(models.Model):
	owner = models.ForeignKey(User)
	{% for field in fields %}
	{{field}} = models.CharField(max_length=1024)
	{% endfor %}
	created_at = models.DateTimeField(auto_now_add=True)
__STRIPPER_TAG__
	class Meta(object):
		db_table = 'app_{{app_name}}_{{resource}}'
RESOUCE2MODEL['{{resource}}'] = {{class_name}}