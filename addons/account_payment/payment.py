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

from osv import fields
from osv import osv
import time
import netsvc
import pooler


class payment_type(osv.osv):
    _name= 'payment.type'
    _description= 'Payment type'
    _columns= {
        'name': fields.char('Name', size=64, required=True),
        'code': fields.char('Code', size=64, required=True),
        'suitable_bank_types': fields.many2many('res.partner.bank.type',
            'bank_type_payment_type_rel',
            'pay_type_id','bank_type_id',
            'Suitable bank types')
    }

payment_type()


class payment_mode(osv.osv):
    _name= 'payment.mode'
    _description= 'Payment mode'
    _columns= {
        'name': fields.char('Name', size=64, required=True),
        'bank_id': fields.many2one('res.partner.bank', "Bank account",
            required=True),
        'journal': fields.many2one('account.journal', 'Journal', required=True,
            domain=[('type', '=', 'cash')]),
        'type': fields.many2one('payment.type','Payment type',required=True),
    }

    def suitable_bank_types(self,cr,uid,payment_code= 'manual',context={}):
        """Return the codes of the bank type that are suitable
        for the given payment type code"""
        cr.execute(""" select t.code
            from res_partner_bank_type t
            join bank_type_payment_type_rel r on (r.bank_type_id = t.id)
            join payment_type pt on (r.pay_type_id = pt.id)
            where pt.code = %s """, [payment_code])
        return [x[0] for x in cr.fetchall()]

payment_mode()


class payment_order(osv.osv):
    _name = 'payment.order'
    _description = 'Payment Order'
    _rec_name = 'date'

    def get_wizard(self,type):
        logger = netsvc.Logger()
        logger.notifyChannel("warning", netsvc.LOG_WARNING,
                "No wizard found for the payment type '%s'." % type)
        return None

    def _total(self, cursor, user, ids, name, args, context=None):
        if not ids:
            return {}
        res = {}
        for order in self.browse(cursor, user, ids, context=context):
            if order.line_ids:
                res[order.id] = reduce(lambda x, y: x + y.amount, order.line_ids, 0.0)
            else:
                res[order.id] = 0.0
        return res

    _columns = {
        'date_planned': fields.date('Scheduled date if fixed'),
        'reference': fields.char('Reference',size=128,required=1),
        'mode': fields.many2one('payment.mode','Payment mode', select=True, required=1),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('open','Confirmed'),
            ('cancel','Cancelled'),
            ('done','Done')], 'State', select=True),
        'line_ids': fields.one2many('payment.line','order_id','Payment lines',states={'done':[('readonly',True)]}),
        'total': fields.function(_total, string="Total", method=True,
            type='float'),
        'user_id': fields.many2one('res.users','User',required=True),
        'date_prefered': fields.selection([
            ('now', 'Directly'),
            ('due', 'Due date'),
            ('fixed', 'Fixed date')
            ], "Prefered date", change_default=True, required=True),
        'date_created': fields.date('Creation date', readonly=True),
        'date_done': fields.date('Execution date', readonly=True),
    }

    _defaults = {
        'user_id': lambda self,cr,uid,context: uid,
        'state': lambda *a: 'draft',
        'date_prefered': lambda *a: 'due',
        'date_created': lambda *a: time.strftime('%Y-%m-%d'),
        'reference': lambda self,cr,uid,context: self.pool.get('ir.sequence').get(cr, uid, 'payment.order'),
    }

    def set_to_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state':'draft'})
        wf_service = netsvc.LocalService("workflow")
        for id in ids:
            wf_service.trg_create(uid, 'payment.order', id, cr)
        return True

    def action_open(self, cr, uid, ids, *args):
        for order in self.read(cr,uid,ids,['reference']):
            if not order['reference']:
                reference = self.pool.get('ir.sequence').get(cr, uid, 'payment.order')
                self.write(cr,uid,order['id'],{'reference':reference})
        return True

    def set_done(self, cr, uid, id, *args):
        self.write(cr,uid,id,{'date_done': time.strftime('%Y-%m-%d'),
            'state': 'done',})
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'payment.order', id, 'done', cr)
        return True

payment_order()


