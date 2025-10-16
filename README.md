# Desafio Técnico Aiqfome
Essa API foi criada seguir as especifiações pedidas no desafio técnico para a vaga de Desenvolvedor Backend no Aiqfome.
A API foi desenvolvida em Python, utilizando o framework Django.

## Guia de instalação
Para utilizar essa API, você precisará ter o Docker instalado na sua máquina, que pode ser facilmente instalado no Windows, Linux ou MAC. Acessar [https://www.docker.com/](https://www.docker.com/) para seguir a instalação que irá melhor te servir.
Com o docker instalado, clone este repositório ou faça o download dele como um arquivo zip e, após ter os arquivos na sua máquina, entre na pasta do repositório e execute o seguinte comando

```bash
docker compose up --build -d
```

Com isso você já terá a API e todos os serviços necessários para o funcionamento dela funcionando, e você pode acessar ela em `http://localhost:8000`.  
Você pode acessar a documentação da API em `http://localhost:8000/docs`.  
Existe o registro e autenticação de usuário, após fazer o registro e se autenticar nas rotas descritas na documentação, você deve usar esse token como um `Bearer Token` para realizar as requisições autenticadas.

## Decisões de projeto

- A API foi desenvolvida com o Django por este ser um framework robusto e que possui muitos módulos prontos, facilitando no desenvolvimento onde eu pude focar apenas nas regras de negócio da API. O Django facilita disponibilizando ferramentas como a autenticação de usuários do Django, conexão com o banco de dados através do Django ORM, verificação e formatação de dados com serializers e até mesmo facilitando na conexão com um serviço de cache como o Redis.
- Todos os serviços foram encapsulados para rodar com o docker, assim facilitando a instalação e a utilização da API.
- Ao invés de criar um super usuário que pode adicionar, remover, editar e ver todos os usuário, decidi seguir o caminho do registro e login de usuários, dessa forma eu abrangi todo o CRUD porém de uma forma que se assemelha mais a realidade, podendo assim também utilizar autenticação e verificação de permissões de um usuário.
- A API é de acesso público porém com rotas autenticadas. Todas as rotas de visualização de informação (rotas GET) são públicas e não precisam de autenticação para serem acessadas, já as rotas de edição de usuário, remoção de usuário e marcar um produto como favorito para um usuário, precisam de autenticação e possuem uma verificação, onde apenas o próprio usuário pode alterar seus dados.
- Os produtos são acessados através da [fakestoreapi](https://fakestoreapi.com/docs), onde é integrado sendo uma API externa de consulta de dados, porém, se um usuário marca um produto como favorito, este produto é salvo no banco de dados para manter a integridade dos dados, já que como é uma API externa, não temos controle sobre os dados e não haveria uma ligação forte entre um usuário e um produto no banco. Quando um produto é salvo no banco, se um outro usuário quiser marcar este mesmo produto como favorito, ele não será duplicado, e sim reutilizado o já existente no banco.
- As respostas das requisições feitas à [fakestoreapi](https://fakestoreapi.com/docs) são salvas em cache durante 60 segundos, assim simulando um cenário real onde cada requisição à API é custosa, e deve ser evitado o disparo frequente de requisições para buscar uma mesma informação. Então se dois usuários buscam pela mesma informação dentro de um pequeno espaço de tempo, o segundo usuário vai receber a resposta de forma mais rápida e sem precisar realizar uma requisição à [fakestoreapi](https://fakestoreapi.com/docs).
- As funções que devem ter suas respostas salvas em cache (como por exemplo as funções de busca na [fakestoreapi](https://fakestoreapi.com/docs)), são encapsuladas por um decorator chamado `@cached_func`, onde abre a possibilidade de em um possível crescimento da API, onde será necessária a utilização de cache em outros lugares, esse decorator salva a resposta de uma função baseado na assinatura dessa função (nome da função + parâmetros).
- É feito um mapeamento de Many to Many para salvar o cliente e seus produtos favoritos, onde o cliente pode atribuir uma nota e uma review para este produto.
