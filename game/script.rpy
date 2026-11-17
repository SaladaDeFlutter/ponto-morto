## =====================================================================
##  PONTO MORTO — versão reescrita para horror
## =====================================================================
##  Se você já tem define / default / transform com esses nomes em
##  outro arquivo, apague o bloco "CONFIGURAÇÃO" abaixo.
## =====================================================================


## ---------------------------------------------------------------------
##  CONFIGURAÇÃO
## ---------------------------------------------------------------------

default coragem = 0
default verdade = False
default nome_cliente = "???"
default guardou_troco = False
default releu_bilhete = False

define marta = Character("Marta", color="#d8d2c4")
define cliente = Character("[nome_cliente]", color="#8fa3a0", what_color="#b9c8c5", slow_speed=20)

## Fundo estático: sem zoom animado, a cena não se mexe.
transform respirar:
    xalign 0.5 yalign 0.5
    zoom 1.02

transform respirar_lento:
    xalign 0.5 yalign 0.5
    zoom 1.02

## Lâmpada falhando: o fundo some e volta, o vulto continua lá.
transform piscar:
    xalign 0.5 yalign 0.5
    zoom 1.03
    alpha 1.0
    pause 0.06
    alpha 0.1
    pause 0.08
    alpha 1.0
    pause 0.14
    alpha 0.25
    pause 0.05
    alpha 1.0

## Primeira entrada: ele aparece devagar, como se já estivesse ali.
transform vulto_entra:
    xalign 0.5 yalign 1.0
    alpha 0.0
    linear 1.5 alpha 1.0

## Segunda entrada: sem aviso, sem fade.
transform vulto_surge:
    xalign 0.5 yalign 1.0
    alpha 1.0

## Corte seco: ele estava longe, agora não está.
transform vulto_perto:
    xalign 0.5 yalign 1.0
    alpha 1.0
    zoom 1.25


## ---------------------------------------------------------------------
##  ABERTURA
## ---------------------------------------------------------------------

label start:

    $ quick_menu = False
    scene black
    with Dissolve(1.5)
    play music "audio/ambiente.ogg" fadein 6.0
    pause 1.5

    centered "{cps=10}{size=+12}PONTO MORTO{/size}{/cps}\n\n{size=-4}{cps=18}Km 42 · BR-116 · 03:07{/cps}{/size}{w=1.5}{nw}"
    centered "{cps=16}{i}Na BR-116, quem passa não para.\nNo Km 42, quem para não passa.{/i}{/cps}{w=2.0}{nw}"

    scene bg posto
    show bg posto at respirar
    with Dissolve(3.0)
    $ quick_menu = True


## ---------------------------------------------------------------------
##  CENA 1 — O POSTO
## ---------------------------------------------------------------------

    "A BR-116 não tem fim, só tem posto."
    "O meu fica lá no Km 42."
    "Cobertura velha de metal, duas bombas que quase não bombeiam, uma geladeira que faz mais barulho do que gela."
    "Turno começa onze hora e só acaba às seis."
    "Já rodei tanto esse balcão que o corpo se ajeita sozinho: em pé, atrás do balcão, entre o caixa e a porta."
    "Sempre de frente pra estrada, nunca de costas."
    "Lá fora quase ninguém passa, e aqui dentro só tem o zumbido da lâmpada."


## ---------------------------------------------------------------------
##  CENA 2 — O BALCÃO
## ---------------------------------------------------------------------

    scene bg balcao
    show bg balcao at respirar
    with dissolve

    "O relógio do caixa marca três e sete."
    "Pedi pro Osvaldo consertá, ele disse que conserta na segunda."
    "Tem três ano que é segunda."
    "O rádio só pega chiado, e eu deixo ligado assim memo."
    "Chiado é melhor que silêncio."
    "O café esfriou na garrafa lá pras onze e meia, e eu não esquento de novo não."
    "Tem um bilhete preso no caixa, amarelado, a letra de quem escreveu com pressa:"

    centered "{cps=22}Depois das três, não olhe pro rosto do cliente.\n\n— L.{/cps}"

    marta "Superstição do Leandro."
    "Ele sempre foi disso, e eu sempre ri."
    "Só que o Leandro não aparece desde o turno de terça."
    "Foi terça.{w=0.5} Quase certeza que foi terça."

    menu:
        "Ler o bilhete de novo.":
            $ coragem += 1
            $ releu_bilhete = True
            "Leio de novo. A letra é torta, apressada, de quem já escreveu com um pé na porta."
            "Dobro o papel e enfio no bolso, sei lá por quê."
        "Deixar o bilhete onde está.":
            "Deixo o bilhete no lugar e volto a arrumá a prateleira."
            "Que já tá arrumada, tá sempre arrumada."


