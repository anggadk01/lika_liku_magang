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


import time
import wizard
import osv
import pooler

section_form = '''<?xml version="1.0"?>
<form string="Create Menu For Dashboard">
    <separator string="Menu Information" colspan="4"/>
    <field name="menu_name"/>
    <field name="menu_parent_id"/>
</form>'''

section_fields = {
    'menu_name': {'string':'Menu Name', 'type':'char', 'required':True, 'size':64},
    'menu_parent_id': {'string':'Parent Menu', 'type':'many2one', 'relation':'ir.ui.menu', 'required':True},
}

def board_menu_create(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    board = pool.get('board.board').browse(cr, uid, data['id'])
    action_id = pool.get('ir.actions.act_window').create(cr, uid, {
        'name': board.name,
        'view_type':'form',
        'view_mode':'form',
        'context': "{'view':%d}" % (board.id,),
        'res_model': 'board.board'
    })
    pool.get('ir.ui.menu').create(cr, uid, {
        'name': data['form']['menu_name'],
        'parent_id': data['form']['menu_parent_id'],
        'icon': 'STOCK_SELECT_COLOR',
        'action': 'ir.actions.act_window,'+str(action_id)
    }, context)
    return {}

class wizard_section_menu_create(wizard.interface):
    states = {
        'init': {
            'actions': [], 
            'result': {'type':'form', 'arch':section_form, 'fields':section_fields, 'state':[('end','Cancel'),('create_menu','Create Menu')]}
        },
        'create_menu': {
            'actions': [board_menu_create], 
            'result': {
                'type':'state', 
                'state':'end'
            }
        }
    }
wizard_section_menu_create('board.board.menu.create')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

