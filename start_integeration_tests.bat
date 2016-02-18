cd weapp

python manage.py test -v2  -- -c=integration_nose2.cfg --with-cov --cov-report=html -B --cov-config=.coveragerc --no-user-config -v --log-level=30 utils

@echo 测试完成
@echo 打开weapp/coverage_html_report/index.html查看测试覆盖率分析结果

pause