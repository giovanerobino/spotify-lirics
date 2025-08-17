# spotify-lyrics

Discover the lyrics of your favorite songs instantly with this Spotify-integrated Python script. As you listen, it fetches and displays the lyrics of the currently playing song in real time.

Script em Python que mostra a faixa que você está ouvindo no Spotify e busca a letra no Genius (API + scraping como fallback).

## Recursos

- Detecta a música atual da sua conta Spotify.
- Busca letra via API do Genius.
- Faz scraping caso a API não retorne a letra completa.
- Tipagem estática (Pyright strict) configurada.

## Requisitos

- Python 3.10+
- Conta Spotify (para OAuth) e app registrado em <https://developer.spotify.com/dashboard>
- Token de acesso do Genius: <https://genius.com/api-clients>

## Instalação

Crie e ative um ambiente virtual (exemplo Windows bash Git):

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Ou usando `pyproject.toml`:

```bash
pip install -e .
```

## Variáveis de Ambiente (.env)

Crie um arquivo `.env` na raiz:

```dotenv
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
GENIUS_ACCESS_TOKEN=seu_token_genius
```

Certifique-se de que a redirect URI cadastrada no app Spotify inclui:

```text
http://localhost:8888/callback
```

## Uso

Execute:

```bash
python spotify_lyrics.py
```

Na primeira execução abrirá o fluxo OAuth no navegador. Após autorizar, o script exibirá algo como:

```text
Tocando agora: Artista - Faixa
<letra>
```

Se nenhuma música estiver tocando: "Nenhuma música tocando no momento.".

## Tipagem / Qualidade

Rodar análise estática:

```bash
pyright
```

(Se não tiver instalado globalmente: `pip install pyright`.)

## Troubleshooting

| Problema | Causa comum | Solução |
|----------|-------------|---------|
| RuntimeError credenciais ausentes | .env não carregado | Verifique nomes das variáveis e uso de `python-dotenv` |
| Abre navegador mas falha callback | Redirect URI divergente | Ajuste no dashboard Spotify |
| "Letra não encontrada" | Música não localizada / proteção anti-scrape | Tente outra faixa, verifique se a letra existe no Genius |
| Timeout em requests | Conexão lenta | Aumente timeout ou tente novamente |

## Próximos Passos (Ideias)

- Cache de letras em arquivo local.
- Interface simples (Tkinter ou web Flask).
- Tradução automática opcional.
- Suporte a histórico de faixas recentes.

## Licença

Uso pessoal/didático. Adapte conforme necessário.
