# pseudo-GD[AE]
Esse é um projeto para criação do GDA + GDE, um Sistema de Avaliação de professores da Unicamp e auxilio de alunos

## Dependências
O projeto é escrito em python3.

As dependências do projeto, com suas respectivas versões, podem ser encontradas no arquivo `dependencies.txt`

É recomendado executar o código com um ambiente virtual de Python (`virtualenv`) para evitar conflitos de versões e problemas de dependencias. Para isso, execute os seguintes comandos para criar o ambiente virtual e ativá-lo

```
virtualenv env
source env/bin/activate
```

Para desativar o ambiente, basta executar o comando `deactivate`, carregado ao se ativar o ambiente.

É necessário instalar as dependencias no ambiente, para isso, execute o comando

```
pip3 install -r dependencies.txt
```
### static's
Para o design html está sendo usada o framework [Foundation](http://foundation.zurb.com/sites/docs/) . Isso pode ser alterado a qualquer momento


## Rodando
O projeto utiliza-se do [framework Django](https://www.djangoproject.com/). Para rodar execute:

```
python3 manage.py makemigrations
python3 manage.py makemigrations dacParser
python3 manage.py makemigrations gda
python3 manage.py migrate
python3 manage.py runserver
```

Para criar um usuário administrador execute `python3 manage.py createsuperuser`.

### Script
Um simples script pra rodar o django foi inserido no proejto. Para executá-lo torne-o em um executável com o comando `chmod +x run_script.sh` e o execute com:

```
./run_script
```

### Banco de dados
Para fazer o download das informações do site da dac, a path é /update/$INSTITUTO
onde $INSTITUTO é o código do instituto (IC, FEEC, FEQ, ...)
Para acessar esse path é necessário estar logado como administrador


## PEP8
O projeto tenta seguir as "normas" [PEP8](http://pep8.org/) utilizando o package pep8. Instale com `pip install pep8` e veja se o arquivo está nas normas usando `pep8 nome_do_arquivo.py`
Não use o autopep8 no projeto

Não necessáriamente estará no padrão perfeitamente mas tente seguir os seguintes principios:

```
                                                                              80
não use mais que 80 linhas (a não ser que seja um caso MUITO importante que    |
                            ficará com a aparencia muito feia se quebrar a     |
                            linha)                                             |
um espaco, entre, virgulas                                                     |
                                                                               |
(sem espco no parenteses)                                                      |
                                                                               |
funcao(sem espaco)                                                             |
```


## Todo's
Para a versão 0.5
- [ ] Remodelar os modelos e reestrutuar o código seguindo o padrão em docs
- [ ] Elaborar um modelo para o questionário [perguntas e respostas]
- [ ] Gerar a view com forms
- [ ] Elaborar as questões de avaliação dos docentes
- [X] Gerar a view para o professor
- [X] Mandar email
- [X] Gerar Tokens e lidar com a página
- [X] Refazer o modelo de disciplina usando Classe e Disciplina

Para versão 0.6
- [ ] Matérias da pós
- [ ] Criar contas de usuário
- [ ] Enviar email tanto para acadêmico quanto pessoal cadastrado em conta de usuário
- [ ] Elaborar um sistema de "crowd-data" em que os usuários podem ajudar com informações que não podem ser mineiradas
- [ ] Gerar páginas cache
- [ ] Gerar relatórios sobre avaliações das disciplinas
- [ ] Gerar relatórios sobre avaliações dos professores

Para versão 0.7 (codenome GDE--)s
- [ ] Possibilidade de email encriptado
- [X] Modalidade dos alunos
- [ ] Horário de disciplinas
- [ ] Pegar ementa de disciplinas, oferecimento (anual/semestral/etc)
- [ ] Curriculo de cursos
- [ ] Cárdapio
