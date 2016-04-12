var React = require('react');
var ShopStore = require('./ShopStore');

var CheckedShops = React.createClass({
	deleteShop: function(event){

	},
	render:function(){
		var checkedShops = ShopStore.getCheckedShops();
		var checkedNodes = checkedShops.map(function(data,index){
			return(
				<div className="btn btn-info mr5" key={index}>
					<span className="mr5">{data.store_name}</span>
					<span data-user-id={data.user_id} onClick={this.deleteShop}>
						<span className="glyphicon glyphicon-remove"></span>
					</span>
				</div>
			)
		});
		
		return(
			<div className="form-group ml15">
				<label className="col-sm-2 control-label"></label>
				<div className="col-sm-5">
					{checkedNodes}
				</div>
			</div>
		)		
	}
})
module.exports = CheckedShops;