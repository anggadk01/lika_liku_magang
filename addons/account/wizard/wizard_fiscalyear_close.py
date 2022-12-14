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
import osv
import pooler
from tools.translate import _

_transaction_form = '''<?xml version="1.0"?>
<form string="Close Fiscal Year">
    <field name="fy_id"/>
    <field name="fy2_id"/>
    <field name="report_new"/>
    <field name="report_name" colspan="3"/>

    <separator string="Are you sure ?" colspan="4"/>
    <field name="sure"/>
</form>'''

_transaction_fields = {
    'fy_id': {'string':'Fiscal Year to close', 'type':'many2one', 'relation': 'account.fiscalyear','required':True, 'domain':[('state','=','draft')]},
    'fy2_id': {'string':'New Fiscal Year', 'type':'many2one', 'relation': 'account.fiscalyear', 'domain':[('state','=','draft')], 'required':True},
    'report_new': {'string':'Create new entries', 'type':'boolean', 'required':True, 'default': lambda *a:True},
    'report_name': {'string':'Name of new entries', 'type':'char', 'size': 64, 'required':True},
    'sure': {'string':'Check this box', 'type':'boolean'},
}

def _data_load(self, cr, uid, data, context):
    data['form']['report_new'] = True
    data['form']['report_name'] = 'End of Fiscal Year Entry'
    return data['form']

def _data_save(self, cr, uid, data, context):
    if not data['form']['sure']:
        raise wizard.except_wizard(_('UserError'), _('Closing of fiscal year canceled, please check the box !'))
    pool = pooler.get_pool(cr.dbname)

    fy_id = data['form']['fy_id']
    if data['form']['report_new']:
        period = pool.get('account.fiscalyear').browse(cr, uid, data['form']['fy2_id']).period_ids[0]
        new_fyear = pool.get('account.fiscalyear').browse(cr, uid, data['form']['fy2_id'])
        start_jp = new_fyear.start_journal_period_id
        if not start_jp:
            raise wizard.except_wizard(_('UserError'),
                        _('The new fiscal year should have a journal for new entries define on it'))

        new_journal = start_jp.journal_id

        if not new_journal.default_credit_account_id or not new_journal.default_debit_account_id:
            raise wizard.except_wizard(_('UserError'),
                    _('The journal must have default credit and debit account'))
        if not new_journal.centralisation:
            raise wizard.except_wizard(_('UserError'),
                    _('The journal must have centralised counterpart'))

        query_line = pool.get('account.move.line')._query_get(cr, uid,
                obj='account_move_line', context={'fiscalyear': fy_id})
        cr.execute('select id from account_account WHERE active')
        ids = map(lambda x: x[0], cr.fetchall())
        for account in pool.get('account.account').browse(cr, uid, ids,
            context={'fiscalyear': fy_id}):
            if account.close_method=='none' or account.type == 'view':
                continue
            if account.close_method=='balance':
                if abs(account.balance)>0.0001:
                    pool.get('account.move.line').create(cr, uid, {
                        'debit': account.balance>0 and account.balance,
                        'credit': account.balance<0 and -account.balance,
                        'name': data['form']['report_name'],
                        'date': period.date_start,
                        'journal_id': new_journal.id,
                        'period_id': period.id,
                        'account_id': account.id
                    }, {'journal_id': new_journal.id, 'period_id':period.id})
            if account.close_method=='unreconciled':
                offset = 0
                limit = 100
                while True:
                    cr.execute('SELECT name, quantity, debit, credit, account_id, ref, ' \
                                'amount_currency, currency_id, blocked, partner_id, ' \
                                'date_maturity, date_created ' \
                            'FROM account_move_line ' \
                            'WHERE account_id = %d ' \
                                'AND ' + query_line + ' ' \
                                'AND reconcile_id is NULL ' \
                            'ORDER BY id ' \
                            'LIMIT %d OFFSET %d', (account.id, limit, offset))
                    result = cr.dictfetchall()
                    if not result:
                        break
                    for move in result:
                        move.update({
                            'date': period.date_start,
                            'journal_id': new_journal.id,
                            'period_id': period.id,
                        })
                        pool.get('account.move.line').create(cr, uid, move, {
                            'journal_id': new_journal.id,
                            'period_id': period.id,
                            })
                    offset += limit
            if account.close_method=='detail':
                offset = 0
                limit = 100
                while True:
                    cr.execute('SELECT name, quantity, debit, credit, account_id, ref, ' \
                                'amount_currency, currency_id, blocked, partner_id, ' \
                                'date_maturity, date_created ' \
                            'FROM account_move_line ' \
                            'WHERE account_id = %d ' \
                                'AND ' + query_line + ' ' \
                            'ORDER BY id ' \
                            'LIMIT %d OFFSET %d', (account.id,fy_id, limit, offset))
                    result = cr.dictfetchall()
                    if not result:
                        break
                    for move in result:
                        move.update({
                            'date': period.date_start,
                            'journal_id': new_journal.id,
                            'period_id': period.id,
                        })
                        pool.get('account.move.line').create(cr, uid, move)
                    offset += limit

    cr.execute('UPDATE account_journal_period ' \
            'SET state = %s ' \
            'WHERE period_id IN (SELECT id FROM account_period WHERE fiscalyear_id = %d)',
            ('done',fy_id))
    cr.execute('UPDATE account_period SET state = %s ' \
            'WHERE fiscalyear_id = %d', ('done',fy_id))
    cr.execute('UPDATE account_fiscalyear ' \
            'SET state = %s, end_journal_period_id = %d' \
            'WHERE id = %d', ('done',start_jp,fy_id))
    return {}

class wiz_journal_close(wizard.interface):
    states = {
        'init': {
            'actions': [_data_load],
            'result': {'type': 'form', 'arch':_transaction_form, 'fields':_transaction_fields, 'state':[('end','Cancel'),('close','Close Fiscal Year')]}
        },
        'close': {
            'actions': [_data_save],
            'result': {'type': 'state', 'state':'end'}
        }
    }
wiz_journal_close('account.fiscalyear.close')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

