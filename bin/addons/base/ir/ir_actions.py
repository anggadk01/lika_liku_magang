# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

from osv import fields,osv
import tools
import time

class actions(osv.osv):
    _name = 'ir.actions.actions'
    _table = 'ir_actions'
    _columns = {
        'name': fields.char('Action Name', required=True, size=64),
        'type': fields.char('Action Type', required=True, size=32),
        'usage': fields.char('Action Usage', size=32),
        'parent_id': fields.many2one('ir.actions.server', 'Parent Action'),
    }
    _defaults = {
        'usage': lambda *a: False,
    }
actions()

class report_custom(osv.osv):
    _name = 'ir.actions.report.custom'
    _table = 'ir_act_report_custom'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Report Name', size=64, required=True, translate=True),
        'type': fields.char('Report Type', size=32, required=True),
        'model':fields.char('Model', size=64, required=True),
        'report_id': fields.integer('Report Ref.', required=True),
        'usage': fields.char('Action Usage', size=32),
        'multi': fields.boolean('On multiple doc.', help="If set to true, the action will not be displayed on the right toolbar of a form views.")
    }
    _defaults = {
        'multi': lambda *a: False,
        'type': lambda *a: 'ir.actions.report.custom',
    }
report_custom()

class report_xml(osv.osv):

    def _report_content(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for report in self.browse(cursor, user, ids, context=context):
            data = report[name + '_data']
            if not data and report[name[:-8]]:
                try:
                    fp = tools.file_open(report[name[:-8]], mode='rb')
                    data = fp.read()
                except:
                    data = False
            res[report.id] = data
        return res

    def _report_content_inv(self, cursor, user, id, name, value, arg, context=None):
        self.write(cursor, user, id, {name+'_data': value}, context=context)

    def _report_sxw(self, cursor, user, ids, name, arg, context=None):
        res = {}
        for report in self.browse(cursor, user, ids, context=context):
            if report.report_rml:
                res[report.id] = report.report_rml.replace('.rml', '.sxw')
            else:
                res[report.id] = False
        return res

    _name = 'ir.actions.report.xml'
    _table = 'ir_act_report_xml'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'type': fields.char('Report Type', size=32, required=True),
        'model': fields.char('Model', size=64, required=True),
        'report_name': fields.char('Internal Name', size=64, required=True),
        'report_xsl': fields.char('XSL path', size=256),
        'report_xml': fields.char('XML path', size=256),
        'report_rml': fields.char('RML path', size=256,
            help="The .rml path of the file or NULL if the content is in report_rml_content"),
        'report_sxw': fields.function(_report_sxw, method=True, type='char',
            string='SXW path'),
        'report_sxw_content_data': fields.binary('SXW content'),
        'report_rml_content_data': fields.binary('RML content'),
        'report_sxw_content': fields.function(_report_content,
            fnct_inv=_report_content_inv, method=True,
            type='binary', string='SXW content',),
        'report_rml_content': fields.function(_report_content,
            fnct_inv=_report_content_inv, method=True,
            type='binary', string='RML content'),
        'auto': fields.boolean('Automatic XSL:RML', required=True),
        'usage': fields.char('Action Usage', size=32),
        'header': fields.boolean('Add RML header',
            help="Add or not the coporate RML header"),
        'multi': fields.boolean('On multiple doc.',
            help="If set to true, the action will not be displayed on the right toolbar of a form views."),
        'report_type': fields.selection([
            ('pdf', 'pdf'),
            ('html', 'html'),
            ('raw', 'raw'),
            ('sxw', 'sxw'),
            ], string='Type', required=True),
        'groups_id': fields.many2many('res.groups', 'res_groups_report_rel', 'uid', 'gid', 'Groups')
        
    }
    _defaults = {
        'type': lambda *a: 'ir.actions.report.xml',
        'multi': lambda *a: False,
        'auto': lambda *a: True,
        'header': lambda *a: True,
        'report_sxw_content': lambda *a: False,
        'report_type': lambda *a: 'pdf',
    }

report_xml()

class act_window(osv.osv):
    _name = 'ir.actions.act_window'
    _table = 'ir_act_window'
    _sequence = 'ir_actions_id_seq'

    def _views_get_fnc(self, cr, uid, ids, name, arg, context={}):
        res={}
        for act in self.browse(cr, uid, ids):
            res[act.id]=[(view.view_id.id, view.view_mode) for view in act.view_ids]
            if (not act.view_ids):
                modes = act.view_mode.split(',')
                find = False
                if act.view_id.id:
                    res[act.id].append((act.view_id.id, act.view_id.type))
                for t in modes:
                    if act.view_id and (t == act.view_id.type) and not find:
                        find = True
                        continue
                    res[act.id].append((False, t))

                if 'calendar' not in modes:
                    mobj = self.pool.get(act.res_model)
                    if mobj._date_name in mobj._columns:
                        res[act.id].append((False, 'calendar'))
        return res

    _columns = {
        'name': fields.char('Action Name', size=64, translate=True),
        'type': fields.char('Action Type', size=32, required=True),
        'view_id': fields.many2one('ir.ui.view', 'View Ref.', ondelete='cascade'),
        'domain': fields.char('Domain Value', size=250),
        'context': fields.char('Context Value', size=250),
        'res_model': fields.char('Model', size=64),
        'src_model': fields.char('Source model', size=64),
        'target': fields.selection([('current','Current Window'),('new','New Window')], 'Target Window'),
        'view_type': fields.selection((('tree','Tree'),('form','Form')),string='Type of view'),
        'view_mode': fields.char('Mode of view', size=250),
        'usage': fields.char('Action Usage', size=32),
        'view_ids': fields.one2many('ir.actions.act_window.view', 'act_window_id', 'Views'),
        'views': fields.function(_views_get_fnc, method=True, type='binary', string='Views'),
        'limit': fields.integer('Limit', help='Default limit for the list view'),
        'auto_refresh': fields.integer('Auto-Refresh',
            help='Add an auto-refresh on the view'),
    }
    _defaults = {
        'type': lambda *a: 'ir.actions.act_window',
        'view_type': lambda *a: 'form',
        'view_mode': lambda *a: 'tree,form',
        'context': lambda *a: '{}',
        'limit': lambda *a: 80,
        'target': lambda *a: 'current',
        'auto_refresh': lambda *a: 0,
    }
