/**
 * Created by cl on 2016/2/24 024.
 */
var React = require('react');
var debug = require('debug')('m:outline.data:DataPage');

var Store = require('.././rule_order/Store');
var getCardRuleStore = require('.././rule_order/getCardRuleStore');
var Action = require('.././rule_order/Action');
var ReactDOM = require('react-dom');
var ApprovalDialog = require('./ApprovalDialog.react');

var Reactman = require('reactman');
var FormInput = Reactman.FormInput;
var FormSubmit = Reactman.FormSubmit;
var FormSelect = Reactman.FormSelect;
var FormText =  Reactman.FormText;
var Dispatcher = Reactman.Dispatcher;
require('./ApprovalCard.css');
var ApprovalCard = React.createClass({

	getInitialState: function() {
		return ({
			card_rule_order: [],
			card_rule_list: [],
			orderInfo:{},
			attribute: 0
		})
	},

	onChangeStore: function() {
		this.setState({
			orderInfo : Store.getData()
		});
	},

	componentWillMount: function() {
		Action.getCardRule();
	},

	componentDidMount: function(){
		getCardRuleStore.addListener(this.getCardRule);
		Store.addListener(this.onChangeStore);
	},

	getCardRule: function(){
		this.setState({
			card_rule_list:getCardRuleStore.getCardRule()
		})
	},

	onCardOrderSave: function(){
		var card_list = Store.getDataCardlines();
		rule_id_list = []
		for(index in card_list){
			rule_id = card_list[index].rule_id
			if (rule_id_list.indexOf(rule_id) != -1){
				Reactman.PageAction.showHint('error', '卡库不能为空且不能重复！');
				return;
			}
			rule_id_list.push(rule_id)
		}
		var order_infos = this.state.orderInfo;
		var ruleStore = Store.getData();
		var rule_order = this.state.card_rule_order;
		var value =  ruleStore.orderAttributes;
		var remark = ruleStore.remark;
		var date = {
			'rule_order':JSON.stringify(card_list),
			'card_rule_num': order_infos['card_rule_num'],
			'valid_time_from': order_infos['valid_time_from'],
			'valid_time_to': order_infos['valid_time_to'],
			'company_info': order_infos['company_info'],
			'responsible_person': order_infos['responsible_person'],
			'contact': order_infos['contact'],
			'sale_name': order_infos['sale_name'],
			'sale_departent': order_infos['sale_departent'],
			'use_departent': order_infos['use_departent'],
			'project_name': order_infos['project_name'],
			'appliaction': order_infos['appliaction'],
			'use_persion': order_infos['use_persion'],
			'order_number': order_infos['order_number'],
			'order_attributes':this.state.attribute,
			'remark':remark
		}
		Action.saveCardRuleOrder(date);
	},

	addCardLines:function() {
		Action.addCardLines();
	},

	ChooseOrderAttribute: function(value, event){
		Action.resetProduct();
		this.setState({
			attribute : value
		})
	},

	render: function(){
		return (
			<div className="xui-outlineData-page xui-formPage xui-cardruleOrder">
				<form className="form-horizontal mt15">
					<header  className="cui-header">
						<span className="xui-fontBold">基本信息</span>
						<span className="xui-fontGary">
							( <i className="star_show pl5"></i>
							表示必填)
						</span>
					</header>

					<CardListLabel />{/*.卡库.*/}
					<legend className="pl10 pt10 pb10"><a href="javascript:void(0);" onClick={this.addCardLines}>添加卡库</a></legend>

			        <fieldset style={{background:'#FFF'}}>
						<FormSelect label="卡类型:" name="orderAttributes" options={[{"value": "-1", "text": "请选择"},{"value": "0", "text": "发售卡"},{"value": "1", "text": "内部使用卡"},{"value": "2", "text": "返点卡"}]} validate="require-select" onChange={this.ChooseOrderAttribute} ref="orderAttributes" />
						<div> <OrderInfoInput chooseOrderAttribute={this.state.attribute} orderInfo={this.state.orderInfo}/> </div>
			        </fieldset>
			        <div style={{marginTop:'20px'}}>
			            <div className="control-group">
			                <FormSubmit className="btn btn-success" onClick={this.onCardOrderSave} />
			            </div>
			        </div>
		       </form>
			</div>
		)
	}
});

