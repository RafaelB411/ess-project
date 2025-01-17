Feature: Login

#Cenários de GUI

Scenario: Login do usuário
Given O sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "123456789-12" e senha "1234"
And Estou na tela "Login de usuário"
When Tento fazer login com Username "phagp", Email "phagp@cin.ufpe.br" e senha "1234"
Then Continuo na tela de "Login de usuário"
And Vejo uma mensagem de "Login realizado com sucesso"
And Eu estou logado no sistema

Scenario: Usuário informou senha incorretamente durante o login 
Given O sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "123456789-12" e senha "1234"
And Estou na tela "Login de usuário"
When Tento fazer login com Username "phagp", Email "phagp@cin.ufpe.br" e senha "12345"
Then Continuo na tela de "Login de usuário"
And Vejo uma mensagem de erro: "Senha incorreta"
And Eu continuo não estando logado ao sistema

Scenario: Usuário informou email não cadastrado durante o login 
Given O sistema não tem cadastrado nenhum usuário com Email "phagp@cin.ufpe.br"
And Estou na tela "Login de usuário"
When Tento fazer login com Username "phagp", Email "phagp@cin.ufpe.br" e senha "12345"
Then Continuo na tela de "Login de usuário"
And Vejo uma mensagem de erro: "Email não cadastrado"
And Eu continuo não estando logado ao sistema

Scenario: Usuário informou username não cadastrado durante o login 
Given O sistema não tem cadastrado nenhum usuário com Username "phagp"
And Estou na tela "Login de usuário"
When Tento fazer login com Username "phagp", Email "phagp@cin.ufpe.br" e senha "12345"
Then Continuo na tela de "Login de usuário"
And Vejo uma mensagem de erro: "Username não cadastrado"
And Eu continuo não estando logado ao sistema

#Cenários de serviço

Scenario: Login do usuário usando username
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
When Uma requisição POST é enviada para "/users/login" com Username "phagp" e senha "12345678"
Then O status da resposta deve ser "200"
And A resposta deve conter "Usuário logado com sucesso!"

Scenario: Login do usuário usando email
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
When Uma requisição POST é enviada para "/users/login" com Email "phagp@cin.ufpe.br" e senha "12345678"
Then O status da resposta deve ser "200"
And A resposta deve conter "Usuário logado com sucesso!"

Scenario: Usuário informou email incorretamente durante o login 
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
When Uma requisição POST é enviada para "/users/login" com Email "phagp2@cin.ufpe.br" e senha "12345678"
Then O status da resposta deve ser "401"
And A resposta deve conter "Email/Username ou senha inválidos."

Scenario: Usuário informou username incorretamente durante o login 
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
And O banco de dados do sistema tem cadastrado um usuário com Username "phagp2"
When Uma requisição POST é enviada para "/users/login" com Username "phagp2" e senha "12345678"
Then O status da resposta deve ser "401"
And A resposta deve conter "Email/Username ou senha inválidos."

Scenario: Usuário informou username não existente no banco de dados
Given O banco de dados do sistema não tem cadastrado nenhum usuário com Username "phagp2"
When Uma requisição POST é enviada para "/users/login" com Username "phagp2" e senha "12345678"
Then O status da resposta deve ser "401"
And A resposta deve conter "Username inválido."

Scenario: Usuário informou senha incorretamente durante o login
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
When Uma requisição POST é enviada para "/users/login" com Username "phagp" e senha "12345679"
Then O status da resposta deve ser "401"
And A resposta deve conter "Email/Username ou senha inválidos."

#Cenários de logout
#Cenários de GUI

#Cenários de serviço

Scenario: Usuário tentou logar já estando logado
Given O banco de dados do sistema tem cadastrado um usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678"
When Uma requisição POST é enviada para "/users/login" com Email "phagp@cin.ufpe.br" e senha "12345678"
Then O status da resposta deve ser "400"
And A resposta deve conter "Usuário já está logado"

Scenario: Logout do usuário
Given O usuário com Nome "Pedro", Username "phagp", Email "phagp@cin.ufpe.br" , CPF "12345678912" e senha "12345678" está logado no sistema
When Uma requisição POST é enviada para "/users/logout"
Then O status da resposta deve ser "200"
And A resposta deve conter "Usuário deslogado com sucesso!"

Scenario: Logout do usuário
Given Nenhum usuário está logado no sistema
When Uma requisição POST é enviada para "/users/logout"
Then O status da resposta deve ser "400"
And A resposta deve conter "Falha ao realizar logout: Usuário não estava logado."