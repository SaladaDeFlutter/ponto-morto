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
    centered "{cps=16}{i}Tem noite que não acaba.\nTem carro que não sai do ponto morto.{/i}{/cps}{w=2.0}{nw}"

    scene bg posto
    show bg posto at respirar
    with Dissolve(3.0)
    $ quick_menu = True


## ---------------------------------------------------------------------
##  CENA 1 — O POSTO
## ---------------------------------------------------------------------

    "A BR-116 não tem fim. Só tem posto."
    "O meu fica no Km 42."
    "Uma cobertura de metal enferrujado. Duas bombas que quase não bombeiam. Uma geladeira que faz mais barulho do que gela."
    "O turno começa às onze e termina às seis. Já fiz isso tantas vezes que o corpo se ajeita sozinho: em pé, atrás do balcão, entre o caixa e a porta."
    "Sempre de frente para a estrada. Nunca de costas."
    "Lá fora, quase ninguém passa. Aqui dentro, só o zumbido da lâmpada e um silêncio que parece esperar alguma coisa."


## ---------------------------------------------------------------------
##  CENA 2 — O BALCÃO
## ---------------------------------------------------------------------

    scene bg balcao
    show bg balcao at respirar
    with dissolve

    "O relógio do caixa marca três e sete."
    "Pedi para o Osvaldo consertar. Ele disse que consertava na segunda."
    "Faz três anos que é segunda."
    "O rádio só pega chiado, mas eu deixo ligado mesmo assim."
    "Chiado é melhor do que silêncio. O silêncio deste posto tem um peso que não deveria ter."
    "A garrafa de café esfriou lá pelas onze e meia. Não esquento de novo; o cheiro de café velho ajuda a me manter acordada."
    "Preso no caixa tem um bilhete. Amarelado, a letra de quem escreveu com pressa, a caneta quase furando o papel:"

    centered "{cps=22}Depois das três, não olhe para o rosto do cliente.\n\n— L.{/cps}"

    marta "Superstição do Leandro."
    "Leandro sempre foi assim. Acreditava em tudo: sal grosso, não passar debaixo de escada, esse bilhete."
    "Eu sempre ri disso."
    "Só que o Leandro não aparece desde o turno de terça."
    "Foi terça.{w=0.5} Tenho quase certeza de que foi terça."

    menu:
        "Ler o bilhete de novo.":
            $ coragem += 1
            $ releu_bilhete = True
            "Leio de novo. A letra é torta, apressada, de quem escreveu já olhando para a porta."
            "Dobro o papel e guardo no bolso. Não sei por quê."
        "Deixar o bilhete onde está.":
            "Deixo o bilhete no lugar e volto a arrumar a prateleira."
            "Que já está arrumada. Está sempre arrumada. Tudo neste posto está sempre no mesmo lugar."


## ---------------------------------------------------------------------
##  CENA 3 — PRIMEIRA VISITA
## ---------------------------------------------------------------------

    play sound "audio/clique.ogg"
    "O chiado do rádio muda de tom. Como se alguém tivesse encostado o dedo na antena, do lado de fora."

    play sound "audio/campainha.ogg"
    show vulto at vulto_entra
    "A porta se abre. Eu não ouvi carro nenhum chegando."
    "Entra um homem molhado dos ombros aos sapatos. A água escorre dele e deixa um rastro no chão."
    "Não chove há semanas."
    "Ele para do outro lado do balcão. A aba do boné esconde o rosto."
    "Um pingo escorre do queixo e cai no chão. O barulho é pequeno. Metálico."

    cliente "Boa noite."
    "A voz é baixa. Sem pressa. Como se ele tivesse a noite inteira."
    "Eu já ouvi essa voz em algum lugar. Não consigo lembrar onde."

    cliente "Um maço de Derby.{w=0.6} E fósforo."

    play sound "audio/clique.ogg"
    "Pego o maço e passo o código. O visor pisca: 12,50."
    marta "Doze e cinquenta."
    "Ele enfia a mão no bolso e tira uma nota de vinte, dobrada em quatro."
    "Está úmida. Morna. Parece pele."

    play sound "audio/clique.ogg"
    "Devolvo sete e cinquenta: uma nota de cinco, duas moedas de um, uma de cinquenta centavos."
    "Ele conta devagar. Como quem está aprendendo a contar, ou como quem tem medo de errar."
    cliente "Você já esteve aqui antes?"
    marta "Eu trabalho aqui."
    cliente "Não.{w=0.6} Antes..."

    "Ele pega o maço, guarda o troco no bolso e vira as costas. Abre a porta antes que eu consiga dizer qualquer coisa."
    play sound "audio/campainha.ogg"
    hide vulto
    with dissolve
    "A porta se fecha atrás dele. Eu ainda digo, para a porta fechada:"
    marta "Antes de quê?"

    "Quando olho para o balcão, as moedas estão lá."
    "A nota de cinco. As duas de um. A de cinquenta."
    "As mesmas que ele acabou de guardar no bolso."
    "O relógio continua marcando três e sete."

    menu:
        "Guardar o troco no caixa.":
            $ guardou_troco = True
            play sound "audio/clique.ogg"
            "Abro a gaveta. Está vazia. Sempre esteve."
            "Coloco as moedas lá dentro e fecho."
        "Deixar o troco no balcão.":
            "Deixo as moedas onde estão."
            "Tocar nelas me dá a sensação de que alguma coisa vai começar."


