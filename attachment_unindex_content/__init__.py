from . import models


def _clear_index_content(cr, registry):
    """Clear the indexed data for records already in database"""
    cr.execute("UPDATE ir_attachment SET index_content=NULL")