var OrderInfoInput = React.createClass({
	getInitialState: function() {
		return ({
			orderInfo:{},
		})
	},

	onChange: function(value, event) {
		var property = event.target.getAttribute('name');
		Action.updateProduct(property, value);
	},

	componentWillMount: function() {
		Action.getCardRule();
	},

	componentDidMount: function(){
		Store.addListener(this.onChangeStore);
	},

	onChangeStore: function() {
		this.setState({
			orderInfo : Store.getData()
		});
		this.props.orderInfo = this.state.orderInfo;
	},

	render: function() {
		var _this=this;
		var chooseOrderAttribute = this.props.chooseOrderAttribute;

		if (chooseOrderAttribute == '0'){
			return(
				<div ref="saleCard" className="sale_card">
					<FormInput label="客户企业信息:" type="text" name="company_info" ref="companyInfo" validate="require-string" placeholder="" value={this.state.orderInfo.company_info} onChange={this.onChange} />
					<FormInput label="客户经办人信息:" type="text" name="responsible_person" validate="require-string" placeholder="" ref="responsiblePerson" value={this.state.orderInfo.responsible_person} onChange={this.onChange} />
					<FormInput label="客户联系方式:" type="text" name="contact" ref="contact" validate="require-notempty" placeholder="" value={this.state.orderInfo.contact} onChange={this.onChange}/>
					<FormInput label="销售员姓名:" type="text" name="sale_name" ref="saleName" validate="require-string" placeholder="" value={this.state.orderInfo.sale_name} onChange={this.onChange}/>
					<FormInput label="销售部门:" type="text" name="sale_departent" ref="saleDepartent" validate="require-string" placeholder="" value={this.state.orderInfo.sale_departent} onChange={this.onChange}/>
					<FormText label="备注:" type="text" name="remark" value={this.state.orderInfo.remark} width="300" height="150" placeholder="" onChange={this.onChange} />
				</div>
			)
		}else if(chooseOrderAttribute == '1'){
			return(
				<div ref="internalCard" className="internal_card">
					<FormInput label="领用部门:" type="text" name="use_departent" ref="useDepartent" validate="require-string" placeholder="" value={this.state.orderInfo.use_departent} onChange={this.onChange}/>
					<FormInput label="项目名称:" type="text" name="project_name" ref="projectName" validate="require-string" placeholder="" value={this.state.orderInfo.project_name} onChange={this.onChange}/>
					<FormInput label="用途:" type="text" name="appliaction" ref="appliaction" validate="require-string" placeholder="" value={this.state.orderInfo.appliaction} onChange={this.onChange}/>
					<FormInput label="领用人:" type="text" name="use_persion" ref="usePersion" validate="require-string" placeholder="" value={this.state.orderInfo.use_persion} onChange={this.onChange}/>
					<FormText label="备注:" type="text" name="remark" value={this.state.orderInfo.remark} width="300" height="150" placeholder="" onChange={this.onChange} />
				</div>
			)
		}else {
			return(
				<div ref="discountCard" className="discount_card">
					<FormInput label="对应发单号:" type="text" name="order_number" ref="orderNumber" validate="require-string" placeholder="" value={this.state.orderInfo.order_number} onChange={this.onChange}/>
					<FormText label="备注:" type="text" name="remark" value={this.state.orderInfo.remark} width="300" height="150" placeholder="" onChange={this.onChange} />
				</div>
			)
		}
	}
})

var CardListLabel = React.createClass({
	getInitialState: function() {
		return ({
			cardlist:[{rule_id:'',card_name:'',card_rule_num:'',valid_time_from:'',valid_time_to:''}]
		})
	},

	onChangeStore: function() {
		this.setState({
			cardlist:Store.getDataCardlines()
		})
	},

	componentDidMount: function(){
		Store.addListener(this.onChangeStore);
	},

	onChange: function(index,value,event) {
		var property = event.target.getAttribute('name');
		Action.updateAddProduct(index, property, value);
	},

	choiceCard: function(index) {
		Reactman.PageAction.showDialog({
			title: "选择卡库", 
			component: ApprovalDialog, 
			data: {
				index: index
			},
			success: function(inputData, dialogState) {
				Action.updateCardLines(inputData.index, dialogState.choiced_card);
			}
		});
	},
	
	render: function() {
		var _this=this;
		var cardlines=this.state.cardlist.map(function(card,index) {
			return (
			<fieldset className="form-inline" key={index}>
				<input name='rule_id' type="text" style={{display:'none'}} value={_this.state.cardlist[index].rule_id}/>
				<FormInput label="卡名称:" type="text" name="card_name" ref="CardName" value={_this.state.cardlist[index].card_name} validate="require-notempty" onChange={_this.onChange.bind(_this,index)}/>
				<a href="javascript:void(0);" style={{display:'inline-block',textAlign:'center',width:'80px'}} onClick={_this.choiceCard.bind(_this,index)}>选择卡库</a>
				<FormInput label="出库数量:" type="text" name="card_rule_num" ref="CardRuleNum" value={_this.state.cardlist[index].card_rule_num} validate="require-positive-int" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput label="有效期:" type="text" name="valid_time_from" ref="valid_time_from" value={_this.state.cardlist[index].valid_time_from} validate="require-notempty" placeholder="请输入有效期开始时间" onChange={_this.onChange.bind(_this,index)}/>
				<FormInput type="text" name="valid_time_to" ref="valid_time_to" value={_this.state.cardlist[index].valid_time_to} validate="require-notempty" placeholder="请输入有效期结束时间" onChange={_this.onChange.bind(_this,index)}/>
			</fieldset>
			)
		})
		return (
			<div className="CardListLabel">
				{cardlines}
			</div>
		);
	}
});
module.exports = ApprovalCard;