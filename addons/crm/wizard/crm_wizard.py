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
<form string="Create Menus For Cases">
    <separator string="Base Information" colspan="4"/>
    <field name="menu_name"/>
    <field name="menu_parent_id"/>
    <field name="section_id"/>
    <separator string="Select Views (empty for default)" colspan="4"/>
    <field name="view_form"/>
    <field name="view_tree"/>
    <field name="view_calendar"/>
</form>'''

section_fields = {
    'menu_name': {'string':'Base Menu Name', 'type':'char', 'required':True, 'size':64},
    'menu_parent_id': {'string':'Parent Menu', 'type':'many2one', 'relation':'ir.ui.menu', 'required':True},
    'section_id': {'string':'Case Section', 'type':'many2one', 'relation':'crm.case.section', 'required':True},
    'view_form': {'string':'Form View', 'type':'many2one', 'relation':'ir.ui.view', 'domain':[('type','=','form'),('model','=','crm.case')] },
    'view_tree': {'string':'Tree View', 'type':'many2one', 'relation':'ir.ui.view', 'domain':[('type','=','tree'),('model','=','crm.case')] },
    'view_calendar': {'string':'Calendar View', 'type':'many2one', 'relation':'ir.ui.view', 'domain':[('type','=','calendar'),('model','=','crm.case')] }
}

menu_lst = [
    (1,'My ',"[('section_id','=',SECTION_ID),('user_id','=',uid)]", 0, 'form,tree'),
    (2,'My Unclosed ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('state','<>','cancel'), ('state','<>','done')]", 1, 'tree,form'),
    (5,'My Open ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('state','=','open')]", 2, 'tree,form'),
    (6,'My Pending ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('state','=','pending')]", 2, 'tree,form'),
    (7,'My Draft ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('state','=','draft')]", 2, 'tree,form'),
    (3,'My Late ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('date_deadline','<=',time.strftime('%Y-%m-%d')), ('state','<>','cancel'), ('state','<>','done')]", 1, 'tree,form'),
    (4,'My Canceled ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('state','=','cancel')]", 1, 'no'),
    (8,'All ',"[('section_id','=',SECTION_ID),]", 0, 'tree,form'),
    (9,'All Unassigned ',"[('section_id','=',SECTION_ID),('user_id','=',False)]", 8, 'no'),
    (10,'All Late ',"[('section_id','=',SECTION_ID),('user_id','=',uid), ('date_deadline','<=',time.strftime('%Y-%m-%d')), ('state','<>','cancel'), ('state','<>','done')]", 8, 'no'),
    (11,'All Canceled ',"[('section_id','=',SECTION_ID),('state','=','cancel')]", 8, 'no'),
    (12,'All Unclosed ',"[('section_id','=',SECTION_ID),('state','<>','cancel'), ('state','<>','done')]", 8, 'tree,form'),
    (13,'All Open ',"[('section_id','=',SECTION_ID),('state','=','open')]", 12, 'tree,form'),
    (14,'All Pending ',"[('section_id','=',SECTION_ID),('state','=','pending')]", 12, 'tree,form'),
    (15,'All Draft ',"[('section_id','=',SECTION_ID),('state','=','draft')]", 12, 'tree,form'),
    (16,'All Unclosed and Unassigned ',"[('section_id','=',SECTION_ID),('user_id','=',False),('state','<>','cancel'),('state','<>','done')]", 12, 'no')
]

section_menu_form = '''<?xml version="1.0"?>
<form string="Created Menus" width="800">
    <separator string="Update The Proposed Menus To Be Created" colspan="4"/>
''' + '\n'.join(map(lambda x: '\t<field name="menu%d" colspan="3"/> <field name="menu%d_option" nolabel="1"/>' % (x[0],x[0]), menu_lst)) + '''\n</form>'''

section_menu_fields = { }
for menu in menu_lst:
    section_menu_fields['menu'+str(menu[0])] = {
        'string': menu[1],
        'type': 'char',
        'size': 64,
        'required': True
    }
    section_menu_fields['menu'+str(menu[0])+'_option'] = {
        'string': menu[1],
        'type': 'selection',
        'selection': [
            ('no',"Don't Create"),
            ('form,tree','New Form'),
            ('form,tree,calendar','New With Calendar'),
            ('tree,form','List'),
            ('tree,form,calendar','List With Calendar'),
            ('calendar,tree,form','Calendar'),
        ],
        'size': 64,
        'required': True,
    }

def case_menu_create(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    pool.get('crm.case.section').menu_create_data(cr, uid, data['form'], menu_lst, context)
    return {}

def _menu_default(self, cr, uid, data, context):
    result = {}
    for menu in menu_lst:
        result['menu'+str(menu[0])] = menu[1] + data['form']['menu_name']
        result['menu'+str(menu[0])+'_option'] = menu[4]
    return result

class wizard_section_menu_create(wizard.interface):
    states = {
        'init': {
            'actions': [], 
            'result': {'type':'form', 'arch':section_form, 'fields':section_fields, 'state':[('end','Cancel'),('design_menu','Create menu Entries')]}
        },
        'design_menu': {
            'actions': [_menu_default], 
            'result': {
                'type':'form', 
                'arch':section_menu_form, 
                'fields':section_menu_fields, 
                'state':[
                    ('end','Cancel'),
                    ('create','Create menu Entries')
                ]
            }
        },
        'create': {
            'actions': [case_menu_create],
            'result': {'type':'state', 'state':'end'}
        }
    }
wizard_section_menu_create('crm.case.section.menu')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

