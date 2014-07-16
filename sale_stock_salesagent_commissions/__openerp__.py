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

{
    'name': 'SalesAgent Commission Sale Stock',
    'version': '0.1',
    'category': 'Hidden',
    'description': """

Salesagent Commissions Sale Stock
=================================

Questo modulo estende il modulo provvigioni (salesagent_commissions).
Una volta selezionato l'agente dal preventivo o ordine vendita, il dato
viene riportato anche nell'ordine consegna, fino all'emissione della fattura.


        """,
    'author': 'ISA srl',
    'website': 'http://www.isa.it/',
    'license': 'AGPL-3',
    "active": False,
    "installable": True,
    'auto_install': True,
    "depends" : ['base', 'salesagent_commissions', 'sale_stock'],
    "data" : [
        ],
}
