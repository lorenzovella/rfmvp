from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from clientflow.app.pagseguro import consultaAssinatura, listaPagamentos
from datetime import date
from django_simple_coupons.models import Coupon
from decimal import Decimal

class Carrinho(models.Model):
    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    plano = models.CharField(max_length=200, blank=True, default="")
    cupom = models.CharField(max_length=200, blank=True, default="")
    pagseguro_plano = models.CharField(max_length=250, blank=True, default="")
    pagseguro_adesao = models.CharField(max_length=250, blank=True, default="")
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_valor_desconto(self):
        sum = 0
        for i in self.item.all():
            sum += i.valor
        if self.cupom:
            instance = Coupon.objects.get(code=self.cupom)
            return sum - instance.get_discounted_value(initial_value = sum)
        return 0

    def get_valor_carrinho(self):
        sum = 0
        for i in self.item.all():
            sum += i.valor
        if self.cupom:
            instance = Coupon.objects.get(code=self.cupom)
            sum = instance.get_discounted_value(initial_value = sum)
        sum += Decimal(self.get_valor_frete())
        return sum

    def get_valor_frete(self):
        for i in self.item.all():
            if i.idEntrega.frequencia == 2:
                return 9.90
        return 0

    def get_status(self):
        return consultaAssinatura(self.pagseguro_adesao)

    def lista_pagamentos(self):
        return listaPagamentos(self.pagseguro_adesao)

    def get_absolute_url(self):
        return reverse("clientflow_carrinho_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_carrinho_update", args=(self.pk,))


class Cliente(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,9}$', message="Digite apenas o número do seu telefone")
    # Fields
    user = models.OneToOneField(User, related_name='cliente', on_delete=models.CASCADE, blank=True, null=True)
    nome = models.CharField('Nome', max_length=150, default="")
    sobrenome = models.CharField('Sobrenome', max_length=150, default="")
    email = models.EmailField('E-mail', default="")
    telefone = models.CharField('Telefone',validators=[phone_regex], null=True, max_length=9)
    areatelefone = models.CharField('DDD', max_length=2,null=True)
    cep = models.BigIntegerField('CEP', null=True)
    cpf = models.CharField('CPF', default="", max_length=13)
    rua = models.CharField('Endereço', max_length=80, default="")
    nascimento = models.DateField('Data de nascimento', null= True)
    numero = models.IntegerField('Número', null=True)
    bairro = models.CharField('Bairro', max_length=60, blank=True)
    complemento = models.CharField('Complemento (opcional)', max_length=40, blank=True)
    cidade = models.CharField('Cidade', max_length=60, default="")
    estado = models.CharField('Estado', max_length=2, default="")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        return reverse("clientflow_Cliente_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Cliente_update", args=(self.pk,))
# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Cliente.objects.create(user=instance)
#     instance.cliente.save()
#

class CachorroEspecial(models.Model):

    condicao_choices = (('alergia', 'Alergia'),
    ('cardiaco', 'Cardiaco'),
    ('diabetes', 'Diabetes'),
    ('renal', 'Renal'),
    ('obesidade', 'Obesidade'),
    ('intestinal', 'Instestinal'),
    ('outro', 'Outro'))
    medicamento_choices = ((1,'Sim'), (0,'Não'))

    # Fields
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    condicao = MultiSelectField('Qual o problema de saúde?', max_length=200, choices=condicao_choices,blank=True, null=True)
    medicamento = models.BooleanField('Ele toma algum medicamento?',  default=0, choices=medicamento_choices)
    descricao   = models.TextField('Breve descrição sobre o problema', default="",blank=True, null=True)
    # anexo = models.URLField('Algum exame ou receita?', help_text='Clique ou arraste os arquivos nessa área para anexá-los', blank=True, null=True)
    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_CachorroEspecial_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_CachorroEspecial_update", args=(self.pk,))

class Plano(models.Model):
    nome = models.CharField('Nome do Plano', max_length=150, default="")
    refeicoes = models.IntegerField('Quantidade de refeições', default=0)
    descricao = models.CharField('Descrição', max_length=300, default="")
    subdescricao = models.CharField('Sub-descrição', max_length=300, default="")
    condicaofrete = models.CharField('Como será o frete? (Ex:"Frete R$9,90")', max_length=50, default="")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-last_updated']
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Plano_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Plano_update", args=(self.pk,))