## ---------------------------------------------------------------------
##  CENA 3 — PRIMEIRA VISITA
## ---------------------------------------------------------------------

    play sound "audio/clique.ogg"
    "O chiado do rádio muda de tom, como se alguém tivesse encostado o dedo na antena."

    play sound "audio/campainha.ogg"
    show vulto at vulto_entra
    "A porta abre e eu não ouvi carro nenhum chegando."
    "Entra um homem molhado dos ombros pra baixo, e não chove há semana."
    "Ele para do outro lado do balcão, a aba do boné tapando o rosto."
    "Um pingo escorre do queixo e cai no chão, faz um barulho pequeno, metálico."

    cliente "Boa noite."
    "A voz é baixa, sem pressa."
    "Já ouvi essa voz em algum canto, só não sei onde."

    cliente "Um maço de Derby.{w=0.6} E fósforo."

    play sound "audio/clique.ogg"
    "Pego o maço e passo o código, o visor pisca: 12,50."
    marta "Doze e cinquenta."
    "Ele enfia a mão no bolso e puxa uma nota de vinte dobrada em quatro."
    "Tá úmida, morna, parece pele."

    play sound "audio/clique.ogg"
    "Devolvo sete e cinquenta: uma nota de cinco, duas de um e uma de cinquenta."
    "Ele conta devagar, como quem tá aprendendo."
    cliente "Cê já esteve aqui antes?"
    marta "Eu trabalho aqui."
    cliente "Não é isso não.{w=0.6} Antes..."

    "Ele pega o maço, guarda o troco no bolso e vira as costas, abrindo a porta antes de eu falá qualquer coisa."
    play sound "audio/campainha.ogg"
    hide vulto
    with dissolve
    "A porta se fecha atrás dele, e eu ainda digo, pra porta fechada:"
    marta "Antes de quê?"

    "Quando olho pro balcão, as moedas tão lá."
    "A nota de cinco, as duas de um, a de cinquenta."
    "As mesmas que ele acabou de guardá no bolso, e o relógio continua em três e sete."

    menu:
        "Guardar o troco no caixa.":
            $ guardou_troco = True
            play sound "audio/clique.ogg"
            "Abro a gaveta, e tá vazia, sempre esteve."
            "Ponho as moedas lá dentro e fecho."
        "Deixar o troco no balcão.":
            "Deixo as moedas onde estão, que mexer nelas me dá a impressão de que alguma coisa vai começá."


