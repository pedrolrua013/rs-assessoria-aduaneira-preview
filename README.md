# Site RS Assessoria Aduaneira

Site estático (HTML/CSS/JS puros, sem dependências).

## Estrutura
- `index.html` e uma pasta por serviço (`despacho-de-importacao/`, `despacho-de-exportacao/`, `drawback/`, `logistica-internacional/`, `brokeragem-de-embarques/`, `comercio-exterior-agronegocio/`), `politica-de-privacidade/`, `404.html`
- `assets/` — `site.css`, `site.js`, fonte, logos, `og.jpg`
- `_tools/build_pages.py` — gera todas as páginas, `sitemap.xml`, `robots.txt` e `vercel.json`. Edite os textos lá e rode `python _tools/build_pages.py`.
- `_tools/preview.py` — gera uma cópia com caminhos relativos para abrir sem servidor.
- `briefing.md` — fontes, decisões e pendências.

## Publicar na Vercel
Na pasta do projeto: `npx vercel --prod` (ou suba para um repositório GitHub e importe em vercel.com/new).
O `vercel.json` já gera as páginas no build (`OUT=public python3 _tools/build_pages.py`) e aplica headers de segurança e redirecionamentos das URLs do site antigo.

Ao conectar o domínio próprio, troque `SITE` no topo de `_tools/build_pages.py` e publique de novo (atualiza canonical, sitemap, OG e schema).

## Pendências
Ver `briefing.md` → "Decisões e inferências".
