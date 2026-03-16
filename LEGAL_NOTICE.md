# Avviso Legale

## Dichiarazione di non affiliazione

Questo progetto ("Fatture in Cloud MCP Server") è un software indipendente che utilizza le API pubbliche v2 di Fatture in Cloud.

**NON è affiliato, associato, autorizzato, approvato o in alcun modo collegato ufficialmente a TeamSystem S.p.A. o a Fatture in Cloud.**

"Fatture in Cloud" è un marchio registrato di TeamSystem S.p.A. (C.F. e P. IVA 01035310414), con sede legale in Via Sandro Pertini, 88 - 61122 Pesaro (PU). Tutti i diritti sul marchio, sul software Fatture in Cloud e sulle relative API sono di esclusiva proprietà di TeamSystem S.p.A.

## Termini di utilizzo delle API

L'utilizzo delle API di Fatture in Cloud tramite questo software è soggetto alle seguenti condizioni stabilite da TeamSystem S.p.A.:

1. **Condizioni Generali di Utilizzo delle API TeamSystem**
   https://developers.fattureincloud.it/docs/legal/terms/

2. **Policy di Acceptable Use**
   https://developers.fattureincloud.it/docs/legal/policy-acceptable-use/

3. **Marketing Resources and Identity Guidelines**
   https://developers.fattureincloud.it/docs/legal/marketing-resources-and-identity-guidelines/

L'Utente è tenuto a leggere, comprendere e accettare tutti i documenti sopra elencati prima di utilizzare questo software.

## Obblighi dell'utente

Ai sensi delle Condizioni Generali di Utilizzo delle API TeamSystem:

### Account e credenziali (par. 2.1, 2.6, 2.7)

- Ogni utente deve possedere un **proprio account Fatture in Cloud** con piano attivo
- Ogni utente deve generare il **proprio Access Token** API
- È vietato condividere token tra utenti diversi
- L'Access Token è un dato sensibile: non deve essere condiviso, pubblicato in repository pubblici, o incluso nel codice sorgente

### Destinazione d'uso (par. 2.6, 2.7)

Questo software può essere utilizzato **esclusivamente** nell'ambito della propria attività imprenditoriale, artigianale, commerciale o professionale.

L'utilizzo da parte di consumatori ai sensi della normativa a tutela dei consumatori è espressamente escluso.

### Scope e permessi

L'utente deve configurare solo gli scope API strettamente necessari, in conformità con il [Principio del Minimo Privilegio](https://developers.fattureincloud.it/docs/general-knowledge/principle-of-least-privilege/).

### Limiti e quote

L'utente deve rispettare i limiti di utilizzo delle API come descritto nella [documentazione ufficiale](https://developers.fattureincloud.it/docs/basics/limits-and-quotas/). In caso di errore 429 (Too Many Requests), rispettare l'header `Retry-After`.

### Funzionalità a pagamento

Alcune funzionalità (come l'invio della fattura elettronica allo SDI tramite il tool `send_einvoice`) richiedono un piano a pagamento su Fatture in Cloud. Questo software non bypassa tali limitazioni.

## Proprietà intellettuale (par. 3)

- Tutti i diritti di proprietà intellettuale sulle API, sui Software Fatture in Cloud e sulla relativa documentazione sono e rimangono di esclusiva titolarità di TeamSystem S.p.A.
- Il codice sorgente di questo server MCP è di proprietà di Matteo Milone ed è distribuito secondo la licenza contenuta nel file LICENSE
- La licenza di questo software NON si estende alle API, al software Fatture in Cloud, ai marchi o a qualsiasi altra proprietà intellettuale di TeamSystem S.p.A.

## Limitazioni di responsabilità (par. 5)

- L'autore di questo software non è responsabile per eventuali danni derivanti dall'uso o dal mancato uso di questo software
- TeamSystem S.p.A. non è responsabile per questo software e non fornisce supporto per esso
- Ai sensi del paragrafo 5.7 delle Condizioni Generali, la responsabilità di TeamSystem nei confronti dello sviluppatore non può eccedere Euro 300,00
- Per problemi relativi alle API di Fatture in Cloud, consultare la [documentazione ufficiale](https://developers.fattureincloud.it/) o contattare il [supporto di Fatture in Cloud](https://developers.fattureincloud.it/docs/support/)

## Riservatezza (par. 12)

Le informazioni relative alle API sono considerate riservate e confidenziali ai sensi delle Condizioni Generali. Questo software utilizza esclusivamente le API pubblicamente documentate e non divulga informazioni riservate.

## Modifiche ai termini (par. 9)

TeamSystem S.p.A. si riserva il diritto di modificare in qualsiasi momento le Condizioni Generali e la Policy di Acceptable Use. L'utente è responsabile di verificare periodicamente eventuali aggiornamenti ai termini di servizio.

## Sospensione e interruzione (par. 6)

TeamSystem S.p.A. può sospendere o interrompere l'accesso alle API in qualsiasi momento per motivi tecnici, di sicurezza, per ordine dell'autorità, o in caso di violazione dei termini. In tali casi, il software potrebbe cessare di funzionare parzialmente o completamente.

## Contatti

Per domande relative a questo software: [GitHub Issues](https://github.com/matteomilonekr/fic-mcp/issues)

Per domande relative alle API Fatture in Cloud: [Supporto Fatture in Cloud](https://developers.fattureincloud.it/docs/support/)
