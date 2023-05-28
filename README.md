# Bob-Alice-EncriptedChat-MongoDB

Este código implementa um sistema de chat seguro entre dois usuários, Bob e Alice, utilizando criptografia simétrica e armazenamento das mensagens em um banco de dados MongoDB.

# Dependências
Certifique-se de ter as seguintes dependências instaladas:

base64
hashlib
json
cryptography
pymongo
datetime
cryptography.fernet

# Funções Principais
gerar_chave_fernet(chave: bytes) -> bytes
Esta função recebe uma chave em bytes e retorna uma chave Fernet a partir dela. A chave é gerada utilizando o algoritmo MD5 e é convertida em base64.

inserir_bd(origin, to, wasRead, message)
Esta função insere uma nova mensagem no banco de dados. Ela recebe os parâmetros origin (usuário remetente), to (usuário destinatário), wasRead (indicador se a mensagem foi lida) e message (conteúdo da mensagem). A função utiliza a biblioteca pymongo para se conectar ao banco de dados MongoDB e insere a mensagem na coleção "messages". Em seguida, a conexão com o banco de dados é encerrada.

imprimir_bd(user)
Esta função busca todas as mensagens do usuário especificado no banco de dados e imprime na saída padrão. Ela recebe o parâmetro user (usuário) e utiliza a biblioteca pymongo para se conectar ao banco de dados MongoDB. As mensagens são buscadas na coleção "messages" filtrando pelo campo "from" igual ao usuário especificado. Em seguida, cada mensagem é impressa na tela. Após imprimir todas as mensagens, a conexão com o banco de dados é encerrada.

decifrar_msg(choice, user)
Esta função decifra uma mensagem específica do usuário no banco de dados. Ela recebe os parâmetros choice (índice da mensagem a ser decifrada) e user (usuário). A função utiliza a biblioteca pymongo para se conectar ao banco de dados MongoDB e busca a mensagem correspondente ao usuário e índice fornecidos. Em seguida, solicita ao usuário a chave secreta para decifrar a mensagem. A chave é convertida em uma chave Fernet utilizando a função gerar_chave_fernet. A mensagem cifrada é decifrada utilizando a chave Fernet e o resultado é impresso na tela. Após a decifração, a função marca a mensagem como lida no banco de dados. Por fim, a conexão com o banco de dados é encerrada.

# Funcionamento do Programa
O programa consiste em um loop principal onde o usuário é solicitado a fazer login como "Bob" ou "Alice". Após fazer o login, o usuário pode escolher entre as seguintes opções:

Enviar mensagem secreta para o outro usuário: O usuário informa a mensagem que deseja enviar e a mensagem é cifrada utilizando uma chave Fernet gerada a partir da chave secreta pré-definida. A mensagem cifrada é então inserida no banco de dados chamando a função inserir_bd.

Ler suas mensagens que estão no banco: O programa busca todas as mensagens do usuário no banco de dados e as imprime na tela chamando a função imprimir_bd. O usuário pode então escolher qual mensagem deseja ler fornecendo o índice correspondente.

Trocar de usuário: O usuário faz logout e volta para a tela de login.

# Observações
O código utiliza uma chave secreta fixa ("n sei") para gerar a chave Fernet. Em um ambiente real, essa chave deveria ser mantida em segredo e não ser compartilhada no código.

O código faz uso de uma instância do banco de dados MongoDB hospedada remotamente. O endereço de conexão com o banco de dados e as credenciais de acesso estão hardcoded no código. Em um ambiente de produção, é recomendado utilizar variáveis de ambiente para armazenar essas informações sensíveis.

O código não possui tratamento avançado de erros ou validações adicionais, sendo apenas um exemplo simplificado para fins educacionais. Em um ambiente real, é importante adicionar tratamento de erros adequado, validação de entrada do usuário e outras medidas de segurança.
