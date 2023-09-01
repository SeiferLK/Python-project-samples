class NodeCsvDumpViewSet(BaseCsvDumpViewSet):
    renderer_classes = [renderers.NodeCsvRenderer]

    def get_queryset(self):
        return Node.objects.filter(
            node_group__mesh__building=self.request.user.building_selected).prefetch_related("model", "node_group")

    def list(self, request):
        content = [
            {
                NodeHeader.NAME.value: node.name,
                NodeHeader.MAC.value: node.mac,
                NodeHeader.NODE_ID.value: node.mesh_addr,
                NodeHeader.MODEL.value: node.model.name,
                NodeHeader.TYPE.value: node.model.light_type,
                NodeHeader.MESH.value: node.node_group.mesh.name,
                NodeHeader.GROUP_NAME.value: node.node_group.name,
                NodeHeader.GROUP_ADDR.value: node.node_group.addr,
                NodeHeader.ENERGY.value: node.energy,
                NodeHeader.X.value: node.x,
                NodeHeader.Y.value: node.y,
                NodeHeader.LAST_ACCESS.value: node.last_access,
            } for node in self.get_queryset()
        ]
        return Response(content, headers={
            'Content-Disposition': f'attachment;filename=node_list-{localdate()}.csv',
            'Content-Type': 'text/csv',
        })
