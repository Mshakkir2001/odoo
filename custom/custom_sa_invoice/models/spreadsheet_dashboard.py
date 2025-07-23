from odoo import models, fields
import json

class SpreadsheetDashboard(models.Model):
    _inherit = 'spreadsheet.dashboard'  # use _inherit to extend, not _name

    def get_readonly_dashboard(self):
        # Fallback to empty JSON if field is empty or null
        data = self.spreadsheet_data or '{}'
        snapshot = json.loads(data)

        # Do your logic with `snapshot` here
        return snapshot  # or whatever your method normally returns
