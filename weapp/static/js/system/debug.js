/*
Copyright (c) 2011-2012 Weizoom Inc
*/

function printStackTrace(a){var a=a||{guess:!0},b=a.e||null,a=!!a.guess,d=new printStackTrace.implementation,b=d.run(b);return a?d.guessAnonymousFunctions(b):b}printStackTrace.implementation=function(){};
printStackTrace.implementation.prototype={run:function(a,b){a=a||this.createException();b=b||this.mode(a);return"other"===b?this.other(arguments.callee):this[b](a)},createException:function(){try{this.undef()}catch(a){return a}},mode:function(a){return a.arguments&&a.stack?"chrome":a.stack&&a.sourceURL?"safari":"string"===typeof a.message&&"undefined"!==typeof window&&window.opera?!a.stacktrace||-1<a.message.indexOf("\n")&&a.message.split("\n").length>a.stacktrace.split("\n").length?"opera9":!a.stack?
"opera10a":0>a.stacktrace.indexOf("called from line")?"opera10b":"opera11":a.stack?"firefox":"other"},instrumentFunction:function(a,b,d){var a=a||window,c=a[b];a[b]=function(){d.call(this,printStackTrace().slice(4));return a[b]._instrumented.apply(this,arguments)};a[b]._instrumented=c},deinstrumentFunction:function(a,b){a[b].constructor===Function&&(a[b]._instrumented&&a[b]._instrumented.constructor===Function)&&(a[b]=a[b]._instrumented)},chrome:function(a){a=(a.stack+"\n").replace(/^\S[^\(]+?[\n$]/gm,
"").replace(/^\s+(at eval )?at\s+/gm,"").replace(/^([^\(]+?)([\n$])/gm,"{anonymous}()@$1$2").replace(/^Object.<anonymous>\s*\(([^\)]+)\)/gm,"{anonymous}()@$1").split("\n");a.pop();return a},safari:function(a){return a.stack.replace(/\[native code\]\n/m,"").replace(/^@/gm,"{anonymous}()@").split("\n")},firefox:function(a){return a.stack.replace(/(?:\n@:0)?\s+$/m,"").replace(/^[\(@]/gm,"{anonymous}()@").split("\n")},opera11:function(a){for(var b=/^.*line (\d+), column (\d+)(?: in (.+))? in (\S+):$/,
a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c+=2){var e=b.exec(a[c]);if(e){var g=e[4]+":"+e[1]+":"+e[2],e=e[3]||"global code",e=e.replace(/<anonymous function: (\S+)>/,"$1").replace(/<anonymous function>/,"{anonymous}");d.push(e+"@"+g+" -- "+a[c+1].replace(/^\s+/,""))}}return d},opera10b:function(a){for(var b=/^(.*)@(.+):(\d+)$/,a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c++){var e=b.exec(a[c]);e&&d.push((e[1]?e[1]+"()":"global code")+"@"+e[2]+":"+e[3])}return d},opera10a:function(a){for(var b=
/Line (\d+).*script (?:in )?(\S+)(?:: In function (\S+))?$/i,a=a.stacktrace.split("\n"),d=[],c=0,f=a.length;c<f;c+=2){var e=b.exec(a[c]);e&&d.push((e[3]||"{anonymous}")+"()@"+e[2]+":"+e[1]+" -- "+a[c+1].replace(/^\s+/,""))}return d},opera9:function(a){for(var b=/Line (\d+).*script (?:in )?(\S+)/i,a=a.message.split("\n"),d=[],c=2,f=a.length;c<f;c+=2){var e=b.exec(a[c]);e&&d.push("{anonymous}()@"+e[2]+":"+e[1]+" -- "+a[c+1].replace(/^\s+/,""))}return d},other:function(a){for(var b=/function\s*([\w\-$]+)?\s*\(/i,
d=[],c,f;a&&a.arguments&&10>d.length;)c=b.test(a.toString())?RegExp.$1||"{anonymous}":"{anonymous}",f=Array.prototype.slice.call(a.arguments||[]),d[d.length]=c+"("+this.stringifyArguments(f)+")",a=a.caller;return d},stringifyArguments:function(a){for(var b=[],d=Array.prototype.slice,c=0;c<a.length;++c){var f=a[c];void 0===f?b[c]="undefined":null===f?b[c]="null":f.constructor&&(f.constructor===Array?b[c]=3>f.length?"["+this.stringifyArguments(f)+"]":"["+this.stringifyArguments(d.call(f,0,1))+"..."+
this.stringifyArguments(d.call(f,-1))+"]":f.constructor===Object?b[c]="#object":f.constructor===Function?b[c]="#function":f.constructor===String?b[c]='"'+f+'"':f.constructor===Number&&(b[c]=f))}return b.join(",")},sourceCache:{},ajax:function(a){var b=this.createXMLHTTPObject();if(b)try{return b.open("GET",a,!1),b.send(null),b.responseText}catch(d){}return""},createXMLHTTPObject:function(){for(var a,b=[function(){return new XMLHttpRequest},function(){return new ActiveXObject("Msxml2.XMLHTTP")},function(){return new ActiveXObject("Msxml3.XMLHTTP")},
function(){return new ActiveXObject("Microsoft.XMLHTTP")}],d=0;d<b.length;d++)try{return a=b[d](),this.createXMLHTTPObject=b[d],a}catch(c){}},isSameDomain:function(a){return"undefined"!==typeof location&&-1!==a.indexOf(location.hostname)},getSource:function(a){a in this.sourceCache||(this.sourceCache[a]=this.ajax(a).split("\n"));return this.sourceCache[a]},guessAnonymousFunctions:function(a){for(var b=0;b<a.length;++b){var d=/^(.*?)(?::(\d+))(?::(\d+))?(?: -- .+)?$/,c=a[b],f=/\{anonymous\}\(.*\)@(.*)/.exec(c);
if(f){var e=d.exec(f[1]);e&&(d=e[1],f=e[2],e=e[3]||0,d&&(this.isSameDomain(d)&&f)&&(d=this.guessAnonymousFunction(d,f,e),a[b]=c.replace("{anonymous}",d)))}}return a},guessAnonymousFunction:function(a,b){var d;try{d=this.findFunctionName(this.getSource(a),b)}catch(c){d="getSource failed with url: "+a+", exception: "+c.toString()}return d},findFunctionName:function(a,b){for(var d=/function\s+([^(]*?)\s*\(([^)]*)\)/,c=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*function\b/,f=/['"]?([0-9A-Za-z_]+)['"]?\s*[:=]\s*(?:eval|new Function)\b/,
e="",g,j=Math.min(b,20),h,i=0;i<j;++i)if(g=a[b-i-1],h=g.indexOf("//"),0<=h&&(g=g.substr(0,h)),g)if(e=g+e,(g=c.exec(e))&&g[1]||(g=d.exec(e))&&g[1]||(g=f.exec(e))&&g[1])return g[1];return"(?)"}};

ensureNS('W.debug');
W.debug.printTB = function() {
	var tbs = printStackTrace();
	for (var i = 0; i < tbs.length; ++i) {
		xlog(tbs[i]);
	}
}

W.debug.getTB = function() {
	var tbs = printStackTrace();
	var items = [];
	for (var i = 0; i < tbs.length; ++i) {
		items.push(tbs[i]);
	}
	return items.join('\n');
}

/**
 * error handler
 */
W.Logger = {
    $msgFrame: null,
    msgQueue: [] // queue messages before frame exists and document is not ready
};
var Logger = W.Logger;

Logger.appendMsg = function( msg ) { // private - internal use only
  this.$msgFrame.append( $( "<div>" ).html( msg ) );
  this.$msgFrame.show();
};

Logger.flushMsgQueue = function() { // private - internal use only
  var queue = this.msgQueue;
  this.msgQueue = [];

  for( var i = 0; i < queue.length; ++i )
    this.appendMsg( queue[i] );
};

Logger.logMsg = function( msg ) {
  if( this.$msgFrame )
    this.appendMsg( msg );
  else
    this.msgQueue.push( msg );
};

Logger.logJsError = function( msg, url, line ) {
  this.logMsg( "<span style='color:red;'>** JavaScript Error: </span><span style='color:red;font-weight:bold;'>" +
       msg + "</span> at <span style='color:blue;font-weight:bold;'>" + url + ":" + line + "</span><br/><br/>" );
};

Logger.logToServer = function(msg, url, line, typeError) {
	var items = [];
	items.push("[异常]: " + msg);
	items.push("[URL]: " + window.location.href);
	url = "view-source:" + url
	items.push("[File]: " + url);
	items.push("[Line]: " + line);
	items.push("[Stack Trace]:");
	if (typeError) {
		items.push(typeError.stack);
	} else {
		items.push("None");
	}
	// items.push("[Window]: " + document.documentElement.outerHTML);
	items.push('\n');
	W.getApi().call({
		app: 'account',
		api: 'js_error/log',
		method: 'post',
		args: {
			message: msg,
			content: items.join('\n')
		},
		success: function(data){},
		error: function(resp){}
	})
}

Logger.ready = function() {
    this.$msgFrame = $( "<div id='msgFrame'>" ).css( {
        zIndex: "2147483584",
        position: 'absolute',
        left: 0,
        top: 0,
        width: '100%',
        borderBottom: '1px solid black',
        background: 'lightyellow',
        padding: '3px 0',
        font: 'normal 11px Verdana'
    });

    this.$msgFrame.hide(); // only show when at least one message posted
    this.$msgFrame.prependTo( 'body' );

    this.flushMsgQueue();
};

// -----------------------------------------------------

Logger.oldErrorHandler = window.onerror; // save old error handler

window.onerror = function() { // install new error handler
	var msg = arguments[0];
	var url = arguments[1];
	var line = arguments[2];
	var column = null;
	var typeError = null;
	if (arguments.length === 5) {
		column = arguments[3];
		typeError = arguments[4] 
	}
	if (typeError) {
		xlog(typeof typeError.stack);
	}
    Logger.logJsError( msg, url, line );
    Logger.logToServer(msg, url, line, typeError);

    if( Logger.oldErrorHandler ) {
    	return Logger.oldErrorHandler( msg, url, line );
    }

    return false;
}

$(document).ajaxError( function( event, request, settings, exception ) {
   Logger.logMsg( "** Ajax Error: " + settings.url + " - " + exception + '<br/><br/>');
});

$(document).ready(function() {
	if (W.isUnderDevelopMode) {
		Logger.ready();
	}
});