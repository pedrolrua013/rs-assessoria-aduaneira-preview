#!/usr/bin/env python3
"""Gera todas as páginas do site da RS Assessoria Aduaneira.
Uso: python3 _tools/build_pages.py  (na raiz do projeto)
"""
import json, hashlib, base64, os, html, datetime, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from blog_posts import POSTS
import thumbs

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://rsassessoriaaduaneira.vercel.app"  # trocar ao conectar o domínio próprio
TODAY = datetime.date.today().isoformat()
WA_NUM = "5513996140042"
TEL1, TEL1_H = "+551332198720", "(13) 3219-8720"
TEL2, TEL2_H = "+551332244333", "(13) 3224-4333"
WA_H = "(13) 99614-0042"
EMAIL = "contatosite@rsassessoriaaduaneira.com.br"
CNPJ = "02.347.994/0001-42"
ADDR = "Av. Ana Costa, 146 – conj. 702/703"
BAIRRO = "Vila Belmiro"
CEP = "11060-000"
MAPS = "https://www.google.com/maps/search/?api=1&query=RS+Assessoria+Aduaneira+Av.+Ana+Costa+146+Santos"
MAP_EMBED = "https://www.google.com/maps?q=Av.+Ana+Costa,+146,+Santos+-+SP,+11060-000&output=embed"
IG = "https://www.instagram.com/rsaduaneira/"
FB = "https://www.facebook.com/RSAssessoriaAduaneira/"
LI = "https://www.linkedin.com/company/rs-assessoria-aduaneira"

def wa(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text=" + quote(msg)

# ---------------- ícones ----------------
I = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>',
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "import": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17h18l-2 3H5l-2-3z"/><path d="M5 17V9h6v8M11 12h6v5"/><path d="M14 3v6m0 0l-2.5-2.5M14 9l2.5-2.5"/></svg>',
 "export": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17h18l-2 3H5l-2-3z"/><path d="M5 17V9h6v8M11 12h6v5"/><path d="M14 9V3m0 0l-2.5 2.5M14 3l2.5 2.5"/></svg>',
 "drawback": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h11a4 4 0 0 1 0 8H8"/><path d="M7 4L4 7l3 3"/><path d="M11 12l-3 3 3 3"/></svg>',
 "logistics": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9S14.5 18.3 12 21M12 3C9.5 5.7 8.2 8.7 8.2 12s1.3 6.3 3.8 9"/></svg>',
 "broker": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/><circle cx="16" cy="9" r="2"/></svg>',
 "agro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21V10"/><path d="M12 10C12 6 9 3 4 3c0 5 3 7 8 7zM12 13c0-4 3-7 8-7 0 5-3 7-8 7z"/></svg>',
 "seed": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3c4 3 6 6.5 6 10a6 6 0 0 1-12 0c0-3.5 2-7 6-10z"/><path d="M12 9v10"/></svg>',
 "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6M10 3v6L4.5 18.5A1.7 1.7 0 0 0 6 21h12a1.7 1.7 0 0 0 1.5-2.5L14 9V3"/><path d="M7 15h10"/></svg>',
 "tractor": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="7" cy="16" r="4"/><circle cx="18" cy="17" r="3"/><path d="M4 12V6h6l2 6h6l1 2M10 6v6"/></svg>',
 "fruit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="14" r="7"/><path d="M12 7c0-2 1-4 3-4M12 7c-1.5-1.5-3.5-2-5-1.5"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8z"/></svg>',
 "li": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.1c.5-1 1.8-2 3.7-2 4 0 4.7 2.6 4.7 6V21h-4v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9V21H9z"/></svg>',
 "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/></svg>',
}

