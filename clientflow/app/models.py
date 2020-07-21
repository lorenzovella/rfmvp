from django.db import models
from django.urls import reverse


class CachorroEspecial(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_CachorroEspecial_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_CachorroEspecial_update", args=(self.pk,))


class Entrega(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Entrega_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Entrega_update", args=(self.pk,))


class Pedido(models.Model):

    # Relationships
    idClient = models.ForeignKey("clientflow.Cliente", on_delete=models.CASCADE)
    idPlano = models.ForeignKey("clientflow.Planos", on_delete=models.CASCADE)
    idEntrega = models.OneToOneField("clientflow.Entrega", on_delete=models.CASCADE)
    refDog = models.ManyToManyField(Cachorro)

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Pedido_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Pedido_update", args=(self.pk,))


class Planos(models.Model):

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Planos_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Planos_update", args=(self.pk,))


class Cachorro(models.Model):

    # Relationships
    idCliente = models.ForeignKey("clientflow.Cliente", on_delete=models.CASCADE)
    dogEspecial = models.OneToOneField("clientflow.CachorroEspecial", on_delete=models.CASCADE)

    # Fields
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Cachorro_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Cachorro_update", args=(self.pk,))


class Cliente(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Cliente_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Cliente_update", args=(self.pk,))
