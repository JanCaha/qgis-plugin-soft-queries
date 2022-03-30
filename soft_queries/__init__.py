__author__ = 'Jan Caha'
__date__ = '2022-03-01'
__copyright__ = '(C) 2022 by Jan Caha'

from .plugin_soft_queries import SoftQueriesPlugin


# noinspection PyPep8Naming
def classFactory(iface):

    return SoftQueriesPlugin(iface)
