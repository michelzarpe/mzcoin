# mzcoin
## Criando demonstração de criptomoeda mzcoin

Para realizar uma demonstração de uma rede distribuida é preciso triplicar o arquivo com o codigo e mudar a porta a ser executado. As portas que vamos utilizar nos exemplos são: 
1.  app.run(host = '0.0.0.0', port = 5001)
2.  app.run(host = '0.0.0.0', port = 5002)
3.  app.run(host = '0.0.0.0', port = 5003)


### EndPoints
1. Retornar blocos do Blockchain: GET http://localhost:PORTA/get_chain
2. Adicionar nós: POST http://localhost:PORTA/connect_node
~~~
{
    "nodes": ["http://127.0.0.1:5001", 
              "http://127.0.0.1:5002", 
              "http://127.0.0.1:5003"]
}
~~~
3. Addicionar transação: POST http://localhost:PORTA/add_transaction
~~~~
{
    "sender": "",
    "receiver": "",
    "amount":   
}
~~~~
4. Minerar: GET http://localhost:PORTA/mine_block
5. Alterar blocos para maior cadeia: POST http://localhost:PORTA/replace_chain 
6. Blockchain é valido: GET http://localhost:PORTA/is_valid


Acima foi listado todos os endpoints disponiveis dentro do projeto. Primeiramente executar o endpoint 1. Depois executar o endpoint 2 adicionando todas as redes. Realizar esses dois primeiros processos para todos os arquivos executados. Depois pode adicionar transações em um nó da rede e pode minerar ele. Para ter esses mesmos blocos minerados nos outros nós (arquivos executados em portas diferentes) em casa nó executar o endpoint 5.