# ---------------- serviços ----------------
SERVICES = [
 dict(slug="despacho-de-importacao", photo="importacao", photo_alt="Guindaste portuário movimentando contêineres", short="Importação", icon="import",
  title="Despacho de importação em Santos | RS Assessoria Aduaneira",
  desc="Despacho aduaneiro de importação em Santos: classificação fiscal, LI, DI/DUIMP, anuências do MAPA e Anvisa e follow-up até a liberação da carga.",
  h1="Despacho aduaneiro de importação em Santos, do custo proforma à carga liberada.",
  lead="Classificação, licenças, registro e acompanhamento junto à Receita Federal e aos órgãos anuentes — conduzido por despachantes aduaneiros desde 1998.",
  card="Custos proforma, classificação fiscal, licenças, registro e follow-up até a carga sair do terminal.",
  wa="Olá! Vim pelo site e quero falar sobre despacho de importação.",
  body=[
   ("O que fazemos na sua importação", "Cada importação começa antes do embarque. Levantamos o custo estimado, conferimos a classificação tarifária e identificamos quais órgãos precisam anuir — para que a carga chegue ao porto com a documentação pronta e não pare no terminal.",
    ["Elaboração dos custos proforma", "Classificação tarifária (NCM)", "Licenças de importação (LI/LSI) e acompanhamento junto aos órgãos competentes", "Registro de DI, DSI, DA e DTA", "Autorizações junto a órgãos federais, estaduais e municipais", "Controle de prazos das licenças", "Follow-up do desembaraço e da liberação da mercadoria", "Acompanhamento com fiscais do Ministério da Agricultura e da Alfândega quando necessário", "Acompanhamento do carregamento no terminal depositário"]),
   ("Cargas com anuência: nossa rotina", "Grande parte dos nossos clientes importa sementes, insumos e máquinas agrícolas — produtos que dependem de órgãos como o Ministério da Agricultura e a Anvisa. Conhecer essas exigências de perto é o que reduz exigências fiscais, armazenagem extra e atrasos.", []),
  ],
  faq=[
   ("Quanto tempo leva o desembaraço de importação?", "Depende do canal de parametrização, da necessidade de anuência e da documentação. Com licenças e documentos prontos antes da chegada, a liberação tende a ser mais rápida. Conversamos sobre o seu caso específico antes do embarque."),
   ("Vocês fazem a classificação fiscal (NCM) do produto?", "Sim. A classificação tarifária faz parte do nosso serviço de importação e define tributos, licenças e anuências necessárias."),
   ("Atendem importações fora do Porto de Santos?", "Sim. Estamos sediados em Santos e contamos com parceiros em outros portos, aeroportos e fronteiras do Brasil."),
  ]),
 dict(slug="despacho-de-exportacao", photo="exportacao", photo_alt="Navio porta-contêineres atracado em terminal portuário", short="Exportação", icon="export",
  title="Despacho de exportação em Santos | RS Assessoria Aduaneira",
  desc="Despacho aduaneiro de exportação: DU-E, LPCO, certificado de origem e fitossanitário, documentos de embarque e desembaraço na Receita Federal.",
  h1="Despacho aduaneiro de exportação com controle do pré-embarque ao destino final.",
  lead="DU-E, LPCO, certificados e documentos de embarque coordenados por uma só equipe, integrada ao embarcador, ao recebedor e aos operadores.",
  card="DU-E, certificados de origem e fitossanitário, documentos de embarque e desembaraço.",
  wa="Olá! Vim pelo site e quero falar sobre despacho de exportação.",
  body=[
   ("Coordenação personalizada da exportação", "Acompanhamos desde a fase de pré-embarque, passando pelas etapas intermediárias, até a entrega no destino final — incluindo a gestão do fluxo de informações entre embarcador, recebedor e operadores.",
    ["Elaboração e registro da DU-E (Declaração Única de Exportação), LPCO e DAT", "Cálculo de custos e viabilidade da exportação", "Emissão da fatura comercial e do packing list", "Análise de carta de crédito", "Certificado de origem conforme exigido pelo importador", "Certificado de seguro (embarque com seguro no Brasil)", "Certificado fitossanitário junto ao Ministério da Agricultura", "Emissão do conhecimento de embarque", "Desembaraço aduaneiro junto à Receita Federal", "Confirmação de embarque ao importador ou agente", "Preparação do set de documentos para o banco e remessa ao importador"]),
   ("Exportação do agro", "Frutas, sementes e insumos agrícolas estão entre as cargas que mais exportamos. Isso envolve certificação fitossanitária e prazos curtos — e é exatamente onde a experiência da equipe faz diferença.", []),
  ],
  faq=[
   ("Vocês emitem o certificado fitossanitário?", "Cuidamos da emissão do certificado fitossanitário junto ao Ministério da Agricultura, assim como do certificado de origem exigido pelo importador."),
   ("O que é a DU-E?", "É a Declaração Única de Exportação, registrada no Portal Único Siscomex. Ele reúne as informações aduaneiras, comerciais e logísticas da operação."),
   ("Vocês trabalham com carta de crédito?", "Sim. Analisamos a carta de crédito e preparamos o set de documentos para entrega ao banco."),
  ]),
 dict(slug="drawback", photo="drawback", photo_alt="Armazém com paletes e empilhadeira", short="Drawback", icon="drawback",
  title="Assessoria em Drawback | RS Assessoria Aduaneira, Santos",
  desc="Assessoria em Drawback: pedido de Ato Concessório, controle de compras e exportações vinculadas e comprovação do regime para reduzir tributos.",
  h1="Drawback: menos tributo nos insumos de quem exporta.",
  lead="O regime aduaneiro especial que suspende ou isenta tributos sobre matérias-primas usadas em produtos exportados — com o controle que ele exige.",
  card="Regime especial que reduz tributos sobre insumos de produtos exportados. Do Ato Concessório à comprovação.",
  wa="Olá! Vim pelo site e quero falar sobre Drawback.",
  body=[
   ("Como funciona o Drawback", "O Drawback é um regime aduaneiro especial criado para incentivar as exportações brasileiras. Ele concede vantagens tributárias sobre matérias-primas adquiridas no Brasil ou importadas, desde que sejam empregadas na produção de bens exportados ou em venda equiparada à exportação.",
    []),
   ("O Ato Concessório", "A concessão é feita por meio de um pedido de Ato Concessório, com período de validade, que especifica valores e quantidades do que será comprado e do que será exportado. É um compromisso assumido previamente: a partir da aprovação, o beneficiário passa a usufruir do regime.",
    ["Avaliação da modalidade mais adequada à sua operação", "Montagem e pedido do Ato Concessório", "Controle de compras (locais e importadas) e exportações vinculadas", "Acompanhamento de prazos e comprovação do regime"]),
   ("Flexibilidade do regime", "Existem diversas modalidades e submodalidades, o que permite ajustar o Drawback às necessidades de cada empresa. Avaliamos o seu fluxo de compras e exportações para indicar o caminho.", []),
  ],
  faq=[
   ("Quem pode usar o Drawback?", "Empresas que compram insumos (no Brasil ou no exterior) para produzir bens que serão exportados ou vendidos em operação equiparada à exportação."),
   ("O que acontece se a exportação não for comprovada?", "O compromisso do Ato Concessório precisa ser cumprido no prazo. Sem comprovação, os tributos suspensos podem ser cobrados. Por isso o controle durante a vigência é parte do nosso trabalho."),
   ("Drawback vale para pequenas empresas?", "Pode valer. A viabilidade depende do volume de insumos e exportações. Fazemos essa análise antes de qualquer pedido."),
  ]),
 dict(slug="logistica-internacional", photo="logistica", photo_alt="Vista aérea de terminal de contêineres", short="Logística", icon="logistics",
  title="Logística internacional e freight forwarder | RS Aduaneira",
  desc="Logística integrada de importação e exportação: escolha de modal e rota, embalagem, coordenação de embarques, controle de cargas em trânsito e contêineres.",
  h1="Logística internacional integrada ao seu despacho aduaneiro.",
  lead="Atuamos como freight forwarder, com uma rede de transportadores aéreos, marítimos e rodoviários e terminais alfandegados — para cada carga seguir pela opção certa.",
  card="Freight forwarder com rede aérea, marítima e rodoviária. Rota, embalagem e controle da carga em trânsito.",
  wa="Olá! Vim pelo site e quero falar sobre logística internacional.",
  body=[
   ("Parcerias como base", "Contratamos e administramos a logística de embarques conforme as necessidades e exigências de cada cliente, por meio de parcerias com transportadores marítimos e rodoviários e com terminais alfandegados e REDEX.",
    ["Analistas especializados em cada tipo de produto, para escolher a melhor embalagem e o equipamento de transporte", "Assistência na escolha dos modais e rotas mais adequados", "Execução e coordenação de embarques", "Status e controle de cargas em trânsito", "Coordenação de liberação de contêiner e estufagem"]),
   ("Despacho e logística na mesma mesa", "Quando quem desembaraça é quem coordena o transporte, a informação não se perde entre fornecedores. Isso reduz retrabalho, armazenagem e custos operacionais.", []),
  ],
  faq=[
   ("Vocês contratam o frete internacional?", "Sim. Como freight forwarder, buscamos e administramos o transporte aéreo, marítimo e rodoviário com nossa rede de parceiros."),
   ("Trabalham com carga consolidada e contêiner cheio?", "Avaliamos a melhor opção para o volume e o tipo de carga. Fale com a equipe sobre o seu embarque."),
   ("Acompanham a carga em trânsito?", "Sim. O controle de cargas em trânsito e o status do embarque fazem parte do serviço."),
  ]),
 dict(slug="brokeragem-de-embarques", photo="brokeragem", photo_alt="Navio cargueiro navegando em mar aberto", short="Brokeragem", icon="broker",
  title="Brokeragem de embarques internacionais | RS Aduaneira",
  desc="Brokeragem de embarques: avaliamos rotas, prazos, tempo de trânsito e particularidades da carga para definir a alternativa de embarque mais conveniente.",
  h1="Brokeragem de embarques: a melhor alternativa para cada carga.",
  lead="Buscamos, avaliamos e definimos com você a opção de embarque mais conveniente, considerando datas, rotas, tempo de trânsito e as particularidades do produto.",
  card="Avaliamos datas, rotas e tempo de trânsito para definir com você a opção de embarque mais conveniente.",
  wa="Olá! Vim pelo site e quero falar sobre brokeragem de embarques.",
  body=[
   ("Decisão em conjunto", "Nossa principal preocupação é buscar, avaliar e definir, junto com o cliente, a alternativa de embarque que melhor atende à operação — sempre respeitando as preferências da sua empresa.",
    ["Comparação de datas, prazos e saídas disponíveis", "Avaliação de rotas e tempo de trânsito entre origem e destino", "Análise das particularidades do produto (perecível, carga sensível, embalagem)", "Recomendação clara, com prós e contras de cada opção"]),
  ],
  faq=[
   ("Brokeragem é o mesmo que agenciamento de carga?", "São complementares. Na brokeragem o foco é comparar e escolher a alternativa de embarque; o agenciamento executa e acompanha o transporte."),
   ("Preciso contratar o despacho junto?", "Não necessariamente, mas a combinação de brokeragem, logística e despacho na mesma equipe evita ruído de informação."),
  ]),
 dict(slug="comercio-exterior-agronegocio", photo="agro", photo_alt="Vista aérea de lavoura com trator", short="Agronegócio", icon="agro",
  title="Comércio exterior para o agronegócio | RS Aduaneira, Santos",
  desc="Importação de sementes, fertilizantes, defensivos e máquinas agrícolas e exportação de frutas e insumos, com anuências do MAPA, Anvisa e Receita Federal.",
  h1="Comércio exterior para o agronegócio, de sementes a máquinas agrícolas.",
  lead="Sementeiras, produtores e indústrias do agro confiam à RS a importação e a exportação de cargas que dependem de anuência — desde 1998, a partir do Porto de Santos.",
  card="Sementes, fertilizantes, defensivos, máquinas agrícolas e frutas, com MAPA e Anvisa no radar.",
  wa="Olá! Vim pelo site e quero falar sobre importação/exportação para o agronegócio.",
  body=[
   ("Cargas do agro que movimentamos", "Na importação: sementes de diversos tipos, fertilizantes, defensivos agrícolas e máquinas agrícolas, de adubadores manuais a tratores. Na exportação, praticamente os mesmos produtos, com destaque para frutas e insumos agrícolas.",
    ["Sementes e material de propagação", "Fertilizantes e defensivos agrícolas", "Máquinas e implementos agrícolas", "Frutas e insumos para exportação"]),
   ("Anuências sem surpresa", "Cargas do agro passam pelo Ministério da Agricultura, Pecuária e Abastecimento e, em alguns casos, pela Anvisa, além da Receita Federal. Acompanhamos os fiscais quando necessário e cuidamos de licenças e certificados fitossanitários.", []),
   ("Quem já confia na RS", "Sakata, Germisul, Germiterra, Andrade Sun Farms, Cisol, Latinsem, Safrasul, Facholi, Germipasto, Gasparim, Pastobrás, Biocross e CT Agroindústria estão entre as empresas atendidas.", []),
  ],
  faq=[
   ("Vocês importam sementes?", "Sim. A importação de sementes, com as licenças e anuências do Ministério da Agricultura, é uma das operações mais frequentes da RS."),
   ("Cuidam do certificado fitossanitário na exportação?", "Sim, emitimos o certificado fitossanitário junto ao Ministério da Agricultura como parte do despacho de exportação."),
   ("Importam máquinas agrícolas?", "Sim, de implementos menores a tratores, incluindo classificação fiscal, licenças e logística."),
  ]),
]