## ---------------------------------------------------------------------
##  CENA 4 — SEGUNDA VISITA
## ---------------------------------------------------------------------

    play sound "audio/campainha.ogg"
    show vulto at vulto_surge
    "A campainha toca antes que eu consiga me mexer."
    "Quando levanto os olhos, ele já está do outro lado do balcão."
    "A mesma roupa molhada. O mesmo pingo no queixo."
    "Só que agora a poça aos pés dele é maior. E a água é mais escura."

    cliente "Boa noite, Marta."
    marta "Como você sabe o meu nome?"
    cliente "Está no seu crachá."
    "Eu não uso crachá."

    cliente "Um maço de Derby.{w=0.6} E fósforo."
    "As mesmas palavras. A mesma pausa, no mesmo lugar."
    "Pego outro maço. E é aí que eu vejo."
    "O que eu vendi ainda está no balcão. Aberto. Faltando um cigarro."
    "Mas eu vi quando ele guardou o maço no bolso."
    marta "Você esqueceu o seu."
    "Ele não responde. Passo o código de novo. O visor pisca o mesmo número."

    ## A trilha morre aqui. O resto da conversa acontece em silêncio.
    stop music fadeout 0.5
    play sound "audio/estatica.ogg"
    "O rádio chia. E por um instante, uma voz no meio do chiado:"
    centered "{cps=30}{i}«…a polícia procura o motorista\nque não parou…»{/i}{/cps}{w=1.2}{nw}"
    "O chiado engole o resto da frase."
    marta "Aqui não pega nada.{w=0.6} Nunca pegou."
    "A mão dele continua estendida, esperando o troco. Ela não treme."

    cliente "Quanto deu?"
    marta "Doze e cinquenta."

    if guardou_troco:
        "Abro a gaveta para pegar o troco. Está vazia."
        "As moedas já estão na minha mão."
    else:
        "O troco continua no balcão, onde eu deixei."

    "As moedas estão quentes. Mais quentes do que antes."
    cliente "Você já esteve aqui antes?"

    menu:
        "«Eu trabalho aqui.»":
            marta "Eu trabalho aqui. Faz três anos."
            cliente "Todo mundo trabalha aqui."
        "«Quem é você?»":
            $ coragem += 1
            marta "Quem é você?"
            cliente "Você sabe."
            "Ele inclina a cabeça. A aba do boné continua escondendo o rosto."
        "Ficar em silêncio.":
            "Não digo nada."
            "O silêncio dura o bastante para o zumbido da lâmpada virar uma frase que eu não quero entender."

    hide vulto
    with dissolve
    play sound "audio/campainha.ogg"
    "A porta se fecha atrás dele."
    "O silêncio fica. Meus dedos ainda estão quentes."


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

    "A lâmpada pisca. O chiado cresce."
    "O relógio continua em três e sete."
    "Eu sinto o coração bater no lugar onde deveria haver ar."

    play sound "audio/coracao.ogg"
    show vulto at vulto_perto
    "A porta fechou. Mas ele não saiu."
    "Ele está do meu lado do balcão. Eu não o vi se mover."
    cliente "Falta pouco."
    cliente "Só falta você olhar."
    "A água que escorre dele não é água. É escura, grossa, e brilha onde a luz bate."
    "Cheira a ferro."

    menu:
        "Olhar o cartaz na parede.":
            $ verdade = True
            $ nome_cliente = "Leandro"
            "Três anos olhando para essa parede, e eu nunca tinha visto esse cartaz."
            "DESAPARECIDO. Leandro Souza, 34 anos. Visto pela última vez no Km 42."
            "A data é de três anos atrás."
            "A foto é dele. O boné é o mesmo."
            marta "Leandro."
            cliente "Agora você sabe o meu nome."
        "Olhar o caixa.":
            $ verdade = True
            $ nome_cliente = "Leandro"
            "Puxo a gaveta até o fundo. Preso na madeira, por baixo, tem um cartão de ponto antigo."
            "Leandro Souza. Último registro: três anos atrás. Três e sete."
            marta "Leandro."
            cliente "Agora você sabe o meu nome."
        "Olhar para o homem.":
            "Não preciso do cartaz para saber."
            "Eu só não queria lembrar."
            cliente "Sabe, sim. Só não quer."

    play sound "audio/coracao.ogg"
    "O relógio marca três e sete."
    "O troco está na minha mão. As moedas estão quentes."

    menu:
        "«Eu não parei.»" if verdade:
            jump final_aceitar
        "«Desculpa.»" if not verdade:
            cliente "Desculpa não é nome."
            jump final_repetir
        "Continuar o turno. Não olhar.":
            jump final_repetir
        "Olhar para o rosto.":
            jump final_olhar


