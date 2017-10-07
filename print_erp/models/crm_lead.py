# -*- coding: utf-'8' "-*-"
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#     (<http://www.serpentcs.com>)
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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Lead(models.Model):
    _inherit = "crm.lead"
    
    @api.multi
    def open_print_order_form(self):
        if not self.ids:
            return True
        for rec in self:
            return {'name': _('Print Order Form'),
                    'context': self._context,
                    'view_type': 'form',
                    'view_mode': 'form',
                    'views': [(self.env.ref('print_erp.view_print_order_form1').id, 'form')],
                    'view_id': self.env.ref('print_erp.view_print_order_form1').id,
                    'res_model': 'print.order',
                    'target': 'new',
                    'type': 'ir.actions.act_window',
                    'res_id': rec.print_order_id and rec.print_order_id.id or False}
        return True
    
    print_order_id = fields.Many2one("print.order", string="Print Order Form")
    print_order_ids = fields.One2many("print.order", 'crm_lead_id', string="Print Orders")

