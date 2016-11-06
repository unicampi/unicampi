# Contribuindo para a Unicamp API

**Nota: este documento é um sumário descrevendo o básico em contribuições.
Por favor, leia-o atentamente a fim de nos ajudar no processo de revisão.
De antemão agradecemos seu interesse em contribuir com o projeto.**


## Informando *bugs* ou sugerindo modificações

Problemas ou sugestões podem ser nos dados através do sistema de
[issues](https://github.com/gabisurita/unicampi/issues) do próprio
repositório.

-  Para sugestões, tente ser claro no POR QUÊ sua sugestão seria uma
   boa adição ao projeto. Se possível, dê exemplos de como ela poderia
   ser usada.

-  Para *bugs*, descreva o comportamento atual (considerado incorreto)
   do código e qual seria o ideal.

   Adicionalmente, se pertinente, por favor inclua informações como seu
   SO e interpretador python. Essas informações podem ser encontradas
   ao rodar o seguinte trecho de código:

  ```python
  import platform; print(platform.platform())
  import sys; print("Python", sys.version)
  ```


## Contribuindo com código

Preferencialmente, uma contribuição ao código fonte da Unicamp API é dada
pelo *forking* do [repositório principal](https://github.com/gabisurita/unicampi),
a clonagem e o desenvolvimento em um *branch* diferente do **master**:

1. Clique no botão 'Fork' no canto superior direito da página do
   [projeto](https://github.com/gabisurita/unicampi) no github. Isso cria uma
   cópia do código na sua conta pessoal.

2. Clone o repositório de sua conta para seu ambiente de trabalho local:

   ```bash
   $ git clone git@github.com:YourLogin/unicampi.git
   $ cd unicampi
   ```

3. Crie um novo *branch* com um nome representativo acerca do que você está
   desenvolvendo. Exemplo:

   ```bash
   $ git checkout -b add-feature-graduate-courses-crawling
   ```

   Procure fazer suas modificações sobre o *branch* criado, e não sobre o
   master.

4. Desenvolva suas modificações, adicionando os arquivos com ``git add`` e
   então confirmando as modificações com ``git commit``:

   ```bash
   $ git add modified_files
   $ git commit
   ```

   Verifique que suas modificações não violam nenhum teste com o
   comando `make tests`.

   *Nota 1: por favor, inclua testes e documentação para todos os
   artefatos criados ou modificados.*

   *Nota 2: liste as modificações realizadas no arquivo `CHANGELOG.rst`

   *Nota 3: se esta é sua primeira contribuição, adicione seu nome ao
   arquivo CONTRIBUTORS.rst.*


   Publique suas mudanças no servidor remoto (GitHub):

   ```bash
   $ git push -u origin add-feature-graduate-courses-crawling
   ```

5. Vá até sua página no GitHub, selecione o *branch* criado e clique
   no botão 'New pull request' -- localizado logo ao lado do botão
   utilizado para navegar entre *branches* -- para requisitar que
   suas mudanças sejam incorporadas ao repositório principal.

   Descrever o seu *pull request* é importante!

   -  Se sua *pull request* aborda uma *issue*, referencie-a pela sua hashcode
      (e.g. fixes #12). Isso associará a *issue* e o *pull request*. Em todo caso,
      sempre tenha claro o problema abordado e o que foi feito para resolvê-lo.

   -  Todos os método públicos criados precisam de docstrings informativas,
      ajudando outros colaboradores a entender como o seu código funciona.

   -  Documentação e alto nível de cobertura são necessários.

   Finalmente, clique no botão *Create pull request*.
   Os revisores serão promptamente notificados.


## Dicas para novos contribuintes

Um jeito fácil de comecar a contribuir é tentar abordar um dos problemas
na lista de [easy-pick issues](https://github.com/gabisurita/unicampi/issues?q=is%3Aopen+is%3Aissue+label%3Aeasy-pick).

Se você está confuso ou incerto sobre os passos acima, não hesite em contatar
os outros colaboradores pelo nosso [slack](https://unicampi.slack.com)
(solite um convite [aqui](https://unicampi-slack.herokuapp.com/)).
Desde já, nós agradecemos qualquer ajuda que você possa dar a este projeto!

