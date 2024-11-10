{
    'name': 'Contacts Extension',
    'version': '18.0',
    'category': 'Contacts',
    'author': 'Jan Hruska',
    'license': 'AGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_view.xml',
        'views/res_partner_list_view.xml',
        'views/res_partner_kanban_view.xml',
    ],
    'installable': True,
    'application': False,
}
