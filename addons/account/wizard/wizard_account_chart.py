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

import wizard
import pooler

class wizard_account_chart(wizard.interface):
    _account_chart_arch = '''<?xml version="1.0"?>
    <form string="Account charts">
        <field name="fiscalyear"/>
        <field name="target_move"/>
    </form>'''
    
    _account_chart_fields = {
            'fiscalyear': {
                'string': 'Fiscal year',
                'type': 'many2one',
                'relation': 'account.fiscalyear',
                'help': 'Keep empty for all open fiscal year',
        },
            'target_move': {
                'string': 'Target Moves', 
                'type': 'selection', 
                'selection': [('all','All Entries'),('posted_only','All Posted Entries')], 
                'required': True, 
                'default': lambda *a:"all",
        },
    }

    def _get_defaults(self, cr, uid, data, context):
        fiscalyear_obj = pooler.get_pool(cr.dbname).get('account.fiscalyear')
        data['form']['fiscalyear'] = fiscalyear_obj.find(cr, uid)
        return data['form']


    def _account_chart_open_window(self, cr, uid, data, context):
        mod_obj = pooler.get_pool(cr.dbname).get('ir.model.data')
        act_obj = pooler.get_pool(cr.dbname).get('ir.actions.act_window')

        result = mod_obj._get_id(cr, uid, 'account', 'action_account_tree')
        id = mod_obj.read(cr, uid, [result], ['res_id'])[0]['res_id']
        result = act_obj.read(cr, uid, [id])[0]
        result['context'] = str({'fiscalyear': data['form']['fiscalyear'],'target_move':data['form']['target_move']})
        return result

    states = {
        'init': {
            'actions': [_get_defaults],
            'result': {'type': 'form', 'arch':_account_chart_arch, 'fields':_account_chart_fields, 'state': [('end', 'Cancel'), ('open', 'Open Charts')]}
        },
        'open': {
            'actions': [],
            'result': {'type': 'action', 'action':_account_chart_open_window, 'state':'end'}
        }
    }
wizard_account_chart('account.chart')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

