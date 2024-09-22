# Pós-graduação em Desenvolvimento Web Full-Stack

**Disciplina:** Banco de Dados  
**Professor:** Daniel Brandão  
**Aluno:** Williams Alves Dantas  
**E-mail:** williamsad9@gmail.com  
**RGM:** 38441381  

## Descrição do Projeto

Criamos o CRUD para Produtos e Clientes. Você deve completar com o CRUD de Pedidos, garantindo que seja feito de acordo com Produtos e Pedidos que existam nas devidas coleções.

### Tarefas

- Siga o exemplo de PEDIDOS (insert) e crie a Listagem, Alteração e Exclusão de Pedidos.
- Crie um repositório no Github e envie por e-mail: [professordanielbrandao@gmail.com](mailto:professordanielbrandao@gmail.com)
- **Prazo:** 22/09/2024

###Execução do projeto
<p>A estrutura inicial do projeto era monolitica</p>
<pre>
/venv
  /lib
  /script
  app.py
  config.py
</pre>
<p>No arquivo app.py estavam definidas as classes, serviços e rotas, enquanto que no arquivo config.py estavam definidas a conexão com o banco de dados MongoDB. A modularização traz diversos benefícios para a escalabilidade, organização e manutenção do código. </p>



  
### Modularização do projeto
<p>  A modularização traz diversos benefícios para a escalabilidade, organização e manutenção do código:

1. Organização e Legibilidade
Separar os diferentes componentes da aplicação (como rotas, lógica de negócios, validações, etc.) em módulos menores, o código fica mais organizado e fácil de entender. Isso permite que novos desenvolvedores compreendam rapidamente cada parte do sistema.

2. Separação de Responsabilidades (SoC)
A modularização segue o princípio de separação de responsabilidades, onde cada módulo é responsável por uma única parte da aplicação. Por exemplo:

3. Reutilização
Ao modularizar, é possível reutilizar o serviço de cliente em diferentes partes do código, como em outras rotas ou módulos. Se, por exemplo,  a lógica de cliente for necessária em outro contexto (como dentro de outro serviço), ela já estará desacoplada e pronta para ser reutilizada.

4. Testabilidade
A modularização facilita a criação de testes unitários, pois cada módulo (como o serviço de cliente) pode ser testado separadamente. Isso melhora a cobertura de testes e ajuda a identificar problemas em partes específicas do código.

5. Escalabilidade
À medida que o projeto cresce, a modularização permite que você expanda cada módulo de forma independente. Se, no futuro, for necessário adicionar mais lógica ao serviço de cliente ou criar novas funcionalidades, você não precisa mexer em todo o código base, apenas no módulo que precisa de ajustes.</p>

###Organização dos Módulos:
<p>
1. Models: classes de modelo em um diretório chamado models. Assim, elas ficam isoladas da lógica de rota e podem ser reutilizadas.
2. Rotas:Rotas em um unico diretório /routes. O módulo de rotas é responsável por lidar com as requisições HTTP. Isso facilita a manutenção e evita que o código de rotas se torne muito grande e misturado com a lógica de negócios.
3. Services: O módulo de serviço é responsável pela lógica de negócio.
4. Arquivo principal (app.py):O app.py registra apenas os Blueprints das rotas e inicia a aplicação.
</p>
<pre>
/venv
  /models
    cliente.py
    produto.py
    pedido.py
  /routes
    clientes.py
    produtos.py
    pedidos.py
  /services
    cliente_service.py
    produto_service.py
    pedido_service.py
  /config
    config.py
  app.py
</pre>




