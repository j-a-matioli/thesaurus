import django_filters

class MovimentoFilter(django_filters.FilterSet):
    mes_corrente = django_filters.NumberFilter(field_name='data', lookup_expr='month')
    ano_corrente = django_filters.NumberFilter(field_name='data', lookup_expr='year')





