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


#	CALCOLATE COMISSION FROM FIX EARNING
class wzd_percentage_calcolate(orm.TransientModel):

    _name = "wzd.percentage_calcolate"

    _columns = {
        'product_price' : fields.float('Product Price'),
        'fix_commission' : fields.float('Fix Salesagent Commission'),
        'percentage' : fields.float('Percentage'),
        }

    def percentage_calcolate(self, cr, uid, ids, context={}):
        wizard = self.browse(cr,uid,ids[0])
        if not wizard.fix_commission or not wizard.product_price:
            raise orm.except_orm(_('Error'), _('Insert valid values!'))
        percentage = wizard.fix_commission / wizard.product_price
        self.write(cr, uid, ids, {'percentage':percentage})
        view_id = self.pool.get('ir.ui.view').search(cr,uid,[
            ('model','=','wzd.percentage_calcolate'),
            ('name','=','wzd.percentage_calcolate.wizard')])
        return {
            'type': 'ir.actions.act_window',
            'name': "Calculate percentage",
            'res_model': 'wzd.percentage_calcolate',
            'res_id': ids[0],
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
            'nodestroy': True,
            'context' : context,
            }
