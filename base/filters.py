from .models import Company
import django_filters


class CompanyFilter(django_filters.FilterSet):
    foundationYear = django_filters.RangeFilter(field_name='foundationYear')
    class Meta:
        model = Company
        fields = {
            'name': ['icontains'],
            'domain': ['icontains'],
            'industry': ['icontains'],
            'companySize': ['icontains'],
            'city': ['icontains'],
            'state': ['icontains'],
            'country': ['icontains'],
            'linkedin': ['icontains'],
    }
