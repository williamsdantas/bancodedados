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

##Execução do projeto
<p>A estrutura inicial do projeto era monolitica</p>
<pre>
/venv
  /lib
  /script
  app.py
  config.py
</pre>
<p>No arquivo app.py estavam definidas as classes, serviços e rotas, enquanto que no arquivo config.py estavam definidas a conexão com o banco de dados MongoDB.</p>

  
### Modularização do projeto
<p>Separação das responsabilidades em diferentes arquivos para organizar melhor o projeto.</p>
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


