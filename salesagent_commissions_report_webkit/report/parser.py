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

import os
from openerp.report import report_sxw
from openerp.tools.translate import _
import logging
from datetime import datetime
from openerp.addons.account_financial_report_webkit.report.common_partner_reports import CommonPartnersReportHeaderWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser


class Parser(report_sxw.rml_parse, CommonPartnersReportHeaderWebkit):

    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)

        self.company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        rows = self.pool.get(context['active_model']).browse(cr, uid, context['active_ids'], context=context)

        self.localcontext.update({
                'cr': cr,
                'uid': uid,
                'screen_rows': rows,
                'get_filter': self._get_filter,
                'get_period_range': self._get_period_range,
            })

    def set_context(self, objects, data, ids, report_type=None):

        header_report_name = ' - '.join((_('RIEPILOGO PROVVIGIONI'), self.company.name, self.company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'fiscal_page_base': data.get('fiscal_page_base'),
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Pagina'), '[page]', _('di'), '[topage]'))),
                ('--footer-line',),
            ],
        })
        return super(Parser, self).set_context(objects, data, ids, report_type=report_type)

    def _get_filter(self, payment):
        t_dict = {}
        if payment:
            self.filter = payment
            t_dict = dict([('P', 'Pagate'), ('N', 'Non Pagate'), ('E', 'Pagate e Non Pagate')])
        return t_dict[self.filter]

    def _get_period_range(self, period_ids):
        period_start = ''
        period_stop = ''
        date_start = None
        date_stop = None
        period_data = self.pool.get('account.period').browse(self.cr, self.uid, period_ids)
        for t_period in period_data:
            if t_period.date_start:
                if not date_start:
                    date_start = t_period.date_start
                if date_start <= t_period.date_start:
                    date_start = t_period.date_start
                period_start = date_start
            if t_period.date_stop:
                if not date_stop:
                    date_stop = t_period.date_stop
                if date_stop >= t_period.date_stop:
                    date_stop = t_period.date_stop
                period_stop = date_stop

        return period_start + ' - ' + period_stop

HeaderFooterTextWebKitParser('report.list_commission_invoice',
                             'account.invoice',
                             os.path.dirname(os.path.realpath(__file__)) + 
                                         '/list_commission_invoice.mako',
                             parser=Parser)
