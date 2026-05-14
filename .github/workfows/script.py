import requests
from bs4 import BeautifulSoup
import os

LEIS = [
    {
        "arquivo": "resolucao-6000/index.html",
        "titulo": "Resolução DG/ANTT nº 6.000, de 2022",
        "url": (
            "https://anttlegis.antt.gov.br/action/UrlPublicasAction.php"
            "?acao=abrirAtoPublico&num_ato=00006000&sgl_tipo=RES"
            "&sgl_orgao=DG/ANTT/MI&vlr_ano=2022&seq_ato=000"
            "&cod_modulo=161&cod_menu=5408"
        ),
    },
    # Adicione mais leis aqui no mesmo formato
]

TEMPLATE = """<!DOCTYPE html>
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
  <p class="aviso">Conteúdo reproduzido do Sistema ANTT Legis.
  Em caso de divergência, prevalece a publicação oficial.</p>
</body>
</html>"""

headers = {"User-Agent": "Mozilla/5.0"}

for lei in LEIS:
    print(f"Extraindo: {lei['titulo']}")
    try:
        r = requests.get(lei["url"], headers=headers, timeout=30, verify=False)
        soup = BeautifulSoup(r.text, "lxml")
        conteudo = soup.find(id="conteudo")

        if not conteudo:
            print("  ⚠ Elemento #conteudo não encontrado")
            conteudo = "<p><em>Conteúdo não localizado.</em></p>"
        else:
            conteudo = str(conteudo)

        html = TEMPLATE.format(titulo=lei["titulo"], conteudo=conteudo)

        os.makedirs(os.path.dirname(lei["arquivo"]), exist_ok=True)
        with open(lei["arquivo"], "w", encoding="utf-8") as f:
            f.write(html)

        print(f"  ✓ Salvo em {lei['arquivo']}")

    except Exception as e:
        print(f"  ✗ Erro: {e}")