FAQ_HOME = [
 ("O que faz um despachante aduaneiro?", "É o profissional habilitado pela Receita Federal para representar importadores e exportadores no despacho aduaneiro: registra declarações, acompanha a conferência e responde às exigências até a liberação da carga. Os sócios da RS são despachantes aduaneiros."),
 ("A RS atende só no Porto de Santos?", "Nossa sede fica em Santos, no maior porto da América Latina, mas contamos com representantes e parceiros em outros portos, aeroportos e fronteiras do Brasil, e operações para 48 países."),
 ("Atendem empresas pequenas?", "Sim. Atendemos empresas de pequeno, médio e grande porte, inclusive quem está começando a importar ou exportar."),
 ("Vocês trabalham com cargas que precisam do MAPA ou da Anvisa?", "Sim, é uma parte importante da nossa rotina — principalmente sementes, fertilizantes, defensivos, máquinas agrícolas e frutas."),
 ("Como peço um orçamento?", "Chame no WhatsApp " + WA_H + ", ligue " + TEL1_H + " ou preencha o formulário desta página com o tipo de operação e a mercadoria."),
]

CLIENTS = [("sakata", "Sakata", 637), ("germisul", "Germisul", 196), ("germiterra", "Germiterra", 114), ("andrade", "Andrade Sun Farms", 334), ("cisol", "Cisol", 263), ("latinsem", "Latinsem", 223), ("safrasul", "Safrasul Sementes", 368), ("facholi", "Facholi", 146), ("germipasto", "Germipasto", 195), ("gasparim", "Grupo Gasparim", 162), ("pastobras", "Pastobrás Sementes", 237), ("biocross", "Biocross", 212), ("ct", "CT Agroindústria (Citrus)", 134), ("defensive-e-agrovant", "Defensive e Agrovant", 314), ("gibran", "Gibran", 119), ("world-sports", "World Sports", 380), ("tropline", "Tropline", 133)]
EMAIL_ENDPOINT = "https://formsubmit.co/ajax/" + EMAIL  # após ativar, trocar o e-mail pelo alias que o FormSubmit enviar

# ---------------- partes comuns ----------------
HEAD_INLINE = "document.documentElement.classList.add('js');window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});"
HEAD_HASH = "sha256-" + base64.b64encode(hashlib.sha256(HEAD_INLINE.encode()).digest()).decode()

ORG = {
 "@type": ["ProfessionalService", "LocalBusiness"], "@id": SITE + "/#org",
 "name": "RS Assessoria Aduaneira", "legalName": "R S Assessoria Aduaneira Ltda",
 "url": SITE + "/", "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/og.jpg",
 "description": "Despachante aduaneiro e assessoria em comércio exterior em Santos/SP desde 1998: importação, exportação, Drawback, logística internacional e brokeragem de embarques.",
 "foundingDate": "1998", "taxID": CNPJ, "email": EMAIL, "telephone": TEL1,
 "address": {"@type": "PostalAddress", "streetAddress": "Av. Ana Costa, 146 – conj. 702/703", "addressLocality": "Santos", "addressRegion": "SP", "postalCode": CEP, "addressCountry": "BR"},
 "geo": {"@type": "GeoCoordinates", "latitude": -23.9603, "longitude": -46.3321},
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00"}],
 "areaServed": [{"@type": "City", "name": "Santos"}, {"@type": "Country", "name": "Brasil"}],
 "contactPoint": [{"@type": "ContactPoint", "telephone": "+55-13-99614-0042", "contactType": "customer service", "availableLanguage": "Portuguese"}],
 "sameAs": [IG, FB, LI],
 "numberOfEmployees": {"@type": "QuantitativeValue", "value": 15},
 "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5", "reviewCount": "5", "bestRating": "5"},
}

def esc(s): return html.escape(s, quote=True)

