class ShelfEtagViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ShelfEtagSerializer
    authentication_classes = [SessionAuthentication]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['serial', 'mac', 'gateway']
    search_fields = ['serial', 'mac']
    filterset_fields = ['serial', 'mac']

    def get_queryset(self):
        if self.request.user.store:
            return ShelfEtag.objects.filter(
                store=self.request.user.store).prefetch_related(
                'shelf', 'store', 'gateway', 'model')
        else:
            return ShelfEtag.objects.filter(
                owner=self.request.user.owner).prefetch_related(
                'shelf', 'store', 'gateway', 'model')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.owner)

    @action(detail=True, methods=['put'])
    def screen_update(self, request, pk=None):
        return Response()

        
 class FactReviewCommentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FactReviewCommentSerializer
    authentication_classes = [SessionAuthentication]
    pagination_class = ResultsTablesPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['country_code', 'item_code']
    filterset_fields = ['country_code', 'item_code']

    def get_queryset(self):
        return FactReviewComment.objects.all()

    def list(self, request):
        store = Store.objects.get(id=request.GET.get('store_id'))
        if not store:
            return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)
        if not store.country:
            return Response({'error': 'Store does not have a country'}, status=status.HTTP_404_NOT_FOUND)
        queryset = self.filter_queryset(self.get_queryset())
        comments = queryset.filter(
            country_code=store.country.code)
        page = self.paginate_queryset(comments)
        serialized = self.get_serializer(page, many=True)
        return self.get_paginated_response(serialized.data)
