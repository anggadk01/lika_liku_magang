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
import wizard
import netsvc
import pooler
from osv import fields, osv
from tools.translate import _

form = """<?xml version="1.0"?>
<form string="Choose Fiscal Year">
    <field name="fyear_id" domain="[('state','=','done')]"/>
</form>
"""

fields = {
    'fyear_id': {'string': 'Fiscal Year to Open', 'type': 'many2one', 'relation': 'account.fiscalyear', 'required': True},
}

def _remove_entries(self, cr, uid, data, context):
    pool = pooler.get_pool(cr.dbname)
    data_fyear = pool.get('account.fiscalyear').browse(cr,uid,data['form']['fyear_id'])
    if not data_fyear.end_journal_period_id:
        raise wizard.except_wizard(_('Error'), _('No journal for ending writings have been defined for the fiscal year'))
    period_journal = data_fyear.end_journal_period_id
    if not period_journal.journal_id.centralisation:
        raise wizard.except_wizard(_('UserError'), _('The journal must have centralised counterpart'))
    ids_move = pool.get('account.move').search(cr,uid,[('journal_id','=',period_journal.journal_id.id),('period_id','=',period_journal.period_id.id)])
    pool.get('account.move').unlink(cr,uid,ids_move)
    cr.execute('UPDATE account_journal_period ' \
            'SET state = %s ' \
            'WHERE period_id IN (SELECT id FROM account_period WHERE fiscalyear_id = %d)',
            ('draft',data_fyear))
    cr.execute('UPDATE account_period SET state = %s ' \
            'WHERE fiscalyear_id = %d', ('draft',data_fyear))
    cr.execute('UPDATE account_fiscalyear ' \
            'SET state = %s, end_journal_period_id = null '\
            'WHERE id = %d', ('draft',data_fyear))
    return {}

class open_closed_fiscal(wizard.interface):
    states = {
        'init' : {
            'actions' : [],
            'result': {
                'type': 'form', 
                'arch': form,
                'fields': fields, 
                'state':[('end','Cancel'),('open','Open')]
            }
        },
        'open': {
            'actions': [],
            'result': {
                'type':'action', 
                'action':_remove_entries, 
                'state':'end'
            },
        },
    }
open_closed_fiscal("account.open_closed_fiscalyear")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

