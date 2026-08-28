from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    Destination,
    DictionaryObject,
    IndirectObject,
    NameObject,
    TextStringObject,
)
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Quando Bate o Doce - Guia Situacional de Consulta DEFINITIVO v2.pdf"
TMP = ROOT / "tmp" / "pdfs" / "qbd-definitivo-v2"
PAGE_W = 390.0
PAGE_H = 844.0

CREAM = HexColor("#FFF6EE")
CREAM_2 = HexColor("#F7E7DA")
INK = HexColor("#251710")
MUTED = HexColor("#715D52")
WINE = HexColor("#A92F43")
PINK = HexColor("#E34F73")
PINK_DARK = HexColor("#C5385B")
CHOCOLATE = HexColor("#321B13")
CHOCOLATE_2 = HexColor("#4B2A1D")
GREEN = HexColor("#6E7E3D")
GREEN_SOFT = HexColor("#E8ECD9")
WHITE = colors.white
LINE = HexColor("#E7D2C4")


def register_fonts() -> None:
    fonts = {
        "QBDSerif": Path(r"C:\Windows\Fonts\georgia.ttf"),
        "QBDSerifBold": Path(r"C:\Windows\Fonts\georgiab.ttf"),
        "QBDSans": Path(r"C:\Windows\Fonts\arial.ttf"),
        "QBDSansBold": Path(r"C:\Windows\Fonts\arialbd.ttf"),
    }
    for name, path in fonts.items():
        if not path.exists():
            raise FileNotFoundError(f"Fonte obrigatoria nao encontrada: {path}")
        pdfmetrics.registerFont(TTFont(name, str(path)))


@dataclass(frozen=True)
class Category:
    id: str
    label: str
    short: str
    icon: Path
    accent: str


@dataclass(frozen=True)
class Situation:
    number: int
    group: str
    title: str
    intro: str
    when: str
    context: str
    goal: str
    tags: frozenset[str]


@dataclass(frozen=True)
class Recipe:
    id: str
    category: str
    name: str
    familiar: str
    time: str
    minutes: int
    difficulty: str
    yield_text: str
    profile: str
    ingredients: tuple[str, ...]
    steps: tuple[str, ...]
    tip: str
    tags: frozenset[str]
    appeal: str
    texture: str


ICON_DIR = ROOT / "public" / "guide-food-icons"
CATEGORIES = (
    Category("low_carb", "Receitas low carb", "Low carb", ICON_DIR / "low-carb-bowl.png", "#A65A3A"),
    Category("brigadeiro_fit", "Brigadeiro fit", "Brigadeiro fit", ICON_DIR / "brigadeiro-fit.png", "#6D3527"),
    Category("sem_acucar", "Doces sem açúcar", "Sem açúcar", ICON_DIR / "sugar-free-dessert.png", "#D18B45"),
    Category("chocolate_zero", "Chocolate zero açúcar", "Chocolate zero", ICON_DIR / "zero-sugar-chocolate.png", "#5A2A22"),
    Category("proteicas", "Opções proteicas", "Proteicas", ICON_DIR / "protein-option.png", "#B98A62"),
    Category("saudaveis", "Receitas saudáveis", "Saudáveis", ICON_DIR / "healthy-strawberry.png", "#C94E4E"),
)
CATEGORY_BY_ID = {category.id: category for category in CATEGORIES}


def S(
    number: int,
    group: str,
    title: str,
    intro: str,
    when: str,
    context: str,
    goal: str,
    tags: Iterable[str],
) -> Situation:
    return Situation(number, group, title, intro, when, context, goal, frozenset(tags))


SITUATIONS = (
    S(1, "DEPOIS DA REFEICAO", "Depois do almoco, quero algo doce", "O almoco acabou, mas ainda falta aquele fechamento doce. Escolha uma direcao que combine com esse momento e com a vontade de seguir na dieta.", "o almoco terminou e voce ainda quer um final doce", "esse final de almoco", "decidir sem improvisar", {"after_meal", "lunch", "quick5"}),
    S(2, "DEPOIS DA REFEICAO", "Depois do jantar, quero um final doce", "O jantar terminou e a vontade apareceu. Uma opcao simples pode fechar a refeicao sem virar uma busca longa ou um preparo pesado.", "o jantar acabou e ainda falta um final doce", "esse momento depois do jantar", "manter a escolha simples", {"after_meal", "dinner", "night", "quick5"}),
    S(3, "DEPOIS DA REFEICAO", "Quero so um pouco de chocolate depois da refeicao", "As vezes a vontade nao e de sobremesa; e de chocolate. Comece pelo sabor que voce reconheceu e escolha o formato que cabe agora.", "a refeicao acabou e chocolate e exatamente o que voce quer", "essa vontade pequena de chocolate", "escolher com clareza", {"after_meal", "chocolate", "quick2"}),
    S(4, "DEPOIS DA REFEICAO", "Quero algo fresco depois de comer", "Depois de comer, algo fresco pode fazer mais sentido do que uma sobremesa pesada. Procure temperatura fria, fruta ou uma textura leve.", "voce terminou de comer e quer algo fresco", "esse final de refeicao mais leve", "seguir a dieta com uma opcao coerente", {"after_meal", "cold", "fruity", "quick5"}),
    S(5, "DEPOIS DA REFEICAO", "Quero algo cremoso depois da refeicao", "A vontade veio com textura definida: cremoso. Escolha uma base compativel e deixe o sabor terminar a decisao.", "a refeicao terminou e a vontade pede cremosidade", "esse momento cremoso depois de comer", "evitar uma busca sem direcao", {"after_meal", "creamy", "quick5"}),
    S(6, "DEPOIS DA REFEICAO", "Quero sobremesa sem preparar nada", "A vontade apareceu, mas cozinhar nao faz parte do plano. Aqui entram montagens e opcoes que ja podem estar prontas.", "voce quer sobremesa sem comecar um preparo", "esse momento de zero cozinha", "continuar na dieta com pouco atrito", {"after_meal", "no_cook", "no_dishes", "quick2"}),
    S(7, "FIM DA TARDE", "Bateu vontade no fim da tarde", "O dia ainda esta acontecendo e a vontade chegou no meio dele. Escolha algo que caiba no seu tempo e ajude a manter a direcao da alimentacao.", "a vontade apareceu no fim da tarde", "essa pausa da tarde", "resolver sem perder o ritmo", {"afternoon", "quick5", "portable"}),
    S(8, "FIM DA TARDE", "Estou trabalhando e quero doce sem parar tudo", "Entre uma tarefa e outra, uma receita longa nao compete com o que ja esta pronto. Prefira algo rapido, portatil e facil de montar.", "voce esta trabalhando e nao quer parar tudo", "essa pausa curta do trabalho", "escolher sem interromper o dia", {"afternoon", "work", "portable", "quick2", "no_dishes"}),
    S(9, "FIM DA TARDE", "Quero algo doce para acompanhar o cafe", "O cafe ja faz parte do momento. Falta decidir se a companhia sera cremosa, crocante, frutada ou com chocolate.", "o cafe esta pronto e voce quer algo doce junto", "esse cafe com um acompanhamento", "manter a escolha intencional", {"afternoon", "coffee", "quick5"}),
    S(10, "FIM DA TARDE", "Quero algo doce e crocante", "Quando a textura faz parte da vontade, uma opcao cremosa nao resolve do mesmo jeito. Comece pelo crocante e escolha o sabor depois.", "a vontade pede algo que tenha crocancia", "esse desejo por textura", "escolher o que realmente combina", {"afternoon", "crunchy", "quick5"}),
    S(11, "FIM DA TARDE", "Quero doce e tenho poucos minutos", "Voce nao precisa abrir dez abas para resolver uma vontade de poucos minutos. Filtre pelo tempo e escolha entre as opcoes que realmente cabem.", "a vontade apareceu e o tempo e curto", "esses poucos minutos", "decidir rapido sem improvisar", {"afternoon", "quick2", "quick5"}),
    S(12, "NOITE", "Chegou a noite e quero beliscar doce", "A noite chegou e a vontade veio junto. Uma opcao definida evita ficar abrindo armarios sem saber o que procura.", "a noite chegou e voce quer beliscar algo doce", "esse momento de beliscar à noite", "seguir a dieta com uma escolha definida", {"night", "snack", "quick5", "no_cook"}),
    S(13, "NOITE", "Estou vendo filme ou serie e quero algo doce", "Aqui existem duas vontades: doce e pequenas mordidas durante o filme. Escolha algo facil de levar e de comer aos poucos.", "o filme comecou e voce quer algo doce por perto", "esse momento no sofa", "escolher antes de comecar a beliscar", {"night", "movie", "snack", "portable", "crunchy"}),
    S(14, "NOITE", "Quero uma sobremesa quentinha à noite", "Quando a vontade pede calor, aroma e textura entram na escolha. Uma preparacao curta pode entregar isso sem sair da direcao planejada.", "a noite pede uma sobremesa quentinha", "esse momento de conforto", "manter a escolha simples e consciente", {"night", "warm", "quick10"}),
    S(15, "NOITE", "Quero algo gelado à noite", "A temperatura ja esta decidida. Procure uma opcao fria que esteja pronta ou exija poucos passos.", "a vontade da noite pede algo bem gelado", "esse final de noite refrescante", "evitar um preparo desnecessario", {"night", "cold", "quick5"}),
    S(16, "NOITE", "Quero chocolate à noite", "E chocolate mesmo que voce quer. Agora basta escolher textura, temperatura e tempo sem transformar isso em uma lista infinita.", "a noite chegou e chocolate e o sabor certo", "essa vontade de chocolate à noite", "seguir na dieta com uma opcao compativel", {"night", "chocolate", "quick5"}),
    S(17, "CHOCOLATE", "Quero chocolate mesmo", "Quando a vontade e especifica, a busca tambem pode ser. Escolha a forma de chocolate que combina com o momento e siga direto para a receita.", "chocolate e exatamente o que voce quer agora", "essa vontade direta de chocolate", "escolher sem rodeios", {"chocolate", "quick5"}),
    S(18, "CHOCOLATE", "Quero chocolate cremoso", "O sabor esta claro e a textura tambem. Comece por uma base cremosa e escolha a intensidade do cacau ou chocolate.", "voce quer chocolate com textura cremosa", "essa vontade de colher", "resolver a escolha com poucos passos", {"chocolate", "creamy", "quick5"}),
    S(19, "CHOCOLATE", "Quero chocolate crocante", "Chocolate sozinho nao precisa carregar toda a textura. Castanhas, sementes e bases crocantes podem completar o que voce imaginou.", "voce quer chocolate com algo que faca crocancia", "essa vontade de chocolate crocante", "montar uma opcao coerente", {"chocolate", "crunchy", "quick5"}),
    S(20, "CHOCOLATE", "Quero chocolate gelado", "Gelado e chocolate funcionam melhor quando existe uma base pronta na geladeira ou no freezer. Escolha a opcao que cabe agora.", "voce quer chocolate frio ou congelado", "essa vontade de chocolate gelado", "usar o que ja esta pronto", {"chocolate", "cold", "quick5"}),
    S(21, "CHOCOLATE", "Quero chocolate em 2 minutos", "Sem forno, panela ou etapa escondida. Aqui so entram opcoes de chocolate que podem ser montadas ou servidas muito rapido.", "voce tem dois minutos e quer chocolate", "essa vontade urgente de chocolate", "chegar a uma opcao realista", {"chocolate", "quick2", "no_cook", "no_dishes"}),
    S(22, "CHOCOLATE", "Quero chocolate com fruta", "A fruta pode trazer frescor, acidez ou textura. Escolha a que voce tem e combine com uma opcao de chocolate coerente.", "voce quer juntar fruta e chocolate", "essa combinacao de fruta com cacau", "escolher pela fruta disponivel", {"chocolate", "fruity", "fruit", "quick5"}),
    S(23, "POUCO TEMPO", "Tenho 2 minutos", "Dois minutos pedem montagem, nao uma receita que esconde etapas. As opcoes abaixo foram filtradas para sair do papel de verdade.", "voce tem somente dois minutos", "essa decisao muito rapida", "evitar uma receita que nao cabe", {"quick2", "no_cook", "no_dishes"}),
    S(24, "POUCO TEMPO", "Tenho 5 minutos", "Cinco minutos permitem misturar, aquecer ou montar sem transformar a vontade em projeto de cozinha. Escolha a direcao e abra a receita.", "voce tem cinco minutos para resolver a vontade", "esse preparo curto", "manter a escolha pratica", {"quick5"}),
    S(25, "POUCO TEMPO", "Tenho 10 minutos", "Dez minutos ja permitem uma preparacao com comeco, meio e fim. Ainda assim, a receita precisa continuar simples e objetiva.", "voce tem ate dez minutos", "esse pequeno tempo de preparo", "fazer algo que realmente caiba", {"quick10", "warm"}),
    S(26, "POUCO TEMPO", "Nao quero lavar louca", "Se a louca e a barreira, use o proprio pote, uma tigela ou uma montagem direta. A melhor receita e a que voce tambem aceita limpar depois.", "voce quer doce sem criar uma pia cheia", "esse momento de pouca louca", "reduzir atrito sem perder a escolha", {"no_dishes", "no_cook", "quick2"}),
    S(27, "POUCO TEMPO", "Nao quero cozinhar", "Sem fogao, forno ou panela. Escolha uma montagem fria ou algo ja preparado e continue na direcao que planejou.", "cozinhar nao faz parte do momento", "essa vontade sem cozinha", "usar uma opcao pronta ou montada", {"no_cook", "quick2", "cold"}),
    S(28, "TEXTURA E TEMPERATURA", "Quero algo cremoso", "A textura esta definida antes do sabor. Escolha uma base cremosa e encontre a variacao que combina com a vontade de agora.", "voce quer algo doce e cremoso", "essa vontade de colher", "filtrar pela textura", {"creamy", "quick5"}),
    S(29, "TEXTURA E TEMPERATURA", "Quero algo crocante", "Crocancia pode vir de castanhas, sementes, frutas firmes ou uma base tostada. Escolha o sabor sem perder a textura.", "a vontade pede algo doce e crocante", "esse momento de textura", "escolher sem improvisar", {"crunchy", "quick5"}),
    S(30, "TEXTURA E TEMPERATURA", "Quero algo gelado", "A temperatura e o primeiro filtro. Veja o que ja esta na geladeira ou no freezer e escolha a categoria que faz sentido.", "voce quer algo doce e bem gelado", "esse momento refrescante", "usar uma opcao que ja esteja fria", {"cold", "quick5"}),
    S(31, "TEXTURA E TEMPERATURA", "Quero algo quentinho", "Aroma e temperatura fazem parte da vontade. Escolha entre bebida, creme ou fruta aquecida sem alongar o preparo.", "voce quer uma opcao doce e quentinha", "esse momento de conforto", "preparar algo curto e coerente", {"warm", "quick10"}),
    S(32, "TEXTURA E TEMPERATURA", "Quero algo frutado", "Aqui a fruta e parte principal do sabor. Escolha se voce quer algo fresco, cremoso, gelado ou aquecido.", "a vontade pede fruta de verdade", "esse desejo por algo frutado", "escolher pela sensacao que procura", {"fruity", "fruit", "quick5"}),
    S(33, "O QUE TEM EM CASA", "Quero usar a fruta que tenho em casa", "A fruta ja resolve o ponto de partida. Agora escolha a categoria e veja quais complementos simples podem transformar o momento.", "voce quer comecar pela fruta que ja tem", "essa escolha com fruta", "aproveitar o que esta disponivel", {"fruit", "fruity", "quick5"}),
    S(34, "O QUE TEM EM CASA", "Tenho iogurte em casa", "Iogurte pode virar base cremosa, gelada ou proteica. Um complemento bem escolhido costuma ser suficiente.", "o iogurte e a base que voce tem agora", "essa montagem com iogurte", "decidir apenas o complemento", {"yogurt", "creamy", "cold", "quick5"}),
    S(35, "O QUE TEM EM CASA", "Tenho aveia, granola ou sementes", "Esses ingredientes podem trazer cremosidade, estrutura ou crocancia. Escolha conforme a categoria e confira os rotulos quando necessario.", "aveia, granola ou sementes sao o ponto de partida", "essa escolha com ingredientes de despensa", "usar a textura a seu favor", {"oats", "seeds", "crunchy", "warm"}),
    S(36, "O QUE TEM EM CASA", "Tenho cacau ou chocolate", "O sabor ja esta resolvido. Falta escolher uma base, a textura e o tempo que voce realmente tem.", "cacau ou chocolate ja estao disponiveis", "essa escolha com sabor de chocolate", "evitar procurar uma receita inteira", {"cocoa", "chocolate", "quick5"}),
    S(37, "O QUE TEM EM CASA", "Tenho poucos ingredientes em casa", "Com poucos ingredientes, a pergunta util e qual base ainda esta disponivel. As opcoes abaixo priorizam listas curtas e preparo simples.", "quase nao ha ingredientes disponiveis", "esse momento de despensa curta", "montar algo com o basico", {"minimal", "quick5", "no_dishes"}),
)


def R(
    id: str,
    category: str,
    name: str,
    familiar: str,
    time: str,
    minutes: int,
    difficulty: str,
    yield_text: str,
    profile: str,
    ingredients: Sequence[str],
    steps: Sequence[str],
    tip: str,
    tags: Iterable[str],
    appeal: str,
    texture: str,
) -> Recipe:
    return Recipe(
        id,
        category,
        name,
        familiar,
        time,
        minutes,
        difficulty,
        yield_text,
        profile,
        tuple(ingredients),
        tuple(steps),
        tip,
        frozenset(tags),
        appeal,
        texture,
    )


