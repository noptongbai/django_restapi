from units.models import UnitCategory
from mgpAPI.serializers.unit_category_serializers import UnitCategorySerializer
from rest_framework import generics
from mgpAPI.pages.page import StandardResultsSetPagination


class UnitCategoryList(generics.ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        return UnitCategory.objects.filter(soft_delete=False)

class UnitCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UnitCategory.objects.all()
    serializer_class = UnitCategorySerializer
