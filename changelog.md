# 📝 Changelog — Refatoração do Menu de Navegação (Header/Footer compartilhados)

> **Data:** 2026-06-08
> **Escopo:** Camada de templates (Jinja2) + CSS. **Sem alteração de backend (`app.py`).**
> **Tipo:** Correção de bug + refatoração estrutural (DRY).

---

## 1. 🎯 Problema reportado

Durante a navegação como **cliente** (login por placa + senha `123456`), a rota **`/ranking`**
exibia o **menu de administrador** (`Dashboard · Categorias · Períodos · Ranking · Veículos`, **sem "Sair"**),
divergindo das rotas `/` e `/loja`, que mostravam corretamente o menu de cliente.

**Comportamento esperado:**

| Perfil | Menu correto |
| --- | --- |
| **Cliente** | Meu Painel · Loja Sustentável · Ranking · Sair |
| **Admin** | Dashboard · Categorias · Períodos · Ranking · Veículos · Sair |

---

## 2. 🔍 Diagnóstico (causa raiz)

O `<nav class="navbar">` estava **duplicado e hardcoded em cada template**, gerando **três variações
diferentes** do menu espalhadas pelo projeto:

| Variação | Templates | Itens |
| --- | --- | --- |
| Menu admin fixo | `ranking.html`, `categorias.html`, `periodos.html`, `veiculos.html` | 5 itens, **sem "Sair"** |
| Menu cliente fixo | `loja.html`, `cliente.html` | 4 itens |
| Menu dinâmico (Jinja) | `index.html` | admin/cliente via `session.perfil`, mas com `onclick` (troca de abas) em vez de URLs |

A rota `/ranking` é **liberada para qualquer perfil logado** e sempre renderizava o `ranking.html`,
que continha o menu de admin embutido. Logo, **todo cliente que acessava `/ranking` via o menu de admin** —
não por lógica de perfil, mas porque o HTML do menu era estático naquele arquivo.

### Problemas secundários encontrados durante a análise

- 🔴 **Link quebrado:** "Meu Painel" no `cliente.html` apontava para `/cliente`, **rota que não existe** (404). O painel do cliente é servido em `/`.
- 🔴 **"Sair" ausente** em todas as páginas administrativas (`ranking`, `categorias`, `periodos`, `veiculos`).
- 🟡 **Footers inconsistentes:** presentes em `index`/`ranking`/`periodos`/`categorias`, ausentes em `veiculos`/`loja`/`cliente`, e com **dois textos diferentes**.
- 🟡 **Estilo inline repetido:** o botão "Sair" usava `style="..."` copiado em vários arquivos.

---

## 3. 🛠️ Solução adotada

Centralizar o cabeçalho (navbar) e o rodapé em **dois partials Jinja** dentro de `templates/common/`,
incluídos via `{% include %}` em cada página. O menu passa a ser montado **uma única vez**, decidindo
admin × cliente a partir de `session.perfil`.

### Por que `{% include %}` e não um `base.html` com `{% extends %}`?

| Critério | `{% include %}` (escolhido) | `{% extends %}` (base layout) |
| --- | --- | --- |
| Invasividade | Baixa — troca apenas o `<nav>` e o `<footer>` | Alta — exigiria reescrever `<head>`, blocos de conteúdo e scripts de cada página |
| Risco de regressão | Baixo | Médio/alto (cada página tem `<head>` e `<script>` próprios) |
| Aderência ao pedido | Total ("abstrair header e footer para `templates/common/`") | Parcial |

Como cada template tem `<head>` e scripts específicos (`dashboard.js`, `ranking.js`, etc.), o `include`
é o refator mais seguro e cirúrgico para este momento.

### Por que `app.py` não mudou

O Flask **injeta automaticamente `session` e `request` no contexto de todos os templates Jinja**.
Portanto o header consegue, sozinho:
- decidir o menu (`session.get('perfil')`);
- destacar o item ativo (`request.path`).

Não foi necessário passar variáveis extras em `render_template(...)` nem criar `context_processor`.

---

## 4. 📦 Alterações por arquivo

### Novos arquivos

| Arquivo | Conteúdo |
| --- | --- |
| `templates/common/header.html` | Navbar única. Menu admin/cliente via `session.perfil`; "Sair" para ambos; `active` por `request.path`. |
| `templates/common/footer.html` | Rodapé padronizado (versão "© 2026"). |

**`templates/common/header.html` (núcleo da lógica):**

```jinja
{% set perfil = session.get('perfil') %}
...
{% if perfil == 'admin' %}
    <li><a href="/" class="nav-link {{ 'active' if request.path == '/' }}">Dashboard</a></li>
    ... Categorias / Períodos / Ranking / Veículos ...
{% elif perfil == 'cliente' %}
    <li><a href="/" class="nav-link {{ 'active' if request.path == '/' }}">Meu Painel</a></li>
    ... Loja Sustentável / Ranking ...
{% endif %}
{% if perfil %}
    <li><a href="/logout" class="nav-link nav-logout">Sair 🚪</a></li>
{% endif %}
```

### Arquivos editados

| Arquivo | Mudança |
| --- | --- |
| `templates/index.html` | `<nav>` e `<footer>` → includes. Menu admin deixou de usar `onclick` (troca de aba) e passou a navegar por URLs reais. Ramo "cliente" (código morto) removido. |
| `templates/cliente.html` | `<nav>` → include. Footer adicionado. Corrigido "Meu Painel" (`/cliente` → `/`). |
| `templates/loja.html` | `<nav>` → include. Footer adicionado. |
| `templates/ranking.html` | `<nav>` e `<footer>` → includes (**correção principal do bug**). |
| `templates/categorias.html` | `<nav>` e `<footer>` → includes. |
| `templates/periodos.html` | `<nav>` e `<footer>` → includes. |
| `templates/veiculos.html` | `<nav>` → include. Footer adicionado. |
| `static/style.css` | Nova classe `.nav-logout` (substitui o `style="..."` inline repetido). |

