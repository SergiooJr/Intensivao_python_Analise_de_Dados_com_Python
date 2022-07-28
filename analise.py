'''Análise de Dados com Python
    Desafio

    Você trabalha em uma empresa de telecom e tem clientes de vários serviços diferentes entre os principais: internet e telefone.
    
    O problema é que analisando o histórico dos clientes dos últimos anos você percebeu que a empresa está com Churn (cancelar um serviço) de mais de 26% dos clientes.
    Isso representa uma perda de milhões para a empresa.
    O que a empresa precisa fazer para resolver isso?
    Link Original do Kaggle: https://www.kaggle.com/radmirzosimov/telecom-users-dataset
'''



# Passo 1:
#  Importar a base de dados (vamos mofica-lá dentro do python, e não mexer no arquivo original).
import pandas as pd

tabela = pd.read_csv("telecom_users.csv")



# Passo 2:
#  Visualizar a base de dados e filtrar as informações.
# Entender as informações que você tem disponível (passar um olho na tabela)

# Decobrir os problemas da base de dados (geralmente os dois problemas principais das bases de dados são:
# 1° Se o python está vendo o tipo das informações de forma correta (número = int ou float, string = object)
# 2° Informações vázias (NaN))

# INFORMAÇÃO QUE NÃO TE AJUDA, TE APTRAPALHA

# Visualizar as infos. da tabela
'''print(tabela.info())'''



# Passo 3:
#  Tratamento de dados (resolver os problemas da base de dados).

# EXEMPLO
# 5986 linhas
# total de 22 colunas
#    #     Coluna          Conta valores preenchidos (não nulos)            Tipo do dado
#    0   IDCliente     5986 non-null (todos os valores preenchidos)         object (string)
#    .     ...                          ...                                   ...
#    4   Dependentes   5985 non-null (uma linha nn tem o valor preenchido)  object (string)

# 1° - A coluna 19 ("TotalGasto") está sendo reconhecida como object pelo python, mas deveria ser numeric
# Ajustar o tipo do "TotalGasto" de objct para int ou float
#                   TO_NUMERIC(precisa de dois parâmetros, qual a coluna, e o que fazer com os erros)
# errors = "ignore" (ignorar o erro);
# errors = "raise" (desistir de converter);
# errors = "coerce" (força a conversão, se um valor for string e não existir conversão para numérico, ele deicará o campo vázio).
tabela["TotalGasto"] = pd.to_numeric(tabela["TotalGasto"], errors="coerce") # Para pegarmos uma coluna apenas da tabela, passamos seu nome entre colchetes

# Exluir coluna inútil ('Unnamed: 0')
#                            DROP (precisa de dois parâmetros, nome da coluna ou linha (o nome da linha, é seu número) e o eixo (axis))
# Existem dois eixos:
# - axis = 0 -> Eixo da linha
# - axis = 1 -> Eixo da coluna

tabela = tabela.drop("Unnamed: 0", axis=1) # o "drop" exclui coisas

# INFORMAÇÕES VÁZIAS
            # DROPNA (exclui linhas ou colunas que possuem todas ou algumas informações vázias, depende do parâmetro)
# precisa de dois parâmetros, o <<how>>, que pode ser "all" (todas as informações) ou "any" (alguma informação), e o eixo

# colunas completamente vázias
tabela = tabela.dropna(how="all", axis=1)

# linhas que tem alguma informação vázia
#                                           IMPORTANTE
#                                se a proporção for pequena, como exemplo na coluna "TotalGasto", existem 10 linhas     com                              alguma informação vázia, porém ao todo são quase 6000 linhas, excluir essas dez não                              impactará tanto na análise.
tabela = tabela.dropna(how="any", axis=0)

# Tabela atualizada
'''print(tabela.info())'''



# Passo 4:
#  Análise inicial dos dados.
# Confirmar se o que te foi passado está certo.

# Para sabermos se 26% realmente cancelaram, temos que analisar a coluna "Churn"
# 1° Contar quantos clientes cancelaram e quantos não
'''print(tabela["Churn"].value_counts())''' # conta os valores da coluna
# percentualmente falando
'''print(tabela["Churn"].value_counts(normalize=True))''' # o "normalize" tranforma os valores em um percentual do total
# formatado
'''print(tabela["Churn"].value_counts(normalize=True).map("{:.1%}".format))''' # dois pontos significa que está sendo formatado, e o ponto um, signifca uma casa percentual (o tipo fica como object)
# resultado: 73% não cancelaram, 26% cancelaram



# Passo 5:
#  Descobrir os motivos do cancelamento.
#                           GRÁFICOS E MINI DASHBORS (utilizando plotly)
# o plotly aceita vários tipos de gráficos, ex.: de linha, histograma, etc
import plotly.express as px

# todo gráfico em python é feito em duas etapas:
# 1° etapa: criar o gráfico
for coluna in tabela.columns:
    grafico = px.histogram(tabela, x=coluna, color="Churn") # "x" é a coluna que queremos analisar, e "color" é a coluna que queremos comparar 
# 2° etapa: exibir o gráfico
    grafico.show()


# CONCLUSÕES E AÇÕES
'''
- Clientes que estão a pouco tempo cancelam muito
    - Poderíamos fazer alguma promoção dando o 1° mês de graça
    - O ínicio do serviço pro cliente ta sendo muito confuso
    - Podemos criar incentivos nos primeiros meses - primeiro ano mais barato

- Boleto eletrônico tem MUITO mais cancelamento do que as outras formas de pagamento
    - Oferecer desconto nas outras formas de pagamento

- Clientes com contrato mensal tem MUITO ais chance de cancelar
    - Dar desconto para pagar a anuidade

- Quanto mais serviço o cliente tem, menor a chance dele cancelar
    - Podemos oferecer serviços extras quase de graça

- Cliente com mais linhas, com família maior tem menos chance de cancelar
    - 2° linha de graça ou com desconto
'''
