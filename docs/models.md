# Models

Deixaremos em bold o primarykey do Modelo. Caso não esteja marcado, será o id

## **Subject** [Disciplina]
*dacParser/models.py*

O Modelo que armazena informações sobre um disciplina da faculdade

### Atributos
| nome atributo | tipo         | descrição                       |
| ------------- | ------------ | ------------------------------  |
| code          | String       | Código da disciplina. Ex: MC102 |
| type  	    | String       | Graducação: **U** Pós: **G**    |
| offering      | Ofering [1:n]| Oferecimentos da disciplina     |
| descryption   | String       | Ementa da matéria               |


## **Ofering** [Oferecimento]
*dacParser/models.py*

O modelo que armazena informações sobre um oferecimento de uma disciplina

### Atributos
|nome atributo| tipo          | descrição
|-------------|---------------|-
| code        | String        | Código da disciplina. Ex: MC102
| ofering_id  | String        | Determinada turma do modelo. Ex: A
| semester    | String        | Semestre do oferecimento
| year        | String        | Ano do oferecimento
| teacher     | Teacher [n:1] | Semestre do oferecimento
| vacancies   | int           | Capacidade de uma turma
| registered  | int           | Número de alunos matriculados
| student     | Student [n:n] | Alunos registrados no oferecimento


## **Student** [Aluno]
*dacParser/models.py*

O modelo que armazena informações sobre um estudante

### Atributos
|nome atributo| tipo          | descrição
|-------------|---------------|-
|***ra***     | ***String***  | ***RA de um aluno***
| name        | String        | Nome
| course      | int           | Curso de graduação [pós]
| course_type | String        | Modalidade do Curso
| oferings    | Ofering [n:n] | Oferecimentos já cursado e cursantes pelo aluno


## **Institute** [Instituto]
*dacParser/models.py*


### Atributos
|nome atributo| tipo          | descrição
|-------------|---------------|-
|    name     | String        | Nome do instituto
| ***code***  | ***String***  | ***Código do instituto. Ex: IC***


## **Teacher** [Professor]
*dacParser/models.py*


### Atributos
|nome atributo| tipo          | descrição
|-------------|---------------|-
|    name     | String        | Nome od professor


## **Token**
*gda/models.py*

Modelo que armazena os tokens gerados para cada aluno

### Atributos
|nome atributo| tipo          | descrição
|-------------|---------------|-
|   student   | Student [1:1] | Nome do professor
| ***token*** | ***String***  | ***Código do token***
|  discipline |Discipline[1:n]| Disciplina a que pertence o token
|     used    | Boolean       | afirma se já foi usada ou não
