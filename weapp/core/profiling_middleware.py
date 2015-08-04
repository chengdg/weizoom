#coding: utf8
"""@package core.profiling_middleware
Profiling中间件(Yet Another Profiling Middleware)

开启之后，在每个页面末尾会添加profiling结果。

Adapted from this: http://www.no-ack.org/2010/12/yet-another-profiling-middleware-for.html
Settings:
* `PROFILE_MIDDLEWARE_SORT`: A list of criteria according to which the profiler stats will be sorted. Equivalent to [Stats.sort_stats](http://docs.python.org/library/profile.html#pstats.Stats.sort_stats).
* `PROFILE_MIDDLEWARE_RESTRICTIONS`: A list of restrictions used to limit the profiler stats. Each restriction is either an integer (to select a count of lines) or a decimal fraction between 0.0 and 1.0 inclusive (to select a percentage of lines), or a regular expression (to pattern match the standard name that is printed). Equivalent to the arguments passed to [Stats.print_stats](http://docs.python.org/library/profile.html#pstats.Stats.print_stats).
* `PROFILE_MIDDLEWARE_STRIP_DIRS`: If set to True, removes all leading path information from filenames in the profiler stats. Equivalent to [Stats.strip_dirs](http://docs.python.org/library/profile.html#pstats.Stats.strip_dirs).
* `PROFILE_MIDDLEWARE_JSON`: Enable the output for JSON responses.
* `ENABLE_PROFILE`: Enable the middleware.

@see https://gist.github.com/versae/4012267

@see https://code.djangoproject.com/wiki/ProfilingDjango

"""

import os
import re
import tempfile
from cStringIO import StringIO
from cProfile import Profile
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from json import dumps
from django.utils.html import escape

COMMENT_SYNTAX = (
    (re.compile(r'^application/(.*\+)?xml|text/html$', re.I),
     '<!--', '-->'),
)
JAVASCRIPT_SYNTAX = (
    (re.compile(r'^application/(.*\+)?xml|text/html$', re.I),
     '', ''),
)
if getattr(settings, "PROFILE_MIDDLEWARE_JSON", True):
    COMMENT_SYNTAX += (
        (re.compile(r'^application/j(avascript|son)$', re.I),
         '/*', '*/'),
    )


