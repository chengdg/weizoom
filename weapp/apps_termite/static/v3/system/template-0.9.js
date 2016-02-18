/*
Copyright (c) 2011-2012 Weizoom Inc
*/

/**
 * 简单的Template模板类，只支持变量替换，无逻辑
 * @constructor
 * @param str - 模板内容
 */
W.Template = function (str) {
	this.nodes = [];
	this.isCompiled = false;
	this.str = str;
	
	this.debug = function() {
		$.each(this.nodes, function(key, value) { alert(key + " " + value);} );
	};
	
	this.compile = function() {
		var length = this.str.length;
		var node = [];
		var inVariable = false;
		var i;
		for(i = 0; i < length; ++i) {
			var c = this.str.charAt(i);
			if(c === '$' && this.str.charAt(i+1) === '{') {
				this.nodes.push(node.join(""));
				node.length = 0;
				inVariable = true;
			}
			else if(inVariable && c === "}") {
				node.push(c);
				this.nodes.push(node.join(""));
				node.length = 0;
				inVariable = false;
				continue;
			}
			node.push(c);
		}
		if(node.length !== 0) {
			this.nodes.push(node.join(""));
		}
		this.isCompiled = true;
	};
	
	this.render = function(data, options) {
		options = options || {};
		if(!this.isCompiled) {
			this.compile();
		}
		var temp = [];
		$.each(this.nodes, function(key, value) {
			if(value.charAt(0) === '$') {
				var variableName = value.substring(2, value.length-1);
				var variableValue = data[variableName];
				if (variableValue === null) {
					temp.push(options['default'] === undefined || options['default'] === null ? value : options['default']);
				}
				else {
					temp.push(data[variableName]);
				}
			}
			else {
				temp.push(value);
			}
		});
		return temp.join("");
	};
};

/**
 * 以data作为context，渲染str
 * @param str
 * @param data
 */
W.render = function(str, data) {
	var template = new W.Template(str);
	return template.render(data);
};


