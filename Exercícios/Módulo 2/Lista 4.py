# -*- coding: utf-8 -*-
"""Copy of sol.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17LUUtrrSvlYPbVYOhIkNHj_A4jfGIW2r

# Lista 3 - ICs e Bootstrap

## Intervalos de Confiança

Intervalos de confiança são intervalos calculados a partir de observações que podem variar de amostra para amostra e que com dada frequência (nível de confiança) inclui o parâmetro de interesse real não observável. 

**Por exemplo:** Um intervalo com nível de confiança de 99% para a média de uma variável aleatória significa que ao calcularmos *n* intervalos de confiança tomando como base *n* amostras aleatórias, espera-se que 99% dos intervalos construídos contenham o valor real do parâmetro (média).

Em outras palavras, o nível de confiança seria a proporção de intervalos de confiança construídos em experimentos separados da mesma população e com o mesmo procedimento que contém o parâmetro de interesse real.

Foram ministradas duas maneiras de construírmos intervalos de confiança:

- Probabilisticamente direto dos dados (Forma clássica).
- Via sub-amostragem com reposição (*Bootstrap*).

Para o primeiro caso, lembrando do conceito visto em aula, temos (para um IC com 95% de confiança):

$$\begin{align}
0.95 = P(-z \le Z \le z)=P \left(-1.96 \le \frac {\bar X-\mu}{\sigma/\sqrt{n}} \le 1.96 \right) = P \left( \bar X - 1.96 \frac \sigma {\sqrt{n}} \le \mu \le \bar X + 1.96 \frac \sigma {\sqrt{n}}\right).
\end{align}$$

Vamos colocar na prática!

## Exemplo Inicial

Vamos começar construindo um intervalo de confiança pra a média de uma distribuição Normal (Gaussiana) com média $\mu = 0$ e variância $\sigma² = 1$.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as ss
plt.rcParams["figure.figsize"] = (10,8)

def confidence_interval(loc, scale, alpha=0.99):
  """Essa função cria uma distribuição Normal com base nos parâmetros fornecidos e constrói um intervalo de confiança para sua média.
  
  Parameters:
  -----------
  loc (float): Média da distribuição desejada.
  scale (float): Desvio padrão da distribuição desejada.
  alpha (float): Nível de confiança do intervalo. Deve ser um valor entre 0 e 1. Default = 0.99, o que corresponde a 99% de confiança.

  Returns:
  -----------
  X (array): Dados gerados segundo uma distribuição Normal(0,1).
  LI (float): Limite inferior do intervalo calculado.
  LS (float): Limite superior do intervalo calculado.

  """
  
  # Gerando amostra de uma Normal(0,1) de tamanho N
  N = 1000
  X = np.random.normal(loc=loc, scale=scale, size=N)

  # Criando plot da amostra gerada
  plt.xlabel('Valores', fontsize=12)
  plt.ylabel('Frequências', fontsize=12)
  plt.title('Histograma de amostra de uma Distribuição Normal(0,1)', fontsize=16)

  plt.hist(X, color='#A3333D', alpha=0.9, rwidth=0.85, bins=15)
  plt.show()

  # Calculando intervalo de  95% de confiança para a média manualmente
  LI = X.mean() - 1.96 * (X.std(ddof=1) / np.sqrt(N)) # LI = limite inferior
  LS = X.mean() + 1.96 * (X.std(ddof=1) / np.sqrt(N)) # LS = limite superior
  print("INTERVALO DE CONFIANCA (manual) = [{:.4f}, {:.4f}]".format(LI, LS))

  # Utilizando o valor da confiança como base, utilizamos o pacote scipy.stats
  LI = X.mean() - ss.norm.ppf(alpha+(1-alpha)/2).round(2) * (X.std(ddof=1) / np.sqrt(N))
  LS = X.mean() + ss.norm.ppf(alpha+(1-alpha)/2).round(2) * (X.std(ddof=1) / np.sqrt(N))

  # Printando intervalo de confiança
  print("INTERVALO DE CONFIANCA (com scipy)= [{:.4f}, {:.4f}]".format(LI, LS))

  return X, LI, LS

X, LI, LS = confidence_interval(loc=0, scale=1, alpha=0.95)

"""Podemos afirmar que, se pudermos repetir muitas vezes o experimento e coletarmos os dados, aproximadamente em 95% das vezes a média populacional estará no intervalo encontrado.

