# -*- coding: utf-8 -*-
"""weapp checkers"""
import six

from logilab.common.ureports import VerbatimText, Paragraph

from pylint.interfaces import IAstroidChecker
from pylint.utils import EmptyReport
from pylint.checkers import BaseChecker
from pylint.checkers.imports import make_tree_defs, repr_tree_defs

class WeappChecker(BaseChecker):
    """weapp checkers"""
    __implements__ = IAstroidChecker

    name = 'weapp'
    msgs = {
        'W5101': ('Weapp deprecated import module %r',
            'weapp-deprecated-module',
            'Used a module marked as deprecated is imported.'),
    }
    priority = -2
    options = (
            ('weapp-deprecated-modules',
                {'default' : 'account,admin,apps,captcha,core,deploy,disttool,example,features,help_system,init_db,manage_tools,market_tools,mobile_app,mockapi,modules,notice,operation,order,product,reports,simulator,templates,termite,test,tools,watchdog,weapp,webapp,weixin,wxpay',
                 'type' : 'csv',
                 'metavar' : '<modules>',
                 'help' : ''}
            ),
            ('weapp-except',
                {'default' : 'util',
                 'type' : 'string',
                 'metavar' : '<file.dot>',
                 'help' : ''}
            ),
        )

    def __init__(self, linter=None):
        BaseChecker.__init__(self, linter)
        self.stats = None
        self.import_graph = None
        self.__int_dep_info = self.__ext_dep_info = None
        # self.reports = (('RP0401', 'External dependencies',
        #                  self.report_external_dependencies),
        #                )

    def open(self):
        """called before visiting project (i.e set of modules)"""
        self.stats = self.linter.stats

    def visit_from(self, node):
        """triggered when an import statement is seen"""
        cur_name = node.root().name
        # 以tests结尾的模块不检查
        if cur_name.endswith('tests'):
            return
        # 同模块的引用不检查
        current_index = cur_name.find('.')
        if current_index > 0 and node.modname.startswith(node.root().name[:current_index+1]):
            return
        
        for deprecated in self.config.weapp_deprecated_modules:
            if node.modname.startswith(deprecated) and node.modname.find(self.config.weapp_except) < 0:
                # print '---jz1', node.root().name
                self.add_message('weapp-deprecated-module', node=node, args=node.modname)
                break

    # def report_external_dependencies(self, sect, _, dummy):
    #     """return a verbatim layout for displaying dependencies"""
    #     dep_info = make_tree_defs(six.iteritems(self._external_dependencies_info()))
    #     if not dep_info:
    #         raise EmptyReport()
    #     tree_str = repr_tree_defs(dep_info)
    #     sect.append(VerbatimText(tree_str))

    # def _external_dependencies_info(self):
    #     """return cached external dependencies information or build and
    #     cache them
    #     """
    #     if self.__ext_dep_info is None:
    #         package = self.linter.current_name
    #         self.__ext_dep_info = result = {}
    #         for importee, importers in six.iteritems(self.stats['dependencies']):
    #             if not importee.startswith(package):
    #                 result[importee] = importers
    #     return self.__ext_dep_info

def register(linter):
    """required method to auto register this checker """
    linter.register_checker(WeappChecker(linter))