RECIPES = (
    # Receitas low carb - o enquadramento depende da escolha de ingredientes e dos rotulos.
    R("lc01", "low_carb", "Creme morno de cacau e amendoim", "Quando voce quer chocolate cremoso com uma lista curta de ingredientes.", "2 min", 2, "Facil", "1 porcao", "Low carb culinario", ["2 c.s. de pasta de amendoim sem acucar", "1 c.cha de cacau em po", "1 a 2 c.s. de agua", "adocante culinario, opcional"], ["Misture a pasta e o cacau.", "Ajuste com agua e aqueça por 20 segundos, se quiser."], "Confira no rotulo se a pasta nao possui acucar adicionado.", {"quick2", "no_cook", "no_dishes", "creamy", "cocoa", "minimal", "coffee", "warm"}, "um creme morno e intenso de cacau", "cremosa e morna"),
    R("lc02", "low_carb", "Morangos com iogurte e nibs", "Uma opcao fresca para quando a vontade pede fruta e cremosidade.", "2 min", 2, "Facil", "1 porcao", "Low carb culinario", ["5 morangos", "3 c.s. de iogurte natural sem acucar", "1 c.cha de nibs de cacau", "baunilha"], ["Fatie os morangos.", "Sirva com iogurte, nibs e baunilha."], "Confira os carboidratos do iogurte no rotulo.", {"quick2", "no_cook", "no_dishes", "cold", "fruit", "fruity", "creamy", "yogurt", "cocoa", "crunchy"}, "fruta fresca com iogurte e cacau", "fresca e crocante"),
    R("lc03", "low_carb", "Cafe cremoso com cacau", "Para uma vontade de chocolate que combina com a pausa do cafe.", "2 min", 2, "Facil", "1 copo", "Low carb culinario", ["1/2 xic. de cafe frio ou quente", "2 c.s. de creme de leite", "1 c.cha de cacau", "gelo e adocante, opcionais"], ["Misture cafe, creme e cacau.", "Sirva quente ou com gelo."], "Dissolva o cacau em uma colher de cafe antes de misturar tudo.", {"quick2", "no_cook", "no_dishes", "cold", "warm", "creamy", "cocoa", "coffee", "minimal"}, "cafe com chocolate e poucos passos", "cremosa"),
    R("lc04", "low_carb", "Pudim de chia e coco", "Bom para deixar pronto e encontrar uma opcao gelada na hora da vontade.", "5 min de preparo + 2 h de geladeira", 5, "Facil", "1 porcao", "Low carb culinario", ["150 ml de leite de coco sem acucar", "2 c.s. de chia", "baunilha", "adocante culinario, opcional"], ["Misture todos os ingredientes.", "Leve a geladeira por pelo menos 2 horas."], "Mexa novamente depois de 10 minutos para distribuir a chia.", {"cold", "creamy", "no_cook", "seeds", "make_ahead", "minimal"}, "um doce gelado que pode ficar pronto", "gelada e cremosa"),
    R("lc05", "low_carb", "Cheesecake de pote com cacau", "Quando voce quer gosto de sobremesa sem precisar preparar uma massa.", "5 min", 5, "Facil", "1 porcao", "Low carb culinario", ["3 c.s. de cream cheese", "2 c.s. de iogurte natural sem acucar", "1 c.cha de cacau", "2 morangos", "adocante, opcional"], ["Misture cream cheese, iogurte e cacau.", "Finalize com os morangos picados."], "Confira os carboidratos dos laticinios no rotulo.", {"quick5", "no_cook", "cold", "creamy", "fruit", "yogurt", "after_meal", "cocoa"}, "uma sobremesa cremosa de cacau e fruta", "cremosa e fresca"),
    R("lc06", "low_carb", "Trufas crocantes de coco e cacau", "Pequenas mordidas para quando voce quer algo mais intenso e definido.", "8 min", 8, "Facil", "4 unidades", "Low carb culinario", ["3 c.s. de coco ralado sem acucar", "1 c.s. de pasta de amendoim", "1 c.cha de cacau", "1 c.s. de sementes de abobora picadas", "adocante, opcional"], ["Misture tudo ate dar liga.", "Modele e passe nas sementes picadas."], "Se a massa estiver seca, use gotas de agua.", {"quick10", "no_cook", "cocoa", "snack", "portable", "seeds", "movie", "crunchy"}, "mordidas crocantes de coco com cacau", "firme e crocante"),
    R("lc07", "low_carb", "Cacau quente com leite de coco", "Uma bebida curta para quando a vontade pede calor e aroma de chocolate.", "4 min", 4, "Facil", "1 xicara", "Low carb culinario", ["180 ml de leite de coco sem acucar", "1 c.cha de cacau", "canela", "adocante culinario, opcional"], ["Aqueça o leite de coco sem ferver.", "Misture cacau, canela e adocante."], "Confira no rotulo se o leite de coco nao possui acucar adicionado.", {"quick5", "warm", "creamy", "cocoa", "minimal", "no_dishes"}, "uma bebida quente de cacau", "quente e cremosa"),
    R("lc08", "low_carb", "Iogurte com coco, castanhas e nibs", "Para resolver a vontade com uma base que pode estar na geladeira.", "2 min", 2, "Facil", "1 porcao", "Low carb culinario", ["1/2 xic. de iogurte natural sem acucar", "1 c.s. de coco sem acucar", "1 c.s. de castanhas picadas", "1 c.cha de nibs de cacau"], ["Coloque o iogurte no pote.", "Finalize com coco, castanhas e nibs."], "Coloque os crocantes apenas na hora de comer.", {"quick2", "no_cook", "no_dishes", "cold", "creamy", "yogurt", "minimal", "crunchy", "seeds", "cocoa"}, "iogurte gelado com cacau e crocancia", "cremosa e crocante"),
    R("lc09", "low_carb", "Castanhas ou sementes com creme de cacau", "Boa para beliscar algo doce sem transformar o momento em preparo longo.", "1 min", 1, "Facil", "1 porcao", "Low carb culinario", ["1 pequeno punhado de castanhas ou sementes", "1 c.s. de creme de cacau sem acucar", "canela, opcional"], ["Separe as castanhas ou sementes em um pote.", "Use o creme como acompanhamento."], "Confira o rotulo do creme e mantenha a porcao definida.", {"quick2", "no_cook", "no_dishes", "crunchy", "portable", "snack", "movie", "coffee", "minimal", "seeds", "cocoa"}, "crocancia com sabor de cacau", "crocante e cremosa"),
    R("lc10", "low_carb", "Morango gelado com creme de coco e cacau", "Quando a vontade pede algo fresco, doce e muito simples de montar.", "3 min", 3, "Facil", "1 porcao", "Low carb culinario", ["5 morangos gelados", "2 c.s. de creme de coco sem acucar", "1/2 c.cha de cacau", "adocante, opcional"], ["Misture creme de coco e cacau.", "Sirva com os morangos gelados."], "Deixe a fruta bem fria para aumentar a sensacao de sobremesa.", {"quick5", "no_cook", "cold", "fruit", "fruity", "creamy", "minimal", "cocoa"}, "morango frio com creme de cacau", "fresca e cremosa"),

    # Brigadeiros fit - nenhum usa a base convencional de leite condensado e manteiga.
    R("bf01", "brigadeiro_fit", "Brigadeiro proteico de colher", "Um creme de cacau para quando voce quer brigadeiro, mas prefere outra composicao.", "3 min", 3, "Facil", "1 porcao", "Brigadeiro fit proteico", ["3 c.s. de iogurte de maior teor proteico", "1 medida de proteina em po", "1 c.cha de cacau", "agua, se necessario"], ["Misture iogurte, proteina e cacau.", "Ajuste a textura com gotas de agua."], "O teor de proteina depende do rotulo dos produtos usados.", {"quick5", "no_cook", "cold", "creamy", "cocoa", "yogurt", "protein", "after_meal"}, "sabor de brigadeiro com base proteica", "cremosa"),
    R("bf02", "brigadeiro_fit", "Brigadeiro de banana e cacau", "Para quando uma banana madura pode virar um doce de colher em minutos.", "2 min", 2, "Facil", "1 porcao", "Brigadeiro fit com fruta", ["1/2 banana bem madura", "1 c.cha de cacau", "1 c.s. de leite em po, opcional"], ["Amasse muito bem a banana.", "Misture o cacau e aqueça por 30 segundos, se quiser."], "Use banana bem madura para uma textura mais uniforme.", {"quick2", "no_cook", "no_dishes", "creamy", "fruit", "cocoa", "minimal", "warm"}, "um doce de banana com cacau", "cremosa"),
    R("bf03", "brigadeiro_fit", "Brigadeiro crocante de amendoim", "Quando voce quer um sabor mais intenso e uma receita de duas etapas.", "2 min", 2, "Facil", "1 porcao", "Brigadeiro fit", ["1 c.s. de pasta de amendoim sem acucar", "1 c.s. de leite em po", "1 c.cha de cacau", "1 c.s. de sementes de abobora picadas", "agua aos poucos"], ["Misture pasta, leite em po e cacau.", "Ajuste com agua e finalize com as sementes."], "Confirme no rotulo que a pasta nao possui acucar adicionado.", {"quick2", "no_cook", "no_dishes", "creamy", "cocoa", "coffee", "seeds", "crunchy"}, "brigadeiro de cacau com amendoim", "densa e crocante"),
    R("bf04", "brigadeiro_fit", "Brigadeiro de leite em po com toque de cacau", "Uma versao rapida para quando voce quer um brigadeiro mais suave.", "2 min", 2, "Facil", "1 porcao", "Brigadeiro fit", ["3 c.s. de leite em po", "1/2 c.cha de cacau", "agua aos poucos", "adocante culinario, opcional"], ["Misture leite em po e cacau.", "Acrescente agua ate formar creme."], "Leite possui acucares naturais; a receita nao recebe acucar adicionado.", {"quick2", "no_cook", "no_dishes", "creamy", "minimal", "cocoa"}, "um brigadeiro suave de cacau", "cremosa"),
    R("bf05", "brigadeiro_fit", "Brigadeiro de coco, chia e cacau", "Boa para quem quer uma textura mais firme e gosto de coco.", "5 min", 5, "Facil", "4 unidades", "Brigadeiro fit", ["3 c.s. de coco em flocos sem acucar", "2 c.s. de iogurte natural", "1 c.cha de cacau", "1 c.s. de chia", "adocante, opcional"], ["Misture ate formar massa umida.", "Modele e passe em coco seco."], "Deixe 10 minutos na geladeira se quiser mais firme.", {"quick5", "no_cook", "cocoa", "yogurt", "portable", "seeds", "crunchy"}, "coco com cacau em pequenas mordidas", "macia e levemente crocante"),
    R("bf06", "brigadeiro_fit", "Brigadeiro de batata-doce", "Uma opcao de preparo curto quando voce ja tem batata-doce cozida.", "8 min de preparo - batata ja cozida", 8, "Facil", "5 unidades", "Brigadeiro fit", ["1/2 xic. de batata-doce cozida", "1 c.s. de cacau", "1 c.s. de leite em po", "adocante, opcional"], ["Amasse a batata ate ficar lisa.", "Misture os demais ingredientes e modele."], "A receita fica mais rapida com a base ja cozida e fria.", {"quick10", "cocoa", "make_ahead", "portable", "warm"}, "brigadeiro macio com base preparada", "macia"),
    R("bf07", "brigadeiro_fit", "Brigadeiro de aveia e cacau", "Para uma vontade de colher com ingredientes comuns de despensa.", "5 min", 5, "Facil", "1 porcao", "Brigadeiro fit", ["2 c.s. de aveia fina", "3 c.s. de leite", "1 c.cha de cacau", "1/2 banana amassada"], ["Misture tudo em uma tigela.", "Aqueça por 60 a 90 segundos, mexendo na metade."], "Use recipiente alto para evitar transbordamento.", {"quick5", "warm", "creamy", "cocoa", "oats", "fruit", "no_dishes"}, "um creme quente de aveia e cacau", "cremosa e quente"),
    R("bf08", "brigadeiro_fit", "Brigadeiro de abacate e cacau", "Quando voce quer cremosidade fria e tem abacate maduro.", "3 min", 3, "Facil", "1 porcao", "Brigadeiro fit com fruta", ["1/4 de abacate maduro", "1 c.s. de cacau", "adocante culinario, opcional", "gotas de baunilha"], ["Amasse o abacate ate ficar liso.", "Misture cacau, baunilha e adocante."], "Sirva gelado para suavizar o sabor do abacate.", {"quick5", "no_cook", "cold", "creamy", "cocoa", "fruit", "minimal"}, "um creme frio e intenso de cacau", "cremosa e fria"),
    R("bf09", "brigadeiro_fit", "Brigadeiro de grao-de-bico e nibs", "Uma alternativa para quando existe grao-de-bico cozido pronto na geladeira.", "7 min de preparo - grao-de-bico ja cozido", 7, "Media", "6 unidades", "Brigadeiro fit", ["1/2 xic. de grao-de-bico cozido", "1 c.s. de cacau", "1 c.s. de pasta de amendoim", "1 c.s. de nibs de cacau", "adocante, opcional"], ["Processe tudo, menos os nibs.", "Modele e passe nos nibs."], "Retire bem a pele do grao-de-bico para textura mais lisa.", {"quick10", "cocoa", "make_ahead", "portable", "seeds", "crunchy"}, "mordidas de cacau com crocancia", "firme e crocante"),
    R("bf10", "brigadeiro_fit", "Brigadeiro gelado de iogurte e morango", "Para uma vontade de brigadeiro que combina melhor com algo frio.", "3 min de preparo + freezer", 3, "Facil", "4 unidades", "Brigadeiro fit", ["3 c.s. de iogurte natural", "1 c.s. de leite em po", "1 c.cha de cacau", "2 morangos picados", "adocante, opcional"], ["Misture os ingredientes.", "Distribua em forminhas e congele ate firmar."], "Deixe porcoes prontas e retire alguns minutos antes de comer.", {"cold", "make_ahead", "cocoa", "yogurt", "portable", "fruit"}, "pequenas porcoes geladas de cacau e fruta", "gelada e cremosa"),

    # Doces sem acucar - nesta categoria significa sem adicao de acucares.
    R("sa01", "sem_acucar", "Banana com cacau e canela", "A fruta madura faz o trabalho doce sem receber acucar na receita.", "2 min", 2, "Facil", "1 porcao", "Sem adicao de acucar", ["1 banana pequena", "1 c.cha de cacau", "canela"], ["Fatie ou amasse a banana.", "Finalize com cacau e canela."], "Use banana madura para um sabor naturalmente mais doce.", {"quick2", "no_cook", "no_dishes", "fruit", "cocoa", "minimal", "creamy"}, "fruta doce com cacau", "macia"),
    R("sa02", "sem_acucar", "Maca quente com canela", "Quando o aroma de sobremesa importa mais do que uma lista longa.", "4 min", 4, "Facil", "1 porcao", "Sem adicao de acucar", ["1 maca", "canela", "1 c.s. de agua"], ["Pique a maca e coloque em uma tigela.", "Aqueça por 2 a 3 minutos e finalize com canela."], "Cubra parcialmente para a fruta cozinhar no proprio vapor.", {"quick5", "warm", "fruit", "minimal", "no_dishes", "after_meal"}, "fruta quente e aromatica", "macia e quente"),
    R("sa03", "sem_acucar", "Pera morna com baunilha", "Uma opcao simples para quando voce quer fruta quente e delicada.", "4 min", 4, "Facil", "1 porcao", "Sem adicao de acucar", ["1 pera madura", "baunilha", "canela, opcional"], ["Corte a pera em cubos.", "Aqueça por 2 minutos e tempere com baunilha."], "Pera madura precisa de menos tempo e fica mais perfumada.", {"quick5", "warm", "fruit", "fruity", "minimal", "no_dishes"}, "fruta morna com aroma de baunilha", "macia e quente"),
    R("sa04", "sem_acucar", "Compota rapida de morango e chia", "Boa quando voce quer colheradas de fruta com textura de geleia.", "8 min de preparo", 8, "Facil", "2 porcoes", "Sem adicao de acucar", ["1 xic. de morangos", "1 c.s. de chia", "2 c.s. de agua"], ["Aqueça os morangos e amasse.", "Misture a chia e espere engrossar."], "Guarde refrigerada e consuma em curto prazo.", {"quick10", "warm", "fruit", "fruity", "seeds", "make_ahead", "creamy"}, "morango concentrado sem acucar adicionado", "cremosa com sementes"),
    R("sa05", "sem_acucar", "Mamao com coco e nibs de cacau", "Para quando fruta fresca ja parece a resposta certa.", "2 min", 2, "Facil", "1 porcao", "Sem adicao de acucar", ["1/2 mamao pequeno", "1 c.s. de coco em laminas sem acucar", "1 c.cha de nibs de cacau", "canela"], ["Corte o mamao.", "Finalize com coco, nibs e canela."], "Coloque os crocantes apenas na hora de comer.", {"quick2", "no_cook", "cold", "fruit", "fruity", "minimal", "crunchy", "cocoa"}, "fruta fresca com coco e cacau", "macia e crocante"),
    R("sa06", "sem_acucar", "Uvas geladas com cacau", "Pequenas mordidas para quando voce quer algo frio e facil de levar.", "2 min", 2, "Facil", "1 porcao", "Sem adicao de acucar", ["1/2 xic. de uvas geladas", "1/2 c.chá de cacau", "coco sem acucar, opcional"], ["Seque bem as uvas.", "Polvilhe pouco cacau e misture."], "Use uma peneira pequena para distribuir o cacau.", {"quick2", "no_cook", "cold", "fruit", "cocoa", "portable", "movie", "no_dishes", "crunchy"}, "fruta gelada em pequenas mordidas", "gelada e firme"),
    R("sa07", "sem_acucar", "Creme de manga, cacau e chia", "Quando voce quer uma fruta cremosa sem adicionar acucar.", "3 min", 3, "Facil", "1 porcao", "Sem adicao de acucar", ["1/2 xic. de manga madura", "2 c.s. de iogurte natural", "1 c.chá de chia", "1/2 c.cha de cacau"], ["Amasse ou processe a manga.", "Misture iogurte, chia e cacau."], "Use pouco cacau para manter o sabor da fruta.", {"quick5", "no_cook", "cold", "fruit", "fruity", "creamy", "yogurt", "seeds", "cocoa"}, "fruta cremosa com um toque de cacau", "cremosa e fresca"),
    R("sa08", "sem_acucar", "Iogurte de cacau com frutas vermelhas", "Uma taca simples para quando voce quer doce, frio e sem preparo.", "2 min", 2, "Facil", "1 porcao", "Sem adicao de acucar", ["1/2 xic. de iogurte natural sem acucar", "1/2 xic. de frutas vermelhas", "1 c.chá de cacau", "1 c.s. de sementes"], ["Misture iogurte e cacau.", "Acrescente as frutas e sementes."], "Confira se o iogurte nao possui acucar adicionado.", {"quick2", "no_cook", "cold", "fruit", "yogurt", "creamy", "after_meal", "cocoa", "crunchy", "seeds"}, "iogurte de cacau com fruta", "fresca e crocante"),
    R("sa09", "sem_acucar", "Panquequinha de banana e aveia", "Quando dez minutos permitem uma receita curta e mais estruturada.", "8 min", 8, "Facil", "2 unidades", "Sem adicao de acucar", ["1 banana pequena", "1 ovo", "2 c.s. de aveia", "canela"], ["Amasse e misture tudo.", "Doure pequenas porcoes em frigideira antiaderente."], "Faça unidades pequenas para virar com facilidade.", {"quick10", "warm", "fruit", "oats", "no_sugar", "breakfast"}, "panquequinhas doces com fruta", "macia e quente"),
    R("sa10", "sem_acucar", "Picole de iogurte e fruta", "Uma opcao que fica pronta no freezer para a vontade gelada.", "2 min para servir - ja preparado", 2, "Facil", "4 unidades", "Sem adicao de acucar", ["1 xic. de iogurte natural sem acucar", "1/2 xic. de fruta madura", "baunilha"], ["Misture ou bata os ingredientes.", "Congele em formas ate firmar."], "A receita exige preparo antecipado; confira o rotulo do iogurte.", {"quick2", "cold", "fruit", "yogurt", "make_ahead", "portable", "no_dishes"}, "um doce gelado ja pronto", "gelada e firme"),

    # Chocolate zero acucar - todas exigem produto rotulado como zero acucar.
    R("cz01", "chocolate_zero", "Morangos com chocolate zero acucar", "Para quando fruta e chocolate sao exatamente a combinacao que voce imaginou.", "2 min", 2, "Facil", "1 porcao", "Chocolate zero acucar", ["5 morangos", "15 g de chocolate zero acucar"], ["Lave e seque os morangos.", "Sirva com o chocolate picado ou ao lado."], "Confirme no rotulo que o chocolate e zero acucar.", {"quick2", "no_cook", "fruit", "fruity", "chocolate", "cold", "minimal"}, "fruta fresca com chocolate zero", "fresca e firme"),
    R("cz02", "chocolate_zero", "Chocolate zero com castanhas ou sementes", "Uma montagem de um minuto para quando voce quer chocolate e crocancia.", "1 min", 1, "Facil", "1 porcao", "Chocolate zero acucar", ["20 g de chocolate zero acucar", "1 pequeno punhado de castanhas ou sementes"], ["Separe os ingredientes em um pote.", "Coma alternando as texturas."], "Confira os rotulos e escolha castanhas ou sementes sem cobertura açucarada.", {"quick2", "no_cook", "no_dishes", "chocolate", "crunchy", "portable", "movie", "coffee", "minimal", "seeds"}, "chocolate zero com crocancia", "crocante"),
    R("cz03", "chocolate_zero", "Banana com chocolate zero acucar", "Quando voce quer chocolate com uma fruta que ja esta na fruteira.", "2 min", 2, "Facil", "1 porcao", "Chocolate zero acucar", ["1/2 banana", "15 g de chocolate zero acucar", "canela, opcional"], ["Fatie a banana.", "Acrescente o chocolate e aqueça por 30 segundos, se quiser."], "Use o chocolate em pedaços pequenos para distribuir o sabor.", {"quick2", "no_cook", "no_dishes", "chocolate", "fruit", "minimal", "warm"}, "banana com chocolate zero", "macia com pedacos"),
    R("cz04", "chocolate_zero", "Bark de iogurte com chocolate zero", "Pequenos pedacos gelados para deixar prontos antes da vontade.", "2 min para servir - ja preparado", 2, "Facil", "4 porcoes", "Chocolate zero acucar", ["1 xic. de iogurte natural", "25 g de chocolate zero acucar", "morangos, opcionais", "1 c.s. de sementes"], ["Espalhe o iogurte em uma forma pequena.", "Cubra, congele e quebre."], "Conserve no freezer e confira os rotulos dos produtos.", {"quick2", "cold", "chocolate", "yogurt", "fruit", "make_ahead", "portable", "movie", "crunchy", "seeds"}, "pedacos gelados de iogurte e chocolate zero", "gelada e crocante"),
    R("cz05", "chocolate_zero", "Chocolate quente zero acucar", "Para quando a vontade pede aroma de cacau e uma bebida quente.", "4 min", 4, "Facil", "1 xicara", "Chocolate zero acucar", ["200 ml de leite", "20 g de chocolate zero acucar", "canela, opcional"], ["Aqueça o leite sem ferver.", "Junte o chocolate e mexa ate derreter."], "O leite contem acucares naturais; o chocolate deve ser rotulado zero acucar.", {"quick5", "warm", "chocolate", "creamy", "night", "coffee", "no_dishes"}, "uma bebida quente de chocolate zero", "quente e cremosa"),
    R("cz06", "chocolate_zero", "Ganache rapida zero acucar", "Um creme mais intenso para quando chocolate de colher faz sentido.", "5 min", 5, "Facil", "2 porcoes", "Chocolate zero acucar", ["40 g de chocolate zero acucar", "3 c.s. de creme de leite"], ["Aqueça o creme de leite.", "Junte o chocolate e mexa ate ficar liso."], "Aqueça em intervalos curtos para nao queimar o chocolate.", {"quick5", "warm", "chocolate", "creamy", "after_meal", "minimal"}, "um creme intenso de chocolate zero", "cremosa e brilhante"),
    R("cz07", "chocolate_zero", "Trufas de coco com chocolate zero", "Para pequenas mordidas de chocolate que podem ficar prontas na geladeira.", "8 min de preparo + geladeira", 8, "Facil", "6 unidades", "Chocolate zero acucar", ["50 g de chocolate zero acucar", "3 c.s. de coco sem acucar", "2 c.s. de creme de leite"], ["Derreta o chocolate com o creme.", "Misture o coco, gele e modele."], "Confirme que coco e chocolate nao possuem acucar adicionado.", {"quick10", "chocolate", "portable", "make_ahead", "coconut", "movie"}, "trufas de chocolate zero e coco", "firme e cremosa"),
    R("cz08", "chocolate_zero", "Uvas geladas com chocolate zero", "Quando voce quer pequenas mordidas frias e sabor de chocolate.", "2 min para servir", 2, "Facil", "1 porcao", "Chocolate zero acucar", ["1/2 xic. de uvas geladas ou congeladas", "15 g de chocolate zero acucar"], ["Coloque as uvas em uma tigela.", "Finalize com o chocolate picado."], "Se as uvas estiverem congeladas, espere um minuto antes de comer.", {"quick2", "no_cook", "cold", "chocolate", "fruit", "portable", "movie", "no_dishes", "crunchy"}, "uvas frias com chocolate zero", "gelada e firme"),
    R("cz09", "chocolate_zero", "Mousse de chocolate zero e iogurte", "Uma opcao fria para quando chocolate cremoso parece a resposta certa.", "5 min", 5, "Facil", "1 porcao", "Chocolate zero acucar", ["1/2 xic. de iogurte natural", "25 g de chocolate zero acucar", "baunilha"], ["Derreta o chocolate e deixe amornar.", "Misture ao iogurte e leve para gelar."], "Junte o chocolate aos poucos para manter o creme uniforme.", {"quick5", "cold", "chocolate", "creamy", "yogurt", "after_meal"}, "mousse fria de chocolate zero", "cremosa e fria"),
    R("cz10", "chocolate_zero", "Chia cremosa com iogurte e raspas zero acucar", "Para deixar pronta e encontrar uma sobremesa gelada quando precisar.", "3 min de preparo + geladeira", 3, "Facil", "1 porcao", "Chocolate zero acucar", ["1 pote de iogurte natural", "2 c.s. de chia", "20 g de chocolate zero acucar", "baunilha"], ["Misture iogurte, chia e baunilha.", "Gele ate firmar e finalize com o chocolate."], "Mexa novamente depois de 10 minutos para evitar grumos.", {"cold", "chocolate", "creamy", "yogurt", "seeds", "make_ahead"}, "um pote gelado com chocolate zero", "cremosa com pedacos"),

    # Opcoes proteicas - a quantidade real depende do rotulo e da porcao usada.
    R("pt01", "proteicas", "Mousse proteica de cacau", "Para quando voce quer chocolate cremoso e uma base com fonte de proteina.", "5 min", 5, "Facil", "1 porcao", "Proteica", ["170 g de iogurte de maior teor proteico", "20 g de proteina em po sabor chocolate", "1 c.chá de cacau", "adocante, opcional"], ["Misture iogurte, proteina e cacau.", "Mexa ate formar um creme uniforme."], "O teor de proteina depende do rotulo dos produtos utilizados.", {"quick5", "no_cook", "cold", "creamy", "cocoa", "yogurt", "protein", "after_meal"}, "chocolate cremoso com fonte proteica", "cremosa e fria"),
    R("pt02", "proteicas", "Taca proteica de morango e nibs", "Uma taca fresca para quando fruta e cremosidade combinam com o momento.", "3 min", 3, "Facil", "1 porcao", "Proteica", ["1 pote de iogurte de maior teor proteico", "5 morangos", "1 c.s. de sementes ou castanhas", "1 c.cha de nibs de cacau"], ["Fatie os morangos.", "Monte com iogurte, sementes e nibs."], "Confirme no rotulo o teor de proteina do iogurte.", {"quick5", "no_cook", "cold", "fruit", "yogurt", "protein", "seeds", "after_meal", "crunchy", "cocoa"}, "fruta fresca com proteina e cacau", "fresca e crocante"),
    R("pt03", "proteicas", "Creme proteico de chocolate", "Quando voce quer um creme de colher com poucos ingredientes.", "3 min", 3, "Facil", "1 porcao", "Proteica", ["2 c.s. de leite em po", "20 g de proteina em po", "1 c.chá de cacau", "agua morna aos poucos"], ["Misture os ingredientes secos.", "Acrescente agua morna ate chegar ao ponto de creme."], "Adicione a agua em gotas para nao perder o ponto.", {"quick5", "no_cook", "no_dishes", "creamy", "cocoa", "protein", "minimal", "warm"}, "um creme morno de chocolate com fonte proteica", "densa e morna"),
    R("pt04", "proteicas", "Iogurte proteico com cacau e castanhas", "Para quando a base ja esta na geladeira e voce quer resolver em dois minutos.", "2 min", 2, "Facil", "1 porcao", "Proteica", ["1 pote de iogurte de maior teor proteico", "1 c.cha de cacau", "1 c.s. de castanhas picadas", "canela"], ["Misture iogurte, cacau e canela.", "Finalize com castanhas."], "Escolha o iogurte observando proteina e acucares no rotulo.", {"quick2", "no_cook", "no_dishes", "cold", "yogurt", "protein", "seeds", "minimal", "crunchy", "cocoa"}, "iogurte proteico com cacau e crocancia", "cremosa e crocante"),
    R("pt05", "proteicas", "Overnight proteico de cacau", "Bom para preparar antes e encontrar uma opcao pronta no dia corrido.", "3 min de preparo + geladeira", 3, "Facil", "1 porcao", "Proteica", ["3 c.s. de aveia", "1 pote de iogurte de maior teor proteico", "1 c.chá de cacau", "2 c.s. de leite", "1 c.s. de sementes"], ["Misture tudo, menos as sementes.", "Gele e finalize com sementes ao servir."], "A textura fica mais macia de um dia para o outro.", {"cold", "oats", "cocoa", "yogurt", "protein", "make_ahead", "work", "crunchy", "seeds"}, "um pote de cacau pronto para o dia", "cremosa e crocante"),
    R("pt06", "proteicas", "Panqueca proteica de banana e cacau", "Quando voce tem alguns minutos e quer uma receita quente de verdade.", "8 min", 8, "Facil", "2 unidades", "Proteica", ["1 ovo", "1 banana pequena", "20 g de proteina em po", "1 c.cha de cacau", "canela"], ["Amasse e misture tudo.", "Doure porcoes pequenas em frigideira antiaderente."], "A proteina varia conforme o produto e o tamanho do ovo.", {"quick10", "warm", "fruit", "protein", "breakfast", "cocoa"}, "panquequinhas quentes de banana e cacau", "macia e quente"),
    R("pt07", "proteicas", "Bolo de caneca proteico", "Para quando dez minutos comportam algo quente, macio e feito na caneca.", "6 min", 6, "Facil", "1 porcao", "Proteica", ["1 ovo", "20 g de proteina em po", "1 c.s. de aveia", "1 c.chá de cacau", "1 c.chá de fermento"], ["Misture na propria caneca.", "Aqueça por 60 a 90 segundos e verifique o ponto."], "Use caneca grande e pare o micro-ondas assim que firmar.", {"quick10", "warm", "cocoa", "oats", "protein", "no_dishes"}, "um bolo quente com fonte proteica", "macia e quente"),
    R("pt08", "proteicas", "Picole proteico de iogurte e cacau", "Uma opcao gelada que pode ficar pronta para a vontade da noite.", "2 min para servir - ja preparado", 2, "Facil", "4 unidades", "Proteica", ["2 potes de iogurte de maior teor proteico", "1/2 xic. de fruta", "1 c.cha de cacau", "baunilha"], ["Misture os ingredientes.", "Congele em formas ate firmar."], "A receita exige preparo antecipado e depende do rotulo do iogurte.", {"quick2", "cold", "fruit", "yogurt", "protein", "make_ahead", "portable", "no_dishes", "cocoa"}, "um doce gelado de fruta e cacau com base proteica", "gelada e firme"),
    R("pt09", "proteicas", "Cottage doce com cacau", "Quando voce quer um creme rapido e tem cottage na geladeira.", "2 min", 2, "Facil", "1 porcao", "Proteica", ["1/2 xic. de cottage", "1 c.chá de cacau", "baunilha", "adocante, opcional"], ["Misture ou processe o cottage.", "Junte cacau, baunilha e adocante."], "Processar deixa a textura mais lisa; a proteina depende do rotulo.", {"quick2", "no_cook", "cold", "creamy", "cocoa", "protein", "minimal", "yogurt"}, "um creme rapido de cacau e cottage", "cremosa e fresca"),
    R("pt10", "proteicas", "Cafe proteico cremoso com cacau", "Uma bebida doce para a pausa do cafe sem precisar montar sobremesa.", "2 min", 2, "Facil", "1 copo", "Proteica", ["1/2 xic. de cafe frio ou morno", "100 ml de leite", "15 g de proteina em po", "1/2 c.cha de cacau", "gelo, opcional"], ["Misture leite, proteina e cacau.", "Junte o cafe e sirva morno ou com gelo."], "Nao misture a proteina diretamente em liquido muito quente.", {"quick2", "no_cook", "no_dishes", "cold", "warm", "coffee", "protein", "work", "portable", "cocoa"}, "cafe com cacau e fonte proteica", "cremosa"),

    # Receitas saudaveis - categoria ampla, sem promessa clinica.
    R("rs01", "saudaveis", "Taca de frutas, iogurte e sementes", "Uma montagem colorida para quando voce quer variedade sem receita longa.", "3 min", 3, "Facil", "1 porcao", "Ingredientes variados", ["1/2 xic. de frutas", "1/2 xic. de iogurte natural", "1 c.s. de sementes"], ["Corte as frutas.", "Monte com iogurte e sementes."], "Use as frutas que ja estao maduras e disponiveis.", {"quick5", "no_cook", "cold", "fruit", "fruity", "yogurt", "seeds"}, "fruta, creme e sementes em uma taca", "fresca e cremosa"),
    R("rs02", "saudaveis", "Crumble de maca, aveia e nibs", "Quando voce quer aroma de sobremesa quente com uma cobertura crocante.", "8 min", 8, "Facil", "1 porcao", "Fruta com aveia", ["1 maca", "2 c.s. de aveia", "1 c.chá de pasta de amendoim", "1 c.cha de nibs de cacau", "canela"], ["Pique a maca e aqueça por 2 minutos.", "Cubra com os demais ingredientes e aqueça mais 1 minuto."], "Coloque parte dos nibs depois de aquecer para preservar a crocancia.", {"quick10", "warm", "fruit", "oats", "crunchy", "no_dishes", "cocoa"}, "maca quente com aveia e cacau", "macia e crocante"),
    R("rs03", "saudaveis", "Banana gelada com tahine e cacau", "Uma montagem de dois minutos para quando a banana ja esta madura.", "2 min", 2, "Facil", "1 porcao", "Fruta com pasta de sementes", ["1 banana pequena gelada", "1 c.chá de tahine", "1/2 c.chá de cacau", "canela"], ["Fatie a banana.", "Finalize com tahine, cacau e canela."], "Se o tahine estiver muito firme, mexa antes de usar.", {"quick2", "no_cook", "no_dishes", "fruit", "seeds", "minimal", "creamy", "cocoa", "cold"}, "banana gelada com creme de gergelim e cacau", "macia e cremosa"),
    R("rs04", "saudaveis", "Morangos com ricota e nibs", "Para quando fruta fresca, creme e cacau parecem suficientes.", "2 min", 2, "Facil", "1 porcao", "Fruta com laticinio", ["5 morangos", "3 c.s. de ricota amassada", "1 c.cha de nibs de cacau", "baunilha"], ["Amasse a ricota com a baunilha.", "Sirva com morangos e nibs."], "Use ricota fresca e mantenha refrigerada.", {"quick2", "no_cook", "cold", "fruit", "fruity", "yogurt", "minimal", "cocoa", "crunchy"}, "fruta fresca com creme e cacau", "fresca e crocante"),
    R("rs05", "saudaveis", "Pudim de chia com fruta", "Uma opcao para preparar antes e encontrar pronta na geladeira.", "3 min de preparo + geladeira", 3, "Facil", "1 porcao", "Sementes e fruta", ["150 ml de leite", "2 c.s. de chia", "1/2 xic. de fruta", "baunilha"], ["Misture leite, chia e baunilha.", "Gele ate firmar e finalize com fruta."], "Mexa depois de 10 minutos para distribuir as sementes.", {"cold", "fruit", "seeds", "make_ahead", "creamy"}, "um pote gelado com fruta", "cremosa e fresca"),
    R("rs06", "saudaveis", "Mingau de aveia e cacau", "Quando a vontade pede algo quente, cremoso e com gosto de chocolate.", "8 min", 8, "Facil", "1 porcao", "Aveia com cacau", ["3 c.s. de aveia", "200 ml de leite", "1 c.chá de cacau", "1/2 banana, opcional"], ["Misture aveia, leite e cacau.", "Cozinhe mexendo ate engrossar."], "A banana madura pode adoçar e deixar o mingau mais cremoso.", {"quick10", "warm", "cocoa", "oats", "creamy", "fruit"}, "um creme quente de aveia e cacau", "quente e cremosa"),
    R("rs07", "saudaveis", "Pera com iogurte e castanhas", "Uma taca rapida que junta fruta macia, creme e crocancia.", "3 min", 3, "Facil", "1 porcao", "Fruta com laticinio e castanhas", ["1 pera", "1/2 xic. de iogurte natural", "1 c.s. de castanhas", "canela"], ["Corte a pera.", "Monte com iogurte, castanhas e canela."], "Coloque as castanhas apenas na hora de comer.", {"quick5", "no_cook", "fruit", "fruity", "yogurt", "crunchy", "seeds"}, "fruta com creme e crocancia", "cremosa e crocante"),
    R("rs08", "saudaveis", "Salada de frutas com nibs de cacau", "Pequenas mordidas para quando voce quer fruta com um toque crocante de cacau.", "4 min", 4, "Facil", "1 porcao", "Frutas variadas", ["1 xic. de frutas picadas", "1 c.s. de nibs de cacau", "canela ou hortela"], ["Misture as frutas.", "Finalize com nibs e o aroma escolhido."], "Acrescente os nibs no final para preservar a textura.", {"quick5", "no_cook", "cold", "fruit", "fruity", "cocoa", "crunchy", "movie"}, "frutas frescas com crocancia de cacau", "fresca e crocante"),
    R("rs09", "saudaveis", "Panquequinha de banana e aveia", "Uma receita curta para quando voce quer algo quente e feito na hora.", "8 min", 8, "Facil", "2 unidades", "Fruta com aveia", ["1 banana pequena", "1 ovo", "2 c.s. de aveia", "canela"], ["Amasse e misture tudo.", "Doure porcoes pequenas em frigideira antiaderente."], "Faça unidades pequenas para cozinhar por igual.", {"quick10", "warm", "fruit", "oats", "breakfast"}, "panquequinhas quentes de banana", "macia e quente"),
    R("rs10", "saudaveis", "Iogurte gelado com banana, cacau e amendoim", "Quando voce quer algo doce, cremoso e montado no proprio pote.", "2 min", 2, "Facil", "1 porcao", "Fruta com laticinio", ["1 pote de iogurte natural gelado", "1/2 banana", "1 c.chá de pasta de amendoim", "1/2 c.cha de cacau"], ["Fatie a banana sobre o iogurte.", "Finalize com pasta e cacau."], "Confira se a pasta nao possui acucar adicionado, se isso for importante para voce.", {"quick2", "no_cook", "no_dishes", "fruit", "yogurt", "creamy", "work", "minimal", "cocoa", "cold"}, "banana e iogurte gelado com cacau", "cremosa e fria"),
)


