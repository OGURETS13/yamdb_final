import django_filters

from django_filters.rest_framework import filters as django_filters_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    genre = django_filters_filters.CharFilter(field_name='genre__slug')
    category = django_filters_filters.CharFilter(field_name='category__slug')
    name = django_filters_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['year', ]
