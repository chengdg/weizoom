# __author__ : "田丰敏"

Feature:更新限定区域配置


Background:
	Given jobs登录系统

	When jobs添加限定区域配置
		"""
		{
			"name": "禁售地区",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市"]
			}]
		}
		"""
	When jobs添加限定区域配置
		"""
		{
			"name": "仅售地区",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市"]
			},{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄市","唐山市","沧州市"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			},{
				"area": "华北-东北",
				"province": "山西省",
				"city": ["太原市","大同市","阳泉市","长治市","晋城市","朔州市","晋中市","运城市","忻州市","临汾市","吕梁市"]
			}]
		}
		"""

@mall2 @product_limit_area @eugene
Scenario:1 更新限定区域配置
	Jobs更新"限定区域配置"
	1. jobs能获得更新后的限定区域列表

	Given jobs登录系统
	When jobs修改'禁售地区'限定区域配置
		"""
		{
			"name": "禁售地区",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			}]
		}
		"""
	When jobs修改'仅售地区'限定区域配置
		"""
		{
			"name": "仅售地区",
			"limit_area": [{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄市","唐山市","沧州市"]
			}]
		}
		"""
	Then jobs能获得限定区域列表
		"""
		[{
			"name": "仅售地区",
			"limit_area": [{
				"area": "华北-东北",
				"province": "河北省",
				"city": ["石家庄市","唐山市","沧州市"]
			}],
			"actions": ["修改","删除"]
		},{
			"name": "禁售地区",
			"limit_area": [{
				"area": "直辖市",
				"province": ["北京市","天津市"]
			},{
				"area": "西北-西南",
				"province": "陕西省",
				"city": ["西安市"]
			}],
			"actions": ["修改","删除"]
		}]
		"""