RECIPE_BY_ID = {recipe.id: recipe for recipe in RECIPES}
RECIPES_BY_CATEGORY = {
    category.id: tuple(recipe for recipe in RECIPES if recipe.category == category.id)
    for category in CATEGORIES
}


V2_SELECTIONS: dict[tuple[int, str], tuple[str, str, str]] = {
    (1, "low_carb"): ("lc05", "lc10", "lc07"),
    (1, "brigadeiro_fit"): ("bf01", "bf05", "bf08"),
    (1, "sem_acucar"): ("sa02", "sa08", "sa07"),
    (1, "chocolate_zero"): ("cz09", "cz06", "cz05"),
    (1, "proteicas"): ("pt02", "pt01", "pt03"),
    (1, "saudaveis"): ("rs01", "rs08", "rs07"),
    (2, "low_carb"): ("lc05", "lc10", "lc07"),
    (2, "brigadeiro_fit"): ("bf01", "bf07", "bf08"),
    (2, "sem_acucar"): ("sa02", "sa08", "sa03"),
    (2, "chocolate_zero"): ("cz06", "cz09", "cz05"),
    (2, "proteicas"): ("pt01", "pt02", "pt03"),
    (2, "saudaveis"): ("rs01", "rs08", "rs07"),
    (3, "low_carb"): ("lc03", "lc02", "lc01"),
    (3, "brigadeiro_fit"): ("bf04", "bf03", "bf02"),
    (3, "sem_acucar"): ("sa08", "sa01", "sa06"),
    (3, "chocolate_zero"): ("cz08", "cz04", "cz03"),
    (3, "proteicas"): ("pt10", "pt09", "pt08"),
    (3, "saudaveis"): ("rs04", "rs03", "rs10"),
    (4, "low_carb"): ("lc05", "lc10", "lc02"),
    (4, "brigadeiro_fit"): ("bf01", "bf08", "bf10"),
    (4, "sem_acucar"): ("sa07", "sa02", "sa05"),
    (4, "chocolate_zero"): ("cz09", "cz06", "cz01"),
    (4, "proteicas"): ("pt02", "pt01", "pt05"),
    (4, "saudaveis"): ("rs08", "rs01", "rs04"),
    (5, "low_carb"): ("lc05", "lc07", "lc10"),
    (5, "brigadeiro_fit"): ("bf01", "bf07", "bf08"),
    (5, "sem_acucar"): ("sa08", "sa07", "sa01"),
    (5, "chocolate_zero"): ("cz09", "cz06", "cz05"),
    (5, "proteicas"): ("pt01", "pt03", "pt09"),
    (5, "saudaveis"): ("rs05", "rs10", "rs03"),
    (6, "low_carb"): ("lc09", "lc08", "lc01"),
    (6, "brigadeiro_fit"): ("bf04", "bf03", "bf02"),
    (6, "sem_acucar"): ("sa08", "sa06", "sa01"),
    (6, "chocolate_zero"): ("cz02", "cz03", "cz08"),
    (6, "proteicas"): ("pt04", "pt10", "pt08"),
    (6, "saudaveis"): ("rs03", "rs10", "rs04"),
    (7, "low_carb"): ("lc09", "lc07", "lc10"),
    (7, "brigadeiro_fit"): ("bf05", "bf10", "bf07"),
    (7, "sem_acucar"): ("sa10", "sa03", "sa06"),
    (7, "chocolate_zero"): ("cz04", "cz02", "cz08"),
    (7, "proteicas"): ("pt10", "pt08", "pt02"),
    (7, "saudaveis"): ("rs07", "rs01", "rs08"),
    (8, "low_carb"): ("lc09", "lc03", "lc08"),
    (8, "brigadeiro_fit"): ("bf04", "bf03", "bf02"),
    (8, "sem_acucar"): ("sa10", "sa06", "sa01"),
    (8, "chocolate_zero"): ("cz02", "cz08", "cz04"),
    (8, "proteicas"): ("pt10", "pt08", "pt04"),
    (8, "saudaveis"): ("rs10", "rs03", "rs04"),
    (9, "low_carb"): ("lc03", "lc01", "lc09"),
    (9, "brigadeiro_fit"): ("bf05", "bf03", "bf07"),
    (9, "sem_acucar"): ("sa03", "sa07", "sa02"),
    (9, "chocolate_zero"): ("cz05", "cz02", "cz09"),
    (9, "proteicas"): ("pt03", "pt02", "pt10"),
    (9, "saudaveis"): ("rs07", "rs01", "rs08"),
    (10, "low_carb"): ("lc08", "lc02", "lc09"),
    (10, "brigadeiro_fit"): ("bf05", "bf03", "bf09"),
    (10, "sem_acucar"): ("sa05", "sa06", "sa08"),
    (10, "chocolate_zero"): ("cz04", "cz02", "cz08"),
    (10, "proteicas"): ("pt02", "pt05", "pt04"),
    (10, "saudaveis"): ("rs07", "rs08", "rs04"),
    (11, "low_carb"): ("lc03", "lc02", "lc01"),
    (11, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (11, "sem_acucar"): ("sa10", "sa05", "sa01"),
    (11, "chocolate_zero"): ("cz01", "cz03", "cz04"),
    (11, "proteicas"): ("pt09", "pt04", "pt08"),
    (11, "saudaveis"): ("rs03", "rs10", "rs04"),
    (12, "low_carb"): ("lc05", "lc04", "lc10"),
    (12, "brigadeiro_fit"): ("bf08", "bf01", "bf05"),
    (12, "sem_acucar"): ("sa07", "sa03", "sa05"),
    (12, "chocolate_zero"): ("cz05", "cz01", "cz03"),
    (12, "proteicas"): ("pt03", "pt01", "pt02"),
    (12, "saudaveis"): ("rs01", "rs07", "rs08"),
    (13, "low_carb"): ("lc06", "lc09", "lc08"),
    (13, "brigadeiro_fit"): ("bf09", "bf06", "bf10"),
    (13, "sem_acucar"): ("sa06", "sa10", "sa05"),
    (13, "chocolate_zero"): ("cz08", "cz04", "cz07"),
    (13, "proteicas"): ("pt05", "pt04", "pt10"),
    (13, "saudaveis"): ("rs02", "rs08", "rs04"),
    (14, "low_carb"): ("lc07", "lc03", "lc01"),
    (14, "brigadeiro_fit"): ("bf06", "bf02", "bf07"),
    (14, "sem_acucar"): ("sa04", "sa09", "sa03"),
    (14, "chocolate_zero"): ("cz05", "cz03", "cz06"),
    (14, "proteicas"): ("pt07", "pt06", "pt03"),
    (14, "saudaveis"): ("rs09", "rs06", "rs02"),
    (15, "low_carb"): ("lc05", "lc10", "lc04"),
    (15, "brigadeiro_fit"): ("bf01", "bf08", "bf10"),
    (15, "sem_acucar"): ("sa07", "sa10", "sa05"),
    (15, "chocolate_zero"): ("cz10", "cz09", "cz01"),
    (15, "proteicas"): ("pt01", "pt09", "pt02"),
    (15, "saudaveis"): ("rs01", "rs05", "rs08"),
    (16, "low_carb"): ("lc07", "lc05", "lc10"),
    (16, "brigadeiro_fit"): ("bf07", "bf08", "bf05"),
    (16, "sem_acucar"): ("sa07", "sa08", "sa01"),
    (16, "chocolate_zero"): ("cz05", "cz06", "cz10"),
    (16, "proteicas"): ("pt01", "pt03", "pt02"),
    (16, "saudaveis"): ("rs08", "rs03", "rs10"),
    (17, "low_carb"): ("lc07", "lc05", "lc10"),
    (17, "brigadeiro_fit"): ("bf01", "bf07", "bf05"),
    (17, "sem_acucar"): ("sa07", "sa05", "sa01"),
    (17, "chocolate_zero"): ("cz09", "cz06", "cz05"),
    (17, "proteicas"): ("pt03", "pt01", "pt05"),
    (17, "saudaveis"): ("rs08", "rs03", "rs10"),
    (18, "low_carb"): ("lc07", "lc05", "lc08"),
    (18, "brigadeiro_fit"): ("bf01", "bf08", "bf07"),
    (18, "sem_acucar"): ("sa07", "sa01", "sa08"),
    (18, "chocolate_zero"): ("cz10", "cz09", "cz06"),
    (18, "proteicas"): ("pt03", "pt01", "pt09"),
    (18, "saudaveis"): ("rs10", "rs06", "rs03"),
    (19, "low_carb"): ("lc02", "lc08", "lc09"),
    (19, "brigadeiro_fit"): ("bf05", "bf03", "bf09"),
    (19, "sem_acucar"): ("sa06", "sa05", "sa08"),
    (19, "chocolate_zero"): ("cz02", "cz04", "cz08"),
    (19, "proteicas"): ("pt05", "pt02", "pt04"),
    (19, "saudaveis"): ("rs08", "rs02", "rs04"),
    (20, "low_carb"): ("lc10", "lc03", "lc02"),
    (20, "brigadeiro_fit"): ("bf01", "bf08", "bf10"),
    (20, "sem_acucar"): ("sa07", "sa06", "sa05"),
    (20, "chocolate_zero"): ("cz10", "cz09", "cz01"),
    (20, "proteicas"): ("pt01", "pt09", "pt08"),
    (20, "saudaveis"): ("rs04", "rs08", "rs03"),
    (21, "low_carb"): ("lc01", "lc03", "lc02"),
    (21, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (21, "sem_acucar"): ("sa01", "sa06", "sa08"),
    (21, "chocolate_zero"): ("cz03", "cz02", "cz08"),
    (21, "proteicas"): ("pt10", "pt04", "pt09"),
    (21, "saudaveis"): ("rs10", "rs03", "rs04"),
    (22, "low_carb"): ("lc10", "lc02", "lc05"),
    (22, "brigadeiro_fit"): ("bf07", "bf08", "bf10"),
    (22, "sem_acucar"): ("sa07", "sa05", "sa06"),
    (22, "chocolate_zero"): ("cz01", "cz03", "cz04"),
    (22, "proteicas"): ("pt02", "pt08", "pt06"),
    (22, "saudaveis"): ("rs08", "rs04", "rs06"),
    (23, "low_carb"): ("lc08", "lc09", "lc01"),
    (23, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (23, "sem_acucar"): ("sa01", "sa06", "sa10"),
    (23, "chocolate_zero"): ("cz03", "cz02", "cz08"),
    (23, "proteicas"): ("pt04", "pt10", "pt09"),
    (23, "saudaveis"): ("rs10", "rs03", "rs04"),
    (24, "low_carb"): ("lc04", "lc07", "lc05"),
    (24, "brigadeiro_fit"): ("bf05", "bf01", "bf07"),
    (24, "sem_acucar"): ("sa02", "sa03", "sa10"),
    (24, "chocolate_zero"): ("cz05", "cz06", "cz10"),
    (24, "proteicas"): ("pt03", "pt05", "pt01"),
    (24, "saudaveis"): ("rs07", "rs01", "rs05"),
    (25, "low_carb"): ("lc06", "lc03", "lc01"),
    (25, "brigadeiro_fit"): ("bf06", "bf09", "bf02"),
    (25, "sem_acucar"): ("sa09", "sa04", "sa02"),
    (25, "chocolate_zero"): ("cz07", "cz03", "cz06"),
    (25, "proteicas"): ("pt07", "pt06", "pt10"),
    (25, "saudaveis"): ("rs09", "rs06", "rs02"),
    (26, "low_carb"): ("lc08", "lc03", "lc02"),
    (26, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (26, "sem_acucar"): ("sa01", "sa06", "sa10"),
    (26, "chocolate_zero"): ("cz02", "cz08", "cz03"),
    (26, "proteicas"): ("pt04", "pt10", "pt08"),
    (26, "saudaveis"): ("rs10", "rs03", "rs02"),
    (27, "low_carb"): ("lc08", "lc03", "lc02"),
    (27, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (27, "sem_acucar"): ("sa05", "sa08", "sa06"),
    (27, "chocolate_zero"): ("cz01", "cz08", "cz04"),
    (27, "proteicas"): ("pt09", "pt04", "pt10"),
    (27, "saudaveis"): ("rs10", "rs04", "rs03"),
    (28, "low_carb"): ("lc04", "lc07", "lc10"),
    (28, "brigadeiro_fit"): ("bf01", "bf08", "bf07"),
    (28, "sem_acucar"): ("sa07", "sa04", "sa08"),
    (28, "chocolate_zero"): ("cz09", "cz10", "cz05"),
    (28, "proteicas"): ("pt03", "pt01", "pt09"),
    (28, "saudaveis"): ("rs05", "rs06", "rs10"),
    (29, "low_carb"): ("lc09", "lc06", "lc08"),
    (29, "brigadeiro_fit"): ("bf05", "bf09", "bf03"),
    (29, "sem_acucar"): ("sa05", "sa08", "sa06"),
    (29, "chocolate_zero"): ("cz04", "cz02", "cz08"),
    (29, "proteicas"): ("pt05", "pt02", "pt04"),
    (29, "saudaveis"): ("rs07", "rs08", "rs02"),
    (30, "low_carb"): ("lc04", "lc05", "lc10"),
    (30, "brigadeiro_fit"): ("bf08", "bf10", "bf01"),
    (30, "sem_acucar"): ("sa07", "sa10", "sa05"),
    (30, "chocolate_zero"): ("cz09", "cz10", "cz01"),
    (30, "proteicas"): ("pt02", "pt01", "pt05"),
    (30, "saudaveis"): ("rs01", "rs05", "rs08"),
    (31, "low_carb"): ("lc01", "lc07", "lc03"),
    (31, "brigadeiro_fit"): ("bf06", "bf02", "bf07"),
    (31, "sem_acucar"): ("sa09", "sa04", "sa03"),
    (31, "chocolate_zero"): ("cz06", "cz05", "cz03"),
    (31, "proteicas"): ("pt07", "pt06", "pt03"),
    (31, "saudaveis"): ("rs09", "rs06", "rs02"),
    (32, "low_carb"): ("lc10", "lc02", "lc05"),
    (32, "brigadeiro_fit"): ("bf10", "bf08", "bf07"),
    (32, "sem_acucar"): ("sa03", "sa02", "sa07"),
    (32, "chocolate_zero"): ("cz01", "cz03", "cz04"),
    (32, "proteicas"): ("pt02", "pt08", "pt06"),
    (32, "saudaveis"): ("rs07", "rs01", "rs05"),
    (33, "low_carb"): ("lc10", "lc02", "lc05"),
    (33, "brigadeiro_fit"): ("bf10", "bf08", "bf07"),
    (33, "sem_acucar"): ("sa03", "sa02", "sa07"),
    (33, "chocolate_zero"): ("cz01", "cz04", "cz03"),
    (33, "proteicas"): ("pt08", "pt02", "pt06"),
    (33, "saudaveis"): ("rs07", "rs01", "rs05"),
    (34, "low_carb"): ("lc05", "lc08", "lc02"),
    (34, "brigadeiro_fit"): ("bf01", "bf10", "bf05"),
    (34, "sem_acucar"): ("sa07", "sa08", "sa10"),
    (34, "chocolate_zero"): ("cz09", "cz10", "cz04"),
    (34, "proteicas"): ("pt01", "pt09", "pt05"),
    (34, "saudaveis"): ("rs05", "rs01", "rs10"),
    (35, "low_carb"): ("lc06", "lc09", "lc04"),
    (35, "brigadeiro_fit"): ("bf09", "bf05", "bf03"),
    (35, "sem_acucar"): ("sa09", "sa04", "sa08"),
    (35, "chocolate_zero"): ("cz02", "cz04", "cz10"),
    (35, "proteicas"): ("pt07", "pt05", "pt04"),
    (35, "saudaveis"): ("rs02", "rs09", "rs06"),
    (36, "low_carb"): ("lc07", "lc01", "lc06"),
    (36, "brigadeiro_fit"): ("bf05", "bf01", "bf04"),
    (36, "sem_acucar"): ("sa07", "sa01", "sa05"),
    (36, "chocolate_zero"): ("cz06", "cz05", "cz09"),
    (36, "proteicas"): ("pt03", "pt01", "pt05"),
    (36, "saudaveis"): ("rs08", "rs06", "rs04"),
    (37, "low_carb"): ("lc07", "lc01", "lc09"),
    (37, "brigadeiro_fit"): ("bf04", "bf02", "bf03"),
    (37, "sem_acucar"): ("sa02", "sa03", "sa01"),
    (37, "chocolate_zero"): ("cz02", "cz06", "cz03"),
    (37, "proteicas"): ("pt03", "pt04", "pt09"),
    (37, "saudaveis"): ("rs03", "rs10", "rs04"),
}



PT_BR_PHRASES = {
    "As vezes": "Às vezes",
    "esta acontecendo": "está acontecendo",
    "esta pronto": "está pronto",
    "esta pronta": "está pronta",
    "voce esta trabalhando": "você está trabalhando",
    "o sabor esta claro": "O sabor está claro",
    "a textura esta definida": "A textura está definida",
    "ainda esta disponivel": "ainda está disponível",
    "ja esta": "já está",
    "ja estao": "já estão",
    "nao e": "não é",
    "sobremesa; e de chocolate": "sobremesa; é de chocolate",
    "tempo e curto": "tempo é curto",
    "vontade e especifica": "vontade é específica",
    "chocolate e exatamente": "chocolate é exatamente",
    "iogurte e a base": "iogurte é a base",
    "louca e a barreira": "louça é a barreira",
    "melhor receita e a": "melhor receita é a",
    "temperatura e o primeiro": "temperatura é o primeiro",
    "fruta e parte": "fruta é parte",
    "pergunta util e": "pergunta útil é",
    "E chocolate mesmo": "É chocolate mesmo",
}


PT_BR_WORDS = {
    "acucar": "açúcar",
    "acucares": "açúcares",
    "adicao": "adição",
    "adocante": "adoçante",
    "adocantes": "adoçantes",
    "alergenicos": "alergênicos",
    "alimentacao": "alimentação",
    "agua": "água",
    "alem": "além",
    "armarios": "armários",
    "aromatica": "aromática",
    "apos": "após",
    "ate": "até",
    "atencao": "atenção",
    "cafe": "café",
    "cha": "chá",
    "classificacao": "classificação",
    "classificacoes": "classificações",
    "composicao": "composição",
    "condicao": "condição",
    "condicoes": "condições",
    "conservacao": "conservação",
    "crocancia": "crocância",
    "diagnostico": "diagnóstico",
    "dificil": "difícil",
    "direcao": "direção",
    "especifica": "específica",
    "especifico": "específico",
    "facil": "fácil",
    "gestacao": "gestação",
    "grao": "grão",
    "hortela": "hortelã",
    "informacao": "informação",
    "informacoes": "informações",
    "inicio": "início",
    "instrucao": "instrução",
    "instrucoes": "instruções",
    "laticinio": "laticínio",
    "laticinios": "laticínios",
    "limao": "limão",
    "maca": "maçã",
    "media": "média",
    "maximo": "máximo",
    "minimo": "mínimo",
    "ministerio": "ministério",
    "nao": "não",
    "nutricional": "nutricional",
    "opcao": "opção",
    "opcoes": "opções",
    "orientacao": "orientação",
    "orientacoes": "orientações",
    "pao": "pão",
    "picoles": "picolés",
    "po": "pó",
    "populacao": "população",
    "porcao": "porção",
    "porcoes": "porções",
    "pratica": "prática",
    "pratico": "prático",
    "principio": "princípio",
    "principios": "princípios",
    "prescricao": "prescrição",
    "proxima": "próxima",
    "propria": "própria",
    "proprio": "próprio",
    "proteica": "proteica",
    "proteicas": "proteicas",
    "proteico": "proteico",
    "proteicos": "proteicos",
    "proteina": "proteína",
    "proteinas": "proteínas",
    "rapida": "rápida",
    "rapido": "rápido",
    "referencias": "referências",
    "refeicao": "refeição",
    "refeicoes": "refeições",
    "rotulo": "rótulo",
    "rotulos": "rótulos",
    "saude": "saúde",
    "servicos": "serviços",
    "serie": "série",
    "situacao": "situação",
    "situacoes": "situações",
    "so": "só",
    "tambem": "também",
    "taca": "taça",
    "transparencia": "transparência",
    "tres": "três",
    "voce": "você",
    "xicara": "xícara",
    "abobora": "abóbora",
    "combinacao": "combinação",
    "combinacoes": "combinações",
    "comecar": "começar",
    "contem": "contém",
    "decisao": "decisão",
    "disponivel": "disponível",
    "disponiveis": "disponíveis",
    "estao": "estão",
    "faca": "faça",
    "ha": "há",
    "ja": "já",
    "liquido": "líquido",
    "liquidos": "líquidos",
    "louca": "louça",
    "necessaria": "necessária",
    "necessario": "necessário",
    "pedaco": "pedaço",
    "pedacos": "pedaços",
    "pereciveis": "perecíveis",
    "picole": "picolé",
    "preparacao": "preparação",
    "sensacao": "sensação",
    "umida": "úmida",
    "util": "útil",
    "variacao": "variação",
    "variacoes": "variações",
    "versao": "versão",
    "almoco": "almoço",
    "basica": "básica",
    "basico": "básico",
    "clinica": "clínica",
    "clinico": "clínico",
    "compativel": "compatível",
    "mamao": "mamão",
    "portatil": "portátil",
    "portateis": "portáteis",
    "sao": "são",
    "sera": "será",
    "xic": "xíc",
    "antecedencia": "antecedência",
    "comeco": "começo",
    "culinaria": "culinária",
    "culinario": "culinário",
    "faceis": "fáceis",
    "fogao": "fogão",
    "intolerancias": "intolerâncias",
    "laminas": "lâminas",
    "obrigatoria": "obrigatória",
    "obrigatorio": "obrigatório",
    "praticas": "práticas",
    "referencia": "referência",
    "referencias": "referências",
    "sofa": "sofá",
}


def pt_text(text: str) -> str:
    def replace(match: re.Match[str], replacement: str) -> str:
        source = match.group(0)
        if source.isupper():
            return replacement.upper()
        if source[:1].isupper():
            return replacement[:1].upper() + replacement[1:]
        return replacement

    result = text
    for source, replacement in PT_BR_PHRASES.items():
        result = re.sub(re.escape(source), replacement, result, flags=re.IGNORECASE)
    for source, replacement in PT_BR_WORDS.items():
        result = re.sub(rf"\b{re.escape(source)}\b", lambda match, value=replacement: replace(match, value), result, flags=re.IGNORECASE)
    return result


def wrap_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    text = pt_text(text)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        proposal = word if not current else f"{current} {word}"
        if pdfmetrics.stringWidth(proposal, font, size) <= max_width:
            current = proposal
        else:
            if current:
                lines.append(current)
            if pdfmetrics.stringWidth(word, font, size) > max_width:
                raise ValueError(f"Palavra excede largura disponivel: {word}")
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def draw_wrapped(
    c: canvas.Canvas,
    text: str,
    x: float,
    y_top: float,
    max_width: float,
    font: str = "QBDSans",
    size: float = 10,
    leading: float | None = None,
    color: colors.Color = INK,
    max_lines: int | None = None,
) -> float:
    lines = wrap_text(text, font, size, max_width)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"Texto excedeu {max_lines} linhas: {text}")
    line_height = leading or size * 1.28
    c.setFillColor(color)
    c.setFont(font, size)
    y = y_top
    for line in lines:
        c.drawString(x, y - size, line)
        y -= line_height
    return y


def draw_centered_wrapped(
    c: canvas.Canvas,
    text: str,
    center_x: float,
    y_top: float,
    max_width: float,
    font: str,
    size: float,
    leading: float | None = None,
    color: colors.Color = INK,
    max_lines: int | None = None,
) -> float:
    lines = wrap_text(text, font, size, max_width)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f"Texto excedeu {max_lines} linhas: {text}")
    line_height = leading or size * 1.25
    c.setFillColor(color)
    c.setFont(font, size)
    y = y_top
    for line in lines:
        c.drawCentredString(center_x, y - size, line)
        y -= line_height
    return y


def draw_image_contain(c: canvas.Canvas, path: Path, x: float, y: float, w: float, h: float) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        iw, ih = image.size
    scale = min(w / iw, h / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (w - dw) / 2, y + (h - dh) / 2, dw, dh, mask="auto")


def recipe_ingredients_text(recipe: Recipe) -> str:
    return " ".join(recipe.ingredients).lower()


def uses_any(recipe: Recipe, terms: tuple[str, ...]) -> bool:
    ingredients = recipe_ingredients_text(recipe)
    return any(re.search(rf"\b{re.escape(term)}", ingredients) for term in terms)


def is_make_ahead(recipe: Recipe) -> bool:
    return "make_ahead" in recipe.tags


def card_time_label(recipe: Recipe) -> str:
    if "para servir" in recipe.time:
        return f"Já pronto - {recipe.minutes} min"
    if " de preparo" in recipe.time:
        return f"Prepare antes - {recipe.minutes} min"
    return recipe.time


def displayed_profile(recipe: Recipe) -> str:
    if recipe.category == "low_carb":
        return "Low carb culinário*"
    if recipe.category == "sem_acucar":
        return "Sem adição de açúcar*"
    return recipe.profile


def category_disclosure(category_id: str) -> str | None:
    if category_id == "low_carb":
        return "*Classificação culinária; confirme ingredientes, marcas e porções conforme sua necessidade."
    if category_id == "sem_acucar":
        return "*Sem açúcar adicionado. Frutas e laticínios podem conter açúcares naturais."
    if category_id == "chocolate_zero":
        return "Use chocolate identificado no rótulo como zero açúcar."
    if category_id == "proteicas":
        return "O teor de proteína depende dos ingredientes, marcas e porções utilizados."
    return None


def recipe_disclosures(recipe: Recipe) -> tuple[str, ...]:
    notes: list[str] = []
    if is_make_ahead(recipe):
        notes.append(f"Tempo total: {recipe.time}.")
    category_note = category_disclosure(recipe.category)
    if category_note:
        notes.append(category_note)
    return tuple(notes)


def category_matches(recipe: Recipe, situation: Situation) -> bool:
    number = situation.number
    tags = recipe.tags
    has_chocolate = uses_any(recipe, ("cacau", "chocolate"))
    has_fruit = uses_any(recipe, ("banana", "morango", "manga", "uva", "fruta", "pera", "maca", "abacate", "mamao"))
    has_yogurt = uses_any(recipe, ("iogurte",))
    has_oats_or_seeds = uses_any(recipe, ("aveia", "granola", "chia", "semente"))
    if number == 4 and (not ("cold" in tags or has_fruit) or ("warm" in tags and "cold" not in tags)):
        return False
    if number in {21, 23} and (recipe.minutes > 2 or not ({"no_cook", "make_ahead"} & tags)):
        return False
    if number in {11, 24} and recipe.minutes > 5:
        return False
    if number == 25 and recipe.minutes > 10:
        return False
    if number in {6, 27} and not ({"no_cook", "make_ahead"} & tags):
        return False
    # O crumble exige aquecimento em etapas e contradiz "Não quero lavar louça".
    # Morangos com ricota e nibs usa apenas uma montagem curta e substitui essa opção.
    if number == 26 and recipe.id == "rs02":
        return False
    if number == 26 and "no_dishes" not in tags and recipe.id != "rs04":
        return False
    if number in {14, 31} and "warm" not in tags:
        return False
    if number in {15, 20, 30} and "cold" not in tags:
        return False
    if number in {5, 18, 28} and "creamy" not in tags:
        return False
    if number in {10, 19, 29} and "crunchy" not in tags:
        return False
    if number in {22, 32, 33} and not has_fruit:
        return False
    if number == 34 and not has_yogurt:
        return False
    if number == 35 and not has_oats_or_seeds:
        return False
    if number == 36 and not has_chocolate:
        return False
    if number == 37 and ("minimal" not in tags or len(recipe.ingredients) > 4):
        return False
    if number in {3, 16, 17, 18, 19, 20, 21, 22} and not has_chocolate:
        return False
    return True


def recipe_score(recipe: Recipe, situation: Situation, category_index: int) -> float:
    score = 12 * len(recipe.tags & situation.tags)
    if recipe.minutes <= 2 and "quick2" in situation.tags:
        score += 24
    elif recipe.minutes <= 5 and "quick5" in situation.tags:
        score += 15
    elif recipe.minutes <= 10 and "quick10" in situation.tags:
        score += 8
    if "after_meal" in situation.tags and "after_meal" in recipe.tags:
        score += 8
    if "night" in situation.tags and ("cold" in recipe.tags or "warm" in recipe.tags):
        score += 4
    if "work" in situation.tags and "portable" in recipe.tags:
        score += 8
    if "movie" in situation.tags and ({"portable", "crunchy"} & recipe.tags):
        score += 8
    score += ((situation.number * 7 + category_index * 5 + int(recipe.id[-2:])) % 9) * 0.35
    return score


SELECTION_SUBSTITUTIONS: list[dict[str, object]] = []

FINAL_V2_SELECTION_OVERRIDES = {
    (6, "low_carb"): {"lc01": "lc04"},
}


def build_selection_map() -> dict[tuple[int, str], tuple[str, str, str]]:
    SELECTION_SUBSTITUTIONS.clear()
    selections: dict[tuple[int, str], tuple[str, str, str]] = {}
    usage: Counter[str] = Counter()
    for situation in SITUATIONS:
        for category_index, category in enumerate(CATEGORIES):
            key = (situation.number, category.id)
            candidates = [
                recipe
                for recipe in RECIPES_BY_CATEGORY[category.id]
                if category_matches(recipe, situation)
            ]
            if len(candidates) < 3:
                raise ValueError(
                    f"Menos de 3 receitas compativeis: situacao={situation.number}, categoria={category.id}, ids={[r.id for r in candidates]}"
                )
            original = V2_SELECTIONS[key]
            chosen_list = [
                recipe_id
                for recipe_id in original
                if category_matches(RECIPE_BY_ID[recipe_id], situation)
            ]
            for removed_id in original:
                if removed_id in chosen_list:
                    continue
                ranked = sorted(
                    (recipe for recipe in candidates if recipe.id not in chosen_list),
                    key=lambda recipe: (
                        recipe_score(recipe, situation, category_index) - usage[recipe.id] * 0.35,
                        recipe.id,
                    ),
                    reverse=True,
                )
                replacement = ranked[0]
                chosen_list.append(replacement.id)
                SELECTION_SUBSTITUTIONS.append(
                    {
                        "situation": situation.number,
                        "category": category.id,
                        "removed": removed_id,
                        "added": replacement.id,
                    }
                )
            chosen = tuple(chosen_list)
            selections[key] = chosen  # type: ignore[assignment]
            usage.update(chosen)

    missing = [recipe for recipe in RECIPES if usage[recipe.id] == 0]
    for recipe in missing:
        category_index = next(i for i, c in enumerate(CATEGORIES) if c.id == recipe.category)
        possibilities = [
            situation
            for situation in SITUATIONS
            if category_matches(recipe, situation)
        ]
        possibilities.sort(
            key=lambda situation: recipe_score(recipe, situation, category_index),
            reverse=True,
        )
        inserted = False
        for situation in possibilities:
            key = (situation.number, recipe.category)
            current = list(selections[key])
            replaceable = sorted(
                current,
                key=lambda recipe_id: (
                    usage[recipe_id] <= 1,
                    recipe_score(RECIPE_BY_ID[recipe_id], situation, category_index),
                ),
            )
            victim = replaceable[0]
            if usage[victim] <= 1:
                continue
            current[current.index(victim)] = recipe.id
            selections[key] = tuple(current)  # type: ignore[assignment]
            usage[victim] -= 1
            usage[recipe.id] += 1
            inserted = True
            break
        if not inserted:
            raise ValueError(f"Não foi possível inserir receita central no fluxo: {recipe.id}")

    for key, replacements in FINAL_V2_SELECTION_OVERRIDES.items():
        current = list(selections[key])
        for removed_id, replacement_id in replacements.items():
            if removed_id not in current:
                raise ValueError(f"Card esperado para substituição não encontrado: {key}/{removed_id}")
            if replacement_id in current:
                raise ValueError(f"Substituição criaria card duplicado: {key}/{replacement_id}")
            current[current.index(removed_id)] = replacement_id
            usage[removed_id] -= 1
            usage[replacement_id] += 1
            SELECTION_SUBSTITUTIONS.append(
                {
                    "situation": key[0],
                    "category": key[1],
                    "removed": removed_id,
                    "added": replacement_id,
                }
            )
        selections[key] = tuple(current)  # type: ignore[assignment]

    if len(selections) != 222:
        raise ValueError(f"Esperadas 222 combinacoes, obtidas {len(selections)}")
    if any(len(set(ids)) != 3 for ids in selections.values()):
        raise ValueError("Uma selecao contem receitas duplicadas")
    if any(usage[recipe.id] < 1 for recipe in RECIPES):
        raise ValueError("Existe receita central sem nenhum link de entrada")
    return selections


V21_SITUATION_MICROCOPY: dict[int, tuple[str, str, str]] = {
    1: ("Para fechar o almoço: {appeal}.", "Depois de comer, {appeal} combina com a pausa.", "Uma opção {texture} para encerrar a refeição."),
    2: ("Para o final do jantar: {appeal}.", "Depois do jantar, {appeal} mantém a escolha simples.", "Uma opção {texture} para fechar a refeição."),
    3: ("Para matar a pequena vontade: {appeal}.", "Quando é só um pouco de chocolate, {appeal} basta.", "Uma opção {texture} para esse final doce."),
    4: ("Para terminar com frescor: {appeal}.", "Depois de comer, {appeal} deixa o final mais leve.", "Uma opção {texture} para uma sobremesa fresca."),
    5: ("Para a vontade de colher: {appeal}.", "Quando a textura importa, {appeal} entrega cremosidade.", "Uma opção {texture} para depois da refeição."),
    6: ("Sem cozinhar: {appeal}.", "Para uma sobremesa sem preparo, {appeal} simplifica.", "Uma opção {texture} que já pode estar pronta."),
    7: ("Para a pausa da tarde: {appeal}.", "Quando a vontade aparece no meio do dia, {appeal} cabe bem.", "Uma opção {texture} para manter o ritmo."),
    8: ("Entre uma tarefa e outra: {appeal}.", "Para não parar tudo, {appeal} resolve com poucos passos.", "Uma opção {texture} para a pausa do trabalho."),
    9: ("Para acompanhar o café: {appeal}.", "Com a xícara pronta, {appeal} completa o momento.", "Uma opção {texture} para a pausa do café."),
    10: ("Para quando crocância é parte da vontade: {appeal}.", "Se o que falta é textura, {appeal} faz sentido.", "Uma opção {texture} para mastigar devagar."),
    11: ("Para poucos minutos: {appeal}.", "Quando o tempo é curto, {appeal} evita uma receita longa.", "Uma opção {texture} que cabe nesta pausa."),
    12: ("Para o belisco da noite: {appeal}.", "Antes de abrir os armários, {appeal} dá uma direção.", "Uma opção {texture} para ter por perto."),
    13: ("Para comer aos poucos no filme: {appeal}.", "Quando o sofá pede algo doce, {appeal} acompanha bem.", "Uma opção {texture} para pequenas mordidas."),
    14: ("Para uma sobremesa quentinha: {appeal}.", "Quando a noite pede conforto, {appeal} chega quente.", "Uma opção {texture} com aroma de sobremesa."),
    15: ("Para um final de noite gelado: {appeal}.", "Quando a temperatura já está decidida, {appeal} refresca.", "Uma opção {texture} para servir bem fria."),
    16: ("Para a vontade de chocolate à noite: {appeal}.", "Quando o sabor já está claro, {appeal} encurta a escolha.", "Uma opção {texture} para fechar o dia."),
    17: ("Quando é chocolate mesmo: {appeal}.", "Sem rodeios, {appeal} vai direto ao sabor pedido.", "Uma opção {texture} para a vontade de chocolate."),
    18: ("Para chocolate de colher: {appeal}.", "Quando a vontade pede creme, {appeal} entrega essa textura.", "Uma opção {texture} com sabor de chocolate."),
    19: ("Para chocolate com crocância: {appeal}.", "Quando textura e cacau vêm juntos, {appeal} faz sentido.", "Uma opção {texture} para pequenas mordidas."),
    20: ("Para chocolate bem gelado: {appeal}.", "Quando a vontade pede freezer, {appeal} chega frio.", "Uma opção {texture} para servir gelada."),
    21: ("Para ter chocolate em dois minutos: {appeal}.", "Sem etapa escondida, {appeal} cabe no relógio.", "Uma opção {texture} para montar ou servir agora."),
    22: ("Para juntar fruta e chocolate: {appeal}.", "Quando a fruta abre a escolha, {appeal} completa o sabor.", "Uma opção {texture} com fruta de verdade."),
    23: ("Para resolver em dois minutos: {appeal}.", "Sem receita longa, {appeal} cabe no tempo real.", "Uma opção {texture} para montar ou servir agora."),
    24: ("Para resolver em cinco minutos: {appeal}.", "Quando há pouco tempo, {appeal} mantém o preparo curto.", "Uma opção {texture} sem virar projeto de cozinha."),
    25: ("Para preparar em até dez minutos: {appeal}.", "Com alguns minutos a mais, {appeal} cabe de verdade.", "Uma opção {texture} com começo, meio e fim."),
    26: ("Para sujar o mínimo possível: {appeal}.", "Quando a louça é a barreira, {appeal} usa poucos utensílios.", "Uma opção {texture} para montar no próprio pote."),
    27: ("Sem fogão ou forno: {appeal}.", "Quando cozinhar não entra no plano, {appeal} simplifica.", "Uma opção {texture} para montar ou tirar da geladeira."),
    28: ("Para a vontade de colher: {appeal}.", "Quando você quer cremosidade, {appeal} vai direto à textura.", "Uma opção {texture} para este momento."),
    29: ("Para a vontade de mastigar: {appeal}.", "Quando o doce precisa ter crocância, {appeal} responde bem.", "Uma opção {texture} para este momento."),
    30: ("Para servir bem gelado: {appeal}.", "Quando a temperatura vem primeiro, {appeal} refresca.", "Uma opção {texture} que funciona fria."),
    31: ("Para comer ainda quentinho: {appeal}.", "Quando aroma e calor importam, {appeal} faz sentido.", "Uma opção {texture} para este momento."),
    32: ("Para quando a fruta é o sabor principal: {appeal}.", "Se a vontade é frutada, {appeal} mantém essa direção.", "Uma opção {texture} com fruta de verdade."),
    33: ("Para começar pela fruta de casa: {appeal}.", "Com a fruta já escolhida, {appeal} completa a ideia.", "Uma opção {texture} para aproveitar o que está maduro."),
    34: ("Para usar o iogurte que está na geladeira: {appeal}.", "Com o iogurte como base, {appeal} define o complemento.", "Uma opção {texture} montada a partir do que você tem."),
    35: ("Para usar aveia, granola ou sementes: {appeal}.", "Com a despensa como ponto de partida, {appeal} ganha textura.", "Uma opção {texture} feita com o que já está em casa."),
    36: ("Para usar o cacau ou chocolate disponível: {appeal}.", "Com o sabor resolvido, {appeal} define a textura.", "Uma opção {texture} sem procurar outra receita."),
    37: ("Para quando a despensa está curta: {appeal}.", "Com poucos ingredientes, {appeal} mantém a receita possível.", "Uma opção {texture} com lista enxuta."),
}


def v21_contextual_micro(situation: Situation, recipe: Recipe, category_index: int, slot: int) -> str:
    if is_make_ahead(recipe):
        return f"Com preparo antecipado, esta opção fica pronta para {situation.context}: {recipe.appeal}."
    pattern = V21_SITUATION_MICROCOPY[situation.number][slot]
    return pattern.format(appeal=recipe.appeal, texture=recipe.texture)


MICROCOPY_CONTEXT: dict[int, tuple[str, str]] = {
    1: ("o almoço acabou e ainda ficou aquela vontade de doce", "fechar o almoço"),
    2: ("o jantar terminou e você quer fechar com algo doce", "encerrar o jantar"),
    3: ("você quer só um pouco de chocolate depois da refeição", "uma vontade pequena de chocolate"),
    4: ("a refeição acabou e algo fresco parece melhor", "um final de refeição mais fresco"),
    5: ("a vontade depois de comer veio cremosa", "uma sobremesa cremosa"),
    6: ("você quer sobremesa sem preparar nada", "uma sobremesa sem cozinha"),
    7: ("a vontade apareceu no fim da tarde", "a pausa da tarde"),
    8: ("você está trabalhando e não quer parar tudo", "uma pausa curta no trabalho"),
    9: ("o café já está pronto e falta algo doce", "acompanhar o café"),
    10: ("a vontade pede algo doce e crocante", "uma vontade de crocância"),
    11: ("você quer doce, mas só tem poucos minutos", "resolver em poucos minutos"),
    12: ("a noite chegou e bateu vontade de beliscar doce", "o belisco da noite"),
    13: ("o filme começou e você quer algo doce por perto", "comer aos poucos durante o filme"),
    14: ("a noite pede uma sobremesa quentinha", "uma sobremesa quente e confortável"),
    15: ("a vontade da noite veio gelada", "um final de noite gelado"),
    16: ("é chocolate que você quer à noite", "a vontade de chocolate à noite"),
    17: ("hoje é chocolate mesmo", "uma vontade direta de chocolate"),
    18: ("a vontade pede chocolate cremoso", "chocolate de colher"),
    19: ("chocolate com crocância é o que veio à cabeça", "chocolate com textura crocante"),
    20: ("a vontade pede chocolate gelado", "chocolate bem gelado"),
    21: ("você quer chocolate e só tem dois minutos", "chocolate em dois minutos"),
    22: ("você quer juntar fruta e chocolate", "combinar fruta e chocolate"),
    23: ("você só tem dois minutos", "uma escolha de dois minutos"),
    24: ("você tem cinco minutos para resolver a vontade", "um preparo de cinco minutos"),
    25: ("você pode dedicar até dez minutos", "um preparo de até dez minutos"),
    26: ("você quer doce sem criar uma pia cheia", "usar o mínimo de louça"),
    27: ("cozinhar não faz parte do plano", "uma escolha sem fogão ou forno"),
    28: ("a vontade veio cremosa", "uma vontade de colher"),
    29: ("a vontade veio crocante", "uma vontade de mastigar"),
    30: ("você quer algo doce e bem gelado", "uma escolha bem gelada"),
    31: ("você quer algo doce e quentinho", "uma escolha servida quente"),
    32: ("a vontade pede fruta de verdade", "uma escolha em que a fruta aparece"),
    33: ("você quer começar pela fruta que já tem", "aproveitar a fruta de casa"),
    34: ("o iogurte é a base disponível agora", "usar o iogurte da geladeira"),
    35: ("aveia, granola ou sementes são o ponto de partida", "usar os ingredientes da despensa"),
    36: ("cacau ou chocolate já estão em casa", "partir do sabor de chocolate"),
    37: ("a despensa está curta e a vontade apareceu", "uma receita com poucos ingredientes"),
}


MICROCOPY_STYLES = (
    "Quando {recognition}, você encontra {appeal}.",
    "Uma opção para {context}: {appeal}.",
    "{recognition_cap}. Aqui a sugestão é {appeal}.",
    "Se {recognition}, vá direto para {appeal}.",
    "Para {context}, uma opção é {appeal}.",
    "Se a vontade está bem definida, esta opção entrega {appeal}.",
    "Sem abrir outra busca, você pode escolher {appeal}.",
    "Boa para este momento: {appeal}.",
    "Se a vontade veio assim, comece por {appeal}.",
    "Uma escolha simples para {context}: {appeal}.",
    "Quando {recognition}, a ideia é {appeal}.",
    "Aqui você já parte de {appeal}.",
    "Para não alongar a decisão: {appeal}.",
    "Se é isso que você quer agora, escolha {appeal}.",
    "A receita segue a direção de {context}: {appeal}.",
    "Para este momento, você encontra {appeal}.",
    "Para {context}, dá para ir de {appeal}.",
    "{recognition_cap}; a opção aqui é {appeal}.",
    "Agora é só escolher: {appeal}.",
    "Uma ideia que combina com {context}: {appeal}.",
    "Se {recognition}, esta é uma forma de chegar a {appeal}.",
    "Aqui a escolha foi filtrada para {context}: {appeal}.",
    "Quando a vontade vem desse jeito, você pode escolher {appeal}.",
    "Para manter tudo rápido e direto: {appeal}.",
    "Para {context}, a receita traz {appeal}.",
    "Se o pensamento foi esse, a opção pode ser {appeal}.",
    "Uma opção prática para {context}: {appeal}.",
    "Você não precisa procurar do zero: {appeal}.",
    "Para esta situação, considere {appeal}.",
    "Quando {recognition}, vale ter {appeal}.",
    "Para este momento, vale considerar {appeal}.",
    "Se quiser manter a decisão simples, vá de {appeal}.",
    "Nesta situação, você já encontra {appeal}.",
    "Para seguir a vontade sem inventar outra: {appeal}.",
    "Esta opção já vem filtrada para o momento: {appeal}.",
    "A escolha pode começar por {appeal}, sem transformar o momento em pesquisa.",
)


MAKE_AHEAD_STYLES = (
    "Com a receita pronta, você tem {appeal} para {context}.",
    "Vale preparar antes; na hora, você encontra {appeal}.",
    "Deixe pronta antes e, quando {recognition}, sirva {appeal}.",
    "Para {context}, esta receita pode ficar pronta: {appeal}.",
    "Aqui o preparo acontece antes; depois, basta servir {appeal}.",
    "Se estiver pronta, a escolha vira {appeal} sem começar outra busca.",
    "Deixe pronta antes; na hora, sirva {appeal}.",
    "Preparada com antecedência, esta receita oferece {appeal}.",
    "Quando {recognition}, ajuda encontrar {appeal} à mão.",
    "O preparo fica para antes; neste momento, você só serve {appeal}.",
    "Se já estiver na geladeira, vá direto para {appeal}.",
    "Para não cozinhar na hora, antecipe o preparo de {appeal}.",
)

DELIVERY_REVISED_REGULAR_STYLE_INDEXES = frozenset({5, 7, 15, 18, 24, 26, 30, 34})
DELIVERY_REVISED_MAKE_AHEAD_STYLE_INDEXES = frozenset({6})

FINAL_V2_MICROCOPY_OVERRIDES = {
    (6, "low_carb", "lc04"): "Prepare antes; quando a vontade aparecer, o pudim de chia e coco já estará pronto para servir.",
    (20, "low_carb", "lc03"): "Café cremoso com cacau servido frio ou com gelo para combinar com a vontade gelada.",
    (22, "brigadeiro_fit", "bf07"): "Cacau e banana aparecem juntos para combinar chocolate e fruta neste preparo.",
    (23, "sem_acucar", "sa01"): "Para quando você só tem dois minutos: fruta doce com cacau, sem complicar.",
    (23, "proteicas", "pt09"): "Para quando você só tem dois minutos: creme rápido de cacau e cottage.",
    (29, "sem_acucar", "sa08"): "O iogurte de cacau fica cremoso; sementes adicionadas na hora trazem a crocância.",
    (29, "proteicas", "pt05"): "Base cremosa de cacau com sementes adicionadas na hora para trazer crocância.",
}


def microcopy_style_index(situation: Situation, category_index: int, slot: int, *, make_ahead: bool) -> int:
    size = len(MAKE_AHEAD_STYLES) if make_ahead else len(MICROCOPY_STYLES)
    return (situation.number * 17 + category_index * 7 + slot * 11) % size


def contextual_micro(situation: Situation, recipe: Recipe, category_index: int, slot: int) -> str:
    category_id = CATEGORIES[category_index].id
    override = FINAL_V2_MICROCOPY_OVERRIDES.get((situation.number, category_id, recipe.id))
    if override is not None:
        return override
    recognition, context = MICROCOPY_CONTEXT[situation.number]
    make_ahead = is_make_ahead(recipe)
    styles = MAKE_AHEAD_STYLES if make_ahead else MICROCOPY_STYLES
    pattern = styles[microcopy_style_index(situation, category_index, slot, make_ahead=make_ahead)]
    return pattern.format(
        recognition=recognition,
        recognition_cap=recognition[:1].upper() + recognition[1:],
        context=context,
        appeal=recipe.appeal,
    )


def expected_page_by_name() -> dict[str, int]:
    return {
        "home": 0,
        "situations": 1,
        **{f"situation_{situation.number:02d}": 1 + situation.number for situation in SITUATIONS},
        **{
            f"category_{situation.number:02d}_{category.id}": 39 + (situation.number - 1) * 6 + category_index
            for situation in SITUATIONS
            for category_index, category in enumerate(CATEGORIES)
        },
        **{f"recipe_{recipe.id}": 261 + recipe_index for recipe_index, recipe in enumerate(RECIPES)},
        "list_base": 321,
        "shortcuts": 322,
        "sources": 323,
        "notice": 324,
    }


def harden_internal_navigation(source: Path, output: Path) -> dict[str, int]:
    reader = PdfReader(str(source))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    expected = expected_page_by_name()
    inverse = {page_index: name for name, page_index in expected.items()}
    if len(inverse) != 325:
        raise ValueError("Mapa de destinos duplicado antes do hardening")

    for name, page_index in expected.items():
        writer.add_named_destination(name, page_index)

    page_ref_to_index = {
        page.indirect_reference.idnum: page_index
        for page_index, page in enumerate(writer.pages)
        if page.indirect_reference is not None
    }
    rewritten = 0
    for source_page, page in enumerate(writer.pages, start=1):
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            if annotation.get("/Subtype") != "/Link":
                raise ValueError(f"Anotação não-Link encontrada na página {source_page}")
            destination = annotation.get("/Dest")
            if destination is None and annotation.get("/A"):
                destination = annotation["/A"].get_object().get("/D")
            if not isinstance(destination, (ArrayObject, list)) or not destination:
                raise ValueError(f"Destino original inesperado na página {source_page}: {destination}")
            target_ref = destination[0]
            target_page_index = page_ref_to_index.get(getattr(target_ref, "idnum", -1))
            if target_page_index is None or target_page_index not in inverse:
                raise ValueError(f"Destino sem página válida na página {source_page}")
            target_name = inverse[target_page_index]
            annotation.pop(NameObject("/Dest"), None)
            annotation[NameObject("/A")] = DictionaryObject(
                {
                    NameObject("/S"): NameObject("/GoTo"),
                    NameObject("/D"): TextStringObject(target_name),
                }
            )
            rewritten += 1

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as stream:
        writer.write(stream)
    return {"goto_links_rewritten": rewritten, "named_destinations_created": len(expected)}


class GuideBuilder:
    def __init__(self, output: Path, selections: dict[tuple[int, str], tuple[str, str, str]]):
        self.output = output
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(output), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
        self.c.setTitle("Quando Bate o Doce - Guia Situacional de Consulta DEFINITIVO")
        self.c.setAuthor("Quando Bate o Doce")
        self.c.setSubject("37 situações com opções fit organizadas para consulta no celular")
        self.c.setKeywords("guia situacional, receitas fit, consulta mobile, doce")
        self.page_no = 0
        self.destinations: list[str] = []
        self.link_count = 0
        self.layout_checks: list[tuple[str, float]] = []
        self.selections = selections
        self.page_by_destination = expected_page_by_name()
        self.apple = ROOT / "public" / "qbd-apple-mark-v1.png"

    def new_page(self, destination: str, title: str, *, header: bool = True, outline_level: int | None = None) -> None:
        if self.page_no:
            self.c.showPage()
        self.page_no += 1
        self.destinations.append(destination)
        self.c.bookmarkPage(destination)
        if outline_level is not None:
            self.c.addOutlineEntry(title, destination, level=outline_level, closed=False)
        self.c.setFillColor(CREAM)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        if header:
            self.draw_header()

    def draw_header(self) -> None:
        draw_image_contain(self.c, self.apple, 22, PAGE_H - 53, 25, 30)
        self.c.setFillColor(INK)
        self.c.setFont("QBDSansBold", 9.2)
        self.c.drawString(53, PAGE_H - 34, "QUANDO BATE")
        self.c.drawString(53, PAGE_H - 45, "O DOCE")
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.7)
        self.c.line(22, PAGE_H - 65, PAGE_W - 22, PAGE_H - 65)
        self.c.setFont("QBDSans", 7.5)
        self.c.setFillColor(MUTED)
        self.c.drawRightString(PAGE_W - 22, 18, f"{self.page_no:03d}")

    def link(self, destination: str, x: float, y: float, w: float, h: float) -> None:
        self.c.linkRect("", destination, Rect=(x, y, x + w, y + h), relative=0, thickness=0)
        self.link_count += 1

    def page_reference(self, destination: str) -> str:
        return f"pág. {self.page_by_destination[destination] + 1}"

    def button(
        self,
        label: str,
        destination: str,
        x: float,
        y: float,
        w: float,
        h: float,
        *,
        fill: colors.Color = WINE,
        text_color: colors.Color = WHITE,
        font_size: float = 11,
        radius: float = 14,
        border: colors.Color | None = None,
        max_lines: int = 2,
    ) -> None:
        self.c.setFillColor(fill)
        self.c.setStrokeColor(border or fill)
        self.c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if border else 0)
        display_label = f"{label}  ›  {self.page_reference(destination)}"
        lines = wrap_text(display_label, "QBDSansBold", font_size, w - 20)
        if len(lines) > max_lines:
            raise ValueError(f"Botao excedeu {max_lines} linhas: {display_label}")
        leading = font_size * 1.16
        total = len(lines) * leading
        top = y + (h + total) / 2 - 2
        self.c.setFillColor(text_color)
        self.c.setFont("QBDSansBold", font_size)
        for i, line in enumerate(lines):
            self.c.drawCentredString(x + w / 2, top - font_size - i * leading, line)
        self.link(destination, x, y, w, h)

    def small_nav(self, items: Sequence[tuple[str, str]], y: float = 27) -> None:
        gap = 8
        total_w = PAGE_W - 44
        width = (total_w - gap * (len(items) - 1)) / len(items)
        for i, (label, dest) in enumerate(items):
            self.button(
                label,
                dest,
                22 + i * (width + gap),
                y,
                width,
                38,
                fill=WHITE,
                text_color=WINE,
                font_size=8.6,
                radius=12,
                border=LINE,
            )

    def draw_home(self) -> None:
        self.new_page("home", "Inicio", header=False, outline_level=0)
        self.c.setFillColor(CREAM)
        self.c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        draw_image_contain(self.c, self.apple, 28, 758, 46, 56)
        self.c.setFillColor(INK)
        self.c.setFont("QBDSansBold", 12)
        self.c.drawString(84, 792, "QUANDO BATE")
        self.c.drawString(84, 776, "O DOCE")
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9.5)
        self.c.drawString(28, 724, "GUIA SITUACIONAL DE CONSULTA")
        draw_wrapped(self.c, "Quando bate a vontade, abra pela situacao.", 28, 688, 330, "QBDSerifBold", 27, 32, INK, 2)
        draw_wrapped(self.c, "Opcoes fit organizadas para consultar no celular, sem comecar outra busca.", 28, 596, 330, "QBDSans", 13, 18, MUTED, 2)

        steps = (
            ("01", "Escolha o que esta acontecendo."),
            ("02", "Escolha o tipo de opcao."),
            ("03", "Abra uma receita."),
        )
        y = 482
        for number, text in steps:
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(28, y, 334, 70, 18, fill=1, stroke=1)
            self.c.setFillColor(GREEN_SOFT)
            self.c.circle(62, y + 35, 21, fill=1, stroke=0)
            self.c.setFillColor(GREEN)
            self.c.setFont("QBDSansBold", 10)
            self.c.drawCentredString(62, y + 31, number)
            draw_wrapped(self.c, text, 94, y + 45, 238, "QBDSansBold", 12.2, 15, INK, 2)
            y -= 84

        self.button("COMEÇAR", "situations", 28, 112, 334, 64, fill=PINK, font_size=14, radius=24)
        self.c.setFillColor(MUTED)
        self.c.setFont("QBDSans", 6.8)
        self.c.drawCentredString(PAGE_W / 2, 84, "Os botões são interativos em leitores compatíveis.")
        self.c.drawCentredString(
            PAGE_W / 2,
            73,
            "Se o visualizador bloquear links, use o número da página exibido no botão.",
        )

    def draw_situations_index(self) -> None:
        self.new_page("situations", "37 situacoes", outline_level=0)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9.5)
        self.c.drawString(22, 748, "ESCOLHA O MOMENTO")
        draw_wrapped(self.c, "O que está acontecendo agora?", 22, 718, 346, "QBDSerifBold", 26, 30, INK, 2)

        left = 22
        gap = 8
        width = (PAGE_W - 44 - gap) / 2
        height = 25
        row_gap = 3
        top = 646
        for index, situation in enumerate(SITUATIONS):
            col = index % 2
            row = index // 2
            x = left + col * (width + gap)
            y = top - row * (height + row_gap) - height
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(x, y, width, height, 10, fill=1, stroke=1)
            self.c.setFillColor(WINE)
            self.c.circle(x + 15, y + height / 2, 9, fill=1, stroke=0)
            self.c.setFillColor(WHITE)
            self.c.setFont("QBDSansBold", 5.6)
            page_number = self.page_by_destination[f"situation_{situation.number:02d}"] + 1
            self.c.drawCentredString(x + 15, y + height / 2 - 2.0, f"p.{page_number}")
            lines = wrap_text(situation.title, "QBDSansBold", 7.3, width - 40)
            if len(lines) > 2:
                raise ValueError(f"Situacao nao cabe no indice: {situation.title}")
            self.c.setFillColor(INK)
            self.c.setFont("QBDSansBold", 7.3)
            if len(lines) == 1:
                self.c.drawString(x + 30, y + 11, lines[0])
            else:
                self.c.drawString(x + 30, y + 17, lines[0])
                self.c.drawString(x + 30, y + 7.5, lines[1])
            self.link(f"situation_{situation.number:02d}", x, y, width, height)
        self.small_nav((("LISTA-BASE", "list_base"), ("ATALHOS", "shortcuts"), ("FONTES", "sources")), y=35)

    def draw_situation(self, situation: Situation) -> None:
        self.new_page(
            f"situation_{situation.number:02d}",
            f"{situation.number:02d} - {situation.title}",
            outline_level=1,
        )
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 8.5)
        self.c.drawString(22, 749, pt_text(f"{situation.group}  /  SITUACAO {situation.number:02d}"))
        y = draw_wrapped(self.c, situation.title, 22, 718, 346, "QBDSerifBold", 25, 29, INK, 3)
        y -= 8
        y = draw_wrapped(self.c, situation.intro, 22, y, 346, "QBDSans", 11.2, 15.2, MUTED, 4)
        self.c.setFillColor(CHOCOLATE)
        self.c.roundRect(22, y - 51, 346, 39, 13, fill=1, stroke=0)
        self.c.setFillColor(WHITE)
        self.c.setFont("QBDSansBold", 9.5)
        self.c.drawString(36, y - 35, pt_text("Escolha o tipo de opcao"))
        self.c.setFont("QBDSans", 8.3)
        self.c.drawRightString(354, y - 35, "6 filtros")

        card_w = 165
        card_h = 109
        col_gap = 16
        row_gap = 12
        top = y - 78
        for index, category in enumerate(CATEGORIES):
            col = index % 2
            row = index // 2
            x = 22 + col * (card_w + col_gap)
            card_y = top - row * (card_h + row_gap) - card_h
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(x, card_y, card_w, card_h, 18, fill=1, stroke=1)
            self.c.setFillColor(HexColor(category.accent))
            self.c.circle(x + 36, card_y + 69, 24, fill=1, stroke=0)
            draw_image_contain(self.c, category.icon, x + 20, card_y + 53, 32, 32)
            draw_wrapped(self.c, category.label, x + 18, card_y + 39, card_w - 36, "QBDSansBold", 10.2, 12, INK, 2)
            category_destination = f"category_{situation.number:02d}_{category.id}"
            self.c.setFillColor(MUTED)
            self.c.setFont("QBDSansBold", 6.2)
            self.c.drawRightString(x + card_w - 16, card_y + 14, self.page_reference(category_destination))
            self.link(category_destination, x, card_y, card_w, card_h)

        previous = SITUATIONS[situation.number - 2] if situation.number > 1 else None
        next_situation = SITUATIONS[situation.number] if situation.number < len(SITUATIONS) else None
        nav_items: list[tuple[str, str]] = [("37 SITUACOES", "situations")]
        if previous:
            nav_items.insert(0, ("ANTERIOR", f"situation_{previous.number:02d}"))
        if next_situation:
            nav_items.append(("PROXIMA", f"situation_{next_situation.number:02d}"))
        self.small_nav(nav_items)

    def draw_category(self, situation: Situation, category: Category, category_index: int) -> None:
        destination = f"category_{situation.number:02d}_{category.id}"
        self.new_page(destination, f"{situation.title} - {category.label}")
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 8.2)
        self.c.drawString(22, 749, pt_text(f"SITUACAO {situation.number:02d}  /  {category.short.upper()}"))
        draw_wrapped(self.c, category.label, 22, 716, 278, "QBDSerifBold", 24, 28, INK, 2)
        draw_wrapped(self.c, situation.title, 22, 661, 346, "QBDSansBold", 11.5, 14, WINE, 2)
        draw_wrapped(self.c, "Tres opcoes filtradas para o momento que voce escolheu.", 22, 624, 346, "QBDSans", 9.6, 12.5, MUTED, 2)
        disclosure = category_disclosure(category.id)
        if disclosure:
            draw_wrapped(self.c, disclosure, 22, 600, 346, "QBDSans", 6.8, 8.2, MUTED, 2)

        recipe_ids = self.selections[(situation.number, category.id)]
        card_h = 162
        gap = 10
        top = 575
        for slot, recipe_id in enumerate(recipe_ids):
            recipe = RECIPE_BY_ID[recipe_id]
            y = top - slot * (card_h + gap) - card_h
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(22, y, 346, card_h, 18, fill=1, stroke=1)
            self.c.setFillColor(HexColor(category.accent))
            self.c.circle(52, y + 123, 20, fill=1, stroke=0)
            draw_image_contain(self.c, category.icon, 39, y + 110, 26, 26)
            draw_wrapped(self.c, recipe.name, 82, y + 141, 260, "QBDSansBold", 12.2, 14, INK, 2)
            micro = contextual_micro(situation, recipe, category_index, slot)
            draw_wrapped(self.c, micro, 38, y + 98, 314, "QBDSans", 8.7, 11.1, MUTED, 2)

            chip_y = y + 43
            chips = (card_time_label(recipe), recipe.difficulty, displayed_profile(recipe))
            chip_x = 38
            for chip in chips:
                chip_w = min(105, max(48, pdfmetrics.stringWidth(chip, "QBDSansBold", 7.1) + 16))
                self.c.setFillColor(GREEN_SOFT)
                self.c.roundRect(chip_x, chip_y, chip_w, 20, 8, fill=1, stroke=0)
                self.c.setFillColor(GREEN)
                self.c.setFont("QBDSansBold", 7.1)
                self.c.drawCentredString(chip_x + chip_w / 2, chip_y + 6.5, pt_text(chip))
                chip_x += chip_w + 6
                if chip_x > 345:
                    break
            self.c.setFillColor(PINK)
            self.c.roundRect(258, y + 14, 94, 25, 10, fill=1, stroke=0)
            self.c.setFillColor(WHITE)
            self.c.setFont("QBDSansBold", 7.1)
            recipe_destination = f"recipe_{recipe.id}"
            self.c.drawCentredString(305, y + 22.5, f"ABRIR - {self.page_reference(recipe_destination)}")
            self.link(recipe_destination, 22, y, 346, card_h)

        self.small_nav((("VOLTAR A SITUACAO", f"situation_{situation.number:02d}"), ("INICIO", "home")), y=18)

    def draw_recipe(self, recipe: Recipe) -> None:
        category = CATEGORY_BY_ID[recipe.category]
        self.new_page(f"recipe_{recipe.id}", recipe.name)
        self.c.setFillColor(HexColor(category.accent))
        self.c.circle(56, 731, 31, fill=1, stroke=0)
        draw_image_contain(self.c, category.icon, 36, 711, 40, 40)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 8.2)
        self.c.drawString(102, 754, pt_text(category.label.upper()))
        y = draw_wrapped(self.c, recipe.name, 102, 730, 266, "QBDSerifBold", 23, 26, INK, 3)
        y -= 4
        y = draw_wrapped(self.c, recipe.familiar, 22, y, 346, "QBDSans", 10.2, 13, MUTED, 3)

        chips = (card_time_label(recipe), recipe.difficulty, recipe.yield_text, displayed_profile(recipe))
        chip_x = 22
        chip_y = y - 29
        for chip in chips:
            chip_w = min(106, max(55, pdfmetrics.stringWidth(chip, "QBDSansBold", 7.2) + 18))
            if chip_x + chip_w > 368:
                chip_x = 22
                chip_y -= 27
            self.c.setFillColor(GREEN_SOFT)
            self.c.roundRect(chip_x, chip_y, chip_w, 21, 8, fill=1, stroke=0)
            self.c.setFillColor(GREEN)
            self.c.setFont("QBDSansBold", 7.2)
            self.c.drawCentredString(chip_x + chip_w / 2, chip_y + 7, pt_text(chip))
            chip_x += chip_w + 6

        disclosures = recipe_disclosures(recipe)
        ingredients_top = chip_y - 18
        if disclosures:
            disclosure_bottom = draw_wrapped(
                self.c,
                " ".join(disclosures),
                22,
                chip_y - 6,
                346,
                "QBDSans",
                6.7,
                8.2,
                MUTED,
                3,
            )
            ingredients_top = disclosure_bottom - 6
        ingredient_h = 190
        self.c.setFillColor(WHITE)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(22, ingredients_top - ingredient_h, 346, ingredient_h, 18, fill=1, stroke=1)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 10)
        self.c.drawString(38, ingredients_top - 25, "INGREDIENTES")
        iy = ingredients_top - 45
        for ingredient in recipe.ingredients:
            self.c.setFillColor(PINK)
            self.c.circle(41, iy - 4, 2.2, fill=1, stroke=0)
            iy = draw_wrapped(self.c, ingredient, 50, iy + 2, 298, "QBDSans", 9.2, 12, INK, 2) - 3
        if iy < ingredients_top - ingredient_h + 14:
            raise ValueError(f"Overflow de ingredientes: {recipe.id}")

        preparation_top = ingredients_top - ingredient_h - 12
        preparation_h = 154
        self.c.setFillColor(WHITE)
        self.c.setStrokeColor(LINE)
        self.c.roundRect(22, preparation_top - preparation_h, 346, preparation_h, 18, fill=1, stroke=1)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 10)
        self.c.drawString(38, preparation_top - 25, "PREPARO")
        py = preparation_top - 48
        for index, step in enumerate(recipe.steps, start=1):
            self.c.setFillColor(PINK)
            self.c.circle(45, py - 5, 9, fill=1, stroke=0)
            self.c.setFillColor(WHITE)
            self.c.setFont("QBDSansBold", 7.3)
            self.c.drawCentredString(45, py - 7.4, str(index))
            py = draw_wrapped(self.c, step, 62, py + 2, 286, "QBDSans", 9.2, 12, INK, 3) - 7
        if py < preparation_top - preparation_h + 12:
            raise ValueError(f"Overflow de preparo: {recipe.id}")

        tip_top = preparation_top - preparation_h - 10
        self.c.setFillColor(CHOCOLATE)
        self.c.roundRect(22, tip_top - 59, 346, 59, 15, fill=1, stroke=0)
        self.c.setFillColor(PINK)
        self.c.setFont("QBDSansBold", 8)
        self.c.drawString(38, tip_top - 18, pt_text("DICA PRATICA"))
        draw_wrapped(self.c, recipe.tip, 38, tip_top - 25, 314, "QBDSans", 8.3, 10.5, WHITE, 3)
        if tip_top - 59 < 72:
            raise ValueError(f"Pagina de receita invadiu navegacao: {recipe.id}")
        self.small_nav((("INICIO", "home"), ("VER 37 SITUACOES", "situations")), y=20)

    def draw_list_base(self) -> None:
        self.new_page("list_base", "Lista-base", outline_level=0)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9)
        self.c.drawString(22, 748, "LISTA-BASE")
        draw_wrapped(self.c, "Algumas escolhas ficam mais faceis quando algumas bases ja estao em casa.", 22, 715, 346, "QBDSerifBold", 23, 27, INK, 3)
        draw_wrapped(self.c, "Nao e uma lista obrigatoria. Use como referencia para montar as opcoes do guia.", 22, 630, 346, "QBDSans", 10.5, 14, MUTED, 3)
        groups = (
            ("GELADEIRA", ["iogurte natural ou de maior teor proteico", "frutas lavadas", "ricota ou cottage", "leite e ovos"]),
            ("DESPENSA", ["cacau em po", "aveia, chia e sementes", "castanhas", "pasta de amendoim sem acucar"]),
            ("CONFERIR ROTULO", ["chocolate zero acucar", "iogurtes sem acucar adicionado", "coco sem acucar", "adoçante culinario, se usar"]),
            ("FREEZER", ["fruta em porcoes", "picoles caseiros", "bark de iogurte", "bases preparadas com antecedencia"]),
        )
        card_w = 165
        card_h = 190
        for index, (title, items) in enumerate(groups):
            col = index % 2
            row = index // 2
            x = 22 + col * 181
            y = 385 - row * 208
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(x, y, card_w, card_h, 18, fill=1, stroke=1)
            self.c.setFillColor(WINE)
            self.c.setFont("QBDSansBold", 9)
            self.c.drawString(x + 14, y + 163, pt_text(title))
            ty = y + 139
            for item in items:
                self.c.setFillColor(PINK)
                self.c.circle(x + 17, ty - 3, 2, fill=1, stroke=0)
                ty = draw_wrapped(self.c, item, x + 25, ty + 2, 126, "QBDSans", 8.3, 10.5, INK, 2) - 7
        self.small_nav((("INICIO", "home"), ("37 SITUACOES", "situations")))

    def draw_shortcuts(self) -> None:
        self.new_page("shortcuts", "Atalhos", outline_level=0)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9)
        self.c.drawString(22, 748, "ATALHOS")
        draw_wrapped(self.c, "Va direto ao filtro que mais importa agora.", 22, 714, 346, "QBDSerifBold", 25, 29, INK, 2)
        shortcuts = (
            ("TENHO 2 MINUTOS", "situation_23"),
            ("TENHO 5 MINUTOS", "situation_24"),
            ("NAO QUERO COZINHAR", "situation_27"),
            ("QUERO CHOCOLATE", "situation_17"),
            ("QUERO ALGO GELADO", "situation_30"),
            ("QUERO USAR FRUTA", "situation_33"),
        )
        y = 560
        for label, dest in shortcuts:
            self.button(label, dest, 28, y, 334, 68, fill=WHITE, text_color=WINE, font_size=11, radius=18, border=LINE)
            y -= 82
        self.small_nav((("INICIO", "home"), ("37 SITUACOES", "situations")), y=24)

    def draw_sources(self) -> None:
        self.new_page("sources", "Fontes", outline_level=0)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9)
        self.c.drawString(22, 748, pt_text("FONTES E TRANSPARENCIA"))
        draw_wrapped(self.c, "Referencias usadas para principios gerais.", 22, 714, 346, "QBDSerifBold", 24, 28, INK, 2)
        draw_wrapped(self.c, "As receitas foram formuladas para este material. As fontes abaixo nao transformam o guia em prescricao individual.", 22, 646, 346, "QBDSans", 10, 13.5, MUTED, 4)
        sources = (
            "Ministerio da Saude. Guia Alimentar para a Populacao Brasileira, 2ª ed., 2014.",
            "World Health Organization. Healthy diet e orientacoes sobre acucares livres.",
            "ANVISA. Cartilha sobre Boas Praticas para Servicos de Alimentacao, RDC 216/2004.",
            "Medeiros ACQ et al. Food cravings among Brazilian population. Appetite. 2017;108:212-218.",
            "Davidson GR et al. Pre- and postprandial variation in implicit attention to food images. Appetite. 2018;125:24-31.",
        )
        y = 540
        for index, source in enumerate(sources, start=1):
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(22, y, 346, 78, 14, fill=1, stroke=1)
            self.c.setFillColor(GREEN_SOFT)
            self.c.circle(48, y + 39, 16, fill=1, stroke=0)
            self.c.setFillColor(GREEN)
            self.c.setFont("QBDSansBold", 8)
            self.c.drawCentredString(48, y + 36, str(index))
            draw_wrapped(self.c, source, 76, y + 58, 272, "QBDSans", 8.5, 11, INK, 4)
            y -= 92
        self.small_nav((("INICIO", "home"), ("AVISO FINAL", "notice")), y=24)

    def draw_notice(self) -> None:
        self.new_page("notice", "Aviso importante", outline_level=0)
        self.c.setFillColor(WINE)
        self.c.setFont("QBDSansBold", 9)
        self.c.drawString(22, 748, "AVISO IMPORTANTE")
        draw_wrapped(self.c, "Este guia organiza escolhas. Ele nao substitui orientacao profissional.", 22, 714, 346, "QBDSerifBold", 24, 28, INK, 3)
        notices = (
            ("USO", "Material educativo e de consulta. Nao realiza diagnostico, nao prescreve dieta e nao promete emagrecimento."),
            ("ROTULOS", "As classificacoes dependem dos ingredientes usados. Confira acucares, carboidratos, proteina e alergênicos nos rotulos."),
            ("SEM ACUCAR", "Neste guia, a categoria indica receitas sem adicao de acucar. Alimentos como frutas e leite podem conter acucares naturais."),
            ("CUIDADOS", "Alergias, intolerancias, gestacao, medicamentos e condicoes de saude exigem orientacao individual de profissional qualificado."),
            ("CONSERVACAO", "Mantenha alimentos pereciveis refrigerados, higienize ingredientes e respeite as instrucoes de conservacao dos rotulos."),
        )
        y = 540
        for title, body in notices:
            self.c.setFillColor(WHITE)
            self.c.setStrokeColor(LINE)
            self.c.roundRect(22, y, 346, 86, 16, fill=1, stroke=1)
            self.c.setFillColor(WINE)
            self.c.setFont("QBDSansBold", 8.5)
            self.c.drawString(38, y + 62, pt_text(title))
            draw_wrapped(self.c, body, 38, y + 52, 314, "QBDSans", 8.7, 11.2, INK, 4)
            y -= 98
        self.button("VOLTAR AO INICIO", "home", 28, 50, 334, 58, fill=PINK, font_size=12.5, radius=22)

    def build(self) -> dict[str, object]:
        self.draw_home()
        self.draw_situations_index()
        for situation in SITUATIONS:
            self.draw_situation(situation)
        for situation in SITUATIONS:
            for category_index, category in enumerate(CATEGORIES):
                self.draw_category(situation, category, category_index)
        for recipe in RECIPES:
            self.draw_recipe(recipe)
        self.draw_list_base()
        self.draw_shortcuts()
        self.draw_sources()
        self.draw_notice()
        if self.page_no != 325:
            raise ValueError(f"Esperadas 325 paginas, geradas {self.page_no}")
        self.c.save()
        return {
            "pages": self.page_no,
            "destinations": len(self.destinations),
            "links_created": self.link_count,
        }