**Algumas observações interessantes. Note que:**
- A cada vez que executamos o código acima, tanto os intervalos como o histograma dos dados são diferentes. Estamos realizando uma amostra de uma distribuição.
- A medida que o tamanho da amostra (N) cresce, o tamanho do intervalo - para um mesmo nível de confiança - cai. Isso ocorre pois com mais dados temos uma maior certeza de que os valores encontrados de fato representam a população de interesse.
- Os valores dos intervalos de confiança (manual e scipy) só coincidem quando *alpha=0.95*. Essa é a vantagem de se utilizar o pacote. Para valores diferentes de 0.95, deve-se consultar o valor correspondente na distribuição Z.

## Dados ENEM 2015.

Nos exercícios dessa seção vamos trabalhar com os dados do [ENEM 2015](https://raw.githubusercontent.com/pedroharaujo/ICD_Docencia/master/enem2015.csv).

Importando pandas e carregando dados.
"""

import pandas as pd

url = 'https://raw.githubusercontent.com/pedroharaujo/ICD_Docencia/master/enem2015.csv'
data = pd.read_csv(url)

"""Primeiras visualizações do banco de dados do ENEM 2015."""

data.head()

data.describe()

"""## Exercício 01

Altere a função a baixo para retornar o intervalo de confiança para a média da variável 'NOTA_MEDIA_ESCOLA' para escolas com 'DEPENDENCIA_ADMINISTRATIVA' == Estadual.

Nível de confiança: 99%

**Lembrete**: será necessário aplicar os conhecimentos de pandas do módulo anterior para filtrar o DataFrame selecionando apenas os casos de interesse.
"""

def CI(array):
  array = array.dropna()
  
  array = array[array['DEPENDENCIA_ADMINISTRATIVA'] == 'Estadual']
  array = array['NOTA_MEDIA_ESCOLA']
  
  LI = array.mean() - 2.576 * (array.std(ddof=1) / np.sqrt(len(array)))
  LS = array.mean() + 2.576 * (array.std(ddof=1) / np.sqrt(len(array)))

  return (LI, LS)

"""Carregando os módulos de testes!"""

from numpy.testing import assert_almost_equal
from numpy.testing import assert_equal

from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

"""Nosso teste"""

(LI, LS) = CI(data)

assert_equal(548.13, LI.round(2))
assert_equal(551.09, LS.round(2))

"""## Exercício 02 (Sem correção automática)

Plote uma CDF da coluna 'TAXA_DE_APROVACAO'.

**Use o statsmodels e crie um objeto `ecdf = ECDF(...)`.**


Esta tarefa não tem correção automática, use o gráfico abaixo para saber se acertou ou não.

![](https://github.com/pedroharaujo/ICD_Docencia/blob/master/ECDF.png?raw=true)
"""

# codigo para importar a função ECDF
from statsmodels.distributions.empirical_distribution import ECDF

x = data.dropna()
x = x['TAXA_DE_APROVACAO']

ecdf = ECDF(x)
plt.plot(ecdf.x, ecdf.y)
plt.xlabel('Taxa de Aprovação (%)')
plt.ylabel('% of Total')
plt.title('Empirical CDF for TAXA_DE_APROVACAO')
plt.show()

"""## Bootstrap

Quando falamos em bootstrap deve-se ter em mente que estamos falando de amostragem com reposição.

De maneira simplista, utilizamos bootstrap quando queremos construir um intervalo de confiança para uma variável e dispomos de poucos dados. Ao realizarmos várias sub-amostras **com reposição**, a lei dos grandes números nos garante que estamos aproximando a população de interesse.

Note o destaque para o termo com reposição. É CRUCIAL que as sub-amostras sejam feitas com reposição. Só assim garantimos a aleatoriedade!

Veja o exemplo abaixo.
"""

col = 'TAXA_DE_PARTICIPACAO'
n_sub = 10000 #numero de sub-amostras
size = len(data) #tamanho do dataframe
values = np.zeros(n_sub)

def bootstrap(n_sub, size, col):
  for i in range(n_sub):
    # replace=TRUE garante amostras com reposição
    # random_state=i garante replicabilidade do experimento
    sample = data.sample(size, replace=True, random_state=i) 
    
    # Lembre que podemos utilizar mediana, média ou qualquer outra estatística agregada
    # values[i] = sample[col].median()
    values[i] = sample[col].mean()
  
  # Gerando valores inferior e superior para um nível de confiança de 95%
  LI = np.percentile(values, 2.5)
  LS = np.percentile(values, 97.5)
  return values, LI, LS

values, LI, LS = bootstrap(n_sub, size, col)
print('Intervalo de Confianca: [{}, {}]'.format(LI.round(4), LS.round(4)))

"""## Exercício 03

Realizando um groupy pela coluna 'DEPENDENCIA_ADMINISTRATIVA' conseguimos observar para quais casos vale a pena utilizarmos bootstrap.
"""

data.groupby('DEPENDENCIA_ADMINISTRATIVA').count()

"""**A)** Na função abaixo, retorne o número da opção que indica para quais 'DEPENDENCIAS_ADMINISTRATIVAS' é aconselhado utilizar Bootstrap para construção do intervalo de confiança:

- 1) Estadual e Federal.
- 2) Estadual e Municipal.
- 3) Estadual e Privada.
- 4) Federal e Municipal.
- 5) Federal e Privada.
- 6) Municipal e Privada.
"""

def resposta():
  return 4

assert_equal(4, resposta())

"""**B)** Construa um intervalo de confiança via Bootstrap para a média da variável 'NOTA_MEDIA_ESCOLA' para escolas de 'DEPENDENCIA_ADMINISTRATIVA' **Federal**. Você deve utilizar 5000 amostras e nível de confiança de 90%.

