/**
 * 广播管理器
 * @class
 */
W.design.Broadcaster = function() {
    this.localBroadcaster = {};
    this.parentBroadcaster = null;
    // 将Backbone.Events的属性复制到localBroadcaster
    _.extend(this.localBroadcaster, Backbone.Events);
};

// Underscore的用法: _.extend(destination, *sources)
// 将sources中的属性复制到destination，返回destination。
_.extend(W.design.Broadcaster.prototype, {
    on: function() {
        // console.log("in Broadcaster.on()");
        this.localBroadcaster.on.apply(this.localBroadcaster, arguments);
    },

    trigger: function() {
        if (this.parentBroadcaster) {
            this.parentBroadcaster.trigger.apply(this.parentBroadcaster, arguments);
        } else {
            xwarn('[design broadcaster]: no this.parentBroadcaster, dispatch to localBroadcaster');
            this.localBroadcaster.trigger.apply(this.localBroadcaster, arguments);
        }
    },

    parentEventHandler: function() {
        this.localBroadcaster.trigger.apply(this.localBroadcaster, arguments);
    },

    attach: function() {
        if (parent && parent !== window) {
            xlog('[design broadcaster]: + attach to parent W.Broadcaster');
            this.parentBroadcaster = parent.W.Broadcaster;
            this.parentBroadcaster.on('all', this.parentEventHandler, this);
        }
        $(window).unload(function() {
            W.Broadcaster.detach();
        });
    },

    detach: function() {
        if (this.parentBroadcaster) {
            xwarn('[design broadcaster]: - detach from parent W.Broadcaster');
            this.parentBroadcaster.off('all', this.parentEventHandler, this);
            this.parentBroadcaster = null;
        } else {
            xwarn('[design broadcaster]: no this.parentBroadcaster');
        }
    }
});

W.Broadcaster = new W.design.Broadcaster();