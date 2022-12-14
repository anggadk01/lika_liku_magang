# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2008 Tiny SPRL (http://tiny.be) All Rights Reserved.
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
###############################################################################
import netsvc
from osv import fields,osv


# Overloaded sale_order to manage carriers :
class sale_order(osv.osv):
    _name = "sale.order"
    _inherit = 'sale.order' 
    _description = "Sale Order"

    _columns = {
        'carrier_id':fields.many2one("delivery.carrier","Delivery method", help="Complete this field if you plan to invoice the shipping based on packings made."),
    }

    def onchange_partner_id(self, cr, uid, ids, part):
        result = super(sale_order, self).onchange_partner_id(cr, uid, ids, part)
        if part:
            dtype = self.pool.get('res.partner').browse(cr, uid, part).property_delivery_carrier.id
            result['value']['carrier_id'] = dtype
        return result

    def action_ship_create(self, cr, uid, ids, *args):
        result = super(sale_order, self).action_ship_create(cr, uid, ids, *args)
        for order in self.browse(cr, uid, ids, context={}):
            pids = [ x.id for x in order.picking_ids]
            self.pool.get('stock.picking').write(cr, uid, pids, {
                'carrier_id':order.carrier_id.id,
            })
        return result
sale_order()





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

