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

from openerp.osv import fields, orm


class sale_order(orm.Model):
    _inherit = 'sale.order'
    _columns = {
        'salesagent_id' : fields.many2one('res.partner', 'Agente'),
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        invoice_vals = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        if order.salesagent_id and order.salesagent_id.id:
            invoice_vals['salesagent_id'] = order.salesagent_id.id
        return invoice_vals

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        if not partner_id:
            return {}
        partner = self.pool.get('res.partner').read(cr, uid, partner_id, ['salesagent_for_customer_id'])
        salesagent_id = partner['salesagent_for_customer_id']
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, partner_id, context)
        if 'value' not in res:
            if salesagent_id and 'value' not in res:
                return {'value': {'salesagent_id': salesagent_id,
                                  }}
            return {'value': {'salesagent_id': None,
                                  }}
        res['value']['salesagent_id'] = salesagent_id

        return res