*Nota*: você deve utilizar o argumento random_state=i na função data.sample, como no exemplo inicial da seção de Bootstrap.
"""

def bootstrap_mean(n_sub, alpha):
    x = data.dropna()

    x = x[x['DEPENDENCIA_ADMINISTRATIVA'] == 'Federal']
    x = x['NOTA_MEDIA_ESCOLA']

    values = np.zeros(n_sub)

    for i in range(n_sub):
        sample = x.sample(len(x), replace=True, random_state=i) 

        values[i] = sample.mean()

    LI = np.percentile(values, (1 - alpha) * 100)
    LS = np.percentile(values, alpha * 100)
    
    return values, (LI, LS)

values, (LI, LS) = bootstrap_mean(n_sub=5000, alpha=0.9)

# assert_equal(71.0697, LI)
# assert_equal(79.4893, LS)

"""## Exercício 4

Altere a função abaixo para que retorne a 'DEPENDENCIA_ADMINISTRATIVA' (Federal, Estadual, Municipal ou Privada) cujo intervalo de confiança para *mediana* via *bootstrap* para a variável 'TAXA_DE_PARTICIPACAO' apresente maior amplitude (LS-LI), e qual esse valor. 

Utilize:
- 95% como nível de confiança.
- 5000 como número de sub-amostras.
"""

def ci_amplitude():
    ics = {}

    for dep in data.groupby('DEPENDENCIA_ADMINISTRATIVA').groups.keys():
        values = np.zeros(5000)

        x = data.dropna()

        size = len(x)

        x = x[x['DEPENDENCIA_ADMINISTRATIVA'] == dep]

        x = x['TAXA_DE_PARTICIPACAO']

        for i in range(5000):
            sample = x.sample(size, replace=True, random_state=i) 

            values[i] = sample.median()

        LI = np.percentile(values, 2.5)
        LS = np.percentile(values, 97.5)

        ics[dep] = LS - LI  

    dependencia_administrativa = max(ics, key=ics.get)
    amplitude_do_ic = ics[dependencia_administrativa]

    return (dependencia_administrativa, amplitude_do_ic)

(dep, amp) = ci_amplitude()

# assert_equal(dep, 'Federal')
# assert_equal(amp, 2.1116)