def validate_content(selections: dict[tuple[int, str], tuple[str, str, str]]) -> dict[str, object]:
    if len(SITUATIONS) != 37:
        raise ValueError(f"Quantidade incorreta de situacoes: {len(SITUATIONS)}")
    if len(CATEGORIES) != 6:
        raise ValueError(f"Quantidade incorreta de categorias: {len(CATEGORIES)}")
    if len(RECIPES) != 60 or len(RECIPE_BY_ID) != 60:
        raise ValueError(f"Quantidade incorreta de receitas unicas: {len(RECIPES)}")
    if len(selections) != 222:
        raise ValueError(f"Quantidade incorreta de combinacoes: {len(selections)}")

    used: set[str] = set()
    micros: list[str] = []
    legacy_micros: list[str] = []
    regular_style_usage: Counter[int] = Counter()
    make_ahead_style_usage: Counter[int] = Counter()
    delivery_microcopy_corrections = 0
    for situation in SITUATIONS:
        for category_index, category in enumerate(CATEGORIES):
            recipe_ids = selections[(situation.number, category.id)]
            if len(recipe_ids) != 3:
                raise ValueError(f"Seleção diferente de três opções: {situation.number}/{category.id}")
            for slot, recipe_id in enumerate(recipe_ids):
                recipe = RECIPE_BY_ID[recipe_id]
                if recipe.category != category.id:
                    raise ValueError(f"Receita em categoria incorreta: {recipe.id}/{category.id}")
                if not category_matches(recipe, situation):
                    raise ValueError(f"Receita incompativel: {situation.number}/{category.id}/{recipe.id}")
                used.add(recipe_id)
                micro = contextual_micro(situation, recipe, category_index, slot)
                if len(wrap_text(micro, "QBDSans", 8.7, 314)) > 2:
                    raise ValueError(f"Microfrase excede duas linhas: {situation.number}/{category.id}/{recipe.id}")
                micros.append(pt_text(micro))
                legacy_micros.append(pt_text(v21_contextual_micro(situation, recipe, category_index, slot)))
                make_ahead = is_make_ahead(recipe)
                style_counter = make_ahead_style_usage if make_ahead else regular_style_usage
                style_index = microcopy_style_index(situation, category_index, slot, make_ahead=make_ahead)
                style_counter[style_index] += 1
                if (
                    make_ahead and style_index in DELIVERY_REVISED_MAKE_AHEAD_STYLE_INDEXES
                ) or (
                    not make_ahead and style_index in DELIVERY_REVISED_REGULAR_STYLE_INDEXES
                ):
                    delivery_microcopy_corrections += 1
    if used != set(RECIPE_BY_ID):
        raise ValueError(f"Receitas sem uso no fluxo: {sorted(set(RECIPE_BY_ID) - used)}")

    for recipe in RECIPES:
        joined = " ".join((*recipe.ingredients, *recipe.steps, recipe.tip)).lower()
        if recipe.category == "chocolate_zero" and "chocolate zero acucar" not in joined:
            raise ValueError(f"Receita de chocolate zero sem ingrediente explicito: {recipe.id}")
        if recipe.category == "brigadeiro_fit" and ("leite condensado" in joined or "manteiga" in joined):
            raise ValueError(f"Brigadeiro fit usa base convencional: {recipe.id}")
        if recipe.category == "proteicas" and not any(
            marker in joined
            for marker in ("proteina em po", "maior teor proteico", "ovo", "cottage")
        ):
            raise ValueError(f"Receita proteica sem fonte coerente: {recipe.id}")
        if recipe.category == "sem_acucar":
            forbidden = ("açucar a gosto", "acucar a gosto", "mel", "leite condensado", "doce de leite")
            if any(re.search(rf"\b{re.escape(term)}\b", joined) for term in forbidden):
                raise ValueError(f"Receita sem acucar com ingrediente incompativel: {recipe.id}")
        prohibited = ("emagrece", "nao engorda", "zero calorias", "perda de peso", "derrete gordura")
        if any(term in joined for term in prohibited):
            raise ValueError(f"Claim proibido em receita: {recipe.id}")
        if is_make_ahead(recipe) and not ("preparo" in recipe.time or "para servir" in recipe.time):
            raise ValueError(f"Tempo antecipado pouco claro: {recipe.id}/{recipe.time}")

    robotic_fragments = (
        "cabe em esse",
        "para não improvisar em esse",
        "para nao improvisar em esse",
        "momento é esse",
        "momento e esse",
        "quando o momento",
        "mantém a escolha simples",
        "completa o momento",
        "responde bem",
        "ganha textura",
        "com preparo antecipado, esta opção fica pronta",
        "neste recorte",
        "uma escolha para uma escolha",
        "uma receita para deixar pronta e usar em",
        "a vontade ficou específica; por isso",
        "o momento já está claro. falta escolher",
    )
    for micro in micros:
        lowered = micro.lower()
        if any(fragment in lowered for fragment in robotic_fragments):
            raise ValueError(f"Microfrase robótica encontrada: {micro}")
        if "�" in micro:
            raise ValueError(f"Caractere inválido em microfrase: {micro}")

    unique_ratio = len(set(micros)) / len(micros)
    if unique_ratio < 0.72:
        raise ValueError(f"Microcopy repetitiva: taxa unica={unique_ratio:.3f}")
    rewritten_count = sum(current != previous for current, previous in zip(micros, legacy_micros, strict=True))
    if rewritten_count != 666:
        raise ValueError(f"Nem todas as microfrases foram reescritas: {rewritten_count}/666")
    exact_repetitions = Counter(micros)
    max_identical = max(exact_repetitions.values())
    if max_identical > 4:
        raise ValueError(f"Microfrase idêntica repetida em excesso: {max_identical} ocorrências")
    max_regular_style = max(regular_style_usage.values())
    max_make_ahead_style = max(make_ahead_style_usage.values())
    if max_regular_style > 20 or max_make_ahead_style > 12:
        raise ValueError(
            f"Estrutura-base repetida em excesso: regular={max_regular_style}, antecipada={max_make_ahead_style}"
        )
    healthy_no_dishes = selections[(26, "saudaveis")]
    if "rs02" in healthy_no_dishes or "rs04" not in healthy_no_dishes:
        raise ValueError(f"Correção da situação sem louça não aplicada: {healthy_no_dishes}")
    no_prep_low_carb = selections[(6, "low_carb")]
    if "lc01" in no_prep_low_carb or "lc04" not in no_prep_low_carb:
        raise ValueError(f"Correção da sobremesa sem preparo não aplicada: {no_prep_low_carb}")
    for (situation_number, category_id, recipe_id), expected_micro in FINAL_V2_MICROCOPY_OVERRIDES.items():
        situation = next(item for item in SITUATIONS if item.number == situation_number)
        category_index = next(index for index, item in enumerate(CATEGORIES) if item.id == category_id)
        recipe_ids = selections[(situation_number, category_id)]
        if recipe_id not in recipe_ids:
            raise ValueError(f"Card da microfrase final não encontrado: {situation_number}/{category_id}/{recipe_id}")
        slot = recipe_ids.index(recipe_id)
        actual_micro = contextual_micro(situation, RECIPE_BY_ID[recipe_id], category_index, slot)
        if actual_micro != expected_micro:
            raise ValueError(f"Microfrase final divergente: {situation_number}/{category_id}/{recipe_id}")
    chocolate_creamy_intro = pt_text(next(item for item in SITUATIONS if item.number == 18).intro)
    texture_creamy_intro = pt_text(next(item for item in SITUATIONS if item.number == 28).intro)
    if not chocolate_creamy_intro.startswith("O sabor está claro"):
        raise ValueError(f"Maiúscula inicial não corrigida: {chocolate_creamy_intro}")
    if not texture_creamy_intro.startswith("A textura está definida"):
        raise ValueError(f"Maiúscula inicial não corrigida: {texture_creamy_intro}")
    return {
        "situations": len(SITUATIONS),
        "categories": len(CATEGORIES),
        "combinations": len(selections),
        "unique_recipes": len(RECIPES),
        "recipe_occurrences": sum(len(ids) for ids in selections.values()),
        "microcopy_unique_ratio": round(unique_ratio, 4),
        "microcopy_rewritten": rewritten_count,
        "max_identical_microcopy": max_identical,
        "max_regular_style_usage": max_regular_style,
        "max_make_ahead_style_usage": max_make_ahead_style,
        "delivery_association_corrections": 1,
        "delivery_microcopy_corrections": delivery_microcopy_corrections,
        "final_v2_card_substitutions": len(FINAL_V2_SELECTION_OVERRIDES),
        "final_v2_microcopy_corrections": len(FINAL_V2_MICROCOPY_OVERRIDES),
        "final_v2_case_corrections": 2,
        "association_substitutions": len(SELECTION_SUBSTITUTIONS),
        "substitutions": list(SELECTION_SUBSTITUTIONS),
    }


