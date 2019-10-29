# © 2019  Vauxoo (<http://www.vauxoo.com/>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Attachment Unindex Content',
    'summary': 'Disable indexing of attachments',
    'version': '12.0.0.0.0',
    'author': 'Vauxoo',
    'website': 'http://www.vauxoo.com/',
    'license': 'AGPL-3',
    'category': 'Tools',
    'depends': [
        'base',
    ],
    'data': [],
    'demo': [],
    'installable': True,
    'application': False,
    'images': [],
    'post_init_hook': '_clear_index_content',
}