> `login.html`, `404.html`, `500.html` ficaram **fora de escopo** (não têm navbar de sessão).
> `app.py` permaneceu **inalterado**.

---

## 5. ✅ Verificação realizada

Servidor iniciado localmente (`http://127.0.0.1:5000`) e validado via login real de cliente e admin:

| Verificação | Resultado |
| --- | --- |
| Cliente em `/`, `/loja`, `/ranking` → mesmo menu (Meu Painel · Loja · Ranking · Sair) | ✅ |
| Admin em `/`, `/ranking`, `/categorias`, `/veiculos` → Dashboard · Categorias · Períodos · Ranking · Veículos · **Sair** | ✅ |
| Item ativo correto por página (`/ranking`→Ranking, `/loja`→Loja) | ✅ |
| "Meu Painel" aponta para `/` (sem 404) | ✅ |
| "Sair" presente nas páginas de admin (antes ausente) | ✅ |
| Regressão de acesso: cliente em `/categorias` → redirect `/login` | ✅ |
| Regressão de acesso: admin em `/loja` → redirect `/` | ✅ |
| Footer presente e idêntico em todas as páginas com sessão | ✅ |

---

## 6. 📈 Ganhos

- **Bug corrigido na origem:** `/ranking` (e qualquer outra página) agora reflete o perfil real do usuário.
- **DRY / fonte única de verdade:** 1 navbar + 1 footer em vez de ~7 cópias divergentes. Mudanças futuras no menu são feitas em **um só lugar**.
- **Bugs adicionais resolvidos de brinde:** link "Meu Painel" quebrado, "Sair" ausente no admin, footers inconsistentes.
- **Menos CSS inline:** estilo do logout centralizado em `.nav-logout`.
- **Estado ativo sem depender de JS:** o destaque do item atual vem do servidor (`request.path`), funcionando mesmo com JavaScript desabilitado.
- **Consistência de UX:** navegação por URLs reais em todas as páginas (inclusive no dashboard do admin).

## 7. ⚠️ Perdas / Trade-offs

- **Mudança de comportamento no dashboard admin (`index.html`):** os itens do menu superior (Categorias, Períodos, Ranking, Veículos) antes faziam *scroll/foco* em gráficos da própria página (`focarElementoAdmin`/`alternarAba`); **agora navegam para as páginas dedicadas** (`/categorias`, etc.). É uma melhoria de consistência, mas é uma alteração de UX que deve ser comunicada.
  - As funções JS `focarElementoAdmin`, `alternarAba`, `mostrarRankingNoCliente` e `mostrarLojaNoCliente` podem ter ficado **sem uso pelo menu** (a `tabs-container` interna do dashboard, independente do navbar, foi preservada). Vale uma limpeza futura no `dashboard.js` se confirmado que não são mais chamadas.
- **Acoplamento ao `session` no template:** o partial lê `session` diretamente. É idiomático em Flask, mas significa que páginas renderizadas **sem sessão** mostrarão apenas o "Sair" oculto e nenhum item — comportamento correto, mas é preciso ter ciência.

---

## 8. 🧭 Cuidados futuros (recomendações ao desenvolvedor original)

1. **Nunca duplicar HTML estrutural entre páginas.** Header, footer, navbar e blocos repetidos devem viver em `templates/common/` e ser incluídos. Este bug existiu **porque o menu era copiado em cada arquivo**.
2. **A autorização é do backend, a exibição é do template — e ambas devem concordar.** A rota `/ranking` libera os dois perfis (correto), mas o template precisava refletir isso. Sempre que uma rota servir múltiplos perfis, garanta que o template **não** assuma um perfil fixo.
3. **Evite estilos inline (`style="..."`) repetidos.** Eles fogem do controle do CSS e divergem com o tempo. Prefira classes (`.nav-logout`).
4. **Considere evoluir para um `base.html` com `{% extends %}`** quando houver tempo. Centralizaria também `<head>`, importação de CSS/JS e metadados, eliminando mais duplicação (hoje cada página repete `<head>` e CDNs).
5. **Padronize a marca:** há divergência de capitalização do logo entre arquivos ("Ecometric" vs "ECOMETRIC"). O header único já resolve isso — mantenha um único texto.
6. **Não confie só no JS para estado de navegação/segurança.** O destaque `active` agora é server-side; mantenha essa abordagem para robustez.
7. **Rotas e links devem ser verificados de ponta a ponta.** O link `/cliente` apontava para uma rota inexistente. Um teste simples de "todas as âncoras retornam 2xx/302 esperado" pegaria isso.

### 🐞 Pendência conhecida (fora do escopo desta entrega)

- **`app.py` quebra ao iniciar no console do Windows (cp1252)** por causa de `print()` com emoji (`🌱`) — `UnicodeEncodeError`. Na verificação foi contornado com `PYTHONUTF8=1`. **Correção recomendada:** definir `PYTHONUTF8=1` no ambiente, ou remover/escapar os emojis dos `print()` de inicialização, ou forçar `sys.stdout.reconfigure(encoding='utf-8')` no topo do `app.py`.

---

## 9. 📂 Resumo dos arquivos tocados

```
templates/
├── common/
│   ├── header.html   (novo)
│   └── footer.html   (novo)
├── index.html        (editado)
├── cliente.html      (editado)
├── loja.html         (editado)
├── ranking.html      (editado)
├── categorias.html   (editado)
├── periodos.html     (editado)
└── veiculos.html     (editado)
static/
└── style.css         (editado — classe .nav-logout)
app.py                (inalterado)
```
