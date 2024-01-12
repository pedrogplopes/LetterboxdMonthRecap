# Letterboxd Month Recap
Letterboxd Month Recap é um projeto pessoal nascido das vontades de ter uma maneira de compartilhar meu diário mensal do Letterboxd com meus amigos, e de começar meu aprendizado com o framework Django. Com esse projeto, o usuário consegue gerar retrospectivas em formato de imagem de um mês de sua escolha, baseadas no diário de seu perfil no Letterboxd. A retrospectiva é gerada em duas imagens, uma de tamanho 1014x1014 ("feed") e outra de tamanho 720x1280 ("story"): 

![schaffrillas_november_2023_story_recap](https://github.com/pedrogplopes/LetterboxdMonthRecap/assets/93411648/cb43231a-4b2c-4f46-8382-9fb1635d3be9)


![schaffrillas_november_2023_feed_recap](https://github.com/pedrogplopes/LetterboxdMonthRecap/assets/93411648/43309646-4ecf-4deb-a3a2-bc07b15ff7bc)


## Como rodar

TBA.

## Erros conhecidos

* Nomes de filmes muito longos ficam muito próximos às (e podem ultrapassar) margens horizontais da imagem:

![flanaganfilm_december_2023_story_recap](https://github.com/pedrogplopes/LetterboxdMonthRecap/assets/93411648/eb93816b-e353-4d4a-8bf8-a4eb33d15ac6)


* Uma grande quantidade de filmes ficam muito próximos às (e podem ultrapassar) margens verticais da imagem:

![flanaganfilm_december_2023_feed_recap](https://github.com/pedrogplopes/LetterboxdMonthRecap/assets/93411648/70f67809-ea5d-4acf-ae26-5d4c041cfac0)


## Adições futuras

* Correção de erros conhecidos e realização de mais testes.
* Realizar o deploy da aplicação Django e enviar retrospectivas do mês passado de maneira automatizada todo início do mês.
