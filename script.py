import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta

LEIS = [
    {
        "pasta": "RCR1",
        "titulo": "RCR1",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00005950&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MI&vlr_ano=2021&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
     {
        "pasta": "RCR2",
        "titulo": "RCR2",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00006000&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MI&vlr_ano=2022&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
     {
        "pasta": "RCR3",
        "titulo": "RCR3",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00006032&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MT&vlr_ano=2023&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
     {
        "pasta": "RCR4",
        "titulo": "RCR4",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00006053&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MT&vlr_ano=2024&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
     {
        "pasta": "RCR5",
        "titulo": "RCR5",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00006063&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MT&vlr_ano=2025&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
    # Adicione mais leis aqui, exemplo:
    # {
    #     "pasta": "resolucao-6063",
    #     "titulo": "Resolução DG/ANTT nº 6.063, de 2025",
    #     "url": "https://anttlegis.antt.gov.br/action/...",
    # },
]

REPO = "normas-ANTT"

TEMPLATE_LEI = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="robots" content="index, follow">
  <title>{titulo}</title>
  <style>
    body {{ font-family: Arial, sans-serif; line-height: 1.6;
            max-width: 900px; margin: 40px auto; color: #111; padding: 0 20px; }}
    hr {{ margin: 24px 0; }}
    p.aviso {{ font-size: 0.85em; color: #555; }}
  </style>
</head>
<body>
  <h1>{titulo}</h1>
  <p><strong>Fonte:</strong> Sistema ANTT Legis</p>
  <hr>
  {conteudo}
  <hr>
  <p class="aviso">Conteudo reproduzido do Sistema ANTT Legis.
  Em caso de divergencia, prevalece a publicacao oficial.</p>
</body>
</html>"""

TEMPLATE_INDEX = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>ANTT - Atos Normativos</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px;
           margin: 40px auto; color: #111; padding: 0 20px; }}
    a {{ color: #1a0dab; }}
  </style>
</head>
<body>
  <h1>ANTT — Atos Normativos</h1>
  <p>Repositorio de consulta de atos normativos da ANTT.</p>
  <ul>
{links}
  </ul>
  <hr>
  <p><small>Ultima atualizacao: {atualizado} — via GitHub Actions.</small></p>
</body>
</html>"""

headers = {"User-Agent": "Mozilla/5.0"}
links = []

fuso_br = timezone(timedelta(hours=-3))
agora = datetime.now(fuso_br).strftime("%d/%m/%Y às %H:%M (Brasília)")

for lei in LEIS:
    print(f"Extraindo: {lei['titulo']}")
    try:
        r = requests.get(lei["url"], headers=headers, timeout=60, verify=False)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "lxml")
        conteudo = soup.find(id="conteudo")

        if not conteudo:
            print("  ⚠ #conteudo nao encontrado, usando body")
            conteudo = soup.find("body")

        if conteudo:
            for tag in conteudo.find_all(["script", "nav", "header", "footer"]):
                tag.decompose()
            conteudo = str(conteudo)
        else:
            conteudo = "<p><em>Conteudo nao localizado.</em></p>"

        html = TEMPLATE_LEI.format(titulo=lei["titulo"], conteudo=conteudo, atualizado=agora)

        pasta = lei["pasta"]
        os.makedirs(pasta, exist_ok=True)
        with open(f"{pasta}/index.html", "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ Salvo em {pasta}/index.html")

        # Adiciona link para o index
        links.append(
            f'    <li><a href="/{REPO}/{pasta}">{lei["titulo"]}</a></li>'
        )

    except Exception as e:
        print(f"  ✗ Erro: {e}")

# Gera index.html automaticamente
index_html = TEMPLATE_INDEX.format(links="\n".join(links))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✓ index.html atualizado")
