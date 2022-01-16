import django_filters

from apps.movimento.models import Movimento

class RelatorioSinteticoFilter(django_filters.FilterSet):
    mes_corrente = django_filters.NumberFilter(field_name='data', lookup_expr='month')
    ano_corrente = django_filters.NumberFilter(field_name='data', lookup_expr='year')
    
    class Meta:
            model = Movimento
            fields = ['id', 'data']

    
