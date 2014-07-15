# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2012 Andrea Cometa All Rights Reserved.
#                       www.andreacometa.it
#                       openerp@andreacometa.it
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
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

from openerp.osv import fields,orm
from openerp.tools.translate import _


#	MANAGE THE COMMISSIONS PAYMENT (ON INVOICE LINE)
class wzd_commissions_payment(orm.TransientModel):

    _name = "wzd.commissions_payment"

    _columns = {
        'payment_date' : fields.date('Payment Date'),
        'payment_commission_note' : fields.char('Notes', size=128),
        }

    def pagamento_provvigioni(self, cr, uid, ids, context={}):
        if not 'active_ids' in context:
            raise orm.except_orm(_('Invalid Operation!'), _('Select at least one line!'))
        # ----- Select records for active model
        wizard_obj = self.browse(cr,uid,ids[0])
        line_obj = self.pool.get(context['active_model'])
        lines = line_obj.browse(cr, uid, context['active_ids'])
        for line in lines:
            # ----- Set Payment
            line_obj.write(cr, uid, [line.id,], {
                'payment_commission_date' : wizard_obj.payment_date,
                'paid_commission' : True,
                'paid_commission_value' : line.commission,
                'paid_commission_percentage_value' : line.commission_percentage,
                'payment_commission_note':wizard_obj.payment_commission_note})
        return {'type': 'ir.actions.act_window_close'}
