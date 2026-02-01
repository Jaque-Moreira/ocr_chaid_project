# OCR + CHAID – Extração e Análise Estatística de Formulários

## Descrição
Pipeline de OCR desenvolvido em Python para extração de dados de formulários
manuscritos e impressos, seguido de análise estatística com CHAID para identificação
de padrões e segmentação de variáveis categóricas.

## Dados
Este repositório utiliza dados sintéticos exclusivamente para fins de demonstração.
Os dados originais foram removidos ou adaptados por conterem informações sensíveis.
A estrutura, o fluxo e o comportamento do pipeline permanecem idênticos ao ambiente real.

Os formulários foram digitalizados em um único arquivo .pdf em que cada página corresponde 
a um formulário individual contendo:
- cinco questões de múltipla escolha; e
- uma questão dissertativa.

A questão dissertativa **não é considerada neste projeto**, de forma deliberada,
para preservar a privacidade dos usuários e evitar o processamento de dados textuais
sensíveis.

## Pipeline de Execução
O projeto é composto por scripts independentes, executados conforme a necessidade:

1. pdf_to_ jpg.py: Conversão de entrada
   Converte o arquivo pdf em uma sequencia de imagens jpg numeradas.
   
2. align_jpg.py: Normalização geométrica
   Alinha as imagens para garantir compatibilidade de coordenadas.
   
3. extract_coordinates.py: Configuração interativa
   Realiza a captura manual das coordenadas das regiões de interesse (ROIs) do formulário por meio de interação gráfica. As
   coordenadas são automaticamente convertidas para a escala original da imagem e registradas em arquivo JSON, servindo como
   configuração para as etapas subsequentes do pipeline OCR.
   
4. visual_check.py: Validação visual
   Realiza a validação visual das regiões de interesse (ROIs) definidas para o formulário através do arquivo JSON construído
   anteriormente.  As coordenadas são carregadas e aplicadas sobre a imagem original do formulário, desenhando caixas
   delimitadoras e identificadores para cada alternativa.
   O objetivo dessa etapa é verificar se as coordenadas capturadas e configuradas estão corretamente posicionadas, antes da
   execução das etapas automáticas de extração, validação de marcações ou OCR. Como resultado, o script gera uma imagem anotada (verificacao_caixas.png), que serve como evidência visual e apoio à depuração do pipeline.
   
5. final_OCR.py:  Extração
   Executa a extração automática das marcações dos formulários em escala de cinza. O código percorre todas as imagens de uma pasta,
   avalia cada alternativa individualmente e identifica se a opção foi marcada ou não com base na quantidade de pixels
   escuros dentro da região delimitada. Para cada alternativa, o script registra se houve marcação (0 ou 1) e o total de pixels escuros detectados, consolidando os resultados em um arquivo CSV estruturado.

6. CHAID_analysis.rmd: Analise CHAID (Chi-square Automatic Interaction Detection)
   Aplica o algoritmo CHAID (Chi-square Automatic Interaction Detection) sobre os dados extraídos pelo OCR, com o objetivo de:
      -Identificar associações estatisticamente significativas entre variáveis observadas
      -Realizar a segmentação hierárquica dos dados com base em testes do qui-quadrado
   Como resultado, é gerada uma árvore de decisão CHAID, na qual:
      -Os nós superiores representam associações mais fortes (menor p-value)
      -Os nós inferiores representam associações mais fracas (maior p-value)

Os parâmetros da análise são definidos por meio da variável ctrl, permitindo controle sobre profundidade da árvore, critérios de divisão e níveis de significância.

OBS: Por se tratar de dados sensíveis, o repositório não contém formulários reais.
Foi incluída apenas uma versão genérica e anonimizada dos formulários, utilizada exclusivamente para ilustrar o procedimento de definição das Regiões de Interesse (ROIs) e a extração automática das marcações via OCR.

Da mesma forma, a análise CHAID requer um volume de dados suficientemente grande para que a significância estatística entre as categorias possa ser adequadamente mensurada.
Assim, para fins demonstrativos, a etapa de análise estatística utiliza como entrada o arquivo: mock_data_base_for_CHAID.csv

Esse conjunto de dados é sintético e tem como único objetivo ilustrar o funcionamento do algoritmo CHAID, a construção da árvore de decisão e a interpretação dos resultados, não representando dados reais ou sensíveis.

## Estrutura de Pastas do Projeto
ocr-chaid-project/
│
├── data/
│   ├── mock_data_forms.pdf
│   ├── mock_data_forms_jpg/
│   │   ├── page_01.jpg
│   │   ├── page_02.jpg
│   │   └── ...
|   |
|   ├── mock_data_base_for_CHAID.csv
│   │
│   └── mock_data_aligned_jpg/
│       ├── page_01.jpg
│       ├── page_02.jpg
│       └── ...
│
├── outcome/
│   ├── coordenadas.json
│   ├── visual_check_box.png
│   ├── resultado_final_.csv
│   └── CHAID.png
│
├── pdf_to_jpg.py
├── align_jpg.py
├── extract_coordinates.py
├── visual_check.py
├── final_ocr.py
|── CHAID_analysis.Rmd
│
├── README.md