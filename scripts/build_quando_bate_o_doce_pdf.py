from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = Path.home() / "Downloads" / "Guia Situacional - Quando Bate o Doce.pdf"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "pdf" / "Guia Situacional - Quando Bate o Doce.pdf"

PAGE_W, PAGE_H = A5
MARGIN = 28

IVORY = HexColor("#F7F0E6")
PAPER = HexColor("#FFFBF5")
PAPER_ALT = HexColor("#F0E3D4")
ESPRESSO = HexColor("#2F211D")
COCOA = HexColor("#54342D")
COCOA_DEEP = HexColor("#221512")
CHERRY = HexColor("#A64F59")
CARAMEL = HexColor("#C98F58")
SAGE = HexColor("#94A486")
ROSE = HexColor("#D5A09A")
MUTED = HexColor("#75665F")
LINE = HexColor("#D8C9B9")
WHITE = HexColor("#FFFFFF")


@dataclass
class Option:
    title: str
    ingredients: str
    instructions: str


@dataclass
class Situation:
    number: int
    page: int
    category: str
    title: str
    context: str
    filters: list[str]
    options: list[Option]
    logic: str


CATEGORY_COLORS = {
    "DEPOIS DA REFEIÇÃO": CHERRY,
    "FIM DA TARDE": CARAMEL,
    "NOITE": HexColor("#76566F"),
    "CHOCOLATE": COCOA,
    "POUCO TEMPO": SAGE,
    "TEXTURA E TEMPERATURA": ROSE,
    "O QUE TEM EM CASA": HexColor("#A47961"),
}


SOURCE_URLS = [
    "https://www.gov.br/saude/pt-br/assuntos/saude-brasil/publicacoes-para-promocao-a-saude/guia_alimentar_populacao_brasileira_2ed.pdf/view",
    "https://www.who.int/news-room/fact-sheets/detail/healthy-diet",
    "https://www.gov.br/anvisa/pt-br/centraisdeconteudo/publicacoes/alimentos/manuais-guias-e-orientacoes/cartilha-boas-praticas-para-servicos-de-alimentacao.pdf/view",
    "https://pubmed.ncbi.nlm.nih.gov/27721012/",
    "https://pubmed.ncbi.nlm.nih.gov/29407747/",
]


def register_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    font_files = {
        "Georgia": "georgia.ttf",
        "Georgia-Bold": "georgiab.ttf",
        "Segoe": "segoeui.ttf",
        "Segoe-Semibold": "seguisb.ttf",
        "Segoe-Bold": "segoeuib.ttf",
    }
    for name, filename in font_files.items():
        pdfmetrics.registerFont(TTFont(name, str(fonts / filename)))


def clean_lines(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip()]


def parse_situation(page_text: str, page_number: int) -> Situation:
    lines = clean_lines(page_text)
    category = lines[1]
    label_index = next(i for i, line in enumerate(lines) if line.startswith("SITUAÇÃO "))
    context_index = lines.index("A SITUAÇÃO")
    moment_index = lines.index("O que importa neste momento")
    options_index = lines.index("Opções já filtradas")
    logic_index = lines.index("SALVE ESTA LÓGICA")

    number = int(re.search(r"\d+", lines[label_index]).group())
    title = " ".join(lines[label_index + 1 : context_index])
    context = " ".join(lines[context_index + 1 : moment_index])
    filters = lines[moment_index + 1 : options_index]

    option_lines = lines[options_index + 1 : logic_index]
    options: list[Option] = []
    cursor = 0
    for expected in ("1", "2", "3"):
        if option_lines[cursor] != expected:
            raise ValueError(f"Página {page_number}: opção {expected} não encontrada")
        cursor += 1
        use_index = option_lines.index("VOCÊ USA", cursor)
        option_title = " ".join(option_lines[cursor:use_index])
        make_index = option_lines.index("COMO FAZER", use_index + 1)
        ingredients = " ".join(option_lines[use_index + 1 : make_index])
        next_markers = [
            i
            for i in range(make_index + 1, len(option_lines))
            if option_lines[i] in {"1", "2", "3"}
        ]
        end_index = next_markers[0] if next_markers else len(option_lines)
        instructions = " ".join(option_lines[make_index + 1 : end_index])
        options.append(Option(option_title, ingredients, instructions))
        cursor = end_index

    footer_index = next(
        i
        for i in range(logic_index + 1, len(lines))
        if lines[i] == str(page_number)
    )
    logic = " ".join(lines[logic_index + 1 : footer_index])
    return Situation(number, page_number, category, title, context, filters, options, logic)


def extract_situations(source: Path) -> list[Situation]:
    reader = PdfReader(str(source))
    if len(reader.pages) != 48:
        raise ValueError(f"O PDF-base deveria ter 48 páginas; foram encontradas {len(reader.pages)}")
    situations = [
        parse_situation(reader.pages[page - 1].extract_text() or "", page)
        for page in range(10, 47)
    ]
    if [item.number for item in situations] != list(range(1, 38)):
        raise ValueError("A sequência das 37 situações não foi preservada")
    return situations