class Entrega(models.Model):
    diadasemana_choices = (('Segunda','Segunda'),('Terça','Terça'),('Quarta','Quarta'),('Quinta','Quinta'),('Sexta','Sexta'),('Sábado','Sábado'))
    periodo_choices = (('Matutino','Matutino'),('Vespertino','Vespertino'),('Noturno','Noturno'))
    preferencia_choices=(('Portaria','Pode deixar na portaria'),('Em mãos', 'Sempre em mãos'))
    frequencia_choices=((1, ' 1 Entrega no mês (Grátis)'),(2,'2 Entregas no mês (R$9,90)'))

    dia = MultiSelectField('Quais dias da semana você pode receber a Ração Do Futuro?', max_length=150, choices=diadasemana_choices, default="")
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
    idCliente = models.ForeignKey("app.Cliente", on_delete=models.CASCADE, null=True, blank=True)
    dogEspecial = models.OneToOneField("app.CachorroEspecial", on_delete=models.CASCADE, related_name="Cachorro", null=True, blank=True)

    sexo_choices = (('Macho','Macho'),('Femea','Fêmea'))
    castrado_choices = ((1,'Sim'), (0,'Não'))
    atividade_choices = (('Caminhadas Diárias','De 30 min até 1:30 de caminhadas diárias.'),('Super Ativo','1:30 até 2:30 de caminhadas diárias.'), ('Nivel Olímpico','2:30 até 3:30 de caminhadas diárias.'))
    fisico_choices =( ('Magro','Magro'),  ('Na Medida','Na Medida'), ('Gordinho','Gordinho'), ('Obeso','Obeso') )
    sabores_choices = (
    ('Carne de panela', mark_safe('/static/css/images/carne.png') ),
    ('Frango Xadrez', mark_safe('/static/css/images/frango.png') ),
    ('Risoto Suíno', mark_safe('/static/css/images/risoto.png') )  )
    # Fields
    nome = models.CharField('Nome do seu dog', max_length=150, default="")
    sexo = models.CharField('Sexo', max_length=50, default="", choices=sexo_choices)
    castrado = models.BooleanField('Ele é castrado?', max_length=50, default=0, choices=castrado_choices)
    raca = models.CharField('Raça', max_length=100, default="")
    nascimento = models.DateField('Data de nascimento', null= True)
    peso = models.DecimalField('Peso', decimal_places=1, max_digits=3, help_text='Observação: Não sabe o peso exato? Não faz mal, você pode inserir um peso próximo.', default=0)
    pesoideal = models.DecimalField('Peso Ideal',  decimal_places=1, max_digits=3, help_text='Segundo o conselho veterinario, caso seu cão tenha até 12 meses é obrigatorio você informar o peso ideal dele quando adulto. Fique tranquilo, você pode informar o peso aproximado.', default=0, null=True, blank=True)
    atividade = models.CharField('Nivel de atividade Diária', max_length=250, default="", choices=atividade_choices)
    fisico = models.CharField('Físico do cão', max_length=100, default="", choices=fisico_choices)
    sabores = MultiSelectField('Escolha os sabores do futuro', default="", choices=sabores_choices)
    calculomes = models.DecimalField('Quantidade de ração a receber (kg/mês)',  decimal_places=1, max_digits=3, default=0)
    calculodia = models.DecimalField('Quantidade de ração diária para o cão (g/dia)', decimal_places=0, max_digits=4, default=0)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    class Meta:
        pass
    def sabores_name(self):
        return  repr(self.sabores).replace("'","").replace("[","").replace("]","")
    def calculate_age(self):
        born = self.nascimento
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("clientflow_Cachorro_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("clientflow_Cachorro_update", args=(self.pk,))


class Pedido(models.Model):

    # Relationships
    idClient = models.ForeignKey("app.Cliente", on_delete=models.CASCADE,null=True,blank=True)
    idPlano = models.ForeignKey("app.Plano", on_delete=models.CASCADE)
    idEntrega = models.OneToOneField("app.Entrega", on_delete=models.CASCADE,null=True, blank=True)
    idDog = models.ForeignKey("app.Cachorro", on_delete=models.CASCADE,null=True,blank=True, related_name='pedido')
    idCarrinho = models.ForeignKey("app.Carrinho", on_delete=models.CASCADE,null=True,blank=True, related_name='item')
    status_choices= ( ('Pedido em aberto','Pedido em aberto'), ('Carrinho criado', 'Carrinho criado'), ('Pedido finalizado pelo cliente','Pedido finalizado pelo cliente'), ('Aguardando confirmação','Aguardando confirmação'), ('Pedido em preparo','Pedido em preparo'), ('Pedido em trânsito','Pedido em trânsito'), ('Pedido concluído','Pedido concluído') )
    # Fields
    valor = models.DecimalField('Valor do pedido', default=0,  decimal_places=2, max_digits=6,)
    status = models.CharField('Status do pedido', max_length=100, default="Pedido em aberto", choices=status_choices)
    observacoes = models.TextField('Observações', default="")
    linkpagseguro = models.URLField('URL do Pagamento', default="")
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-last_updated']
        pass

    def __str__(self):
        return str(self.pk)

    def get_valor_carrinho(self):
        sum = 0
        for i in Pedido.objects.filter(idClient = self.idClient).filter(status="Pedido em aberto"):
            sum += i.valor
        sum += Decimal(self.get_valor_frete())
        return sum

    def get_valor_frete(self):
        return Decimal(9.90) if self.idEntrega.frequencia == 2 else 0

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