class payment_line(osv.osv):
    _name = 'payment.line'
    _description = 'Payment Line'

    def partner_payable(self, cr, uid, ids, name, args, context={}):
        if not ids: return {}
        partners= self.read(cr, uid, ids, ['partner_id'], context)
        partners= dict(map(lambda x: (x['id'], x['partner_id'][0]), partners))
        debit = self.pool.get('res.partner')._debit_get(cr, uid,
                partners.values(), name, args, context)
        for i in partners:
            partners[i] = debit[partners[i]]
        return partners

    def translate(self, orig):
        return {
#               "to_pay": "credit",
                "due_date": "date_maturity",
                "reference": "ref"}.get(orig, orig)

    def info_owner(self, cr, uid, ids, name=None, args=None, context=None):
        if not ids: return {}
        result = {}
        info=''
        for line in self.browse(cr, uid, ids, context=context):
            owner=line.order_id.mode.bank_id.partner_id
            result[line.id]=False
            if owner.address:
                for ads in owner.address:
                    if ads.type=='default':
                        st=ads.street and ads.street or ''
                        st1=ads.street2 and ads.street2 or ''
                        if 'zip_id' in ads:
                            zip_city= ads.zip_id and self.pool.get('res.partner.zip').name_get(cr,uid,[ads.zip_id.id])[0][1] or ''
                        else:
                            zip=ads.zip and ads.zip or ''
                            city= ads.city and ads.city or  ''
                            zip_city= zip + ' ' + city
                        cntry= ads.country_id and ads.country_id.name or ''
                        info=owner.name + "\n" + st + " " + st1 + "\n" + zip_city + "\n" +cntry
                        result[line.id]=info
                        break
        return result

    def info_partner(self, cr, uid, ids, name=None, args=None, context=None):
        if not ids: return {}
        result = {}
        info=''
        for line in self.browse(cr, uid, ids, context=context):
            result[line.id]=False
            if not line.partner_id:
                break
            partner = line.partner_id.name or ''
            if line.partner_id.address:
                for ads in line.partner_id.address:
                    if ads.type=='default':
                        st=ads.street and ads.street or ''
                        st1=ads.street2 and ads.street2 or ''
                        if 'zip_id' in ads:
                            zip_city= ads.zip_id and self.pool.get('res.partner.zip').name_get(cr,uid,[ads.zip_id.id])[0][1] or ''
                        else:
                            zip=ads.zip and ads.zip or ''
                            city= ads.city and ads.city or  ''
                            zip_city= zip + ' ' + city
                        cntry= ads.country_id and ads.country_id.name or ''
                        info=partner + "\n" + st + " " + st1 + "\n" + zip_city + "\n" +cntry
                        result[line.id]=info
                        break
        return result

    def select_by_name(self, cr, uid, ids, name, args, context=None):
        if not ids: return {}

        partner_obj = self.pool.get('res.partner')
        cr.execute("""SELECT pl.id, ml.%s
            from account_move_line ml
                inner join payment_line pl
                on (ml.id = pl.move_line_id)
            where pl.id in (%s)"""%
            (self.translate(name), ','.join(map(str,ids))) )
        res = dict(cr.fetchall())
        print "res: ", res
        print "name ", name

        if name == 'partner_id':
            partner_name = {}
            for p_id, p_name in partner_obj.name_get(cr,uid,
                filter(lambda x:x and x != 0,res.values()),context=context):
                partner_name[p_id] = p_name

            for id in ids:
                if id in res and partner_name:
                    res[id] = (res[id],partner_name[res[id]])
                else:
                    res[id] = (False,False)
        else:
            for id in ids:
                res.setdefault(id, (False, ""))
        return res