def pstyle(
    font: str = "Segoe",
    size: float = 9,
    leading: float | None = None,
    color: Color = ESPRESSO,
    alignment: int = TA_LEFT,
) -> ParagraphStyle:
    return ParagraphStyle(
        "inline",
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.28,
        textColor=color,
        alignment=alignment,
        spaceAfter=0,
        spaceBefore=0,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=True,
    )


def para(
    c: canvas.Canvas,
    text: str,
    x: float,
    top: float,
    width: float,
    font: str = "Segoe",
    size: float = 9,
    leading: float | None = None,
    color: Color = ESPRESSO,
    alignment: int = TA_LEFT,
) -> float:
    safe = html.escape(text).replace("\n", "<br/>")
    paragraph = Paragraph(safe, pstyle(font, size, leading, color, alignment))
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(c, x, top - height)
    return height


def draw_round_rect(
    c: canvas.Canvas,
    x: float,
    y: float,
    width: float,
    height: float,
    radius: float = 10,
    fill: Color = PAPER,
    stroke: Color = LINE,
    stroke_width: float = 0.7,
) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(stroke_width)
    c.roundRect(x, y, width, height, radius, fill=1, stroke=1)


def draw_image_cover(c: canvas.Canvas, image_path: Path, x: float, y: float, width: float, height: float) -> None:
    image = ImageReader(str(image_path))
    source_w, source_h = image.getSize()
    scale = max(width / source_w, height / source_h)
    draw_w, draw_h = source_w * scale, source_h * scale
    draw_x = x + (width - draw_w) / 2
    draw_y = y + (height - draw_h) / 2
    c.saveState()
    clip = c.beginPath()
    clip.rect(x, y, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(image, draw_x, draw_y, draw_w, draw_h, mask="auto")
    c.restoreState()


def draw_header(c: canvas.Canvas, section: str, page: int, accent: Color = CHERRY) -> None:
    c.setFillColor(ESPRESSO)
    c.setFont("Segoe-Bold", 5.8)
    c.drawString(MARGIN, PAGE_H - 22, "QUANDO BATE O DOCE")
    c.setFillColor(accent)
    c.setFont("Segoe-Semibold", 5.8)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 22, section.upper())
    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(MARGIN, PAGE_H - 30, PAGE_W - MARGIN, PAGE_H - 30)


def draw_footer(c: canvas.Canvas, page: int, with_index: bool = True) -> None:
    c.setStrokeColor(LINE)
    c.setLineWidth(0.45)
    c.line(MARGIN, 25, PAGE_W - MARGIN, 25)
    c.setFont("Segoe", 5.8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 13, "QUANDO BATE O DOCE")
    c.drawRightString(PAGE_W - MARGIN, 13, str(page))
    if with_index:
        label = "Índice"
        label_w = pdfmetrics.stringWidth(label, "Segoe-Semibold", 6.2)
        x = (PAGE_W - label_w) / 2
        c.setFont("Segoe-Semibold", 6.2)
        c.setFillColor(COCOA)
        c.drawString(x, 13, label)
        c.linkRect("", "index", (x - 6, 8, x + label_w + 6, 23), relative=0, thickness=0)


def draw_nav_footer(c: canvas.Canvas, situation: Situation) -> None:
    draw_footer(c, situation.page, with_index=True)
    c.setFont("Segoe", 5.4)
    c.setFillColor(MUTED)
    if situation.number > 1:
        c.drawString(MARGIN, 31, "‹ anterior")
        c.linkRect("", f"situation-{situation.number - 1}", (MARGIN - 2, 27, MARGIN + 45, 40), relative=0, thickness=0)
    if situation.number < 37:
        c.drawRightString(PAGE_W - MARGIN, 31, "próxima ›")
        c.linkRect("", f"situation-{situation.number + 1}", (PAGE_W - MARGIN - 48, 27, PAGE_W - MARGIN + 2, 40), relative=0, thickness=0)