## ---------------------------------------------------------------------
##  FINAL 1 — O TROCO CERTO
## ---------------------------------------------------------------------

label final_aceitar:

    $ quick_menu = False
    stop music fadeout 3.0
    "Abro a boca. A palavra sai pequena."
    "Do tamanho de uma moeda."
    marta "Eu não parei."

    "O homem fica imóvel."
    "Por um segundo, acho que ele vai dizer alguma coisa."
    "Então os ombros dele caem. Como se ele estivesse segurando o mundo há três anos e, enfim, pudesse soltar."
    cliente "Obrigado."

    if coragem >= 2:
        "Minha voz saiu firme. Sem tremer."
        "É a primeira coisa que digo em três anos que não é uma desculpa."

    "Ele deixa o maço no balcão. O troco. O boné."
    hide vulto
    with Dissolve(1.0)
    play sound "audio/campainha.ogg"
    "A porta se abre. Dessa vez, eu escuto os passos dele na brita, se afastando."

    play sound "audio/clique.ogg"
    "O relógio do caixa faz um clique."
    "São três e oito."

    scene bg amanhecer
    show bg amanhecer at respirar_lento
    with Dissolve(3.0)

    "A luz entra devagar. Cinza. Depois dourada."
    "E a BR aparece do jeito que é: comprida, vazia, indiferente."
    "Pego o telefone. Tem tom."
    "Faz três anos que eu não escuto um tom de discagem."
    marta "Alô?{w=0.6} Eu preciso confessar uma coisa."

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

    "Não digo nada."
    "Pego outro maço. Passo o código. Devolvo o troco."
    "Ele conta as moedas devagar. Como quem está aprendendo."
    cliente "Você já esteve aqui antes?"
    marta "Já."
    cliente "Não.{w=0.6} Antes."

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
        "O bilhete pesa no meu bolso. Li duas vezes."
        "E mesmo assim, olho."
    else:
        "Olho."

    "A aba do boné sobe."

    show vulto rosto at vulto_perto
    with vpunch
    play sound "audio/estatica.ogg"

    "O rosto está lá. Sempre esteve."
    "É o Leandro."
    "O do cartaz. O do turno de terça."
    "O que acendia o Derby com fósforo porque dizia que isqueiro dava câncer."

    play sound "audio/coracao.ogg"
    "E então o rosto muda."
    "E é o meu."

    $ nome_cliente = "Marta"
    cliente "Agora você sabe."
    marta "Leandro..."

    play sound "audio/estatica.ogg"
    "A lâmpada estoura. A geladeira para."
    "O chiado vira um zunido só. Comprido."
    "E o zunido é a minha voz."

    scene black
    with Dissolve(1.0)
    play sound "audio/coracao.ogg"
    pause 1.5

    scene bg estrada
    show bg estrada at respirar_lento
    with Dissolve(2.0)

    "Estou na estrada."
    "O farol está quebrado."
    "Tem alguém no acostamento."
    "Eu não paro."
    play sound "audio/coracao.ogg"
    "Eu nunca parei."

    centered "{cps=16}{size=+6}O ROSTO{/size}\n\n{size=-4}final 3 de 3{/size}{/cps}"
    centered "{cps=24}FIM.{/cps}"
    return
