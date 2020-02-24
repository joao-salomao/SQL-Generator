# SQL Generator
Script Generator é um script feito com Python 3 para gerar arquivos SQL a partir de planilhas.
  - É necessário ter o pacote pandas instalado para que o script funcione. 
  - Para mais informações sobre a instalação dessse pacote acesse o site: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
  
# Como usar
  - Os argumentos necessários são: operação(insert, update), o nome da tabela e o nome/path da planilha incluíndo a extensão do arquivo.
  - A primeira linha da planilha deve conter em suas células os nomes das colunas.
  
# Exemplo insert:
  - Ex: python sql_generator.py insert users users.xlsx
# Exemplo update:
  - PS: Quando a operação for update, a última coluna deve ser a condicional (WHERE)
  - Ex: python sql_generator.py update users users.xlsx