JSFUNC = '''


    $(document).ready(function(){
        $('html body').prepend('<div id="mainChart" style="height:100%;width:50%;background:grey;position:fixed;top:0"></div>');
        var ChartOptions = {
            div: 'mainChart',
            title: 'WEAPP 性能剖析',
            title_link: '',
            subtext: 'URL:数据',
            subtext_link:'',
            backgroundColor:0,
            name: '函数调用',
            nodes: [],
            links: [],
            ctgls: [
                {name:'内建函数', symbol:'diamond'},
                {name:'weapp 模板　层'},
                {name:'weapp 数据库 层'},
                {name:'weapp 辅助　层'},
                {name:'weapp - 预留 层'},
                {name:'MySQLdb数据'},
                {name:'Django - DB 层'},
                {name:'Django　- 模板 层'},
                {name:'Django　- 辅助 层'},
                {name:'/usr/lib 库函数'},
                {name:'其他库函数'},
            ],
            path:'/static/js/echarts-all.js',
            mods:[
                'echarts',
                'echarts/chart/line',   // 按需加载所需图表，如需动态类型切换功能，别忘了同时加载相应图表
                'echarts/chart/bar',
                'echarts/chart/pie',
                'echarts/chart/force',
                'echarts/chart/chord',
            ],
            formatter: function(n){
               var v = n.data;
               var seriesName = this.seriesName; // "函数调用"
               var series = this.series;
               var ret = v.perf + '<br/>' + n[0] + ':' +  n[1] + '<br/>';
               ret += '调用者：';
                _.map(v.callers, function(c){
                    var idx_caller = c[0];
                    ret += '<br/>&nbsp;&nbsp;&nbsp;&nbsp;' + idx_caller;
                });
                return ret;
            },
            clicker: function(param) {
                switch (param.dataIndex) {
                }
            },
            zventer: function(e){
                var o = e.target;
                var x = this;

            }
        }

    function __W_DBG_parseProfs(json, ChartOptions) {
        var  all_nodes = ChartOptions.nodes;
        var  all_links = ChartOptions.links;
        var has_subs  = function(str, subs){ return (str && (str.IndexOf(subs) > -1) ) ? true : false; }
        var get_name = function(v){
            var fname = v[6];
            if(fname && fname[0] == '<' && fname.indexOf("<method '") === 0){
                fname.replace(/\<method\ \'([a-zA-Z_]+)\'\ of\ \'([a-zA-Z_\.]+)\'.*/, function($0, $1, $2){ return $2 + '.' + $1; } );
                return fname;
            }
        };
        var get_ctgr = function(v){
            var mod = v[4];
            if (mod == '~')return 0;
            if (mod.indexOf('/weapp/',0)>-1){
                if (mod.indexOf('/template',0)>-1)return 1;
                if (mod.indexOf('/db',0)>-1)return 2;
                return 3;
                return 4;
            }
            if (mod.indexOf('/MySQLdb/',0)>-1)return 5;
            if (mod.indexOf('/django/',0)>-1){
                if (mod.indexOf('/django/db/',0)>-1)return 6;
                if (mod.indexOf('/django/template/',0)>-1)return 7;
                return 8;
            };
            return 9;
        };

        _.map(json.funcmap, function(v, k){
//        for entry in entries:
//            func = label(entry.code)
//            nc = entry.callcount         # ncalls column of pstats (before '/')
//            cc = nc - entry.reccallcount # ncalls column of pstats (after '/')
//            tt = entry.inlinetime        # tottime column of pstats
//            ct = entry.totaltime         # cumtime column of pstats
//            callers = {}
//            self.stats[func] = cc, nc, tt, ct, callers

            var perf = '调用次数:' + v[0]+', 递归次数:'+ v[1] +  ', 共耗时间:' + (v[2]*1000) + '毫秒' +  ', 累计时值:' + (v[3]*1000) + '毫秒';
            var callers = json.callmap[k];
            var n = {category:get_ctgr(v), name:k ,value: v[2], label:v[6], perf:perf, callers:callers};
            all_nodes.push(n);
        });

        _.map(json.callmap, function(callers, k){
            var idx_callee = k;
            var val_callee = json.funcmap[k];
            _.map(callers, function(c){
                var idx_caller = c[0];
                var val_caller = c[1];
                all_links.push({source:idx_caller, target:idx_callee, weight:(val_callee[2]+val_caller[2]) });
            });
        });

        __w_DBG_renderChart(ChartOptions);
    }

        function __w_DBG_renderChart(cos){
            dom = document.getElementById(cos.div);
            if (dom === null){
                alert('错误: DOM节点 "'+ cos.div + '" 不存在! 请检查参数中 "div" 的值是否正确，　并创建该节点．');
                return null;
            };
            var lengendData = [];
            for (i in cos.ctgls){ lengendData.push(cos.ctgls[i].name);};
            var cos = {
                div: cos.div,
                mods: cos.mods,
                path: cos.path,
                title : {text: cos.title, link:cos.title_link, subtext: cos.subtext, sublink:cos.subtext_link, x:'right', y:'bottom'},
                tooltip : {trigger: 'item', formatter: cos.formatter},
                toolbox: {show : true, feature : {restore : {show: true}, magicType: {show: true, type: ['force']}, saveAsImage : {show: true}}},
                legend: {x: 'left', data:lengendData},
                series : [{type:'force', draggable:true, ribbonType:false, minRadius:10, maxRadius : 50, gravity: 1.5, scaling: 1.2,
                            steps:10,coolDown: 0.9,linkSymbol: 'arrow',
                        roam:true,
                        itemStyle: {
                            normal: {label:{show:true,textStyle:{color:'#333'}},
                                nodeStyle : {brushType:'both',borderColor:'rgba(255,215,0,0.4)',borderWidth:1}},
                            emphasis: {
                                label: {show:true},
                                nodeStyle : {},
                                linkStyle : {width:0.2},
                            }
                        },
                        nodes:cos.nodes,
                        links:cos.links,
                        categories:cos.ctgls,
                        name:cos.name,
                    }],
                clicker: cos.clicker,
                zventer: cos.zventer,
            };

            var isBtnRefresh = false;
            var needRefresh = true;
            var requireCallback = function(ec) {
                echarts = ec;
                refresh();
            }
            var refresh = function (){
                if (isBtnRefresh) {
                    needRefresh = true;
                    focusGraphic();
                    return;
                }
                needRefresh = false;
                chart = echarts.init(document.getElementById(cos.div));
                chart.on(echarts.config.EVENT.CLICK, cos.clicker);
                window.onresize = chart.resize;
                chart.setOption(cos, true);
                chart.zrender = chart.getZrender();
                chart.zrender.on('click', cos.zventer);
                window.weapp_prof_json.chart = chart;
            }
            var autoResize = function() {
                focusGraphic();
            }
            var focusGraphic = function () {
                if (needRefresh) {
                    chart.showLoading();
                    setTimeout(refresh, 100);
                };
            };
    //        require.config({paths:{echarts: cos.path}});
    //      require(cos.mods, requireCallback);
            requireCallback(echarts);
        }


        __W_DBG_parseProfs(window.weapp_prof_json, ChartOptions);
        });



'''

