# -*- coding: iso-8859-1 -*-
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


view_form_end = """<?xml version="1.0"?>
<form string="System upgrade done">
	<separator string="System upgrade done"/>
	<label align="0.0" string="The modules have been upgraded / installed !" colspan="4"/>
	<label align="0.0" string="You may have to reinstall some language pack." colspan="4"/>
	<label align="0.0" string="We suggest you to reload the menu tab (Ctrl+t Ctrl+r)." colspan="4"/>
</form>"""

view_form = """<?xml version="1.0"?>
<form string="System Upgrade">
	<image name="gtk-dialog-info" colspan="2"/>
	<group colspan="2" col="4">
		<label align="0.0" string="Your system will be upgraded." colspan="4"/>
		<label align="0.0" string="Note that this operation my take a few minutes." colspan="4"/>
		<separator string="Modules to update"/>
		<field name="module_info" nolabel="1" colspan="4"/>
		<separator string="Modules to download"/>
		<field name="module_download" nolabel="1" colspan="4"/>
	</group>
</form>"""

view_field = {
	"module_info": {'type': 'text', 'string': 'Modules to update',
		'readonly': True},
	"module_download": {'type': 'text', 'string': 'Modules to download',
		'readonly': True},
}

class module_install_upgrade_start(wizard_osv):
    _name = 'ir.module.module.install_upgrade.start'

module_install_upgrade_start()

class wizard_info_get(wizard.interface):
	def _get_install(self, cr, uid, data, context):
		pool=pooler.get_pool(cr.dbname)
		mod_obj = pool.get('ir.module.module')
		ids = mod_obj.search(cr, uid, [
			('state', 'in', ['to upgrade', 'to remove', 'to install'])])
		res = mod_obj.read(cr, uid, ids, ['name','state'], context)
		url = mod_obj.download(cr, uid, ids, download=False, context=context)
		return {'module_info': '\n'.join(map(lambda x: x['name']+' : '+x['state'], res)),
				'module_download': '\n'.join(url)}

	def _upgrade_module(self, cr, uid, data, context):
		db, pool = pooler.get_db_and_pool(cr.dbname)
		cr = db.cursor()
		mod_obj = pool.get('ir.module.module')
		ids = mod_obj.search(cr, uid, [
			('state', 'in', ['to upgrade', 'to remove', 'to install'])])
		mod_obj.download(cr, uid, ids, context=context)
		cr.commit()
		db, pool = pooler.restart_pool(cr.dbname, update_module=True)
		return {}

	def _config(self, cr, uid, data, context=None):
		return {
                'view_type': 'form',
				'res_model': 'ir.module.module.configuration.wizard',
				'type': 'ir.actions.act_window',
         }

	states = {
		'init': {
			'actions': [_get_install],
			'result': {'type':'form', 'arch':view_form, 'fields': view_field,
				'state':[
					('end', 'Cancel', 'gtk-cancel'),
					('start', 'Start Upgrade', 'gtk-ok', True)
				]
			}
		},
		'start': {
			'actions': [_upgrade_module],
			'result': {
                'type': 'form',
                'object': 'ir.module.module.install_upgrade.start',
                'state': [
                    ('config', 'Ok', 'tryton-ok', True),
                ],
            },
        },
        'config': {
            'result': {
                'type': 'action',
                'action': _config,
                'state': 'end',
            },
        },
    }

wizard_info_get('module.upgrade')

class module_config(wizard.interface):
	def _action_open(self, cr, uid, datas, context=None):
		pool=pooler.get_pool(cr.dbname)
	 	model_data_obj = pool.get('ir.model.data')
	 	act_window_obj = pool.get('ir.actions.act_window')
	 	model_data_ids = model_data_obj.search(cr, uid, [
            ('name', '=', 'open_module_tree'),
            ('module', '=', 'base'),
            ], limit=1, context=context)
	 	model_data = model_data_obj.browse(cr, uid, model_data_ids[0],
                context=context)
	 	res = act_window_obj.read(cr, uid, model_data.res_id, context=context)
	 	return res
	states = {
        'init': {
            'result': {
                'type': 'action',
                'action': _action_open,
                'state': 'end',
            },
        },
    }

module_config('ir.module.module.config')