## ---------------------------------------------------------------------
##  CENA 4 — SEGUNDA VISITA
## ---------------------------------------------------------------------

    play sound "audio/campainha.ogg"
    show vulto at vulto_surge
    "A campainha toca antes de eu conseguir me mexê."
    "Quando levanto os olhos, ele já tá do outro lado do balcão, a mesma roupa molhada, o mesmo pingo no queixo."
    "Só que agora a poça aos pés dele é maior."

    cliente "Boa noite, Marta."
    marta "Como é que cê sabe meu nome?"
    cliente "Tá no seu crachá."
    "Eu não uso crachá."

    cliente "Um maço de Derby.{w=0.6} E fósforo."
    "As mesmas palavras, a mesma pausa, no mesmo lugar."
    "Pego outro maço, e é aí que eu vejo: o que eu vendi ainda tá no balcão, aberto, faltando um cigarro."
    "Mas eu vi ele guardá o maço no bolso."
    marta "Cê esqueceu o seu."
    "Ele não responde, eu passo o código de novo e o visor pisca o mesmo número."

    ## A trilha morre aqui. O resto da conversa acontece em silêncio.
    stop music fadeout 0.5
    play sound "audio/estatica.ogg"
    "O rádio chia, e por um instante tem uma voz no meio do chiado:"
    centered "{cps=30}{i}«…a polícia procura o motorista\nque não parou…»{/i}{/cps}{w=1.2}{nw}"
    "O chiado engole o resto da frase."
    marta "Aqui não pega nada.{w=0.6} Nunca pegou."
    "A mão dele continua estendida, esperando o troco."

    cliente "Quanto deu?"
    marta "Doze e cinquenta."

    if guardou_troco:
        "Abro a gaveta pra pegá o troco, e ela tá vazia."
        "As moedas já tão na minha mão."
    else:
        "O troco continua no balcão, onde eu deixei."

    "As moedas tão quentes, mais quentes que antes."
    cliente "Cê já esteve aqui antes?"

    menu:
        "«Eu trabalho aqui.»":
            marta "Eu trabalho aqui, faz três ano."
            cliente "Todo mundo trabalha aqui."
        "«Quem é cê?»":
            $ coragem += 1
            marta "Quem é cê?"
            cliente "Cê sabe."
            "Ele inclina a cabeça, a aba do boné escondendo o rosto, como sempre escondeu."
        "Ficar em silêncio.":
            "Não digo nada, e o silêncio dura o bastante pro zumbido da lâmpada virar uma frase."

    hide vulto
    with dissolve
    play sound "audio/campainha.ogg"
    "A porta se fecha atrás dele, o silêncio fica, e meus dedos ainda tão quentes."


## ---------------------------------------------------------------------
##  CENA 5 — O CLÍMAX
## ---------------------------------------------------------------------

    play music "audio/tensao.ogg" fadein 3.0

    show bg balcao at piscar
    play sound "audio/estatica.ogg"
    show glitch_balcao
    with vpunch
    pause 0.12
    hide glitch_balcao

    "A lâmpada pisca, o chiado cresce."
    "O relógio continua em três e sete, e eu sinto o coração bater no lugar onde devia ter ar."

    play sound "audio/coracao.ogg"
    show vulto at vulto_perto
    "A porta fechou, mas ele não saiu."
    "Tá do meu lado do balcão, e eu não vi ele se mexê."
    cliente "Falta pouco."
    cliente "Só falta cê olhá."
    "A água que escorre dele não é água, é escura, brilha onde a luz bate, e cheira a ferro."

    menu:
        "Olhar o cartaz na parede.":
            $ verdade = True
            $ nome_cliente = "Leandro"
            "Três ano olhando pra essa parede, e eu nunca vi esse cartaz."
            "DESAPARECIDO. Leandro Souza, 34 anos. Visto pela última vez no Km 42."
            "A data é de três ano atrás, a foto é dele, e o boné é o memo."
            marta "Leandro."
            cliente "Agora cê sabe o meu nome."
        "Olhar o caixa.":
            $ verdade = True
            $ nome_cliente = "Leandro"
            "Puxo a gaveta até o fundo, e preso na madeira, por baixo, tem um cartão de ponto antigo."
            "Leandro Souza. Último registro: três ano atrás. Três e sete."
            marta "Leandro."
            cliente "Agora cê sabe o meu nome."
        "Olhar pro homem.":
            "Não preciso do cartaz pra sabê, eu só não queria lembrá."
            cliente "Sabe sim, só não quer."

    play sound "audio/coracao.ogg"
    "O relógio marca três e sete, o troco tá na minha mão, e as moedas tão quentes."

    menu:
        "«Eu não parei.»" if verdade:
            jump final_aceitar
        "«Desculpa.»" if not verdade:
            cliente "Desculpa não é nome."
            jump final_repetir
        "Continuar o turno. Não olhar.":
            jump final_repetir
        "Olhar pro rosto.":
            jump final_olhar


## ---------------------------------------------------------------------
##  FINAL 1 — O TROCO CERTO
## ---------------------------------------------------------------------

