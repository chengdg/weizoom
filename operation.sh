#!/bin/bash
function enter_current_dir() {
	THIS="$0"
	THIS=`dirname "$THIS"`
	cd $THIS
	THIS="`pwd`"
	echo "enter : `pwd`" 1>&2
}

OLD_DIR="`pwd`"
enter_current_dir

	function get_status() {
	pid=`cat weapp.pid`
	proc=`ps -ef|grep -v grep|grep ' '$pid' ' |wc -l`
	if [ $proc -gt 0 ]; then
		STATUS=running
	else
		STATUS=stoped
	fi
	echo uwsgi is $STATUS
}

function wait_stop() {
	get_status
	
	while [ "$STATUS" = "running" ]
	do
		echo 'sleep 2 seconds to wait the stop operation finished...'
		sleep 2
		get_status
	done
}

function show_info() {
	INFO=`python status.py detail`
	echo "$INFO"
}

function get_operation_action() {
	echo "start"
	echo "stop"
	echo "update"
	echo "restart"
	echo "info"
}

function update() {
	cd weapp
	echo "now enter `pwd`"
	svn up
	cd ..
	echo "now return to `pwd`"
	do_stop
	do_start
}

function do_stop() {
	uwsgi --stop weapp.pid
	wait_stop
}

function do_start() {
	uwsgi --ini weapp.ini
}

function do_restart() {
	uwsgi --reload weapp.pid
}

CMD=$1
shift

if [ "$CMD" = "status" ]; then
	get_status
elif [ "$CMD" = "actions" ]; then
	get_operation_action
elif [ "$CMD" = "update" ]; then
	update
elif [ "$CMD" = "stop" ]; then
	do_stop
elif [ "$CMD" = "start" ]; then
	do_start
elif [ "$CMD" = "restart" ]; then
	do_restart
elif [ "$CMD" = "info" ]; then
	show_info
else
	echo "unknown command"
fi

cd $OLD_DIR
echo "return to `pwd`" 1>&2