class ProfileMiddleware(object):

    def __init__(self):
        self.profile = Profile()
        self.prefix = settings.PROJECT_HOME
        self.path_info = ''
        if not getattr(settings, "ENABLE_PROFILE", True):
            raise MiddlewareNotUsed("Profiling middleware not used")

    def process_view(self, request, callback, args, kwargs):
        if 'prof' not in request.GET:
            return None

        profile = self.profile
        exception = False
        stats = None
        try:
            # Profile the call of the view function.
            response = profile.runcall(callback, request, *args, **kwargs)
            if response.status_code // 100 == 3:
                return response
            for regex, begin_comment, end_comment in COMMENT_SYNTAX:
                split_response = response['Content-Type'].split(';')
                if regex.match(split_response[0].strip()):
                    break
            else:
                return response
            content = profile.runcall(response.__class__.content.fget, response)
            profile.snapshot_stats()
        except:
            exception = True
            profile = None
            raise
        if not profile.stats:
            return  None
        index = lambda (mod,lineno,name): '%s:%s:%s' % (mod,lineno,name)
        callmap = {}
        funcmap = dict([(index(k), list(v[:4])+list(k))  for k,v in profile.stats.iteritems()])
        prim_calls  =0
        total_calls =0
        total_time  =0
        cumul_time  =0
        for k,v in profile.stats.iteritems():
            prim_calls  += v[0]# 非递归调用次数
            total_calls += v[1]# 含递归
            total_time  += v[2]# 总时间
            cumul_time  += v[3]# 权重时间
            idx_callee  = index(k)
            val_callee  = funcmap[idx_callee]
            for c,i in v[4].items():
                idx_caller = index(c)
                val_caller = list(i) + list(c)
                if idx_caller not in funcmap:
                    funcmap[idx_caller] = val_caller
                    print 'got V: %s, Called: %s' % (idx_caller, index(k))
                if not callmap.has_key(idx_callee):
                    callmap[idx_callee] = [(idx_caller, val_callee[3]+val_caller[3])]
                else:
                    callmap[idx_callee].append((idx_caller, val_callee[3]+val_caller[3]))
        stats = dict([ (id(k), v[:4])  for k,v in profile.stats.iteritems()])
        jsons = dumps({'stats': stats, 'callmap': callmap, 'funcmap':funcmap, 
                        'prim_calls' :prim_calls, 
                        'total_calls':total_calls, 
                        'total_time' :total_time,  
                        'cumul_time' :cumul_time, 
                       'path':request.path_info})
        
        file('/tmp/prof.log', 'w').write('\n%s\n'%jsons)
        jsonprof = '''
        <script src="http://echarts.baidu.com/build/dist/echarts.js"></script>
        <script>
        window.weapp_jsonprof=%s;

        %s;
        </script>
        
        ''' % (jsons, JSFUNC)
