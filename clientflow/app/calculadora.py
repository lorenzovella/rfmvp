from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

# Verifica se é castrado
def calcularFator(atividade, nascimento, fisico, castrado):
    idade = calculate_age(nascimento)
    if castrado:
        return switchHandlerCastradoTrue(atividade, idade, fisico)
    else:
        return switchHandlerCastradoFalse(atividade, idade, fisico)

# Verifica fisico
## castrado true
def switchHandlerCastradoTrue(atividade, idade, fisico):
    if fisico == 'Magro':
        return switchHandlerCastradoTrueFisicoBaixoPeso(atividade, idade)
    elif fisico == 'Na Medida' or fisico == 'Gordinho':
        return switchHandlerCastradoTrueFisicoIdeal(atividade, idade)
    elif fisico == 'Obeso':
        return switchHandlerCastradoTrueFisicoSobrepeso(atividade, idade)

##castrado false
def switchHandlerCastradoFalse(atividade, idade, fisico):
    if fisico == 'Magro':
        return switchHandlerCastradoFalseFisicoBaixoPeso(atividade, idade)
    elif fisico == 'Na Medida' or fisico == 'Gordinho':
        return switchHandlerCastradoFalseFisicoIdeal(atividade, idade)
    elif fisico == 'Obeso':
        return switchHandlerCastradoFalseFisicoSobrepeso(atividade, idade)

# Verifica idade
## castrado true
### baixo peso
def switchHandlerCastradoTrueFisicoBaixoPeso(atividade, idade):
    return 121.5

### peso ideal
def switchHandlerCastradoTrueFisicoIdeal(atividade, idade):
    if idade < 1:
        return 0
    elif idade < 7:
        return switchHandlerCastradoTrueFisicoIdealAdulto(atividade)
    elif idade >= 7:
        return switchHandlerCastradoTrueFisicoIdealIdoso(atividade)

### sobrepeso
def switchHandlerCastradoTrueFisicoSobrepeso(atividade, idade):
    return 54.25

## castrado false
### baixo peso
def switchHandlerCastradoFalseFisicoBaixoPeso(atividade, idade):
    return 126.5

### peso ideal
def switchHandlerCastradoFalseFisicoIdeal(atividade, idade):
    if idade < 1:
        return 0
    elif idade < 7:
        return switchHandlerCastradoFalseFisicoIdealAdulto(atividade)
    elif idade >= 7:
        return switchHandlerCastradoFalseFisicoIdealIdoso(atividade)

### sobrepeso
def switchHandlerCastradoFalseFisicoSobrepeso(atividade, idade):
    return 59.25

# Verifica atividade
## castrado True
### adulto
def switchHandlerCastradoTrueFisicoIdealAdulto(atividade):
    if atividade == 'Caminhadas Diárias':
        return 90
    elif atividade == 'Super Ativo':
        return 105
    elif atividade == 'Nivel Olímpico':
        return 125

#### idoso
def switchHandlerCastradoTrueFisicoIdealIdoso(atividade):
    if atividade == 'Caminhadas Diárias':
        return 80
    elif atividade == 'Super Ativo':
        return 85
    elif atividade == 'Nivel Olímpico':
        return 85
## castrado False
### adulto
def switchHandlerCastradoFalseFisicoIdealAdulto(atividade):
    if atividade == 'Caminhadas Diárias':
        return 95
    elif atividade == 'Super Ativo':
        return 110
    elif atividade == 'Nivel Olímpico':
        return 130

#### idoso
def switchHandlerCastradoFalseFisicoIdealIdoso(atividade):
    if atividade == 'Caminhadas Diárias':
        return 90
    elif atividade == 'Super Ativo':
        return 95
    elif atividade == 'Nivel Olímpico':
        return 95
