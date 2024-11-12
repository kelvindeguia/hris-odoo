# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "HRIS Odoo 17 New",
    "summary": """Human Resources Information System Odoo 17 New""",
    # "icon":"hris_test_module.static/src/description/icon.jpg",
    "version": "1.0.1",
    "sequence": -100,
    # "license": "AGPL-3",
    "category": "Productivity",
    "author": "Marc Roda",
    "website": "",
    "depends": ["base", "mail", "utm"],
    # 'qweb': [
    #     'static/src/hris_style.scss',
    # ],
    "data": [
        "data/hr_isw_groups.xml",
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/actions.xml",
        "views/menus.xml",
        "views/tree_views.xml",
        "views/search_filters.xml",
        "views/form_views.xml",
        
    ],
    "application": True,
    "auto_install": False,
    "installable": True,
}