def _resolve(obj):
    return obj.get_object() if isinstance(obj, IndirectObject) else obj


def validate_pdf(path: Path) -> dict[str, object]:
    reader = PdfReader(str(path))
    if len(reader.pages) != 325:
        raise ValueError(f"PDF reaberto com {len(reader.pages)} paginas; esperado 325")

    named = reader.named_destinations
    expected_pages = expected_page_by_name()
    if len(expected_pages) != 325 or set(expected_pages.values()) != set(range(325)):
        raise ValueError("Mapa interno de paginas incompleto ou duplicado")
    if set(named) != set(expected_pages):
        raise ValueError(
            f"Named destinations divergentes: faltando={sorted(set(expected_pages) - set(named))[:5]}, "
            f"extras={sorted(set(named) - set(expected_pages))[:5]}"
        )
    for name, expected_page in expected_pages.items():
        actual_page = reader.get_destination_page_number(named[name])
        if actual_page != expected_page:
            raise ValueError(f"Named destination incorreto: {name} -> {actual_page + 1}, esperado {expected_page + 1}")

    page_ref_to_index: dict[int, int] = {}
    for index, page in enumerate(reader.pages):
        if page.indirect_reference:
            page_ref_to_index[page.indirect_reference.idnum] = index

    link_count = 0
    goto_link_count = 0
    invalid_links: list[str] = []
    non_link_annotations: list[str] = []
    duplicate_links: list[str] = []
    external_or_script_actions: list[str] = []
    link_report: list[dict[str, object]] = []
    linked_recipes: set[str] = set()
    linked_page_indices: set[int] = set()
    recipe_id_by_page = {
        expected_pages[f"recipe_{recipe.id}"]: recipe.id
        for recipe in RECIPES
    }
    blank_pages: list[int] = []
    font_names: set[str] = set()
    embedded_font_names: set[str] = set()
    page_texts: list[str] = []

    for page_index, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        if abs(width - PAGE_W) > 0.1 or abs(height - PAGE_H) > 0.1:
            raise ValueError(f"Tamanho de pagina inesperado na pagina {page_index + 1}: {width}x{height}")
        page_text = page.extract_text() or ""
        page_texts.append(page_text)
        if not page_text.strip():
            blank_pages.append(page_index + 1)

        resources = _resolve(page.get("/Resources", {}))
        fonts = _resolve(resources.get("/Font", {})) if resources else {}
        for font_ref in fonts.values():
            font = _resolve(font_ref)
            base_name = str(font.get("/BaseFont", ""))
            font_names.add(base_name)
            descriptor = font.get("/FontDescriptor")
            if descriptor:
                descriptor = _resolve(descriptor)
                if any(descriptor.get(key) is not None for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                    embedded_font_names.add(base_name)

        annotations = page.get("/Annots", [])
        seen_rectangles: set[tuple[float, float, float, float]] = set()
        for annotation_ref in annotations:
            annotation = _resolve(annotation_ref)
            if annotation.get("/Subtype") != "/Link":
                non_link_annotations.append(f"pagina {page_index + 1}: {annotation.get('/Subtype')}")
                continue
            link_count += 1
            rect = annotation.get("/Rect")
            if not rect or len(rect) != 4:
                invalid_links.append(f"pagina {page_index + 1}: retangulo ausente")
                continue
            x1, y1, x2, y2 = map(float, rect)
            if x2 <= x1 or y2 <= y1 or x1 < -0.1 or y1 < -0.1 or x2 > width + 0.1 or y2 > height + 0.1:
                invalid_links.append(f"pagina {page_index + 1}: retangulo invalido {rect}")
            rect_key = tuple(round(value, 2) for value in (x1, y1, x2, y2))
            if rect_key in seen_rectangles:
                duplicate_links.append(f"pagina {page_index + 1}: {rect_key}")
            seen_rectangles.add(rect_key)

            if annotation.get("/Dest") is not None:
                invalid_links.append(f"pagina {page_index + 1}: /Dest direto permaneceu após hardening")
            action = annotation.get("/A")
            if not action:
                invalid_links.append(f"pagina {page_index + 1}: ação /GoTo ausente")
                continue
            action = _resolve(action)
            action_type = str(action.get("/S", ""))
            if action_type != "/GoTo":
                external_or_script_actions.append(f"pagina {page_index + 1}: {action_type}")
                continue
            goto_link_count += 1
            destination = _resolve(action.get("/D"))
            if destination is None:
                invalid_links.append(f"pagina {page_index + 1}: destino ausente")
                continue
            if isinstance(destination, (NameObject, TextStringObject, str)):
                name = str(destination).lstrip("/")
                if name not in named:
                    invalid_links.append(f"pagina {page_index + 1}: destino nomeado inexistente {name}")
                else:
                    target_page = reader.get_destination_page_number(named[name])
                    linked_page_indices.add(target_page)
                    if target_page in recipe_id_by_page:
                        linked_recipes.add(recipe_id_by_page[target_page])
                    link_report.append(
                        {
                            "source_page": page_index + 1,
                            "destination": name,
                            "target_page": target_page + 1,
                            "rect": list(rect_key),
                        }
                    )
                if name.startswith("recipe_"):
                    linked_recipes.add(name.removeprefix("recipe_"))
            else:
                invalid_links.append(f"pagina {page_index + 1}: tipo de destino desconhecido {type(destination)}")

    if blank_pages:
        raise ValueError(f"Paginas sem texto: {blank_pages}")
    if non_link_annotations:
        raise ValueError(f"Anotações não-Link encontradas: {non_link_annotations[:10]}")
    if invalid_links:
        raise ValueError(f"Links invalidos: {invalid_links[:10]}")
    if duplicate_links:
        raise ValueError(f"Anotações duplicadas ou conflitantes: {duplicate_links[:10]}")
    if external_or_script_actions:
        raise ValueError(f"Acoes externas ou scripts encontrados: {external_or_script_actions[:10]}")
    if link_count != 1615 or goto_link_count != link_count or len(link_report) != link_count:
        raise ValueError(
            f"Contagem de navegação inesperada: links={link_count}, /GoTo={goto_link_count}, relatório={len(link_report)}"
        )
    missing_link_targets = set(range(325)) - linked_page_indices
    if missing_link_targets:
        raise ValueError(f"Paginas sem caminho de navegacao: {[index + 1 for index in sorted(missing_link_targets)[:10]]}")
    if len(linked_recipes) != 60:
        raise ValueError(f"Somente {len(linked_recipes)} receitas possuem link de entrada")
    if not any("Georgia" in name for name in font_names) or not any("Arial" in name for name in font_names):
        raise ValueError(f"Fontes do projeto nao encontradas: {sorted(font_names)}")
    if not any("Georgia" in name for name in embedded_font_names) or not any("Arial" in name for name in embedded_font_names):
        raise ValueError(f"Fontes nao incorporadas: {sorted(embedded_font_names)}")

    full_text = "\n".join(page_texts)
    if "�" in full_text:
        raise ValueError("O PDF contém caractere de substituição inválido")
    if re.search(r"\b(?:app|aplicativo)\b", full_text, flags=re.IGNORECASE):
        raise ValueError("O PDF apresenta o produto como aplicativo")
    fallback_page_references = len(re.findall(r"\bpág\.\s*\d+\b", full_text, flags=re.IGNORECASE))
    fallback_page_references += len(re.findall(r"\bp\.\s*\d+\b", full_text, flags=re.IGNORECASE))
    if fallback_page_references != link_count:
        raise ValueError(
            f"Fallbacks de página divergentes: referências={fallback_page_references}, links={link_count}"
        )
    language_patterns = (
        r"\bdà\b",
        r"\bfim dà tarde\b",
        r"\bnão e\b",
        r";\s*e de chocolate\b",
        r"\bvontadé\b",
        r"\bquenté\b",
        r"\bà noite (?:chegou|pede)\b",
        r"\besta claro\b",
        r"\besta definida\b",
        r"\bainda esta\b",
        r"\bvocê esta\b",
        r"\balmoco\b",
        r"\bcomecar\b",
        r"\bcomeco\b",
        r"\bdecisao\b",
        r"\bfogao\b",
        r"\bsofa\b",
        r"\bculinari[oa]\b",
        r"\bobrigatori[oa]\b",
        r"\breferencia(?:s)?\b",
        r"\bfaceis\b",
        r"\bpraticas\b",
        r"\bantecedencia\b",
        r"\bintolerancias\b",
        r"\blaminas\b",
        r"\bopcoes\b",
        r"\bpreparacao\b",
        r"\bsituacoes\b",
        r"\bvoce\b",
        r"\bja\b",
        r"\bnao\b",
        r"\bTres\b",
    )
    language_issues = [pattern for pattern in language_patterns if re.search(pattern, full_text, flags=re.IGNORECASE)]
    if language_issues:
        raise ValueError(f"Ortografia sem acento detectada no PDF: {language_issues}")
    concordance_patterns = (
        r"\bfrutas\b[^\n.!?]{0,100}\b(?:combina|resolve|chega|ganha|define)\b",
        r"\buvas\b[^\n.!?]{0,100}\b(?:combina|resolve|chega|ganha|define)\b",
        r"\bpanquequinhas\b[^\n.!?]{0,100}\b(?:combina|resolve|chega|ganha|define)\b",
        r"\bpedaços\b[^\n.!?]{0,100}\b(?:combina|resolve|chega|ganha|define)\b",
        r"\bmordidas\b[^\n.!?]{0,100}\b(?:combina|resolve|chega|ganha|define)\b",
    )
    concordance_issues = [
        pattern for pattern in concordance_patterns if re.search(pattern, full_text, flags=re.IGNORECASE)
    ]
    if concordance_issues:
        raise ValueError(f"Concordância suspeita detectada no PDF: {concordance_issues}")
    robotic_patterns = (
        "Cabe em esse",
        "Para não improvisar em esse",
        "Para nao improvisar em esse",
        "momento é esse",
        "mantém a escolha simples",
        "completa o momento",
        "responde bem",
        "ganha textura",
        "com preparo antecipado, esta opção fica pronta",
        "neste recorte",
        "uma escolha para uma escolha",
        "uma receita para deixar pronta e usar em",
        "a vontade ficou específica; por isso",
        "o momento já está claro. falta escolher",
    )
    robotic_issues = [fragment for fragment in robotic_patterns if fragment.lower() in full_text.lower()]
    if robotic_issues:
        raise ValueError(f"Microcopy robótica detectada no PDF: {robotic_issues}")

    sample_destinations = (
        "home",
        "situations",
        "situation_01",
        "category_01_proteicas",
        "recipe_pt01",
        "situation_12",
        "situation_17",
        "situation_24",
        "category_01_low_carb",
        "category_01_brigadeiro_fit",
        "category_01_sem_acucar",
        "category_01_chocolate_zero",
        "category_01_saudaveis",
        "sources",
        "notice",
    )
    samples = {name: expected_pages[name] + 1 for name in sample_destinations}
    return {
        "pages": len(reader.pages),
        "named_destinations": len(named),
        "internal_page_targets": len(linked_page_indices),
        "links_validated": link_count,
        "goto_links_validated": goto_link_count,
        "fallback_page_references": fallback_page_references,
        "link_report_entries": len(link_report),
        "linked_unique_recipes": len(linked_recipes),
        "fonts_seen": sorted(font_names),
        "embedded_fonts": sorted(embedded_font_names),
        "sample_pages": samples,
        "file_bytes": path.stat().st_size,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera o guia mobile definitivo Quando Bate o Doce.")
    parser.add_argument("--qa-only", action="store_true", help="Reabre e valida o PDF existente sem gerar novamente.")
    args = parser.parse_args()

    register_fonts()
    selections = build_selection_map()
    content_qa = validate_content(selections)
    if args.qa_only:
        if not OUTPUT.exists():
            raise FileNotFoundError(OUTPUT)
        pdf_qa = validate_pdf(OUTPUT)
        print(json.dumps({"content": content_qa, "pdf": pdf_qa}, ensure_ascii=False, indent=2))
        return

    TMP.mkdir(parents=True, exist_ok=True)
    try:
        raw_pdf = TMP / "qbd-definitivo-raw.pdf"
        builder = GuideBuilder(raw_pdf, selections)
        build_summary = builder.build()
        navigation_summary = harden_internal_navigation(raw_pdf, OUTPUT)
        pdf_qa = validate_pdf(OUTPUT)
        print(
            json.dumps(
                {
                    "content": content_qa,
                    "build": build_summary,
                    "navigation": navigation_summary,
                    "pdf": pdf_qa,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        if TMP.exists():
            shutil.rmtree(TMP)


if __name__ == "__main__":
    main()
