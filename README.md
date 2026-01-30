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

1. pdf_to_ jpg: Conversão de entrada
   Converte o arquivo pdf em uma sequencia de imagens jpg numeradas.
   
2. align_jpg: Normalização geométrica
   Alinha as imagens para garantir compatibilidade de coordenadas.
   
3. extract_coordinates: Configuração interativa
   Realiza a captura manual das coordenadas das regiões de interesse (ROIs) do formulário por meio de interação gráfica. As
   coordenadas são automaticamente convertidas para a escala original da imagem e registradas em arquivo JSON, servindo como
   configuração para as etapas subsequentes do pipeline OCR.
   
4. visual_check: Validação visual
   Realiza a validação visual das regiões de interesse (ROIs) definidas para o formulário através do arquivo JSON construído
   anteriormente.  As coordenadas são carregadas e aplicadas sobre a imagem original do formulário, desenhando caixas
   delimitadoras e identificadores para cada alternativa.
   O objetivo dessa etapa é verificar se as coordenadas capturadas e configuradas estão corretamente posicionadas, antes da
   execução das etapas automáticas de extração, validação de marcações ou OCR. Como resultado, o script gera uma imagem anotada
   (verificacao_caixas.png), que serve como evidência visual e apoio à depuração do pipeline.
   
5. final OCR:  Extração
   Executa a extração automática das marcações dos formulários em escala de cinza. O código percorre todas as imagens de uma pasta,
   avalia cada alternativa individualmente e identifica se a opção foi marcada ou não com base na quantidade de pixels
   escuros dentro da região delimitada. Para cada alternativa, o script registra se houve marcação (0 ou 1) e o total de pixels
   escuros detectados, consolidando os resultados em um arquivo CSV estruturado.

6. ## Teste de sincronização com GitHub

