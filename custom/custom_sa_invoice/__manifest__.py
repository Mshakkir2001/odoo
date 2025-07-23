{
    'name': 'Saudi Invoice Customization',
    'version': '1.0',
    'depends': ['account','base'],
    'license': 'LGPL-3',
    'sequence': 1,
    'data': [
        'views/report_invoice_wrapper_custom.xml',
        'views/custom_invoice_template.xml',
        'views/override_invoice_report.xml',
        'views/account_move_view.xml',

    ],
     'assets': {
        'web.report_assets_common': [
        'custom_sa_invoice/static/src/img/stamp.png',
        'custom_sa_invoice/static/src/img/header.png',
        'custom_sa_invoice/static/src/css/invoice_style.css',
     ],
    },
    'installable': True,
    'auto_install': False,
}
