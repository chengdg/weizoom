/*
Copyright (c) 2011-2012 Weizoom Inc
*/
Handlebars.registerHelper('ifCond', function (v1, operator, v2, options) {
    switch (operator) {
        case '==':
            return (v1 == v2) ? options.fn(this) : options.inverse(this);
        case '!==':
            return (v1 !== v2) ? options.fn(this) : options.inverse(this);
        case '===':
            return (v1 === v2) ? options.fn(this) : options.inverse(this);
        case '<':
            return (v1 < v2) ? options.fn(this) : options.inverse(this);
        case '<=':
            return (v1 <= v2) ? options.fn(this) : options.inverse(this);
        case '>':
            return (v1 > v2) ? options.fn(this) : options.inverse(this);
        case '>=':
            return (v1 >= v2) ? options.fn(this) : options.inverse(this);
        case '&&':
            return (v1 && v2) ? options.fn(this) : options.inverse(this);
        case '||':
            return (v1 || v2) ? options.fn(this) : options.inverse(this);
        case 'isvalid':
            return v1 ? options.fn(this) : options.inverse(this);
        case 'isnotvalid':
            return v1 ? options.inverse(this) : options.fn(this);
        default:
            return options.inverse(this);
    }
});

Handlebars.registerHelper('ifequal', function (v1, v2, options) {
    return (v1 == v2) ? options.fn(this) : options.inverse(this);
});


Handlebars.registerHelper('not', function (value, options) {
	return !value;
});


Handlebars.registerHelper('updateContext', function (obj, options) {
    if (obj) {
        var _this = this;
        _.each(obj.runtime_context, function(value, key) {
            _this[key] = value;
        });
    }
    return options.fn(this);
});
Handlebars.registerHelper('if_in', function(str, array, options) {
    var flag = false;
    for(var i=0; i<array.length; i++){
        if(array[i] == str){
            flag = true;
            break;
        }
    }
    if(flag) {
        return options.fn(this);
    } else {
        return options.inverse(this);
    }
});

Handlebars.registerHelper('list', function(item_message, options) {
    var out = '<ul>';
    for(var i=0, l=item_message.length; i<l; i++) {
        var message = item_message[i].split('：');
        out = out + '<li>' + message[0] + '：' + '<span>' + message[1] + '</span>' + '</li>';
    }
    return out + '</ul>';
});