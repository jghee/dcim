import django_tables2 as tables


class BaseTable(tables.Table):
    exempt_columns = ()

    class Meta:
        attrs = {
            'class': 'table table-hover object-list'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
