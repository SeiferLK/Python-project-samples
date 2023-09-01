class ShelfCsvUploadViewSet(BaseCsvUploadViewSet):
    queryset = Shelf.objects.all()

    def create(self, request):
        f = request.data['file']
        reader = csv.DictReader(decode_iterator(f))

        failures = list()
        created = 0
        updated = 0
        for index, row in enumerate(reader):
            try:
                if self.request.user.store:
                    store = self.request.user.store
                    shelf = Shelf.objects.filter(
                        store=self.request.user.store,
                        code=row.get(ShelfHeader.CODE.value)
                    ).first()
                else:
                    store = Store.objects.filter(
                        name=row.get(ShelfHeader.STORE.value),
                        owner=request.user.owner).first()
                    shelf = Shelf.objects.filter(
                        code=row.get(ShelfHeader.CODE.value),
                        owner=request.user.owner,
                    ).first()
                if not shelf:
                    params = {
                        'code': row.get(ShelfHeader.CODE.value),
                        'name': row.get(ShelfHeader.NAME.value),
                        'store': store,
                        'owner': request.user.owner,
                    }
                    Shelf.objects.create(**params)
                    created += 1
                else:
                    shelf.code = row.get(Shelf.CODE.value)
                    shelf.name = row.get(Shelf.NAME.value) if \
                        row.get(Shelf.NAME.value) else None
                    shelf.store = store
                    shelf.save(update_fields=[
                        'code', 'name', 'store'
                    ])
                    updated += 1
            except Exception as e:
                failures.append(f'Row[{index+1}]: {e}')
                continue

        return Response({"Created": created, "Updated": updated, "Failed": failures })


class ShelfEtagCsvUploadViewSet(BaseCsvUploadViewSet):
    queryset = ShelfEtag.objects.all()

    def create(self, request):
        f = request.data['file']
        reader = csv.DictReader(decode_iterator(f))

        failures = list()
        created = 0
        updated = 0
        for index, row in enumerate(reader):
            try:
                store = self.request.user.store or Store.objects.filter(
                        name=row.get(ShelfPanelHeader.STORE.value),
                        owner=request.user.owner).first()
                gateway = Gateway.objects.filter(
                    store=store,
                    serial=row.get(ShelfPanelHeader.GATEWAY.value)
                ).first()
                shelf_etag = ShelfEtag.objects.filter(
                    store=store,
                    serial=row.get(ShelfPanelHeader.SERIAL.value),
                ).first()
                shelf = Shelf.objects.filter(
                    store=store,
                    code=row.get(ShelfPanelHeader.SHELF_CODE.value),
                ).first()
                model = EtagModel.objects.filter(name=row.get(ShelfPanelHeader.MODEL.value)).first()
                if not shelf_etag:
                    params = {
                        'serial': row.get(ShelfPanelHeader.SERIAL.value),
                        'mac': row.get(ShelfPanelHeader.MAC.value),
                        'gateway': gateway,
                        'model': model,
                        'store': store,
                        'shelf': shelf,
                        'owner': request.user.owner,
                    }
                    ShelfEtag.objects.create(**params)
                    created += 1
                else:
                    shelf_etag.serial = row.get(ShelfPanelHeader.SERIAL.value)
                    shelf_etag.mac = row.get(ShelfPanelHeader.MAC.value)
                    shelf_etag.gateway = gateway
                    shelf_etag.model = model
                    shelf_etag.store = store
                    shelf_etag.shelf = shelf
                    shelf_etag.save(update_fields=[
                        'serial', 'mac', 'gateway',
                        'model', 'store', 'shelf'
                    ])
                    updated += 1
            except Exception as e:
                failures.append(f'Row[{index+1}]: {e}')
                continue

        return Response({"Created": created, "Updated": updated, "Failed": failures})