def draw_phone_mockup(c: canvas.Canvas, x: float, y: float, width: float, height: float) -> None:
    c.setFillColor(COCOA_DEEP)
    c.roundRect(x, y, width, height, 18, fill=1, stroke=0)
    inset = 7
    c.setFillColor(PAPER)
    c.roundRect(x + inset, y + inset, width - inset * 2, height - inset * 2, 13, fill=1, stroke=0)
    c.setFillColor(COCOA_DEEP)
    c.roundRect(x + width * 0.36, y + height - 10, width * 0.28, 3, 1.5, fill=1, stroke=0)
    c.setFont("Segoe-Bold", 5.4)
    c.setFillColor(ESPRESSO)
    c.drawString(x + 14, y + height - 27, "QUANDO BATE O DOCE")
    para(c, "O que está acontecendo agora?", x + 14, y + height - 38, width - 28, "Georgia-Bold", 8.1, 9.2)
    rows = ["Depois do almoço", "Fim da tarde", "À noite", "Quero chocolate"]
    row_y = y + height - 88
    for index, label in enumerate(rows):
        c.setFillColor(WHITE)
        c.setStrokeColor(LINE)
        c.roundRect(x + 13, row_y - index * 23, width - 26, 18, 5, fill=1, stroke=1)
        c.setFillColor([CHERRY, CARAMEL, COCOA, SAGE][index])
        c.circle(x + 21, row_y + 9 - index * 23, 2.5, fill=1, stroke=0)
        c.setFont("Segoe", 5.3)
        c.setFillColor(ESPRESSO)
        c.drawString(x + 28, row_y + 6.8 - index * 23, label)
    c.setFillColor(COCOA)
    c.roundRect(x + 13, y + 15, width - 26, 19, 6, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Semibold", 5.3)
    c.drawCentredString(x + width / 2, y + 22, "abrir pela situação")


def cover_page(c: canvas.Canvas, hero_image: Path) -> None:
    c.bookmarkPage("cover")
    c.addOutlineEntry("Quando Bate o Doce", "cover", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CHERRY)
    c.roundRect(MARGIN, PAGE_H - 63, 126, 19, 9.5, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 6.2)
    c.drawCentredString(MARGIN + 63, PAGE_H - 56, "GUIA SITUACIONAL DE CONSULTA")
    para(c, "Quando\nBate o Doce", MARGIN, PAGE_H - 82, PAGE_W - 56, "Georgia-Bold", 29, 31, ESPRESSO)
    para(
        c,
        "37 situações organizadas para consultar quando a vontade aparece - sem começar outra busca do zero.",
        MARGIN,
        PAGE_H - 166,
        PAGE_W - 70,
        "Segoe",
        9.2,
        12.2,
        COCOA,
    )

    photo_y, photo_h = 42, 286
    draw_image_cover(c, hero_image, 0, photo_y, PAGE_W, photo_h)
    c.saveState()
    c.setFillAlpha(0.82)
    c.setFillColor(IVORY)
    c.roundRect(22, 70, 220, 75, 13, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(CHERRY)
    c.setFont("Segoe-Bold", 6.1)
    c.drawString(37, 128, "COMECE PELO MOMENTO")
    para(c, "37 situações • consulta rápida • feito para o celular", 37, 117, 178, "Segoe-Semibold", 7.4, 9.8, ESPRESSO)
    para(c, "Situação → contexto → opções → escolha", 37, 92, 178, "Segoe", 6.5, 8.2, MUTED)
    draw_phone_mockup(c, PAGE_W - 138, 61, 108, 196)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 5.8)
    c.drawString(MARGIN, 20, "QUANDO BATE O DOCE")
    c.drawRightString(PAGE_W - MARGIN, 20, "1")
    c.showPage()


def how_to_page(c: canvas.Canvas) -> None:
    c.bookmarkPage("how-to")
    c.addOutlineEntry("Como usar o guia", "how-to", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Como usar", 2)
    para(c, "Comece pelo momento,\nnão pela receita", MARGIN, 530, PAGE_W - 56, "Georgia-Bold", 22, 24.5)
    para(c, "Quando a vontade aparece, o guia funciona como um atalho de decisão. Identifique o que está acontecendo agora e abra a situação correspondente.", MARGIN, 466, PAGE_W - 56, "Segoe", 8.4, 11.2, MUTED)
    steps = [
        ("O que aconteceu?", "Depois do almoço, fim da tarde, noite..."),
        ("O que você quer?", "Chocolate, cremoso, crocante, gelado..."),
        ("Quanto tempo tem?", "2, 5, 10 minutos ou zero preparo."),
        ("Escolha uma opção", "Sem procurar por onde começar."),
    ]
    top = 407
    for index, (title, body) in enumerate(steps, 1):
        y = top - (index - 1) * 69
        draw_round_rect(c, MARGIN, y - 50, PAGE_W - 56, 54, 10, PAPER, LINE)
        c.setFillColor(CHERRY if index == 1 else [CARAMEL, SAGE, COCOA][index - 2])
        c.circle(MARGIN + 22, y - 23, 11, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Segoe-Bold", 7.5)
        c.drawCentredString(MARGIN + 22, y - 25.8, f"{index:02d}")
        c.setFillColor(ESPRESSO)
        c.setFont("Segoe-Semibold", 8.4)
        c.drawString(MARGIN + 45, y - 18, title)
        c.setFillColor(MUTED)
        c.setFont("Segoe", 6.9)
        c.drawString(MARGIN + 45, y - 33, body)
    draw_round_rect(c, MARGIN, 55, PAGE_W - 56, 58, 12, COCOA, COCOA)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 11)
    c.drawString(MARGIN + 15, 90, "A lógica em uma linha")
    c.setFont("Segoe-Semibold", 7.2)
    c.drawString(MARGIN + 15, 70, "SITUAÇÃO  →  CONTEXTO  →  OPÇÕES  →  ESCOLHA")
    draw_footer(c, 2)
    c.showPage()


def why_page(c: canvas.Canvas, coffee_image: Path) -> None:
    c.bookmarkPage("why")
    c.addOutlineEntry("Por que um guia situacional?", "why", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Por que existe", 3)
    para(c, "A vontade é específica.\nA busca também pode ser.", MARGIN, 528, PAGE_W - 56, "Georgia-Bold", 21, 23.5)
    para(c, "Desejos por alimentos podem ser específicos por sabor e contexto. Estudos apontam chocolate entre itens de craving e mostram que estímulos de sobremesa podem continuar capturando atenção mesmo depois de uma refeição [4][5].", MARGIN, 462, PAGE_W - 56, "Segoe", 8, 10.6, MUTED)
    draw_image_cover(c, coffee_image, MARGIN, 269, PAGE_W - 56, 113)
    c.setStrokeColor(WHITE)
    c.setLineWidth(1)
    c.roundRect(MARGIN, 269, PAGE_W - 56, 113, 12, fill=0, stroke=1)
    c.setFillColor(CHERRY)
    c.setFont("Segoe-Bold", 6.3)
    c.drawString(MARGIN, 244, "POR ISSO, O GUIA NÃO COMEÇA POR “RECEITAS”")
    para(c, "Ele começa pelo que está acontecendo agora. Tempo, textura, ingredientes disponíveis e tipo de vontade funcionam como filtros. O objetivo é reduzir a busca, não criar regras.", MARGIN, 229, PAGE_W - 56, "Segoe", 8.1, 10.8, ESPRESSO)
    flow = [("SITUAÇÃO", CHERRY), ("FILTRO", CARAMEL), ("OPÇÕES", SAGE), ("ESCOLHA", COCOA)]
    box_w = 75
    gap = 12
    start_x = (PAGE_W - (box_w * 4 + gap * 3)) / 2
    for index, (label, color) in enumerate(flow):
        x = start_x + index * (box_w + gap)
        c.setFillColor(color)
        c.roundRect(x, 101, box_w, 31, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Segoe-Bold", 6.2)
        c.drawCentredString(x + box_w / 2, 112, label)
        if index < len(flow) - 1:
            c.setStrokeColor(LINE)
            c.setLineWidth(1)
            c.line(x + box_w, 116.5, x + box_w + gap, 116.5)
    para(c, "As referências usadas nesta lógica estão reunidas no fim do guia.", MARGIN, 78, PAGE_W - 56, "Segoe", 6.4, 8.2, MUTED, TA_CENTER)
    draw_footer(c, 3)
    c.showPage()


def map_page(c: canvas.Canvas, situations: list[Situation]) -> None:
    c.bookmarkPage("map")
    c.addOutlineEntry("Mapa rápido", "map", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Atalhos", 4)
    para(c, "O que está acontecendo agora?", MARGIN, 522, PAGE_W - 56, "Georgia-Bold", 21, 24)
    para(c, "Toque em uma situação para ir direto ao ponto do guia.", MARGIN, 475, PAGE_W - 56, "Segoe", 8.3, 10.6, MUTED)
    shortcuts = [
        ("Depois do almoço", 1), ("Fim da tarde", 7),
        ("À noite", 12), ("Quero chocolate", 17),
        ("Tenho 2 minutos", 23), ("Tenho 5 minutos", 24),
        ("Não quero cozinhar", 27), ("Quero cremoso", 28),
        ("Quero crocante", 29), ("Quero gelado", 30),
        ("Poucos ingredientes", 37), ("Ver índice completo", 0),
    ]
    cols = 2
    card_w = (PAGE_W - 56 - 10) / 2
    card_h = 43
    start_y = 422
    for index, (label, target) in enumerate(shortcuts):
        col, row = index % cols, index // cols
        x = MARGIN + col * (card_w + 10)
        y = start_y - row * 52
        fill = PAPER if target else PAPER_ALT
        draw_round_rect(c, x, y, card_w, card_h, 9, fill, LINE)
        c.setFillColor(CHERRY if target else COCOA)
        c.circle(x + 17, y + card_h / 2, 3, fill=1, stroke=0)
        para(c, label, x + 28, y + 27, card_w - 40, "Segoe-Semibold", 7.2, 8.8, ESPRESSO)
        dest = f"situation-{target}" if target else "index"
        c.linkRect("", dest, (x, y, x + card_w, y + card_h), relative=0, thickness=0)
    draw_footer(c, 4)
    c.showPage()


def draw_index_page(c: canvas.Canvas, situations: list[Situation], page: int, title: str) -> None:
    if page == 5:
        c.bookmarkPage("index")
        c.addOutlineEntry("Índice", "index", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Índice", page)
    para(c, title, MARGIN, 524, PAGE_W - 56, "Georgia-Bold", 20, 22.5)
    para(c, "Escolha a situação. O número à direita é a página do PDF.", MARGIN, 482, PAGE_W - 56, "Segoe", 7.8, 10, MUTED)
    rows = situations[:20] if page == 5 else situations[20:]
    top = 449
    row_h = 19.1 if page == 5 else 22.5
    current_category = None
    for item in rows:
        if item.category != current_category:
            current_category = item.category
            c.setFillColor(CATEGORY_COLORS[item.category])
            c.setFont("Segoe-Bold", 5.7)
            c.drawString(MARGIN + 2, top, item.category)
            top -= 12
        y = top - row_h + 3
        if item.number % 2 == 0:
            c.setFillColor(Color(1, 1, 1, alpha=0.38))
            c.rect(MARGIN, y, PAGE_W - 56, row_h, fill=1, stroke=0)
        c.setFillColor(MUTED)
        c.setFont("Segoe-Semibold", 6.5)
        c.drawString(MARGIN + 3, top - 10, f"{item.number:02d}")
        c.setFillColor(ESPRESSO)
        c.setFont("Segoe", 6.7)
        c.drawString(MARGIN + 26, top - 10, item.title)
        c.setFont("Segoe-Semibold", 6.5)
        c.setFillColor(CATEGORY_COLORS[item.category])
        c.drawRightString(PAGE_W - MARGIN - 3, top - 10, str(item.page))
        c.linkRect("", f"situation-{item.number}", (MARGIN, y, PAGE_W - MARGIN, y + row_h), relative=0, thickness=0)
        top -= row_h
    if page == 5:
        c.setFillColor(PAPER_ALT)
        c.roundRect(PAGE_W - MARGIN - 102, 35, 102, 24, 8, fill=1, stroke=0)
        c.setFillColor(COCOA)
        c.setFont("Segoe-Semibold", 6.5)
        c.drawCentredString(PAGE_W - MARGIN - 51, 43.5, "continuar índice  →")
        c.linkRect("", "index-2", (PAGE_W - MARGIN - 102, 35, PAGE_W - MARGIN, 59), relative=0, thickness=0)
    else:
        c.bookmarkPage("index-2")
        c.setFillColor(PAPER_ALT)
        c.roundRect(MARGIN, 43, 91, 24, 8, fill=1, stroke=0)
        c.setFillColor(COCOA)
        c.setFont("Segoe-Semibold", 6.5)
        c.drawCentredString(MARGIN + 45.5, 51.5, "← voltar ao início")
        c.linkRect("", "cover", (MARGIN, 43, MARGIN + 91, 67), relative=0, thickness=0)
    draw_footer(c, page, with_index=False)
    c.showPage()


def pantry_page(c: canvas.Canvas, fruit_image: Path) -> None:
    c.bookmarkPage("pantry")
    c.addOutlineEntry("Lista-base de ingredientes", "pantry", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Lista-base", 7)
    para(c, "Algumas escolhas ficam mais fáceis\nquando algumas bases já estão em casa", MARGIN, 526, PAGE_W - 56, "Georgia-Bold", 18.5, 20.5)
    para(c, "A lista não é obrigatória. Ela reúne ingredientes recorrentes nas 37 situações e permite muitas combinações simples.", MARGIN, 448, 235, "Segoe", 7.3, 9.4, MUTED)
    draw_image_cover(c, fruit_image, PAGE_W - MARGIN - 92, 398, 92, 58)
    c.setStrokeColor(WHITE)
    c.roundRect(PAGE_W - MARGIN - 92, 398, 92, 58, 10, fill=0, stroke=1)
    groups = [
        ("GELADEIRA", ["iogurte natural", "leite", "frutas lavadas", "chocolate porcionado"]),
        ("ARMÁRIO", ["cacau em pó", "aveia ou granola", "canela", "castanhas", "pasta de amendoim", "chocolate"]),
        ("FREEZER", ["banana em rodelas", "uvas", "frutas vermelhas", "1 sobremesa pronta"]),
        ("EXTRAS", ["coco ralado", "geleia", "doce de leite", "baunilha", "biscoito ou torrada"]),
    ]
    card_w = (PAGE_W - 56 - 10) / 2
    card_h = 112
    for index, (title, items) in enumerate(groups):
        col, row = index % 2, index // 2
        x = MARGIN + col * (card_w + 10)
        y = 278 - row * 123
        draw_round_rect(c, x, y, card_w, card_h, 11, PAPER, LINE)
        c.setFillColor(CHERRY if index % 2 == 0 else CARAMEL)
        c.setFont("Segoe-Bold", 6.2)
        c.drawString(x + 13, y + card_h - 19, title)
        item_y = y + card_h - 38
        for item in items:
            c.setFillColor(SAGE if index > 1 else CARAMEL)
            c.circle(x + 16, item_y + 2.2, 2, fill=1, stroke=0)
            c.setFillColor(ESPRESSO)
            c.setFont("Segoe", 6.7)
            c.drawString(x + 24, item_y, item)
            item_y -= 14
    draw_round_rect(c, MARGIN, 55, PAGE_W - 56, 77, 11, HexColor("#DFE5D6"), HexColor("#CAD4BF"))
    c.setFillColor(COCOA)
    c.setFont("Segoe-Bold", 6.1)
    c.drawString(MARGIN + 13, 112, "PREPARO ANTECIPADO QUE GANHA TEMPO")
    para(c, "Se quiser, congele banana em rodelas e uvas já higienizadas. Preparações com leite ou iogurte devem permanecer refrigeradas; a Anvisa orienta manter alimentos frios abaixo de 5 °C e reduzir o tempo fora de refrigeração [3].", MARGIN + 13, 101, PAGE_W - 82, "Segoe", 6.4, 8.2, COCOA)
    c.setFillColor(MUTED)
    c.setFont("Segoe", 5.4)
    c.drawString(MARGIN, 43, "Abreviações: c.s. = colher de sopa • c.chá = colher de chá • xíc. = xícara")
    draw_footer(c, 7)
    c.showPage()


def quick_page(c: canvas.Canvas, coffee_image: Path) -> None:
    c.bookmarkPage("quick")
    c.addOutlineEntry("Doce em 5", "quick", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Doce em 5", 8)
    para(c, "Porque uma opção de 40 minutos não compete com aquilo que já está pronto", MARGIN, 524, 255, "Georgia-Bold", 18, 20.3)
    draw_image_cover(c, coffee_image, PAGE_W - MARGIN - 98, 430, 98, 84)
    c.setStrokeColor(WHITE)
    c.roundRect(PAGE_W - MARGIN - 98, 430, 98, 84, 10, fill=0, stroke=1)
    para(c, "Escolha pelo tempo real que você tem. Os atalhos levam às situações completas.", MARGIN, 440, 240, "Segoe", 7.4, 9.5, MUTED)
    rows = [
        ("2 MINUTOS", CHERRY, ["Chocolate + castanhas", "Iogurte + fruta", "Banana + pasta"], 23),
        ("5 MINUTOS", CARAMEL, ["Maçã quente", "Taça de cacau", "Banana morna"], 24),
        ("10 MINUTOS", SAGE, ["Bolo de caneca", "Mingau de cacau", "Morangos + chocolate"], 25),
    ]
    top = 375
    for label, color, items, target in rows:
        draw_round_rect(c, MARGIN, top - 73, PAGE_W - 56, 67, 11, PAPER, LINE)
        c.setFillColor(color)
        c.roundRect(MARGIN + 10, top - 62, 74, 45, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Segoe-Bold", 6.4)
        c.drawCentredString(MARGIN + 47, top - 42, label)
        item_x = MARGIN + 99
        for index, item in enumerate(items):
            x = item_x + index * 86
            c.setFillColor(ESPRESSO)
            c.setFont("Segoe-Semibold", 6.2)
            para(c, item, x, top - 27, 78, "Segoe-Semibold", 6.2, 7.5, ESPRESSO)
            c.setFillColor(color)
            c.setFont("Segoe", 5.2)
            c.drawString(x, top - 55, "abrir situação  →")
        c.linkRect("", f"situation-{target}", (MARGIN, top - 73, PAGE_W - MARGIN, top - 6), relative=0, thickness=0)
        top -= 82
    draw_round_rect(c, MARGIN, 55, PAGE_W - 56, 70, 11, COCOA, COCOA)
    c.setFillColor(WHITE)
    c.setFont("Georgia-Bold", 11)
    c.drawString(MARGIN + 14, 102, "Regra do Doce em 5")
    para(c, "Primeiro escolha o tempo. Depois escolha o sabor. Se inverter essa ordem, você tende a abrir opções que não cabem no momento.", MARGIN + 14, 88, PAGE_W - 84, "Segoe", 6.8, 8.8, WHITE)
    draw_footer(c, 8)
    c.showPage()


def no_cook_page(c: canvas.Canvas) -> None:
    c.bookmarkPage("no-cook")
    c.addOutlineEntry("Não quero cozinhar", "no-cook", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Zero preparo", 9)
    para(c, "Não quero cozinhar", MARGIN, 524, PAGE_W - 56, "Georgia-Bold", 22, 24)
    para(c, "Esta página existe para um daqueles momentos em que a vontade apareceu, mas a disposição para cozinhar não. Aqui, tudo é montagem.", MARGIN, 474, PAGE_W - 56, "Segoe", 8.2, 10.6, MUTED)
    items = [
        ("Chocolate + fruta", "Escolha a fruta pronta. Acrescente o chocolate que você realmente quer."),
        ("Iogurte + granola", "Abra, misture e coma. Chocolate picado é opcional."),
        ("Banana + pasta de amendoim", "Banana aberta ou fatiada + uma camada fina da pasta."),
        ("Sorvete + fruta", "Uma bola + fruta fresca ou congelada."),
        ("Chocolate + castanhas", "Dois sabores fortes, nenhuma receita."),
        ("Café + doce pequeno", "Se o café faz parte do momento, monte a experiência ao redor dele."),
    ]
    top = 414
    for index, (title, body) in enumerate(items):
        y = top - index * 54
        draw_round_rect(c, MARGIN, y - 43, PAGE_W - 56, 46, 10, PAPER, LINE)
        c.setFillColor([CHERRY, CARAMEL, SAGE][index % 3])
        c.circle(MARGIN + 17, y - 20, 4.2, fill=1, stroke=0)
        c.setFillColor(ESPRESSO)
        c.setFont("Segoe-Semibold", 7.4)
        c.drawString(MARGIN + 31, y - 15, title)
        para(c, body, MARGIN + 31, y - 23, PAGE_W - 105, "Segoe", 6.1, 7.8, MUTED)
    c.setFillColor(PAPER_ALT)
    c.roundRect(MARGIN, 44, PAGE_W - 56, 25, 8, fill=1, stroke=0)
    c.setFillColor(COCOA)
    c.setFont("Segoe-Semibold", 6.3)
    c.drawCentredString(PAGE_W / 2, 53, "ver a situação 27 - Não quero cozinhar  →")
    c.linkRect("", "situation-27", (MARGIN, 44, PAGE_W - MARGIN, 69), relative=0, thickness=0)
    draw_footer(c, 9)
    c.showPage()


def draw_option_card(c: canvas.Canvas, option: Option, number: int, y: float, color: Color) -> None:
    height = 69
    draw_round_rect(c, MARGIN, y, PAGE_W - 56, height, 10, PAPER, LINE)
    c.setFillColor(color)
    c.circle(MARGIN + 16, y + height - 17, 7.3, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 6.3)
    c.drawCentredString(MARGIN + 16, y + height - 19.2, str(number))
    para(c, option.title, MARGIN + 30, y + height - 11, PAGE_W - 101, "Segoe-Semibold", 7.2, 8.4, ESPRESSO)
    label_x = MARGIN + 14
    text_x = MARGIN + 68
    c.setFillColor(MUTED)
    c.setFont("Segoe-Bold", 4.7)
    c.drawString(label_x, y + 33, "VOCÊ USA")
    para(c, option.ingredients, text_x, y + 39, PAGE_W - text_x - MARGIN - 5, "Segoe", 5.7, 6.8, MUTED)
    c.setFillColor(MUTED)
    c.setFont("Segoe-Bold", 4.7)
    c.drawString(label_x, y + 13, "COMO FAZER")
    para(c, option.instructions, text_x, y + 19, PAGE_W - text_x - MARGIN - 5, "Segoe", 5.7, 6.8, MUTED)


def situation_page(c: canvas.Canvas, item: Situation) -> None:
    accent = CATEGORY_COLORS[item.category]
    c.bookmarkPage(f"situation-{item.number}")
    section_starts = {1: ("Depois da refeição", 0), 7: ("Fim da tarde", 0), 12: ("Noite", 0), 17: ("Chocolate", 0), 23: ("Pouco tempo", 0), 28: ("Textura e temperatura", 0), 33: ("O que tem em casa", 0)}
    if item.number in section_starts:
        c.addOutlineEntry(section_starts[item.number][0], f"situation-{item.number}", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, item.category, item.page, accent)
    c.setFillColor(accent)
    c.setFont("Segoe-Bold", 6.2)
    c.drawString(MARGIN, 542, f"SITUAÇÃO {item.number:02d}")
    c.setStrokeColor(accent)
    c.setLineWidth(2.2)
    c.line(MARGIN, 530, MARGIN + 29, 530)
    para(c, item.title, MARGIN, 518, PAGE_W - 56, "Georgia-Bold", 17.3, 19.3, ESPRESSO)
    draw_round_rect(c, MARGIN, 407, PAGE_W - 56, 58, 11, PAPER, LINE)
    c.setFillColor(accent)
    c.setFont("Segoe-Bold", 5.5)
    c.drawString(MARGIN + 13, 449, "A SITUAÇÃO")
    para(c, item.context, MARGIN + 13, 438, PAGE_W - 82, "Segoe", 6.4, 8, ESPRESSO)
    c.setFillColor(MUTED)
    c.setFont("Segoe-Semibold", 5.6)
    c.drawString(MARGIN, 393, "O que importa neste momento")
    x = MARGIN
    for filter_text in item.filters:
        width = min(119, max(82, pdfmetrics.stringWidth(filter_text, "Segoe", 5.2) + 20))
        c.setFillColor(PAPER_ALT)
        c.roundRect(x, 368, width, 18, 9, fill=1, stroke=0)
        c.setFillColor(COCOA)
        c.setFont("Segoe", 5.2)
        c.drawCentredString(x + width / 2, 374.5, filter_text)
        x += width + 6
    c.setFillColor(ESPRESSO)
    c.setFont("Georgia-Bold", 11.8)
    c.drawString(MARGIN, 341, "Opções já filtradas")
    for index, option in enumerate(item.options):
        draw_option_card(c, option, index + 1, 261 - index * 77, [CHERRY, CARAMEL, SAGE][index])
    draw_round_rect(c, MARGIN, 45, PAGE_W - 56, 48, 10, COCOA, COCOA)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 4.9)
    c.drawString(MARGIN + 12, 80, "SALVE ESTA LÓGICA")
    para(c, item.logic, MARGIN + 12, 72, PAGE_W - 80, "Segoe", 5.8, 7.1, WHITE)
    draw_nav_footer(c, item)
    c.showPage()


def sources_page(c: canvas.Canvas) -> None:
    c.bookmarkPage("sources")
    c.addOutlineEntry("Fontes e referências", "sources", level=0)
    c.setFillColor(IVORY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_header(c, "Fontes", 47)
    para(c, "Fontes e referências", MARGIN, 524, PAGE_W - 56, "Georgia-Bold", 22, 24)
    para(c, "As fontes orientaram princípios gerais de alimentação, segurança dos alimentos e desejos alimentares. As combinações culinárias foram formuladas para este material.", MARGIN, 474, PAGE_W - 56, "Segoe", 7.4, 9.6, MUTED)
    references = [
        "Ministério da Saúde - Guia Alimentar para a População Brasileira, 2ª ed. (2014).",
        "World Health Organization - Healthy diet / guidance on free sugars.",
        "ANVISA - Cartilha sobre Boas Práticas para Serviços de Alimentação (RDC 216/2004).",
        "Medeiros ACQ et al. Food cravings among Brazilian population. Appetite. 2017;108:212-218. DOI: 10.1016/j.appet.2016.10.009.",
        "Davidson GR et al. Pre- and postprandial variation in implicit attention to food images reflects appetite and sensory-specific satiety. Appetite. 2018;125:24-31.",
    ]
    top = 420
    card_h = 56
    for index, (reference, url) in enumerate(zip(references, SOURCE_URLS), 1):
        y = top - (index - 1) * 65
        draw_round_rect(c, MARGIN, y - card_h, PAGE_W - 56, card_h, 10, PAPER, LINE)
        c.setFillColor(CHERRY)
        c.circle(MARGIN + 18, y - card_h / 2, 9, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont("Segoe-Bold", 6.3)
        c.drawCentredString(MARGIN + 18, y - card_h / 2 - 2.4, str(index))
        para(c, reference, MARGIN + 38, y - 11, PAGE_W - 105, "Segoe", 6.4, 7.9, MUTED)
        c.setFillColor(COCOA)
        c.setFont("Segoe-Semibold", 5.4)
        c.drawString(MARGIN + 38, y - card_h + 9, "abrir fonte  →")
        c.linkURL(url, (MARGIN, y - card_h, PAGE_W - MARGIN, y), relative=0, thickness=0)
    draw_round_rect(c, MARGIN, 43, PAGE_W - 56, 50, 10, PAPER_ALT, PAPER_ALT)
    para(c, "Como ler as fontes: os marcadores [1]-[5] usados no guia apontam para esta lista. Não é necessário lê-las para usar o produto; elas dão transparência à base do material.", MARGIN + 13, 80, PAGE_W - 82, "Segoe", 5.9, 7.5, MUTED)
    draw_footer(c, 47)
    c.showPage()


def notice_page(c: canvas.Canvas) -> None:
    c.bookmarkPage("notice")
    c.addOutlineEntry("Aviso importante", "notice", level=0)
    c.setFillColor(COCOA_DEEP)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(CHERRY)
    c.roundRect(MARGIN, PAGE_H - 60, 103, 19, 9, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 6.1)
    c.drawCentredString(MARGIN + 51.5, PAGE_H - 53, "AVISO IMPORTANTE")
    para(c, "Este guia ajuda a organizar escolhas.\nEle não substitui orientação profissional.", MARGIN, 492, PAGE_W - 56, "Georgia-Bold", 21, 23.8, WHITE)
    c.setFillColor(HexColor("#382520"))
    c.setStrokeColor(HexColor("#5A3D36"))
    c.setLineWidth(0.8)
    c.roundRect(MARGIN, 145, PAGE_W - 56, 225, 13, fill=1, stroke=1)
    body = [
        "O Quando Bate o Doce é um material educativo e de consulta, criado para ajudar você a encontrar opções culinárias de forma mais rápida e organizada. Ele não realiza diagnóstico, não prescreve dieta e não substitui avaliação individual de nutricionista, médico ou outro profissional de saúde qualificado.",
        "Necessidades alimentares variam conforme idade, condições de saúde, uso de medicamentos, alergias, intolerâncias, gestação, objetivos e contexto individual. Se alguma dessas situações se aplica a você, use este material apenas como referência e siga as orientações do profissional que acompanha seu caso.",
        "Verifique sempre os rótulos dos ingredientes em caso de alergias ou intolerâncias. Em preparações com alimentos perecíveis, siga boas práticas de higiene, conservação e refrigeração.",
    ]
    top = 352
    for paragraph in body:
        height = para(c, paragraph, MARGIN + 15, top, PAGE_W - 86, "Segoe", 7.2, 9.5, WHITE)
        top -= height + 16
    c.setStrokeColor(CHERRY)
    c.setLineWidth(1.6)
    c.line(MARGIN, 128, PAGE_W - MARGIN, 128)
    para(c, "Use o guia para consultar. Use profissionais para decisões individualizadas.", MARGIN, 111, PAGE_W - 56, "Segoe-Semibold", 7, 9, ROSE, TA_CENTER)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 7.1)
    c.drawCentredString(PAGE_W / 2, 47, "QUANDO BATE O DOCE")
    c.setFillColor(ROSE)
    c.circle(PAGE_W / 2, 69, 4, fill=1, stroke=0)
    c.showPage()


def build_pdf(source: Path, output: Path) -> None:
    register_fonts()
    situations = extract_situations(source)
    hero = PROJECT_ROOT / "public" / "hero-chocolate-editorial.png"
    coffee = PROJECT_ROOT / "assets" / "pdf" / "editorial-context-coffee.png"
    fruit = PROJECT_ROOT / "assets" / "pdf" / "editorial-fruit-chocolate.png"
    for required in (hero, coffee, fruit):
        if not required.exists():
            raise FileNotFoundError(required)

    output.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output), pagesize=A5, pageCompression=1)
    c.setTitle("Quando Bate o Doce - Guia Situacional de Consulta")
    c.setAuthor("Quando Bate o Doce")
    c.setSubject("37 situações organizadas para consultar quando a vontade de doce aparece")
    c.setKeywords("doce, guia situacional, chocolate, sobremesa, consulta rápida")

    cover_page(c, hero)
    how_to_page(c)
    why_page(c, coffee)
    map_page(c, situations)
    draw_index_page(c, situations, 5, "Índice clicável")
    draw_index_page(c, situations, 6, "Índice clicável - continuação")
    pantry_page(c, fruit)
    quick_page(c, coffee)
    no_cook_page(c)
    for item in situations:
        situation_page(c, item)
    sources_page(c)
    notice_page(c)
    c.save()


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconstrói o guia Quando Bate o Doce com layout editorial premium.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    build_pdf(args.source.resolve(), args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
