from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField


class Cliente(models.Model):
    # Fields
    nome = models.CharField('Nome', max_length=150, default="")
    sobrenome = models.CharField('Sobrenome', max_length=150, default="")
    email = models.EmailField('E-mail', default="")
    telefone = models.BigIntegerField('Telefone', default="")
    cep = models.BigIntegerField('CEP', default="")
    rua = models.CharField('Endereço', max_length=300, default="")
    numero = models.IntegerField('Número', default="")
    complemento = models.CharField('Complemento (opcional)', max_length=200, blank=True)
    cidade = models.CharField('Cidade', max_length=150, default="")
    estado = models.CharField('Estado', max_length=100, default="")
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
    descricao   = models.TextField('Breve descrição sobre o problema', help_text='Escreva aqui', default="")
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
    nome = models.CharField('Nome do Plano', max_length=150, default="")
    refeicoes = models.IntegerField('Quantidade de refeições', default="")
    descricao = models.CharField('Descrição', max_length=300, default="")
    subdescricao = models.CharField('Sub-descrição', max_length=300, default="")
    condicaofrete = models.CharField('Como será o frete? (Ex:"Frete R$9,90")', max_length=50, default="")
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
    diadasemana_choices = (('Segunda','Segunda'),('Terça','Terça'),('Quarta','Quarta'),('Quinta','Quinta'),('Sexta','Sexta'),('Sábado','Sábado'),('Domingo','Domingo'))
    periodo_choices = (('Matutino','Matutino'),('Vespertino','Vespertino'),('Noturno','Noturno'))
    preferencia_choices=(('Em mãos', 'Sempre em mãos'),('Portaria','Pode deixar na portaria.'))
    frequencia_choices=((1, ' 1 Entrega no mês (Grátis)'),(2,'2 Entregas no mês (R$9,90)'))

    dia = MultiSelectField('Quais dias da semana você pode receber a Ração Do Futuro?', choices=diadasemana_choices, default="")
    periodo = MultiSelectField('Qual o período ideal para ser realizada a entrega?', choices=periodo_choices, default="")
    preferencia = models.CharField('Para quem podemos entregar?', max_length=150, default="", choices=preferencia_choices)
    frequencia = models.IntegerField('Com qual frequência quer receber a Ração do Futuro?', default=0, choices=frequencia_choices)
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

    sexo_choices = (('Macho','Macho'),('Femea','Femea'),('Indefinido','Indefinido'))
    castrado_choices = ((0,'Não'),(1,'Sim'))
    atividade_choices = (('Caminhadas Diárias','Caminhadas Diárias'),('Super Ativo','Super Ativo'), ('Nivel Olímpico','Nivel Olímpico'))
    fisico_choices =( ('Magro','Magro'),  ('Na Medida','Na Medida'), ('Gordinho','Gordinho'), ('Obeso','Obeso') )
    # Fields
    nome = models.CharField('Nome do seu Dog', help_text='Digite aqui o nome (sobrenome opcional)', max_length=150, default="")
    sexo = models.CharField('Sexo', max_length=50, default="", choices=sexo_choices)
    castrado = models.BooleanField('Ele é castrado?', max_length=50, default=0, choices=castrado_choices)
    raca = models.CharField('Raça', help_text='Digite aqui...', max_length=100, default="")
    nascimento = models.DateField('Data de nascimento - Apenas mês e ano', default="")
    peso = models.IntegerField('Peso', help_text='Observação: Não sabe o peso exato? Não faz mal, você pode inserir um peso próximo.', default=0)
    pesoideal = models.IntegerField('Peso Ideal', help_text='Segundo o conselho veterinario, caso seu cão tenha até 12 meses é obrigatorio você informar o peso ideal dele quando adulto. Fique tranquilo, você pode informar o peso aproximado.', default=0)
    atividade = models.CharField('Nivel de atividade Diária', max_length=100, default="", choices=atividade_choices)
    fisico = models.CharField('Físico do cão', help_text='Não sabe o estado físico do seu cão? Não tem problema, clique aqui e descubra.', max_length=100, default="", choices=fisico_choices)
    calculomes = models.IntegerField('Quantidade de ração a receber (kg/mês)', default=0)
    calculodia = models.IntegerField('Quantidade de ração diária para o cão (g/dia)', default=0)
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

    status_choices= ( ('Pedido em aberto','Pedido em aberto'), ('Pedido finalizado pelo cliente','Pedido finalizado pelo cliente'), ('Aguardando confirmação','Aguardando confirmação'), ('Pedido em preparo','Pedido em preparo'), ('Pedido em trânsito','Pedido em trânsito'), ('Pedido concluído','Pedido concluído') )
    sabores_choices = ( ('Carne de panela', 'Carne de panela'), ('Frango Xadrez', 'Frango Xadrez'), ('Risoto Suíno','Risoto Suíno')  )
    # Fields
    valor = models.IntegerField('Valor do pedido', default=0)
    status = models.CharField('Status do pedido', max_length=100, default="", choices=status_choices)
    observacoes = models.TextField('Observações', default="")
    linkpagseguro = models.URLField('URL do Pagamento', default="")
    sabores = MultiSelectField('Escolha os sabores do futuro', default="", choices=sabores_choices)
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