#        if getattr(settings, 'PROFILE_MIDDLEWARE_STRIP_DIRS', False):
#            stats.strip_dirs()
#        if getattr(settings, 'PROFILE_MIDDLEWARE_SORT', None):
#            stats.sort_stats(*settings.PROFILE_MIDDLEWARE_SORT)
        response.content = content + jsonprof
        if response.has_header('Content-Length'):
            content_lenght = int(response['Content-Length']) + len(jsonprof)
            response['Content-Length'] = content_lenght
        return response



import sys
import os
import time
import marshal
import re
from functools import cmp_to_key

class Stats:
    def __init__(self, *args, **kwds):
        # I can't figure out how to explictly specify a stream keyword arg
        # with *args:
        #   def __init__(self, *args, stream=sys.stdout): ...
        # so I use **kwds and sqauwk if something unexpected is passed in.
        self.stream = sys.stdout
        if "stream" in kwds:
            self.stream = kwds["stream"]
            del kwds["stream"]
        if kwds:
            keys = kwds.keys()
            keys.sort()
            extras = ", ".join(["%s=%s" % (k, kwds[k]) for k in keys])
            raise ValueError, "unrecognized keyword args: %s" % extras
        if not len(args):
            arg = None
        else:
            arg = args[0]
            args = args[1:]
        self.init(arg)
        self.add(*args)

    def init(self, arg):
        self.all_callees = None  # calc only if needed
        self.files = []
        self.fcn_list = None
        self.total_tt = 0
        self.total_calls = 0
        self.prim_calls = 0
        self.max_name_len = 0
        self.top_level = {}
        self.stats = {}
        self.sort_arg_dict = {}
        self.load_stats(arg)
        trouble = 1
        try:
            self.get_top_level_stats()
            trouble = 0
        finally:
            if trouble:
                print >> self.stream, "Invalid timing data",
                if self.files: print >> self.stream, self.files[-1],
                print >> self.stream

    def load_stats(self, arg):
        if not arg:  self.stats = {}
        elif isinstance(arg, basestring):
            f = open(arg, 'rb')
            self.stats = marshal.load(f)
            f.close()
            try:
                file_stats = os.stat(arg)
                arg = time.ctime(file_stats.st_mtime) + "    " + arg
            except:  # in case this is not unix
                pass
            self.files = [ arg ]
        elif hasattr(arg, 'create_stats'):
            arg.create_stats()
            self.stats = arg.stats
            arg.stats = {}
        if not self.stats:
            raise TypeError("Cannot create or construct a %r object from %r"
                            % (self.__class__, arg))
        return

    def get_top_level_stats(self):
        for func, (cc, nc, tt, ct, callers) in self.stats.items():
            self.total_calls += nc
            self.prim_calls  += cc
            self.total_tt    += tt
            if ("jprofile", 0, "profiler") in callers:
                self.top_level[func] = None
            if len(func_std_string(func)) > self.max_name_len:
                self.max_name_len = len(func_std_string(func))

    def add(self, *arg_list):
        if not arg_list: return self
        if len(arg_list) > 1: self.add(*arg_list[1:])
        other = arg_list[0]
        if type(self) != type(other) or self.__class__ != other.__class__:
            other = Stats(other)
        self.files += other.files
        self.total_calls += other.total_calls
        self.prim_calls += other.prim_calls
        self.total_tt += other.total_tt
        for func in other.top_level:
            self.top_level[func] = None

        if self.max_name_len < other.max_name_len:
            self.max_name_len = other.max_name_len

        self.fcn_list = None

        for func, stat in other.stats.iteritems():
            if func in self.stats:
                old_func_stat = self.stats[func]
            else:
                old_func_stat = (0, 0, 0, 0, {},)
            self.stats[func] = add_func_stats(old_func_stat, stat)
        return self

    def dump_stats(self, filename):
        """Write the profile data to a file we know how to load back."""
        f = file(filename, 'wb')
        try:
            marshal.dump(self.stats, f)
        finally:
            f.close()

    # list the tuple indices and directions for sorting,
    # along with some printable description
    sort_arg_dict_default = {
              "calls"     : (((1,-1),              ), "call count"),
              "ncalls"    : (((1,-1),              ), "call count"),
              "cumtime"   : (((3,-1),              ), "cumulative time"),
              "cumulative": (((3,-1),              ), "cumulative time"),
              "file"      : (((4, 1),              ), "file name"),
              "filename"  : (((4, 1),              ), "file name"),
              "line"      : (((5, 1),              ), "line number"),
              "module"    : (((4, 1),              ), "file name"),
              "name"      : (((6, 1),              ), "function name"),
              "nfl"       : (((6, 1),(4, 1),(5, 1),), "name/file/line"),
              "pcalls"    : (((0,-1),              ), "primitive call count"),
              "stdname"   : (((7, 1),              ), "standard name"),
              "time"      : (((2,-1),              ), "internal time"),
              "tottime"   : (((2,-1),              ), "internal time"),
              }

    def get_sort_arg_defs(self):
        """Expand all abbreviations that are unique."""
        if not self.sort_arg_dict:
            self.sort_arg_dict = dict = {}
            bad_list = {}
            for word, tup in self.sort_arg_dict_default.iteritems():
                fragment = word
                while fragment:
                    if not fragment:
                        break
                    if fragment in dict:
                        bad_list[fragment] = 0
                        break
                    dict[fragment] = tup
                    fragment = fragment[:-1]
            for word in bad_list:
                del dict[word]
        return self.sort_arg_dict

    def sort_stats(self, *field):
        if not field:
            self.fcn_list = 0
            return self
        if len(field) == 1 and isinstance(field[0], (int, long)):
            # Be compatible with old profiler
            field = [ {-1: "stdname",
                       0:  "calls",
                       1:  "time",
                       2:  "cumulative"}[field[0]] ]

        sort_arg_defs = self.get_sort_arg_defs()
        sort_tuple = ()
        self.sort_type = ""
        connector = ""
        for word in field:
            sort_tuple = sort_tuple + sort_arg_defs[word][0]
            self.sort_type += connector + sort_arg_defs[word][1]
            connector = ", "

        stats_list = []
        for func, (cc, nc, tt, ct, callers) in self.stats.iteritems():
            stats_list.append((cc, nc, tt, ct) + func +
                              (func_std_string(func), func))

        stats_list.sort(key=cmp_to_key(TupleComp(sort_tuple).compare))

        self.fcn_list = fcn_list = []
        for tuple in stats_list:
            fcn_list.append(tuple[-1])
        return self

    def reverse_order(self):
        if self.fcn_list:
            self.fcn_list.reverse()
        return self

    def strip_dirs(self):
        oldstats = self.stats
        self.stats = newstats = {}
        max_name_len = 0
        for func, (cc, nc, tt, ct, callers) in oldstats.iteritems():
            newfunc = func_strip_path(func)
            if len(func_std_string(newfunc)) > max_name_len:
                max_name_len = len(func_std_string(newfunc))
            newcallers = {}
            for func2, caller in callers.iteritems():
                newcallers[func_strip_path(func2)] = caller

            if newfunc in newstats:
                newstats[newfunc] = add_func_stats(
                                        newstats[newfunc],
                                        (cc, nc, tt, ct, newcallers))
            else:
                newstats[newfunc] = (cc, nc, tt, ct, newcallers)
        old_top = self.top_level
        self.top_level = new_top = {}
        for func in old_top:
            new_top[func_strip_path(func)] = None

        self.max_name_len = max_name_len

        self.fcn_list = None
        self.all_callees = None
        return self

    def calc_callees(self):
        if self.all_callees: return
        self.all_callees = all_callees = {}
        for func, (cc, nc, tt, ct, callers) in self.stats.iteritems():
            if not func in all_callees:
                all_callees[func] = {}
            for func2, caller in callers.iteritems():
                if not func2 in all_callees:
                    all_callees[func2] = {}
                all_callees[func2][func]  = caller
        return

    #******************************************************************
    # The following functions support actual printing of reports
    #******************************************************************

    # Optional "amount" is either a line count, or a percentage of lines.

    def eval_print_amount(self, sel, list, msg):
        new_list = list
        if isinstance(sel, basestring):
            try:
                rex = re.compile(sel)
            except re.error:
                msg += "   <Invalid regular expression %r>\n" % sel
                return new_list, msg
            new_list = []
            for func in list:
                if rex.search(func_std_string(func)):
                    new_list.append(func)
        else:
            count = len(list)
            if isinstance(sel, float) and 0.0 <= sel < 1.0:
                count = int(count * sel + .5)
                new_list = list[:count]
            elif isinstance(sel, (int, long)) and 0 <= sel < count:
                count = sel
                new_list = list[:count]
        if len(list) != len(new_list):
            msg += "   List reduced from %r to %r due to restriction <%r>\n" % (
                len(list), len(new_list), sel)

        return new_list, msg

    def get_print_list(self, sel_list):
        width = self.max_name_len
        if self.fcn_list:
            stat_list = self.fcn_list[:]
            msg = "   Ordered by: " + self.sort_type + '\n'
        else:
            stat_list = self.stats.keys()
            msg = "   Random listing order was used\n"

        for selection in sel_list:
            stat_list, msg = self.eval_print_amount(selection, stat_list, msg)

        count = len(stat_list)

        if not stat_list:
            return 0, stat_list
        print >> self.stream, msg
        if count < len(self.stats):
            width = 0
            for func in stat_list:
                if  len(func_std_string(func)) > width:
                    width = len(func_std_string(func))
        return width+2, stat_list

    def print_stats(self, *amount):
        for filename in self.files:
            print >> self.stream, filename
        if self.files: print >> self.stream
        indent = ' ' * 8
        for func in self.top_level:
            print >> self.stream, indent, func_get_function_name(func)

        print >> self.stream, indent, self.total_calls, "function calls",
        if self.total_calls != self.prim_calls:
            print >> self.stream, "(%d primitive calls)" % self.prim_calls,
        print >> self.stream, "in %.3f seconds" % self.total_tt
        print >> self.stream
        width, list = self.get_print_list(amount)
        if list:
            self.print_title()
            for func in list:
                self.print_line(func)
            print >> self.stream
            print >> self.stream
        return self

    def print_callees(self, *amount):
        width, list = self.get_print_list(amount)
        if list:
            self.calc_callees()

            self.print_call_heading(width, "called...")
            for func in list:
                if func in self.all_callees:
                    self.print_call_line(width, func, self.all_callees[func])
                else:
                    self.print_call_line(width, func, {})
            print >> self.stream
            print >> self.stream
        return self

    def print_callers(self, *amount):
        width, list = self.get_print_list(amount)
        if list:
            self.print_call_heading(width, "was called by...")
            for func in list:
                cc, nc, tt, ct, callers = self.stats[func]
                self.print_call_line(width, func, callers, "<-")
            print >> self.stream
            print >> self.stream
        return self

    def print_call_heading(self, name_size, column_title):
        print >> self.stream, "Function ".ljust(name_size) + column_title
        # print sub-header only if we have new-style callers
        subheader = False
        for cc, nc, tt, ct, callers in self.stats.itervalues():
            if callers:
                value = callers.itervalues().next()
                subheader = isinstance(value, tuple)
                break
        if subheader:
            print >> self.stream, " "*name_size + "    ncalls  tottime  cumtime"

    def print_call_line(self, name_size, source, call_dict, arrow="->"):
        print >> self.stream, func_std_string(source).ljust(name_size) + arrow,
        if not call_dict:
            print >> self.stream
            return
        clist = call_dict.keys()
        clist.sort()
        indent = ""
        for func in clist:
            name = func_std_string(func)
            value = call_dict[func]
            if isinstance(value, tuple):
                nc, cc, tt, ct = value
                if nc != cc:
                    substats = '%d/%d' % (nc, cc)
                else:
                    substats = '%d' % (nc,)
                substats = '%s %s %s  %s' % (substats.rjust(7+2*len(indent)),
                                             f8(tt), f8(ct), name)
                left_width = name_size + 1
            else:
                substats = '%s(%r) %s' % (name, value, f8(self.stats[func][3]))
                left_width = name_size + 3
            print >> self.stream, indent*left_width + substats
            indent = " "

    def print_title(self):
        print >> self.stream, '   ncalls  tottime  percall  cumtime  percall',
        print >> self.stream, 'filename:lineno(function)'

    def print_line(self, func):  # hack : should print percentages
        cc, nc, tt, ct, callers = self.stats[func]
        c = str(nc)
        if nc != cc:
            c = c + '/' + str(cc)
        print >> self.stream, c.rjust(9),
        print >> self.stream, f8(tt),
        if nc == 0:
            print >> self.stream, ' '*8,
        else:
            print >> self.stream, f8(float(tt)/nc),
        print >> self.stream, f8(ct),
        if cc == 0:
            print >> self.stream, ' '*8,
        else:
            print >> self.stream, f8(float(ct)/cc),
        print >> self.stream, func_std_string(func)