label final_aceitar:

    $ quick_menu = False
    stop music fadeout 3.0
    "Abro a boca, e a palavra sai pequena... do tamanho de uma moeda."
    marta "Eu não parei."

    "O homem fica imóvel, e por um segundo acho que ele vai dizê alguma coisa."
    "Aí os ombros dele caem, como se tivesse segurando o mundo esse tempo todo e, enfim, pudesse soltá."
    cliente "Obrigado."

    if coragem >= 2:
        "Minha voz saiu firme, sem tremê, e é a primeira coisa que eu digo em três ano que não é uma desculpa."

    "Ele deixa o maço no balcão, o troco, o boné."
    hide vulto
    with Dissolve(1.0)
    play sound "audio/campainha.ogg"
    "A porta abre, e dessa vez eu escuto os passos dele na brita se afastando."

    play sound "audio/clique.ogg"
    "O relógio do caixa faz um clique, e é três e oito."

    scene bg amanhecer
    show bg amanhecer at respirar_lento
    with Dissolve(3.0)

    "A luz entra devagar, cinza, depois dourada, e a BR aparece do jeito que é: comprida, vazia, indiferente."
    "Pego o telefone, tem tom, e faz três ano que eu não escuto um tom de discagem."
    marta "Alô?{w=0.6} Eu preciso confessá uma coisa."

    centered "{cps=14}{size=+6}O TROCO CERTO{/size}\n\n{size=-4}final 1 de 3{/size}{/cps}"
    centered "{cps=24}FIM.{/cps}"
    return


## ---------------------------------------------------------------------
##  FINAL 2 — PONTO MORTO (o loop)
## ---------------------------------------------------------------------

label final_repetir:

    $ quick_menu = False
    stop music fadeout 2.0
    play music "audio/ambiente.ogg" fadein 2.0

    "Não digo nada, pego outro maço, passo o código e devolvo o troco."
    "Ele conta as moedas devagar, como quem tá aprendendo."
    cliente "Cê já esteve aqui antes?"
    marta "Já."
    cliente "Não é isso não.{w=0.6} Antes."

    show glitch_balcao
    play sound "audio/estatica.ogg"
    pause 0.15
    hide glitch_balcao

    "O relógio marca três e sete."
    play sound "audio/campainha.ogg"

    show glitch_balcao
    with vpunch
    play sound "audio/estatica.ogg"
    pause 0.4

    scene black
    with Dissolve(0.8)
    stop music fadeout 4.0

    centered "{cps=45}três e sete{/cps}{w=0.5}{nw}"
    centered "{cps=70}três e sete{/cps}{w=0.4}{nw}"
    centered "{cps=110}três e sete{/cps}{w=0.3}{nw}"

    pause 1.5
    play sound "audio/campainha.ogg"
    pause 2.0
    centered "{cps=8}Boa noite.{/cps}{w=1.5}{nw}"

    centered "{cps=14}{size=+6}PONTO MORTO{/size}\n\n{size=-4}final 2 de 3{/size}{/cps}"
    centered "{cps=24}FIM.{/cps}"
    return


## ---------------------------------------------------------------------
##  FINAL 3 — O ROSTO
## ---------------------------------------------------------------------

label final_olhar:

    $ quick_menu = False

    ## Corte seco, sem fade: o silêncio é o susto.
    stop music

    if releu_bilhete:
        "O bilhete pesa no meu bolso, li duas vez, e mesmo assim eu olho."
    else:
        "Olho."

    "A aba do boné sobe."

    show vulto rosto at vulto_perto
    with vpunch
    play sound "audio/estatica.ogg"

    "O rosto tá lá, sempre esteve."
    "É o Leandro, o do cartaz, o do turno de terça, o que acendia o Derby com fósforo porque dizia que isqueiro dava câncer."

    play sound "audio/coracao.ogg"
    "E então o rosto muda, e é o meu."

    $ nome_cliente = "Marta"
    cliente "Agora cê sabe."
    marta "Leandro..."

    play sound "audio/estatica.ogg"
    "A lâmpada estoura, a geladeira para, o chiado vira um zunido só, comprido, e o zunido é a minha voz."

    scene black
    with Dissolve(1.0)
    play sound "audio/coracao.ogg"
    pause 1.5

    scene bg estrada
    show bg estrada at respirar_lento
    with Dissolve(2.0)

    "Tô na estrada, o farol tá quebrado, e tem alguém no acostamento."
    "Eu não paro."
    play sound "audio/coracao.ogg"
    "Eu nunca parei."

    centered "{cps=16}{size=+6}O ROSTO{/size}\n\n{size=-4}final 3 de 3{/size}{/cps}"
    centered "{cps=24}FIM.{/cps}"
    return
