import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt

df = pd.read_csv("vendas.csv")#Para carregar o dataset

df.rename(columns={
    'Qualidade' : 'Quantidade'
}, inplace= True) #Renomeando a Coluna, o parametro "implace= True" faz alteração no dataframe sem precisar de uma nova váriavel

#O dataset foi criado com a coluna valor ja com formato em moeda "R$00,00", dai esse trecho é para converter para float
df['Preco'] = df['Preco'].str.replace('R$', '', regex= False) #Removendo o R$ de cada valor da coluna preco.
df['Preco'] = df['Preco'].str.replace(',', '.', regex= False)#Fazendo a troca da "," para .
df['Preco'] = df['Preco'].astype(float)#Convertendo de moeda para float, permitindo operações matemática

#Convertendo o valor da coluna 'Data' para datetime
df['Data'] = pd.to_datetime(df['Data'], dayfirst= True)#O parametro "dayfirst= True" informa ao pandas que o formato da data no CSV 
#é dia/mês/ano

#Criando a coluna total para armazenar o valor calculado de cada venda
df['total'] = df['Preco'] * df['Quantidade']
print(df.head(6))

#Faturamento total
faturamento_total = df['total'].sum() #Criando uma variavel para armazenar a soma de todos os valores na coluna 'total'.
print(f"\nFaturamento tota: R${faturamento_total:.2f}")

#Faturamento por produto
vendas_produto = df.groupby('Produto')['total'].sum().sort_values(ascending= False)#O metodo "df.groupby" ele agrupa os dados com base na coluna "produto", e o "['total'].sum()" soma os totais de venda para cada produto
print('\nFaturamento por Produtos')
print(vendas_produto)

#Vendas Mensais
df.set_index('Data', inplace= True)
vendas_mensais = df.resample('M')['total'].sum()
print('\nFaturamento Mensal:')
print(vendas_mensais)

#Estatisticas usando numpy
media_produto = np.mean(vendas_produto)
mediana_produto = np.median(vendas_produto)
std_produto = np.std(vendas_produto)
print(f'\nMédia faturamento dos produtos: {media_produto:.2f}')
print(f'Mediana faturamento dos produtos: {mediana_produto:.2f}')
print(f'Desvio padrão: {std_produto:.2f}')

#Vizualização da evolução do faturamento mensal
plt.figure(figsize=(10, 6))
plt.plot(vendas_mensais.index, vendas_mensais.values, marker='o', linestyle='-', color='teal')
plt.title("Evolução do Faturamento Mensal")
plt.xlabel("Mês")
plt.ylabel("Total de Vendas (R$)")
plt.grid(True)
plt.tight_layout()
plt.show()




