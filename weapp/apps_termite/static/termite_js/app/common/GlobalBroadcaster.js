/*
Copyright (c) 2011-2012 Weizoom Inc
*/

W.common.GlobalBroadcaster = {};
_.extend(W.common.GlobalBroadcaster, Backbone.Events);
W.common.GlobalBroadcaster.backboneTrigger = W.common.GlobalBroadcaster.trigger;
W.common.GlobalBroadcaster.trigger = function() {
	var eventName = arguments[0];
	if (eventName !== 'component:drag') {
		xlog('>>>>>>>>>>>>>>>>>>>> broadcaster event');
		xlog(arguments);
		xlog('<<<<<<<<<<<<<<<<<<<< broadcaster event');
	}
	W.common.GlobalBroadcaster.backboneTrigger.apply(this, arguments);
}
W.Broadcaster = W.common.GlobalBroadcaster;