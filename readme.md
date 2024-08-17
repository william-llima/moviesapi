
# Título do Projeto

Bisoflix api de filmes e series para listar filmes e listar segundo preferencias do usuario

# !importante 

Alterar as configuraçoes do arquivo database.py para apontar para o host do seu banco caso necessario.

# !importante
criar arquivo  .env com os seguintes parametros

SECRET_KEY = senha para assinatura do jwt

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = tempo de expiração do token

# rota "/users/create"

rota "/users/create"  para criar o usuario

json de envio 

{
    'email': str 
    'full_name': str 
    'password':str
}

# rota "/token"
rota para gerar o token necessario nas rotas.

dados envio

'Content-Type': 'application/x-www-form-urlencoded'

username=str

password=str

# rota "/filmes"
e uma rota get não precisa de parametros so do header Authorization: com o token jwt

# rota /usuarios/avaliacoes 
e uma rota Post onde vai ser atualizado a avalicoes dos filmes

vai precisar do header Authorization: com o token jwt

dados envio

{

    'movie_id': int > id de algum filme retornado na rota /filmes nao usar _id usar id,

    'rating':int  > de 1 a 5
}

# rota "/usuarios/watchedmovies"

e uma rota Post onde vai ser atualizado o status de assistido ou não de cada filme

vai precisar do header Authorization: com o token jwt

dados envio

{

    {'movieid':id de algum filme retornado na rota /filmes nao usar _id usar id}
}


# rota "/filmes/{usuario_id}/recomendacoes"
# !importante 
passar o usuario id na requisicao no campo indicado acima o id do usuario pode ser adquirido decodificando o token jwt nesse site https://jwt.io/.
e uma rota get onde vai ser retornado filmes de acordo com os filmes que voce assistiu e avaliações 

vai precisar do header Authorization: com o token jwt 


# !Dica Caso precise a rota '/docs' pode ajudar.

# rodar projeto comando  uvicorn main:app --reload












