# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv


class account_invoice(osv.osv):

    _inherit = "account.invoice"

    def create(self, cr, uid, vals, context=None):
        if 'type' in vals and vals['type']=='out_refund':
            if context.get('active_id',False):
                inv_data = self.browse(cr, uid, context['active_id'])
                if inv_data.salesagent_id:
                    vals.update({'salesagent_id':inv_data.salesagent_id.id})
        # QUI DOVRA RICHIAMARE L'AGENTE PARTENDO DAL CLIENTE
        if 'salesagent_id' not in vals or not vals['salesagent_id']:
            partner = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'], context)
            if partner.salesagent_for_customer_id:
                vals.update({'salesagent_id':partner.salesagent_for_customer_id.id})
        return super(account_invoice, self).create(cr, uid, vals, context)

    def _amount_untaxed_commission(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            tot = 0.0
            for line in invoice.invoice_line:
                if line.no_commission:
                    continue
                tot += line.price_unit * (1-(line.discount or 0.0)/100.0) * line.quantity
            res[invoice.id] = tot
        return res

    def _total_commission(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            sign = 1
            total_commission = 0.0 
            for line in invoice.invoice_line:
                total_commission += (line.commission * sign)
            res[invoice.id] = total_commission
        return res

    def _paid_commission(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            paid_commission = True
            for line in invoice.invoice_line:
                if line.commission_presence and not line.paid_commission:
                    paid_commission = False
            res[invoice.id] = paid_commission
        return res

    def onchange_partner_id(self, cr, uid, ids, type, partner_id, date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        if not partner_id:
            return {}
        partner = self.pool.get('res.partner').read(cr, uid, partner_id, ['salesagent_for_customer_id'])
        salesagent_id = partner['salesagent_for_customer_id']
        res = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id, date_invoice, payment_term, partner_bank_id, company_id)
        res['value']['salesagent_id'] = salesagent_id
        return res

    def _get_commission(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids,
                                                              context=context):
            if line.invoice_id:
                result[line.invoice_id.id] = True
        return result.keys()

    def _get_paid_commission(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids,
                                                              context=context):
            if line.invoice_id:
                result[line.invoice_id.id] = True
        return result.keys()

    _columns = {
        'salesagent_id' : fields.many2one('res.partner', 'Salesagent'),
        'commission' : fields.function(_total_commission,
                                       method=True,
                                       string='Commission',
                                       type='float',
                                       store={
                                              'account.invoice.line': (_get_commission,
                                                                    ['commission'],
                                                                    20),
                                                }),
        'paid_commission' : fields.function(_paid_commission,
                                            type='boolean',
                                            method=True,
                                            string="Paid Commission",
                                            help="If True, Indicates all commission, for this invoice, have been paid",
                                            store={
                                                   'account.invoice.line': (_get_paid_commission,
                                                                         ['paid_commission'],
                                                                         20),
                                                    }),
        'paid_date' : fields.date('Commission Payment Date'),
        'amount_untaxed_commission' : fields.function(_amount_untaxed_commission, method=True, string='Amount Untaxed Commission', type='float', store=False),
    }
