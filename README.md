# 🚨 Análise Exploratória de Dados da Proteção Civil em Portugal

Este projeto foi desenvolvido no âmbito da unidade curricular **Fundamentos de Ciência de Dados** do **Mestrado em Controlo de Gestão e Ciência de Dados (IPV/ESTGL, 2025/2026)**.

O objetivo principal consiste na realização de uma **Análise Exploratória de Dados (EDA)** sobre ocorrências registadas pela Autoridade Nacional de Emergência e Proteção Civil (ANEPC), identificando padrões temporais, geográficos e operacionais que possam apoiar futuras iniciativas de previsão, planeamento e tomada de decisão.

## 👥 Autores

* Hélder Vieira (nº 23678)
* Bruno Barros (nº 3547)

## 📖 Enquadramento

A Proteção Civil desempenha um papel fundamental na prevenção e resposta a emergências em Portugal. A crescente disponibilidade de dados públicos permite explorar tendências e comportamentos das ocorrências registadas ao longo dos anos.

Este trabalho utiliza dados disponibilizados pela iniciativa pública Central de Dados, que agrega informação oficial de diversas entidades governamentais.

### Fonte dos Dados

* Repositório oficial: Central de Dados – Proteção Civil

## 🎯 Objetivos

* Analisar a distribuição temporal das ocorrências;
* Identificar os distritos e concelhos com maior incidência;
* Explorar padrões geográficos através de coordenadas GPS;
* Avaliar a relação entre tipos de ocorrência e recursos mobilizados;
* Detectar problemas de qualidade dos dados;
* Criar uma base sólida para futuros modelos preditivos.

## 📂 Estrutura dos Dados

O estudo utiliza dados de ocorrências da ANEPC entre:

* 2016
* 2017
* 2018
* 2019
* 2020

Os datasets incluem informações como:

* Distrito
* Concelho
* Freguesia
* Localidade
* Data e hora da ocorrência
* Tipo de ocorrência
* Número de operacionais envolvidos
* Meios terrestres mobilizados
* Coordenadas geográficas

## 🛠️ Tecnologias Utilizadas

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Scikit-Learn
* Jupyter Notebook
* ipywidgets

## 📊 Análises Realizadas

### Análise Temporal

* Distribuição das ocorrências por ano;
* Identificação de sazonalidade;
* Análise por mês e hora do dia.

### Análise Geográfica

* Distribuição das ocorrências por distrito;
* Distribuição por concelho;
* Visualização espacial utilizando latitude e longitude.

### Recursos Operacionais

* Número de operacionais envolvidos;
* Relação entre operacionais e meios terrestres;
* Avaliação de padrões operacionais por tipo de ocorrência.

## 📈 Visualizações Produzidas

O notebook inclui:

* Histogramas;
* Gráficos de barras;
* Heatmaps;
* Dashboards interativos com widgets;
* Mapas de dispersão geográfica;
* Análises comparativas por distrito e concelho.

## ✅ Conclusões

A análise exploratória permitiu identificar padrões relevantes na distribuição temporal, geográfica e tipológica das ocorrências da Proteção Civil.

Apesar de algumas limitações relacionadas com qualidade e consistência dos dados, os resultados obtidos demonstram o potencial destes dados para:

* Apoio à tomada de decisão;
* Planeamento operacional;
* Gestão do risco;
* Desenvolvimento de sistemas de monitorização;
* Criação de aplicações interativas em Streamlit;
* Desenvolvimento de modelos preditivos futuros.

## 📄 Licença

Este projeto tem fins exclusivamente académicos e utiliza dados públicos disponibilizados pela ANEPC através do projeto Central de Dados. Respeitam-se os respetivos termos de utilização e atribuição das fontes originais.
