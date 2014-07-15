# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 ISA s.r.l. (<http://www.isa.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

import time
from openerp.osv import orm, fields
from openerp.tools.translate import _


class wizard_list_commission(orm.TransientModel):

    _name = "wizard.list.commission"

    def _get_period(self, cr, uid, context=None):
        ctx = dict(context or {}, account_period_prefer_normal=True)
        period_ids = self.pool.get('account.period').find(cr, uid, context=ctx)
        return period_ids

    def _get_account(self, cr, uid, context=None):
        user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
        accounts = self.pool.get('account.account').search(cr, uid, [('parent_id', '=', False), ('company_id', '=', user.company_id.id)], limit=1)
        return accounts and accounts[0] or False

    def _get_fiscalyear(self, cr, uid, context=None):
        if context is None:
            context = {}
        now = time.strftime('%Y-%m-%d')
        company_id = False
        ids = context.get('active_ids', [])
        if ids and context.get('active_model') == 'account.account':
            company_id = self.pool.get('account.account').browse(cr, uid, ids[0], context=context).company_id.id
        else:  # use current company id
            company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
        fiscalyears = self.pool.get('account.fiscalyear').search(cr, uid, domain, limit=1)
        return fiscalyears and fiscalyears[0] or False

    _columns = {
        'chart_account_id': fields.many2one('account.account', 'Chart of Account', help='Select Charts of Accounts', required=True, domain = [('parent_id','=',False)]),
        'company_id': fields.related('chart_account_id', 'company_id', type='many2one', relation='res.company', string='Company', readonly=True),
        'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year', help='Keep empty for all open fiscal year'),
        'filter': fields.selection([('filter_period', 'Periods'), ('filter_date', 'Date')], "Filter by", required=True),
        'date_from': fields.date("Start Date"),
        'date_to': fields.date("End Date"),
        'period_ids': fields.many2many('account.period',
                                       'list_commission_periods_rel',
                                       'period_id',
                                       'commission_id',
                                       'Periodi',
                                       help='Select periods you want retrieve documents from',
                                       required=True),
        'message': fields.char('Messaggio', size=64,
                                       readonly=True),
        'payment': fields.selection(
                                [
                                 ('E', 'Pagate e Non Pagate'),
                                 ('P', 'Pagate'),
                                 ('N', 'Non Pagate'),],
                                'Partite',
                                required=True),
        }

    _defaults = {
        'payment': 'E',
        'period_ids': _get_period,
        'filter': 'filter_period',
        'chart_account_id': _get_account,
        'fiscalyear_id': _get_fiscalyear,
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.common.report',context=c),
        }

    def onchange_filter(self, cr, uid, ids, filter='filter_period', fiscalyear_id=False, context=None):
        res = {'value': {}}
        if filter == 'filter_date':
            res['value'] = {'period_from': False, 'period_to': False, 'date_from': time.strftime('%Y-01-01'), 'date_to': time.strftime('%Y-%m-%d')}
        if filter == 'filter_period' and fiscalyear_id:
            start_period = end_period = False
            cr.execute('''
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.special = false
                               ORDER BY p.date_start ASC, p.special ASC
                               LIMIT 1) AS period_start
                UNION ALL
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.date_start < NOW()
                               AND p.special = false
                               ORDER BY p.date_stop DESC
                               LIMIT 1) AS period_stop''', (fiscalyear_id, fiscalyear_id))
            periods =  [i[0] for i in cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            res['value'] = {'period_from': start_period, 'period_to': end_period, 'date_from': False, 'date_to': False}
        return res

    def onchange_chart_id(self, cr, uid, ids, chart_account_id=False, context=None):
        res = {}
        if chart_account_id:
            company_id = self.pool.get('account.account').browse(cr, uid, chart_account_id, context=context).company_id.id
            now = time.strftime('%Y-%m-%d')
            domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
            fiscalyears = self.pool.get('account.fiscalyear').search(cr, uid, domain, limit=1)
            res['value'] = {'company_id': company_id, 'fiscalyear_id': fiscalyears and fiscalyears[0] or False}
        return res

    def print_registro(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wizard = self.browse(cr, uid, ids)[0]
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')
        obj_model_data = self.pool.get('ir.model.data')

        t_filter = [
            ('commission', '!=', False),
            ('commission', '!=', None),
            ('commission', '!=', 0.0),
            '|',('state', '=', 'open'),
            ('state', '=', 'paid'),
            ]
        if wizard.payment:
            if wizard.payment == 'P':
                t_filter.append(('paid_commission', '=', True))
            elif wizard.payment == 'N':
                t_filter.append(('paid_commission', '=', False))
                t_filter.append(('paid_commission', '=', None))

        if wizard.filter == 'filter_period':
            t_filter.append(('period_id', 'in', [p.id for p in wizard.period_ids]))

        inv_ids = inv_obj.search(cr, uid, t_filter,
                                 order='salesagent_id, date_invoice')

        if wizard.filter == 'filter_date':
            if inv_ids:
                t_items = "(" + ",".join(str(x) for x in inv_ids) + ") "
                line_filter = ''
                if wizard.date_from:
                    line_filter = line_filter + " and account_invoice_line.payment_commission_date >= '" + wizard.date_from + "'"
                if wizard.date_to:
                    line_filter = line_filter + " and account_invoice_line.payment_commission_date <= '" + wizard.date_to + "'"

                query = """
                              select account_invoice.id
                              from account_invoice
                                   join account_invoice_line on account_invoice.id = account_invoice_line.invoice_id
                              WHERE account_invoice.id IN """ + t_items + """
                                    """ + line_filter + """
                              order by account_invoice.salesagent_id, account_invoice.date_invoice
                              """

                cr.execute(query)
                inv_ids = [val[0] for val in cr.fetchall()]

        if not inv_ids:
            self.write(cr, uid,  ids, {'message': _('No documents found in the current selection')})
            model_data_ids = obj_model_data.search(cr, uid, [('model','=','ir.ui.view'), ('name','=','wizard_list_commission')])
            resource_id = obj_model_data.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
            return {
                'name': _('No documents'),
                'res_id': ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'wizard.list.commission',
                'views': [(resource_id,'form')],
                'context': context,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        datas = {'ids': inv_ids, 'form': {},}
        datas['model'] = 'account.invoice'
        datas['period_ids'] = [p.id for p in wizard.period_ids]
        datas['payment'] = wizard.payment
        datas['date_from'] = wizard.date_from
        datas['date_to'] = wizard.date_to
        datas['fiscalyear'] = None
        if wizard.fiscalyear_id:
            datas['fiscalyear'] = wizard.fiscalyear_id.name

        res= {
            'type': 'ir.actions.report.xml',
            'datas': datas,
        }

        res['report_name'] = 'list_commission_invoice'

        return res
