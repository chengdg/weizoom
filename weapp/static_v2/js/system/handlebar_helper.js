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