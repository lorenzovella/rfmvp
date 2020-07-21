from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


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


class CachorroEspecial(models.Model):

    condicao_choices = (('alergia', 'Alegia'),
    ('cardiaco', 'Cardiaco'),
    ('diabetes', 'Diabetes'),
    ('renal', 'Renal'),
    ('obesidade', 'Obesidade'),
    ('intestinal', 'Instestinal'),
    ('outro', 'Outro'))

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    condicao = MultiSelectField('Qual o problema de saúde?', max_length=200, choices=condicao_choices)
    medicamento = models.BooleanField('Ele toma algum medicamento?', default=False)
    descricao   = models.TextField('Breve descrição sobre o problema', help_text='Escreva aqui')
    anexo = models.FileField('Algum exame ou receita?', help_text='Clique ou arraste os arquivos nessa área para anexá-los', upload_to='uploads/anexos/%Y/%m/')
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_CachorroEspecial_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_CachorroEspecial_update", args=(self.pk,))

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

class Cachorro(models.Model):

    # Relationships
    idCliente = models.ForeignKey("app.Cliente", on_delete=models.CASCADE)
    dogEspecial = models.OneToOneField("app.CachorroEspecial", on_delete=models.CASCADE)

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


class Pedido(models.Model):

    # Relationships
    idClient = models.ForeignKey("app.Cliente", on_delete=models.CASCADE)
    idPlano = models.ForeignKey("app.Planos", on_delete=models.CASCADE)
    idEntrega = models.OneToOneField("app.Entrega", on_delete=models.CASCADE)
    refDog = models.ManyToManyField("app.Cachorro")

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


class Lead(models.Model):

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Lead_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Lead_update", args=(self.pk,))
