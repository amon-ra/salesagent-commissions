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

{
    'name': 'SalesAgent Commission - Provvigioni Agenti',
    'version': '0.2',
    'category': 'Account',
    'description': """
[ITA] Modulo per la gestione degli agenti di vendita
[ENG] Module to manage salesagent



Salesagent Commissions
======================

Il modulo  è pensato per calcolare in maniera dinamica le provvigioni 
per gli agenti facenti parte del corpo aziendale.

Come vengono calcolate le provvigioni?
--------------------------------------

Il modulo esegue il calcolo della percentuale nel seguente ordine:
Cerca la provvigione sul cliente legata al prodotto
Cerca la provvigione generica sul cliente
Cerca la provvigione sull'agente legata al prodotto
Cerca la provvigione generica sul prodotto
Cerca la provvigione generica sull'agente

Come si nota è possibile costruire in maniera dinamica il calcolo.

Come funziona il modulo?
------------------------

All'interno dell'anagrafica cliente è possibile selezionare l'agente
collegato. Esso verrà richiamato automaticamente in fase di fatturazione


Le percentuali provvigioni usate nel calcolo sono lette
col seguente ordine:

# Se il cliente ha la provvigione impostata per uno specifico prodotto
# altrimenti se il cliente ha la provvigione impostata per una specifica categoria di prodotto
# altrimenti se il cliente ha una provvigione generica
# altrimenti se l'agente ha la provvigione impostata per uno specifico prodotto
# altrimenti se l'agente ha la provvigione impostata per una specifica categoria di prodotto
# altrimenti se l'agente ha una provvigione generica
# altrimenti se il prodotto ha una provvigione generica
# altrimenti se la categoria del prodotto ha una provvigione generica



        """,
    'author': ["ISA srl", "www.andreacometa.it"],
    'website': 'http://www.andreacometa.it',
    'license': 'AGPL-3',
    "active": False,
    "installable": True,
    "depends" : ['base', 'product', 'account'],
    "data" : [
        'security/security.xml',
        'security/ir.model.access.csv',
        'partner/partner_view.xml',
        'product/category_view.xml',
        'product/product_view.xml',
        'account/invoice_view.xml',
        'account/invoice_line_view.xml',
        'wizard/wizard_percentage_calcolate_view.xml',
        'wizard/wizard_commissions_payment_view.xml',
        'wizard/wizard_invoice_commissions_payment_view.xml',
        'wizard/wizard_payment_cancellation_view.xml',
        'wizard/wizard_invoice_payment_cancellation_view.xml',
        'menu_items.xml',
        ],
}