#   def _currency(self, cursor, user, ids, name, args, context=None):
#       if not ids:
#           return {}
#       res = {}
#
#       currency_obj = self.pool.get('res.currency')
#       account_obj = self.pool.get('account.account')
#       cursor.execute('''SELECT pl.id, ml.currency_id, ml.account_id
#       FROM account_move_line ml
#           INNER JOIN payment_line pl
#               ON (ml.id = pl.move_line_id)
#       WHERE pl.id in (''' + ','.join([str(x) for x in ids]) + ')')
#
#       res2 = {}
#       account_ids = []
#       for payment_line_id, currency_id, account_id in cursor.fetchall():
#           res2[payment_line_id] = [currency_id, account_id]
#           account_ids.append(account_id)
#
#       account2currency_id = {}
#       for account in account_obj.browse(cursor, user, account_ids,
#               context=context):
#           account2currency_id[account.id] = account.company_currency_id.id
#
#       for payment_line_id in ids:
#           if res2[payment_line_id][0]:
#               res[payment_line_id] = res2[payment_line_id][0]
#           else:
#               res[payment_line_id] = \
#                       account2currency_id[res2[payment_line_id][1]]
#
#       currency_names = {}
#       for currency_id, name in currency_obj.name_get(cursor, user, res.values(),
#               context=context):
#           currency_names[currency_id] = name
#       for payment_line_id in ids:
#           res[payment_line_id] = (res[payment_line_id],
#                   currency_names[res[payment_line_id]])
#       return res
#
#   def _to_pay_currency(self, cursor, user, ids, name , args, context=None):
#       if not ids:
#           return {}
#
#       cursor.execute('''SELECT pl.id,
#           CASE WHEN ml.amount_currency < 0
#               THEN - ml.amount_currency
#               ELSE ml.credit
#           END
#       FROM account_move_line ml
#           INNER JOIN payment_line pl
#               ON (ml.id = pl.move_line_id)
#       WHERE pl.id in (''' + ','.join([str(x) for x in ids]) + ')')
#       return dict(cursor.fetchall())

    def _amount(self, cursor, user, ids, name, args, context=None):
        if not ids:
            return {}
        currency_obj = self.pool.get('res.currency')
        if context is None:
            context = {}
        res = {}
        for line in self.browse(cursor, user, ids, context=context):
            ctx = context.copy()
            ctx['date'] = line.order_id.date_done or time.strftime('%Y-%m-%d')
            res[line.id] = currency_obj.compute(cursor, user, line.currency.id,
                    line.company_currency.id,
                    line.amount_currency, context=ctx)
        return res

    def _value_date(self, cursor, user, ids, name, args, context=None):
        if not ids:
            return {}
        res = {}
        for line in self.browse(cursor, user, ids, context=context):
            if line.order_id.date_prefered == 'fixed':
                res[line.id] = line.order_id.date_planned
            elif line.order_id.date_prefered == 'due':
                res[line.id] = line.due_date or time.strftime('%Y-%m-%d')
            else:
                res[line.id] = time.strftime('%Y-%m-%d')
        return res

    def _get_currency(self, cr, uid, context):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if user.company_id:
            return user.company_id.currency_id.id
        else:
            return self.pool.get('res.currency').search(cr, uid, [('rate','=',1.0)])[0]

#   def select_move_lines(*a):
#       print a
#       return []

