class LitetraceBridge(models.Model):
    model_type = models.CharField(max_length=12)
    mac = models.CharField(max_length=32)
    ip = models.CharField(max_length=15, blank=True, null=True)
    port = models.CharField(max_length=6, blank=True, null=True)
    is_dhcp = models.BooleanField(default=False)
    mesh = models.ForeignKey(
        Mesh,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='litetrace_bridges')
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='litetrace_bridges')

    class Meta:
        unique_together = ('model_type', 'mac',)