class TupleComp:
    """This class provides a generic function for comparing any two tuples.
    Each instance records a list of tuple-indices (from most significant
    to least significant), and sort direction (ascending or decending) for
    each tuple-index.  The compare functions can then be used as the function
    argument to the system sort() function when a list of tuples need to be
    sorted in the instances order."""

    def __init__(self, comp_select_list):
        self.comp_select_list = comp_select_list

    def compare (self, left, right):
        for index, direction in self.comp_select_list:
            l = left[index]
            r = right[index]
            if l < r:
                return -direction
            if l > r:
                return direction
        return 0

#**************************************************************************
# func_name is a triple (file:string, line:int, name:string)

def func_strip_path(func_name):
    filename, line, name = func_name
    return os.path.basename(filename), line, name

def func_get_function_name(func):
    return func[2]

def func_std_string(func_name): # match what old profile produced
    if func_name[:2] == ('~', 0):
        # special case for built-in functions
        name = func_name[2]
        if name.startswith('<') and name.endswith('>'):
            return '{%s}' % name[1:-1]
        else:
            return name
    else:
        return "%s:%d(%s)" % func_name

#**************************************************************************
# The following functions combine statists for pairs functions.
# The bulk of the processing involves correctly handling "call" lists,
# such as callers and callees.
#**************************************************************************

def add_func_stats(target, source):
    """Add together all the stats for two profile entries."""
    cc, nc, tt, ct, callers = source
    t_cc, t_nc, t_tt, t_ct, t_callers = target
    return (cc+t_cc, nc+t_nc, tt+t_tt, ct+t_ct,
              add_callers(t_callers, callers))

def add_callers(target, source):
    """Combine two caller lists in a single list."""
    new_callers = {}
    for func, caller in target.iteritems():
        new_callers[func] = caller
    for func, caller in source.iteritems():
        if func in new_callers:
            if isinstance(caller, tuple):
                # format used by cProfile
                new_callers[func] = tuple([i[0] + i[1] for i in
                                           zip(caller, new_callers[func])])
            else:
                # format used by profile
                new_callers[func] += caller
        else:
            new_callers[func] = caller
    return new_callers

def count_calls(callers):
    """Sum the caller statistics to get total number of calls received."""
    nc = 0
    for calls in callers.itervalues():
        nc += calls
    return nc

#**************************************************************************
# The following functions support printing of reports
#**************************************************************************

def f8(x):
    return "%8.3f" % x
