# -*- coding: utf-8 -*-
"""
@author: michel
"""
import datetime 
import hashlib 
import json
from flask import Flask, jsonify, request
import requests 
from uuid import uuid4
from urllib.parse import urlparse



#primeira parte -> criar um blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction = []
        self.createBlock(proof = 1, previous_hash='0')
        self.nodes = set() #objetos do tipo set para os nós participantes da rede
    
    def createBlock(self,proof, previous_hash):
        #criando um dicionario 
        block = {'index':len(self.chain)+1,
                 'timestamp':str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash,
                 'transactions':self.transaction}
        self.transaction = []
        self.chain.append(block)
        return block
    
    #retornando o bloco anterior
    def getPreviousBlock(self):
        return self.chain[-1]
    
    #processo de mineração, achar novo nonce
    def proofOfWork(self,previous_proof):
        newProof = 1
        checkProof = False #check se a prova é correta
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2-previous_proof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1
        return newProof
    
    #gera e retorna o sha256
    def hash(self,block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self,chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            block = chain[blockIndex]
            #verificar se o previous hash do bloco atual é igual ao hash do anterior
            if block['previous_hash'] != self.hash(previousBlock):
                return False
            
            #verificar se o proof tem 0000 no inicio
            previousProof = previousBlock['proof']
            proof = block['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            
            previousBlock = block
            blockIndex += 1
        return True
    
    # criando formato de transação e retornando qual bloco vai ser adicionado
    def addTransaction(self, sender, receiver, amount):
        self.transaction.append({'sender':sender,
                                 'receiber':receiver,
                                 'amount':amount})
        previousBlock = self.getPreviousBlock()
        return previousBlock['index']+1
    
    #adicionar nós
    def addNode(self,address):
        parsedUrl =  urlparse(address)
        self.nodes.add(parsedUrl.netloc)
        
    #protocolo de consenso procurando qual é a maior rede
    def replaceChain(self):
        network = self.nodes #copia da rede
        longestChain = None #variavel de controle para checar se encotrou uma cadeia mais longa
        maxLength = len(self.chain) #para achar uma cadeia mais longa
        #saber qual é a cadeia mais longe de cada nó da rede
        for node in network: 
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['lenght']
                chain = response.json()['chain']
                if length > maxLength and self.isChainValid(chain):
                    maxLength = length #atualizar
                    longestChain = chain #atualizar chain mais novo
        if longestChain: 
            self.chain = longestChain
            return True
        return False
                            
        
            

app = Flask(__name__)

nodeAdress = str(uuid4()).replace('-', '')

blockchian = Blockchain()

@app.route('/mine_block',methods = ['GET'])
def mine_block():
    previousBlock = blockchian.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchian.proofOfWork(previousProof)
    previousHash = blockchian.hash(previousBlock)
    blockchian.addTransaction(nodeAdress, 'Vilson', 1)
    block = blockchian.createBlock(proof, previousHash)
    response = {'message':'Parabéns por minerar um bloco',
                'index': block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transaction': block['transctions']}
    return jsonify(response), 200


@app.route('/get_chain',methods = ['GET'])
def get_chain():
    response = {'chain':blockchian.chain,
                'lenght':len(blockchian.chain)}
    return jsonify(response), 200

@app.route('/is_valid',methods = ['GET'])
def is_valid():
    isValid = blockchian.isChainValid(blockchian.chain)
    if isValid:
        response = {'message':'blockchain is valid'}
    else:
        response = {'message':'blockchain is not valid'}
        
    return jsonify(response), 200

@app.route('/add_transaction',methods = ['POST'])
def add_transaction(): 
    json = request.get_json()
    transactionKeys = ['sender','receiver','amount']
    if not all(key in json for key in transactionKeys): 
        return 'Alguns elementos estão faltando', 400
    index = blockchian.addTransaction(json['sender'], json['receiver'], json['amount'])
    response = {'message':f'Esta transacao será adicionada ao bloco {index}'} 
    return jsonify(response), 201

@app.route('/connect_node',methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "vazio!", 400
    for node in nodes:
        blockchian.addNode(node)
    response = {'message': 'Todos os nós conectados',
                    'total_nodes': list(blockchian.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain',methods = ['POST'])
def replace_chain():
    isChainReplace = blockchian.replaceChain()
    if isChainReplace():
        response = {'message': 'nos foram substituidos devido a cadeias diferentes', 
                    'new_chain':blockchian.chain}
    else:
        response = {'message': 'não houve substituição',
                    'chain': blockchian}
    return jsonify(response), 201

app.run(host = '0.0.0.0', port = 5000)























