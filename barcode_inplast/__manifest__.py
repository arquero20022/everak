{
    "name": "RRHH Personalizada",
    "summary": "añade una serie de campos requeridos para los empleados",
    "version": "17.0.1.0.1",
    "category": "Customizations",
    "website": "https://www.puntsistemes.es",
    "author": "Punt Sistemes",
    "maintainers": [
        "PuntSistemes S.L.U"
    ],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base","mrp",

    ],
    "data": [
        'views/stock_lot_views.xml',
        'views/mrp_cajas_views.xml',
        'views/mrp_cajas_actions.xml',
        'views/mrp_workorder_inherit_views.xml',
    ],

}
