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

from openerp import models, fields, api, _
from openerp.exceptions import UserError
from datetime import date
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class PrintOredrRejectWiz(models.TransientModel):
    _name = 'print.order.reject.wiz'

    reject_remarks = fields.Text(string='Reject Reason')
    end_date = fields.Date(string='End Date')

    @api.multi
    def action_reject(self):
        context = dict(self._context) or {}
        for rec in self:
            if context.get('active_id'):
                print_order_rec = self.env['print.order'].browse(context.get('active_id'))
                if rec.end_date < print_order_rec.date_order or rec.end_date > date.today().strftime(DEFAULT_SERVER_DATE_FORMAT):
                    raise UserError(_("End Date must be between Print Order Date and Current Date"))
                print_order_rec.write({'reject_reason': rec.reject_remarks or '',
                                       'end_date': rec.end_date or False,
                                       'state': 'rejected'})
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
