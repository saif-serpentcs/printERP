# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Printing ERPs',
    'category': 'Printing',
    'summary': 'Printing Maanagement',
    'version': '1.0',
    'description': ''' This module is used for shop for all your personalized corporate and individual needs''',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': ['crm', 'sale', 'mrp'],
    'data': [
            'data/print_saizes_data.xml',
            'data/product_attribute_data.xml',
            'data/product_category_data.xml',
            'data/product_data.xml',
            'views/email_template.xml',
            'wizard/print_order_reject_wiz.xml',
            'views/crm_lead_view.xml',
            'views/print_order_view.xml',
            'views/product_view.xml',
            'views/attachment_view.xml',
            'views/sale_view.xml',
            'views/bom_view.xml',
             ],
    'application': True,
    'auto_install': False,
    'installable': True,
}