act_window()

class act_window_view(osv.osv):
    _name = 'ir.actions.act_window.view'
    _table = 'ir_act_window_view'
    _rec_name = 'view_id'
    _columns = {
        'sequence': fields.integer('Sequence'),
        'view_id': fields.many2one('ir.ui.view', 'View'),
        'view_mode': fields.selection((
            ('tree', 'Tree'),
            ('form', 'Form'),
            ('graph', 'Graph'),
            ('calendar', 'Calendar')), string='Type of view', required=True),
        'act_window_id': fields.many2one('ir.actions.act_window', 'Action', ondelete='cascade'),
        'multi': fields.boolean('On multiple doc.',
            help="If set to true, the action will not be displayed on the right toolbar of a form views."),
    }
    _defaults = {
        'multi': lambda *a: False,
    }
    _order = 'sequence'
act_window_view()

class act_wizard(osv.osv):
    _name = 'ir.actions.wizard'
    _table = 'ir_act_wizard'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Wizard info', size=64, required=True, translate=True),
        'type': fields.char('Action type', size=32, required=True),
        'wiz_name': fields.char('Wizard name', size=64, required=True),
        'multi': fields.boolean('Action on multiple doc.', help="If set to true, the wizard will not be displayed on the right toolbar of a form views."),
        'groups_id': fields.many2many('res.groups', 'res_groups_wizard_rel', 'uid', 'gid', 'Groups')
    }
    _defaults = {
        'type': lambda *a: 'ir.actions.wizard',
        'multi': lambda *a: False,
    }
act_wizard()

class act_url(osv.osv):
    _name = 'ir.actions.url'
    _table = 'ir_act_url'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Action Name', size=64, translate=True),
        'type': fields.char('Action Type', size=32, required=True),
        'url': fields.text('Action Url',required=True),
        'target': fields.selection((
            ('new', 'New Window'),
            ('self', 'This Window')),
            'Action Target', required=True
        )
    }
    _defaults = {
        'type': lambda *a: 'ir.actions.act_url',
        'target': lambda *a: 'new'
    }
act_url()

#
# Actions that are run on the server side
#
class actions_server(osv.osv):
    _name = 'ir.actions.server'
    _table = 'ir_act_server'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Action Name', required=True, size=64),
        'state': fields.selection([
            ('python','Python Code'),
            ('dummy','Dummy'),
            ('trigger','Trigger'),
            ('email','Email'),
            ('sms','SMS'),
            ('object_create','Create Object'),
            ('object_write','Write Object'),
            ('client_action','Client Action'),
            ('other','Others Actions'),
        ], 'Action State', required=True, size=32),
        'code': fields.text('Python Code'),
        'sequence': fields.integer('Sequence'),
        'model_id': fields.many2one('ir.model', 'Model', required=True),
        'trigger_name': fields.char('Trigger Name', size=128),
        'trigger_object': fields.char('Trigger Object', size=128),
        'trigger_object_id': fields.char('Trigger Object ID', size=128),
        'message': fields.text('Message', translate=True),
        'address': fields.char('Email Address', size=128),
        'child_ids': fields.one2many('ir.actions.actions', 'parent_id', 'Others Actions'),
        'usage': fields.char('Action Usage', size=32),
        'type': fields.char('Report Type', size=32, required=True),
    }
    _defaults = {
        'state': lambda *a: 'dummy',
        'type': lambda *a: 'ir.actions.server',
        'sequence': lambda *a: 0,
        'code': lambda *a: """# You can use the following variables
#    - object
#    - object2
#    - time
#    - cr
#    - uid
#    - ids
# If you plan to return an action, assign: action = {...}
"""
    }
    #
    # Context should contains:
    #   ids : original ids
    #   id  : current id of the object
    # OUT:
    #   False : Finnished correctly
    #   ACTION_ID : Action to launch
    def run(self, cr, uid, ids, context={}):
        for action in self.browse(cr, uid, ids, context):
            if action.state=='python':
                localdict = {
                    'self': self.pool.get(action.model_id.model),
                    'context': context,
                    'time': time,
                    'ids': ids,
                    'cr': cr,
                    'uid': uid
                }
                print action.code
                exec action.code in localdict
                print localdict.keys()
                if 'action' in localdict:
                    return localdict['action']
        return False
actions_server()

class act_window_close(osv.osv):
    _name = 'ir.actions.act_window_close'
    _table = 'ir_actions'
    _sequence = 'ir_actions_id_seq'
    _columns = {
        'name': fields.char('Action Name', size=64, translate=True),
        'type': fields.char('Action Type', size=32, required=True),
    }
    _defaults = {
        'type': lambda *a: 'ir.actions.act_window_close',
    }
act_window_close()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