def head(title, desc, path, extra_ld=None, robots="index,follow", og_image="/assets/og.jpg", og_type="website"):
    PRELOAD = '\n<link rel="preload" href="/assets/video/hero-poster.webp" as="image" fetchpriority="high" media="(min-width: 901px)">\n<link rel="preload" href="/assets/video/hero-poster-m.webp" as="image" fetchpriority="high" media="(max-width: 900px)">' if path == "/" else ""
    url = SITE + path
    ld = [{"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "RS Assessoria Aduaneira", "inLanguage": "pt-BR", "publisher": {"@id": SITE + "/#org"}}] + (extra_ld or [])}]
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0C0D10">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="RS Assessoria Aduaneira">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="RS Assessoria Aduaneira — despachante aduaneiro em Santos desde 1998">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/inter-display-600.woff" as="font" type="font/woff" crossorigin>{PRELOAD}
<link rel="stylesheet" href="/assets/site.css?v={VER}">
<script>{HEAD_INLINE}</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
'''

def nav(home=True, light=False):
    p = "" if home else "/"
    return f'''<header class="nav{' light' if light else ''}" role="banner">
 <div class="container nav-in">
  <a class="logo" href="/" aria-label="RS Assessoria Aduaneira — início"><img class="l-light" src="/assets/logo-light.svg" alt="RS Assessoria Aduaneira" width="156" height="56"><img class="l-dark" src="/assets/logo.svg" alt="" width="156" height="56" aria-hidden="true"></a>
  <nav class="nav-links" id="menu" aria-label="Principal">
   <a href="{p}#servicos">Serviços</a>
   <a href="/comercio-exterior-agronegocio/">Agronegócio</a>
   <a href="{p}#sobre" class="hide-md">Sobre</a>
   <a href="/blog/">Blog</a>
   <a href="{p}#faq" class="hide-md">Dúvidas</a>
   <a href="{p}#contato">Contato</a>
   <a class="btn btn-sm btn-wa" href="{wa('Olá! Vim pelo site da RS Assessoria Aduaneira e quero falar com a equipe.')}" target="_blank" rel="noopener" data-wa="nav">{I['wa']}Falar no WhatsApp</a>
  </nav>
  <button class="burger" type="button" aria-label="Abrir menu" aria-controls="menu" aria-expanded="false"><span></span><span></span><span></span></button>
 </div>
</header>
'''

def footer(wa_msg):
    svc_links = "".join(f'<li><a href="/{s["slug"]}/">{s["short"]}</a></li>' for s in SERVICES)
    return f'''<footer class="footer" role="contentinfo">
 <div class="container">
  <div class="foot-grid">
   <div>
    <img class="logo" src="/assets/logo-light.svg" alt="RS Assessoria Aduaneira" width="170" height="61" loading="lazy">
    <p>Despachante aduaneiro e assessoria em comércio exterior em Santos/SP desde 1998.</p>
    <div class="socials">
     <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram da RS Assessoria Aduaneira">{I['ig']}</a>
     <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook da RS Assessoria Aduaneira">{I['fb']}</a>
     <a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn da RS Assessoria Aduaneira">{I['li']}</a>
    </div>
   </div>
   <div><h4>Serviços</h4><ul>{svc_links}</ul></div>
   <div><h4>Institucional</h4><ul><li><a href="/#sobre">Sobre a RS</a></li><li><a href="/#como-funciona">Como trabalhamos</a></li><li><a href="/blog/">Blog</a></li><li><a href="/#faq">Perguntas frequentes</a></li><li><a href="/#contato">Contato</a></li><li><a href="/politica-de-privacidade/">Política de privacidade</a></li></ul></div>
   <div><h4>Contato</h4><ul>
    <li>{ADDR}<br>{BAIRRO}, Santos/SP · CEP {CEP}</li>
    <li><a href="tel:{TEL1}">{TEL1_H}</a> · <a href="tel:{TEL2}">{TEL2_H}</a></li>
    <li><a href="{wa(wa_msg)}" target="_blank" rel="noopener" data-wa="footer">WhatsApp {WA_H}</a></li>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li>Seg. a sex., 8h às 18h</li>
   </ul></div>
  </div>
  <div class="foot-bottom"><span>© {datetime.date.today().year} R S Assessoria Aduaneira Ltda · CNPJ {CNPJ}</span><span>Fotos: <a href="https://unsplash.com/" target="_blank" rel="noopener">Unsplash</a> · Santos · SP · Brasil</span></div>
 </div>
</footer>
<a class="wa-float" href="{wa(wa_msg)}" target="_blank" rel="noopener" aria-label="Falar com a RS Assessoria Aduaneira no WhatsApp" data-wa="float">{I['wa']}</a>
<div class="cookie" role="dialog" aria-live="polite" aria-label="Aviso de cookies">
 <p>Usamos cookies de medição somente com a sua autorização, para entender o uso do site. Veja a <a href="/politica-de-privacidade/">política de privacidade</a>.</p>
 <div class="row"><button class="btn btn-sm" type="button" data-consent="granted">Aceitar</button><button class="btn btn-sm btn-ghost" type="button" data-consent="denied" style="--fg:#fff">Recusar</button></div>
</div>
<script src="/assets/site.js?v={VER}" defer></script>
</body>
</html>
'''

def faq_html(items):
    out = []
    for i, (q, a) in enumerate(items):
        out.append(f'<details class="rv" style="--d:{i*0.05:.2f}s"><summary>{esc(q)}<i aria-hidden="true"></i></summary><div class="ans"><p>{esc(a)}</p></div></details>')
    return "\n".join(out)

def faq_ld(items, path):
    return {"@type": "FAQPage", "@id": SITE + path + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def contact_section(wa_msg, preset=""):
    opts = ["Importação", "Exportação", "Drawback", "Logística internacional", "Brokeragem de embarques", "Agronegócio", "Outro assunto"]
    opt_html = "".join(f'<option{" selected" if o == preset else ""}>{o}</option>' for o in opts)
    return f'''<section class="section contact dark" id="contato" aria-labelledby="contato-t">
 <div class="container contact-wrap">
  <div class="rv-l">
   <span class="eyebrow">Contato</span>
   <h2 id="contato-t">Conte qual é a carga. A gente diz o caminho.</h2>
   <p class="lead">Atendimento de segunda a sexta, das 8h às 18h, direto com quem conduz o despacho.</p>
   <ul class="info-list">
    <li><span class="ii">{I['wa']}</span><div><small>WhatsApp</small><a href="{wa(wa_msg)}" target="_blank" rel="noopener" data-wa="contato">{WA_H}</a></div></li>
    <li><span class="ii">{I['phone']}</span><div><small>Telefones</small><a href="tel:{TEL1}">{TEL1_H}</a> · <a href="tel:{TEL2}">{TEL2_H}</a></div></li>
    <li><span class="ii">{I['mail']}</span><div><small>E-mail</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
    <li><span class="ii">{I['pin']}</span><div><small>Endereço</small><a href="{MAPS}" target="_blank" rel="noopener">{ADDR} · {BAIRRO}, Santos/SP · {CEP}</a></div></li>
   </ul>
   <div class="map"><button type="button" data-map="{MAP_EMBED}">{I['pin']}<span>Carregar mapa do Google</span></button></div>
  </div>
  <form class="form rv" id="form-contato" novalidate style="--d:.1s" action="{EMAIL_ENDPOINT.replace('/ajax','')}" method="post" data-endpoint="{EMAIL_ENDPOINT}">
   <h3>Peça um orçamento</h3>
   <p class="fhint">Sua mensagem vai direto para o e-mail da equipe. Respondemos em horário comercial.</p>
   <div class="fgrid">
    <div class="field"><label for="f-nome">Nome *</label><input id="f-nome" name="nome" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
    <div class="field"><label for="f-empresa">Empresa</label><input id="f-empresa" name="empresa" autocomplete="organization"><span class="err"></span></div>
    <div class="field"><label for="f-tel">Telefone / WhatsApp *</label><input id="f-tel" name="telefone" type="tel" inputmode="tel" autocomplete="tel" required><span class="err" aria-live="polite"></span></div>
    <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email"><span class="err" aria-live="polite"></span></div>
    <div class="field full"><label for="f-serv">Assunto</label><select id="f-serv" name="servico">{opt_html}</select><span class="err"></span></div>
    <div class="field full"><label for="f-msg">Mensagem *</label><textarea id="f-msg" name="mensagem" placeholder="Ex.: importação de sementes da Holanda, via Santos, previsão para março." required></textarea><span class="err" aria-live="polite"></span></div>
    <div class="hp" aria-hidden="true"><label for="f-web">Site</label><input id="f-web" name="website" tabindex="-1" autocomplete="off"></div>
   </div>
   <button class="btn" type="submit">{I['mail']}Enviar mensagem</button>
   <p class="form-status" role="status"></p>
  </form>
 </div>
</section>
'''

# ---------------- HOME ----------------
# ---------------- pátio de contêineres (home) ----------------
CRATES = {  # vídeo -> (desktop, celular, quadro de pausa). Rastreio em assets/video/<nome>.json
    "crate": ("/assets/video/crate.mp4", "/assets/video/crate-m.mp4", "/assets/video/crate-hold.webp"),
    "take-3": ("/assets/video/take-3-s.mp4", "/assets/video/take-3-s-m.mp4", "/assets/video/take-3-hold.webp"),
    "hero": ("/assets/video/hero-s.mp4", "/assets/video/hero-s-m.mp4", "/assets/video/hero-hold.webp"),
}

def crate_tracks():
    return "{" + ",".join(f'"{k}":' + (ROOT / f"assets/video/{k}.json").read_text() for k in CRATES) + "}"

def crate(video, code, sid, label, face):
    """Cena do contêiner real: vídeo controlado pelo scroll, com o conteúdo (cards) preso
    na lateral do contêiner, que foi rastreada quadro a quadro (_tools/track.py)."""
    src, mob, poster = CRATES[video]
    attrs = f' id="{sid}" aria-labelledby="{sid}-t"' if sid else f' aria-label="{esc(label)}"'
    return f'''<section class="crate" data-crate="{video}"{attrs}>
 <div class="crate-stage">
  <img class="crate-poster" src="{poster}" alt="" width="1600" height="900" loading="lazy" decoding="async" aria-hidden="true">
  <video class="crate-video" muted playsinline preload="none" aria-hidden="true" tabindex="-1" data-src="{src}" data-src-m="{mob}"></video>
  <div class="crate-shade" aria-hidden="true"></div>
  <div class="crate-face"><div class="crate-paint"><span class="f-code" aria-hidden="true">{code}</span>{face}
  </div></div>
 </div>
</section>
'''

TAKES = {
    2: ("Atendimento direto com os sócios", "Cada carga tem um despachante responsável, do primeiro documento à liberação."),
    3: ("Carga liberada", "Agora é a vez da sua operação. Conte o que você precisa importar ou exportar."),
}

def take_band(n):
    """Faixa de vídeo controlada pelo scroll. Só aparece se assets/video/take-N.mp4 existir."""
    if not (ROOT / f"assets/video/take-{n}.mp4").exists():
        return ""
    mob = f"/assets/video/take-{n}-m.mp4" if (ROOT / f"assets/video/take-{n}-m.mp4").exists() else f"/assets/video/take-{n}.mp4"
    poster = f'<img class="take-poster" src="/assets/video/take-{n}-poster.webp" alt="" width="1280" height="720" loading="lazy" decoding="async">' if (ROOT / f"assets/video/take-{n}-poster.webp").exists() else ""
    t, p = TAKES[n]
    return f'''<div class="take" data-scrub>
 <div class="take-stage">
  {poster}<video class="take-video" muted playsinline preload="metadata" aria-hidden="true" tabindex="-1" data-src-m="{mob}" data-src="/assets/video/take-{n}.mp4"></video>
  <div class="take-shade" aria-hidden="true"></div>
  <div class="container take-copy"><p class="take-t">{t}</p><p class="take-p">{p}</p></div>
 </div>
</div>
'''

def home():
    wa_msg = "Olá! Vim pelo site da RS Assessoria Aduaneira e quero falar com a equipe."
    cards = []
    for i, s in enumerate(SERVICES[:5]):
        cards.append(f'''<a class="svc rv" data-tilt href="/{s['slug']}/" style="--d:{i*0.07:.2f}s">
   <div class="svc-photo"><img src="/assets/fotos/{s['photo']}-sm.webp" alt="" width="800" height="450" loading="lazy" decoding="async"></div>
   <div class="svc-num"><span class="svc-ico">{I[s['icon']]}</span><span>0{i+1}</span></div>
   <h3>{s['short'] if s['short'] not in ('Logística','Brokeragem') else ('Logística internacional' if s['short']=='Logística' else 'Brokeragem de embarques')}</h3>
   <p>{s['card']}</p>
   <span class="link-arrow">Saiba mais {I['arrow']}</span>
  </a>''')
    def tiles(hidden):
        return "".join(f'<span class="logo-tile"{" aria-hidden=\"true\"" if hidden else ""}><img src="/assets/clientes/{f}.webp" alt="{"" if hidden else esc(n)}" width="{w}" height="112" loading="lazy" decoding="async"></span>' for f, n, w in CLIENTS)
    marquee = tiles(False) + tiles(True)
    ld = [faq_ld(FAQ_HOME, "/")] + [{"@type": "Service", "name": s["short"] if s["slug"] != "logistica-internacional" else "Logística internacional", "url": f"{SITE}/{s['slug']}/", "provider": {"@id": SITE + "/#org"}, "areaServed": "BR"} for s in SERVICES]
    out = head("Despachante aduaneiro em Santos | RS Assessoria Aduaneira",
               "Despachante aduaneiro em Santos desde 1998: importação, exportação, Drawback e logística internacional. Atendimento direto com os sócios. Fale no WhatsApp.",
               "/", ld)
    out += nav()
    out += f'''<main id="conteudo">
<div class="hero-pin" data-scrub>
<section class="hero" aria-labelledby="hero-t">
 <picture class="hero-poster" aria-hidden="true"><source srcset="/assets/video/hero-poster-m.webp" media="(max-width: 900px)"><img src="/assets/video/hero-poster.webp" alt="" width="1600" height="900" fetchpriority="high" decoding="async"></picture>
 <video class="hero-video" muted playsinline preload="auto" aria-hidden="true" tabindex="-1" data-src-m="/assets/video/hero-m.mp4" data-src="/assets/video/hero.mp4"></video>
 <div class="hero-shade" aria-hidden="true"></div>
 <div class="container">
  <div class="hero-in">
   <span class="eyebrow rv">Santos/SP · Comércio exterior desde 1998</span>
   <h1 id="hero-t" data-split>Despachante aduaneiro em Santos para sua carga <em>não ficar parada.</em></h1>
   <p class="lead rv" style="--d:.35s">Importação, exportação, Drawback e logística internacional com atendimento direto dos sócios despachantes aduaneiros.</p>
   <div class="hero-ctas rv" style="--d:.45s">
    <a class="btn btn-wa" href="{wa('Olá! Vim pelo site e quero um orçamento de despacho aduaneiro.')}" target="_blank" rel="noopener" data-wa="hero">{I['wa']}Pedir orçamento no WhatsApp</a>
    <a class="btn btn-ghost" href="#servicos">Ver serviços {I['arrow']}</a>
   </div>
   <div class="hero-meta rv" style="--d:.55s">
    <div><strong>28 anos</strong>no porto de Santos</div>
    <div><strong>150+</strong>empresas atendidas</div>
    <div><strong>5,0 ★</strong>no Google</div>
   </div>
  </div>
 </div>
 <span class="hero-scroll" aria-hidden="true"></span>
 <div class="hero-hud" aria-hidden="true"><span>Içando carga</span><i><b></b></i><span class="hud-n">RSAU 199801-3</span></div>
</section>
</div>
<div class="yard">
<script type="application/json" id="crate-track">{crate_tracks()}</script>
'''
    out += crate("crate", "RSAU 199801-3", None, "Números da RS Assessoria Aduaneira", f"""
    <div class="f-stats">
     <div><b><span data-count="28">28</span></b><span>anos no comércio exterior</span></div>
     <div><b><span data-count="150">150</span>+</b><span>clientes atendidos</span></div>
     <div><b><span data-count="48">48</span></b><span>países nas operações</span></div>
     <div><b><span data-count="15">15</span></b><span>profissionais</span></div>
    </div>""")
    out += f'''<section class="proof" aria-label="Empresas atendidas">
 <div class="container">
  <div class="marquee" aria-label="Algumas empresas atendidas">
   <p class="marquee-label">Empresas que confiam na RS</p>
   <div class="marquee-track">{marquee}</div>
  </div>
 </div>
</section>
'''
    svc_cards = "".join(f'''<a class="f-card" href="/{s['slug']}/"><span class="f-ico">{I[s['icon']]}</span><small>0{i+1}</small><b>{s['short'] if s['short'] not in ('Logística','Brokeragem') else ('Logística internacional' if s['short']=='Logística' else 'Brokeragem de embarques')}</b><span class="f-t">{s['card']}</span><em>Saiba mais {I['arrow']}</em></a>''' for i, s in enumerate(SERVICES[:5]))
    out += crate("crate", "RSAU 199802-9", "servicos", None, f"""
    <span class="f-eyebrow">Serviços</span>
    <h2 id="servicos-t">Assessoria aduaneira completa, do pedido ao destino.</h2>
    <div class="f-cards">{svc_cards}</div>""")
    agro_cards = "".join(f'<div class="f-card"><span class="f-ico">{I[ic]}</span><b>{t}</b><span class="f-t">{d}</span></div>' for ic, t, d in [
        ("seed", "Sementes", "Importação com licenças e anuência do Ministério da Agricultura."),
        ("flask", "Fertilizantes e defensivos", "Insumos com registro e liberação acompanhados de perto."),
        ("tractor", "Máquinas agrícolas", "Classificação fiscal, licença e logística do equipamento."),
        ("fruit", "Frutas e insumos para exportação", "Certificação fitossanitária e prazos de carga perecível.")])
    out += crate("take-3", "RSAU 199803-4", "agronegocio", None, f"""
    <span class="f-eyebrow">Nosso diferencial</span>
    <h2 id="agronegocio-t">Quem move o agro brasileiro passa pela RS.</h2>
    <div class="f-cards">{agro_cards}</div>
    <a class="f-link" href="/comercio-exterior-agronegocio/">Comércio exterior para o agro {I['arrow']}</a>""")
    out += take_band(2)
    team = "".join(f'<div class="f-card f-member"><span class="f-av">{a}</span><b>{n}</b><span class="f-t">{r}</span></div>' for a, n, r in [
        ("JL", "José Luiz de Abreu Pestana", "Sócio-diretor · importação"),
        ("JR", "José Roberto Sassaki", "Sócio-diretor · exportação"),
        ("RA", "Rafael Arrazi", "Sócio-diretor · legislação de exportação")])
    out += crate("hero", "RSAU 199804-0", "sobre", None, f"""
    <span class="f-eyebrow">Sobre a RS · desde 1998</span>
    <h2 id="sobre-t">Quase três décadas no maior porto da América Latina.</h2>
    <div class="f-cards">{team}</div>""")
    steps = "".join(f'<div class="f-card"><small>{n}</small><b>{t}</b><span class="f-t">{d}</span></div>' for n, t, d in [
        ("01", "Diagnóstico", "Produto, origem, destino, prazos, custos e viabilidade."),
        ("02", "Documentação", "Classificação fiscal, licenças, anuências e certificados."),
        ("03", "Embarque e trânsito", "Rota, modal, transportadores e controle da carga."),
        ("04", "Desembaraço", "Registro, fiscalização e liberação no terminal.")])
    out += crate("crate", "RSAU 199805-5", "como-funciona", None, f"""
    <span class="f-eyebrow">Como trabalhamos</span>
    <h2 id="como-funciona-t">Da primeira conversa à carga liberada.</h2>
    <div class="f-cards">{steps}</div>
    <a class="f-link f-wa" href="{wa('Olá! Vim pelo site e tenho uma operação de comércio exterior para avaliar.')}" target="_blank" rel="noopener" data-wa="cta-crate">{I['wa']}Falar no WhatsApp</a>""")
    out += f'''<!-- Depoimentos: só publicar com depoimentos reais autorizados pelos clientes -->
<section class="section testimonials" id="depoimentos" hidden aria-label="Depoimentos"></section>
<section class="section blog-teaser" id="blog" aria-labelledby="blog-t">
 <div class="container">
  <div class="blog-head">
   <div><span class="eyebrow rv">Blog</span><h2 id="blog-t" data-split>Comércio exterior sem complicação.</h2></div>
   <a class="link-arrow rv" href="/blog/">Ver todos os artigos {I['arrow']}</a>
  </div>
  <div class="post-grid">{"".join(post_card(p, i) for i, p in enumerate(POSTS[:3]))}</div>
 </div>
</section>
<section class="section faq" id="faq" aria-labelledby="faq-t">
 <div class="container faq-wrap">
  <div>
   <span class="eyebrow rv">Dúvidas frequentes</span>
   <h2 id="faq-t" data-split>Perguntas que ouvimos toda semana.</h2>
   <p class="muted rv">Não achou a sua? Chame a equipe no WhatsApp.</p>
  </div>
  <div class="faq-list">
{faq_html(FAQ_HOME)}
  </div>
 </div>
</section>
'''
    out += "</div>\n"
    out += contact_section(wa_msg)
    out += "</main>\n" + footer(wa_msg)
    return out

# ---------------- SERVIÇO ----------------
def service(s):
    path = f"/{s['slug']}/"
    bc = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": s["short"], "item": SITE + path}]}
    svc = {"@type": "Service", "@id": SITE + path + "#service", "name": s["h1"].rstrip("."), "serviceType": s["short"], "description": s["desc"], "url": SITE + path, "provider": {"@id": SITE + "/#org"}, "areaServed": [{"@type": "City", "name": "Santos"}, {"@type": "Country", "name": "Brasil"}]}
    out = head(s["title"], s["desc"], path, [bc, svc, faq_ld(s["faq"], path)])
    out += nav(home=False)
    body = ""
    for i, (h, p, items) in enumerate(s["body"]):
        lis = "".join(f"<li>{esc(x)}</li>" for x in items)
        body += f'<h2 class="rv">{esc(h)}</h2><p class="rv">{esc(p)}</p>' + (f'<ul class="checks rv">{lis}</ul>' if items else "")
    others = "".join(f'<a href="/{o["slug"]}/"{" aria-current=page" if o is s else ""}>{o["short"]} {I["arrow"] if o is not s else ""}</a>' for o in SERVICES)
    preset = {"Importação": "Importação", "Exportação": "Exportação", "Drawback": "Drawback", "Logística": "Logística internacional", "Brokeragem": "Brokeragem de embarques", "Agronegócio": "Agronegócio"}[s["short"]]
    out += f'''<main id="conteudo">
<section class="phero has-photo" aria-labelledby="h1">
 <img class="phero-bg" src="/assets/fotos/{s['photo']}-lg.webp" alt="{esc(s['photo_alt'])}" width="1440" height="810" fetchpriority="high" decoding="async">
 <div class="hero-grid" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">{s['short']}</span></nav>
  <span class="eyebrow rv">RS Assessoria Aduaneira · Santos/SP</span>
  <h1 id="h1" data-split>{esc(s['h1'])}</h1>
  <p class="lead rv" style="--d:.3s">{esc(s['lead'])}</p>
  <div class="hero-ctas rv" style="--d:.4s"><a class="btn btn-wa" href="{wa(s['wa'])}" target="_blank" rel="noopener" data-wa="phero">{I['wa']}Falar sobre {s['short'].lower() if s['short']!='Drawback' else 'Drawback'}</a><a class="btn btn-ghost" href="#contato">Pedir orçamento</a></div>
 </div>
</section>
<section class="section content" aria-label="Detalhes do serviço">
 <div class="container content-wrap">
  <article class="prose">{body}
   <h2 class="rv" id="faq">Perguntas frequentes</h2>
   <div class="faq-list">{faq_html(s['faq'])}</div>
  </article>
  <aside class="aside">
   <div class="aside-card dk rv"><h3>Fale com um despachante</h3><p>Atendimento direto com os sócios, seg. a sex., 8h às 18h.</p><a class="btn btn-wa" href="{wa(s['wa'])}" target="_blank" rel="noopener" data-wa="aside">{I['wa']}WhatsApp {WA_H}</a><a class="btn btn-ghost" href="tel:{TEL1}" style="--fg:#fff">{I['phone']}{TEL1_H}</a></div>
   <div class="aside-card rv"><h3>Outros serviços</h3><div class="aside-links">{others}</div></div>
  </aside>
 </div>
</section>
'''
    out += contact_section(s["wa"], preset)
    out += "</main>\n" + footer(s["wa"])
    return out

# ---------------- PRIVACIDADE ----------------
def privacy():
    wa_msg = "Olá! Vim pelo site da RS Assessoria Aduaneira."
    out = head("Política de privacidade | RS Assessoria Aduaneira", "Como a RS Assessoria Aduaneira trata os dados pessoais recebidos pelo site, conforme a LGPD (Lei 13.709/2018).", "/politica-de-privacidade/")
    out += nav(home=False)
    out += f'''<main id="conteudo">
<section class="phero"><div class="container"><nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">Política de privacidade</span></nav><h1>Política de privacidade</h1><p class="lead">Última atualização: {datetime.date.today().strftime('%d/%m/%Y')}</p></div></section>
<section class="section content legal"><div class="container"><div class="prose">
<h2>Quem somos</h2><p>R S Assessoria Aduaneira Ltda, CNPJ {CNPJ}, {ADDR}, {BAIRRO}, Santos/SP, CEP {CEP}. Contato do encarregado de dados: {EMAIL}.</p>
<h2>Quais dados recebemos</h2><p>Pelo formulário do site recebemos nome, empresa, telefone, e-mail, assunto e mensagem, enviados por e-mail à RS por meio do serviço FormSubmit. Também recebemos os dados que você nos envia por WhatsApp, telefone ou e-mail.</p>
<h2>Para que usamos</h2><p>Para responder ao seu contato, elaborar orçamentos e prestar os serviços contratados (base legal: procedimentos preliminares a contrato e execução de contrato, art. 7º, V, da LGPD).</p>
<h2>Serviços de terceiros</h2><ul class="checks"><li>FormSubmit: entrega por e-mail as mensagens enviadas pelo formulário.</li><li>WhatsApp (Meta): recebe a mensagem que você decide enviar.</li><li>Google Maps: o mapa só é carregado se você clicar em “Carregar mapa”.</li><li>Google Analytics (Consent Mode v2): só é ativado se você aceitar os cookies de medição.</li><li>Vercel: hospedagem do site, que registra dados técnicos de acesso (como IP) para segurança.</li></ul>
<h2>Cookies</h2><p>Por padrão, nenhum cookie de medição é gravado. Sua escolha fica salva no seu navegador e pode ser refeita limpando os dados do site.</p>
<h2>Seus direitos</h2><p>Você pode pedir confirmação, acesso, correção, anonimização, portabilidade ou exclusão dos seus dados escrevendo para {EMAIL}.</p>
<h2>Retenção</h2><p>Mantemos os dados pelo tempo necessário para o atendimento e para cumprir obrigações legais e regulatórias do comércio exterior.</p>
</div></div></section>
</main>
'''
    out += footer(wa_msg)
    return out

def page404():
    wa_msg = "Olá! Vim pelo site da RS Assessoria Aduaneira."
    out = head("Página não encontrada | RS Assessoria Aduaneira", "A página que você procurou não existe. Veja os serviços da RS Assessoria Aduaneira em Santos.", "/404", robots="noindex,follow")
    out += nav(home=False)
    links = "".join(f'<a class="btn btn-ghost btn-sm" href="/{s["slug"]}/">{s["short"]}</a>' for s in SERVICES)
    out += f'''<main id="conteudo"><section class="phero" style="min-height:100svh;display:flex;align-items:center"><div class="hero-grid" aria-hidden="true"></div><div class="container"><span class="eyebrow">Erro 404</span><h1>Esta carga não chegou ao destino.</h1><p class="lead">A página que você procurou não existe ou mudou de endereço.</p><div class="hero-ctas"><a class="btn" href="/">Voltar ao início</a>{links}</div></div></section></main>
'''
    out += footer(wa_msg)
    return out

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
def fdate(iso):
    y, m, d = iso.split("-"); return f"{int(d)} de {MESES[int(m)-1]} de {y}"

def post_card(p, i=0, big=False):
    return f'''<a class="post-card rv{' big' if big else ''}" href="/blog/{p['slug']}/" data-cat="{esc(p['category'])}" style="--d:{i*0.06:.2f}s">
   <div class="thumb"><img src="/assets/fotos/{p['photo']}-{'lg' if big else 'sm'}.webp" alt="" width="{1600 if big else 800}" height="{900 if big else 450}" loading="{'eager' if big else 'lazy'}" decoding="async"></div>
   <div class="post-body">
    <div class="post-meta"><span class="cat">{esc(p['category'])}</span><span>{p['read']} min de leitura</span></div>
    <h3>{esc(p['title'])}</h3>
    <p>{esc(p['desc'])}</p>
    <span class="link-arrow">Ler artigo {I['arrow']}</span>
   </div>
  </a>'''

def blog_index():
    wa_msg = "Olá! Vim pelo blog da RS Assessoria Aduaneira."
    bc = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"}]}
    blog_ld = {"@type": "Blog", "@id": SITE + "/blog/#blog", "name": "Blog da RS Assessoria Aduaneira", "url": SITE + "/blog/", "publisher": {"@id": SITE + "/#org"}, "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{SITE}/blog/{p['slug']}/", "datePublished": p["date"]} for p in POSTS]}
    out = head("Blog de comércio exterior | RS Assessoria Aduaneira", "Artigos sobre despacho aduaneiro, importação, exportação, Drawback e comércio exterior para o agronegócio, escritos pela equipe da RS em Santos.", "/blog/", [bc, blog_ld])
    out += nav(home=False)
    cats = []
    for p in POSTS:
        if p["category"] not in cats: cats.append(p["category"])
    chips = '<button class="fchip on" type="button" data-filter="*">Todos</button>' + "".join(f'<button class="fchip" type="button" data-filter="{esc(c)}">{esc(c)}</button>' for c in cats)
    out += f'''<main id="conteudo">
<section class="phero blog-hero" aria-labelledby="h1">
 <div class="hero-grid" aria-hidden="true"></div>
 <div class="container">
  <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><span aria-current="page">Blog</span></nav>
  <span class="eyebrow rv">Blog da RS</span>
  <h1 id="h1" data-split>Comércio exterior explicado por quem está no porto.</h1>
  <p class="lead rv" style="--d:.3s">Guias práticos sobre despacho aduaneiro, regimes especiais e importação e exportação do agronegócio.</p>
 </div>
</section>
<section class="section blog-list" aria-label="Artigos">
 <div class="container">
  {post_card(POSTS[0], 0, big=True)}
  <div class="filters rv" role="toolbar" aria-label="Filtrar por categoria">{chips}</div>
  <div class="post-grid" id="post-grid">{"".join(post_card(p, i) for i, p in enumerate(POSTS[1:]))}</div>
  <div class="cta-band rv">
   <h2>Tem uma dúvida sobre a sua operação? Pergunte a um despachante.</h2>
   <a class="btn" href="{wa(wa_msg)}" target="_blank" rel="noopener" data-wa="blog">{I['wa']}Falar no WhatsApp</a>
  </div>
 </div>
</section>
</main>
'''
    out += footer(wa_msg)
    return out

def blog_post(p):
    path = f"/blog/{p['slug']}/"
    wa_msg = f"Olá! Li o artigo \"{p['title']}\" no site da RS e quero tirar uma dúvida."
    bc = {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Início", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"}, {"@type": "ListItem", "position": 3, "name": p["title"], "item": SITE + path}]}
    art = {"@type": "BlogPosting", "@id": SITE + path + "#post", "headline": p["title"], "description": p["desc"], "datePublished": p["date"], "dateModified": p["date"], "image": f"{SITE}/assets/blog/og-{p['slug']}.jpg", "author": {"@type": "Organization", "name": "RS Assessoria Aduaneira", "url": SITE + "/"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + path, "inLanguage": "pt-BR", "articleSection": p["category"]}
    out = head(p["seo"], p["desc"], path, [bc, art], og_image=f"/assets/blog/og-{p['slug']}.jpg", og_type="article")
    out += nav(home=False)
    related = [q for q in POSTS if q is not p][:3]
    out += f'''<main id="conteudo">
<article class="post">
 <header class="post-hero">
  <div class="hero-grid" aria-hidden="true"></div>
  <div class="container narrow">
   <nav class="crumbs" aria-label="Você está em"><a href="/">Início</a><span aria-hidden="true">/</span><a href="/blog/">Blog</a><span aria-hidden="true">/</span><span aria-current="page">{esc(p['category'])}</span></nav>
   <div class="post-meta light"><span class="cat">{esc(p['category'])}</span><span>{fdate(p['date'])}</span><span>{p['read']} min de leitura</span></div>
   <h1 data-split>{esc(p['title'])}</h1>
   <p class="lead rv" style="--d:.3s">{esc(p['desc'])}</p>
  </div>
 </header>
 <div class="container narrow">
  <figure class="post-cover rv"><img src="/assets/fotos/{p['photo']}-lg.webp" alt="" width="1600" height="900" fetchpriority="high"></figure>
  <div class="prose post-prose">{p['body']}</div>
  <aside class="post-cta">
   <div><b>Precisa de ajuda com isso?</b><p>Fale direto com um despachante aduaneiro da RS.</p></div>
   <a class="btn btn-wa" href="{wa(wa_msg)}" target="_blank" rel="noopener" data-wa="post">{I['wa']}Falar no WhatsApp</a>
  </aside>
  <p class="post-author">Por <strong>Equipe RS Assessoria Aduaneira</strong> · Santos/SP</p>
 </div>
</article>
<section class="section related" aria-labelledby="rel-t">
 <div class="container">
  <div class="blog-head"><h2 id="rel-t">Continue lendo</h2><a class="link-arrow" href="/blog/">Todos os artigos {I['arrow']}</a></div>
  <div class="post-grid">{"".join(post_card(q, i) for i, q in enumerate(related))}</div>
 </div>
</section>
</main>
'''
    out += footer(wa_msg)
    return out

OUT = pathlib.Path(os.environ.get("OUT", str(ROOT))).resolve()

def write(rel, txt):
    p = OUT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")

VER = hashlib.md5((ROOT / "assets/site.css").read_bytes() + (ROOT / "assets/site.js").read_bytes()).hexdigest()[:8]

if __name__ == "__main__":
    import shutil
    # logo claro gerado a partir do logo principal
    lg = (ROOT / "assets/logo.svg").read_text()
    (ROOT / "assets/logo-light.svg").write_text(lg.replace("#B11116", "#E0262C").replace("#3A3A3C", "#ffffff"))
    if OUT != ROOT:
        OUT.mkdir(parents=True, exist_ok=True)
        if (OUT / "assets").exists(): shutil.rmtree(OUT / "assets")
        shutil.copytree(ROOT / "assets", OUT / "assets")
        shutil.copy(ROOT / "assets/mark.svg", OUT / "favicon.svg")
        for f in ["favicon-32.png", "apple-touch-icon.png"]:
            shutil.copy(ROOT / f, OUT / f)
    write("index.html", home())
    for s in SERVICES:
        write(f"{s['slug']}/index.html", service(s))
    write("politica-de-privacidade/index.html", privacy())
    write("blog/index.html", blog_index())
    for p in POSTS:
        write(f"blog/{p['slug']}/index.html", blog_post(p))
    write("404.html", page404())
    urls = ["/"] + [f"/{s['slug']}/" for s in SERVICES] + ["/blog/"] + [f"/blog/{p['slug']}/" for p in POSTS] + ["/politica-de-privacidade/"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if u=='/' else '0.8' if 'politica' not in u else '0.3'}</priority></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    csp = ("default-src 'self'; "
           f"script-src 'self' '{HEAD_HASH}' https://www.googletagmanager.com; "
           "style-src 'self' 'unsafe-inline'; img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com; "
           "font-src 'self'; connect-src 'self' https://formsubmit.co https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com https://www.googletagmanager.com; "
           "frame-src https://www.google.com https://maps.google.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self' https://formsubmit.co; object-src 'none'; upgrade-insecure-requests")
    vercel = {
      "buildCommand": "OUT=public python3 _tools/build_pages.py",
      "outputDirectory": "public",
      "framework": None,
      "cleanUrls": True, "trailingSlash": True,
      "headers": [
        {"source": "/(.*)", "headers": [
          {"key": "Strict-Transport-Security", "value": "max-age=63072000; includeSubDomains; preload"},
          {"key": "Content-Security-Policy", "value": csp},
          {"key": "X-Frame-Options", "value": "DENY"},
          {"key": "X-Content-Type-Options", "value": "nosniff"},
          {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
          {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"}]},
        {"source": "/assets/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]}
      ],
      "redirects": [
        {"source": "/home", "destination": "/", "permanent": True},
        {"source": "/servico/importacao", "destination": "/despacho-de-importacao/", "permanent": True},
        {"source": "/servico/exportacao", "destination": "/despacho-de-exportacao/", "permanent": True},
        {"source": "/servico/drawback", "destination": "/drawback/", "permanent": True},
        {"source": "/servico/logistica", "destination": "/logistica-internacional/", "permanent": True},
        {"source": "/servico/brokeragem", "destination": "/brokeragem-de-embarques/", "permanent": True},
        {"source": "/fale-conosco", "destination": "/#contato", "permanent": True},
        {"source": "/rs-assessoria-aduaneira", "destination": "/#sobre", "permanent": True},
        {"source": "/servicos", "destination": "/#servicos", "permanent": True},
        {"source": "/clientes", "destination": "/#agronegocio", "permanent": True}
      ]
    }
    write("vercel.json", json.dumps(vercel, ensure_ascii=False, indent=2))
    print("ok", VER, HEAD_HASH)