#   def create(self, cr, uid, vals, context):
#       print "created!!!"
#       vals['company_currency'] = self._get_currency(cr, uid, context)
#       return super(payment_line, self).create(cr, uid, vals, context)

    def _get_ml_inv_ref(self, cr, uid, ids, *a):
        res={}
        for id in self.browse(cr, uid, ids):
            res[id.id] = ""
            print "test"
            if id.move_line_id:
                print "blablabl"
                res[id.id] = "pas de invoice"
                if id.move_line_id.invoice:
                    res[id.id] = str(id.move_line_id.invoice.number)
                    if id.move_line_id.invoice.name: 
                        res[id.id] += " " + id.move_line_id.invoice.name
        return res

    def _get_ml_maturity_date(self, cr, uid, ids, *a):
        res={}
        for id in self.browse(cr, uid, ids):
            if id.move_line_id:
                res[id.id] = id.move_line_id.date_maturity
            else:
                res[id.id] = ""
        return res

    def _get_ml_created_date(self, cr, uid, ids, *a):
        res={}
        for id in self.browse(cr, uid, ids):
            if id.move_line_id:
                res[id.id] = id.move_line_id.date_created
            else:
                res[id.id] = ""
        return res

    _columns = {
        'name': fields.char('Your Reference', size=64, required=True),
        'communication': fields.char('Communication', size=64, required=True),
        'communication2': fields.char('Communication 2', size=64),
        'move_line_id': fields.many2one('account.move.line','Entry line', domain=[('reconcile_id','=', False), ('account_id.type', '=','payable')]),
        'amount_currency': fields.float('Amount', digits=(16,2),
            required=True, help='Payment amount in the partner currency'),
#       'to_pay_currency': fields.function(_to_pay_currency, string='To Pay',
#           method=True, type='float',
#           help='Amount to pay in the partner currency'),
#       'currency': fields.function(_currency, string='Currency',
#           method=True, type='many2one', obj='res.currency'),
        'currency': fields.many2one('res.currency','Currency',required=True),
        'company_currency': fields.many2one('res.currency','Currency',readonly=True),
        'bank_id': fields.many2one('res.partner.bank', 'Destination Bank account'),
        'order_id': fields.many2one('payment.order', 'Order', required=True,
            ondelete='cascade', select=True),
        'partner_id': fields.many2one('res.partner', string="Partner",required=True),
        'amount': fields.function(_amount, string='Amount',
            method=True, type='float',
            help='Payment amount in the company currency'),
#       'to_pay': fields.function(select_by_name, string="To Pay", method=True,
#           type='float', help='Amount to pay in the company currency'),
#       'due_date': fields.function(select_by_name, string="Due date",
#           method=True, type='date'),
        'ml_date_created': fields.function(_get_ml_created_date, string="Effective Date",
            method=True, type='date',help="Invoice Effective Date"),
#       'reference': fields.function(select_by_name, string="Ref", method=True,
#           type='char'),
        'ml_maturity_date': fields.function(_get_ml_maturity_date, method=True, type='char', string='Maturity Date'),
        'ml_inv_ref': fields.function(_get_ml_inv_ref, method=True, type='char', string='Invoice Ref'),
        'info_owner': fields.function(info_owner, string="Owner Account", method=True, type="text"),
        'info_partner': fields.function(info_partner, string="Destination Account", method=True, type="text"),
        'partner_payable': fields.function(partner_payable,
            string="Partner payable", method=True, type='float'),
#       'value_date': fields.function(_value_date, string='Value Date',
#           method=True, type='date'),
        'date': fields.date('Payment Date'),
        'create_date': fields.datetime('Created' ,readonly=True),
        'state': fields.selection([('normal','Free'), ('structured','Structured')], 'Communication Type', required=True)
    }
    _defaults = {
        'name': lambda obj, cursor, user, context: obj.pool.get('ir.sequence'
            ).get(cursor, user, 'payment.line'),
        'state': lambda *args: 'normal',
        'currency': _get_currency,
        'company_currency': _get_currency,
    }
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'The payment line name must be unique!'),
    ]

    def onchange_move_line(self,cr,uid,ids,move_line_id,payment_type,context=None):
        data={}
        data['amount_currency']=data['currency']=data['communication']=data['partner_id']=data['reference']=data['date_created']=data['bank_id']=False
        if move_line_id:
            line=self.pool.get('account.move.line').browse(cr,uid,move_line_id)
            data['amount_currency']=line.amount_to_pay
            data['partner_id']=line.partner_id.id
            data['currency']=line.currency_id and line.currency_id.id or False
            if not data['currency']:
                data['currency']=line.invoice and line.invoice.currency_id.id or False
            # calling onchange of partner and updating data dictionary
            temp_dict=self.onchange_partner(cr,uid,ids,line.partner_id.id)
            data.update(temp_dict['value'])

            data['reference']=line.ref
            data['date_created']=line.date_created
            data['communication']=line.ref

            if payment_type:
                payment_mode = self.pool.get('payment.mode').browse(cr,uid,payment_type).type.code
            else:
                payment_mode=False

#           data['bank_id']=self.pool.get('account.move.line').line2bank(cr, uid,
#               [move_line_id],
#               payment_mode or 'manual', context)[move_line_id]

        return {'value': data}

    def onchange_partner(self,cr,uid,ids,partner_id,context=None):
        data={}
        data['info_partner']=data['bank_id']=False

        if partner_id:
            part_obj=self.pool.get('res.partner').browse(cr,uid,partner_id)
            partner=part_obj.name or ''

            if part_obj.address:
                for ads in part_obj.address:
                    if ads.type=='default':
                        st=ads.street and ads.street or ''
                        st1=ads.street2 and ads.street2 or ''

                        if 'zip_id' in ads:
                            zip_city= ads.zip_id and self.pool.get('res.partner.zip').name_get(cr,uid,[ads.zip_id.id])[0][1] or ''
                        else:
                            zip=ads.zip and ads.zip or ''
                            city= ads.city and ads.city or  ''
                            zip_city= zip + ' ' + city

                        cntry= ads.country_id and ads.country_id.name or ''
                        info=partner + "\n" + st + " " + st1 + "\n" + zip_city + "\n" +cntry

                        data['info_partner']=info

            if part_obj.bank_ids and len(part_obj.bank_ids)==1:
                data['bank_id']=self.pool.get('res.partner.bank').name_get(cr,uid,[part_obj.bank_ids[0].id])[0][0]

        return {'value': data}

    def fields_get(self, cr, uid, fields=None, context=None):
        res = super(payment_line, self).fields_get(cr, uid, fields, context)
        if 'communication2' in res:
            res['communication2'].setdefault('states', {})
            res['communication2']['states']['structured'] = [('readonly', True)]
            res['communication2']['states']['normal'] = [('readonly', False)]

        return res

payment_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

