##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
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
import netsvc
import pooler

import time
from osv import osv

track_form = '''<?xml version="1.0"?>
<form string="Tracking a move">
 <field name="tracking_prefix"/>
 <newline/>
 <field name="quantity"/>
</form>
'''
fields = {
		'tracking_prefix': {
			'string': 'Tracking prefix',
			'type': 'char',
			'size': 64,
		},
		'quantity': {
			'string': 'Quantity per lot',
			'type': 'float',
			'default': 1,
		}
}

def _track_lines(self, cr, uid, data, context):
	move_id = data['id']

	prodlot_obj = pooler.get_pool(cr.dbname).get('stock.production.lot')
	move_obj = pooler.get_pool(cr.dbname).get('stock.move')
	sequence = pooler.get_pool(cr.dbname).get('ir.sequence').get(cr, uid, 'stock.lot.serial')
	if data['form']['tracking_prefix']:
		sequence=data['form']['tracking_prefix']+'/'+(sequence or '')
	if not sequence:
		raise wizard.except_wizard('Error !', 'No tracking prefix defined')

	move = move_obj.browse(cr, uid, [move_id])[0]
	quantity=data['form']['quantity']
	if quantity <= 0 or move.product_qty == 0:
		return {}
	uos_qty=quantity/move.product_qty*move.product_uos_qty

	quantity_rest = move.product_qty%quantity
	uos_qty_rest = quantity_rest/move.product_qty*move.product_uos_qty

	update_val = {
		'product_qty': quantity,
		'product_uos_qty': uos_qty,
	}
	for idx in range(int(move.product_qty//quantity)):
		if idx:
			current_move = move_obj.copy(cr, uid, move.id, {'state': move.state, 'production_id': move.production_id.id})
		else:
			current_move = move.id
		new_prodlot = prodlot_obj.create(cr, uid, {'name': sequence, 'ref': '%d'%idx})
		update_val['prodlot_id'] = new_prodlot
		move_obj.write(cr, uid, [current_move], update_val)
	
	if quantity_rest > 0:
		idx = int(move.product_qty//quantity)
		update_val['product_qty']=quantity_rest
		update_val['product_uos_qty']=uos_qty_rest
		if idx:
			current_move = move_obj.copy(cr, uid, move.id, {'state': move.state, 'production_id': move.production_id.id})
		else:
			current_move = move.id
		new_prodlot = prodlot_obj.create(cr, uid, {'name': sequence, 'ref': '%d'%idx})
		update_val['prodlot_id'] = new_prodlot
		move_obj.write(cr, uid, [current_move], update_val)

	return {}

class wizard_track_move(wizard.interface):
	states = {
		'init': {
			'actions': [],
			'result': {'type': 'form', 'arch': track_form, 'fields': fields, 'state': [('end', 'Cancel', 'gtk-cancel'), ('track', 'Ok', 'gtk-ok')]},
			},
		'track': {
			'actions': [_track_lines],
			'result': {'type':'state', 'state':'end'}
		}
	}

wizard_track_move('stock.move.track')

