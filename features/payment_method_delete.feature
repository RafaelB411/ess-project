Feature: Deletar forma de pagamento

    As a usuário 
    I want to deletar formas de pagamento
    so that eu posso remover formas de pagamento cadastradas

    Scenario: Deletar forma de pagamento (operação sucedida)
        Given eu estou logado como usuário "Henrique"
	    And eu estou na página "Formas de pagamento"
	    And eu vejo a forma de pagamento "Cascalho" de número/código "123456-789" listada no perfil
	    When eu seleciono "Remover forma de pagamento"
	    And eu seleciono "Confirmar"
	    Then eu consigo ver uma mensagem de confirmação da remoção da nova forma de pagamento
	    And eu continuo na página "Formas de pagamento"
	    And o perfil de usuário "Henrique" é registrado no sistema sem formas de pagamento cadastradas
	    And eu consigo ver que não há formas de pagamento listadas no perfil 
