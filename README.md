# Fatture in Cloud MCP Server

Server MCP (Model Context Protocol) per gestire [Fatture in Cloud](https://www.fattureincloud.it/) direttamente da Claude, Cursor, Windsurf e qualsiasi client MCP compatibile.

Costruito con [FastMCP](https://gofastmcp.com/).

## Come funziona

Parli con Claude in linguaggio naturale e lui gestisce Fatture in Cloud per te:

```
Tu:     "Mostrami le fatture di questo mese"
Claude:  chiama list_issued_documents e ti mostra i risultati

Tu:     "Crea una fattura per Mario Rossi, consulenza SEO, 800 euro"
Claude:  chiama create_issued_document con i dati corretti

Tu:     "Invia la fattura 12345 allo SDI"
Claude:  chiama send_einvoice e la fattura elettronica parte
```

## Guida all'installazione (passo passo)

### Passo 1: Installa Python e FastMCP

Serve Python 3.10 o superiore. Verifica con:

```bash
python3 --version
```

Poi installa FastMCP:

```bash
pip install fastmcp
```

### Passo 2: Scarica il server

```bash
git clone https://github.com/matteomilonekr/fic-mcp.git
```

Oppure scarica direttamente il file `server.py` dal repository.

### Passo 3: Ottieni il token API da Fatture in Cloud

1. Vai su [secure.fattureincloud.it](https://secure.fattureincloud.it) e accedi
2. Clicca sull'icona ingranaggio in alto a destra per andare nelle **Impostazioni**
3. Nella barra laterale, clicca su **Sviluppatori**
4. Se non hai ancora un'app, clicca su **Crea applicazione**
   - Dai un nome (es. "MCP Server")
   - Nella sezione Autenticazione, attiva **Token Manuale**
   - Clicca **Salva**
5. Clicca su **Gestisci** accanto alla tua app
6. Scorri fino alla sezione **Token Manuali**
7. Clicca **Genera nuovo token**
8. Seleziona i permessi (scope) che ti servono:
   - Per iniziare, seleziona almeno: `entity.clients:r`, `issued_documents.invoices:r`
   - Se vuoi anche creare fatture: `issued_documents.invoices:a`
   - Se vuoi gestire tutto: seleziona tutti gli scope con `:a`
9. Seleziona l'azienda su cui vuoi operare
10. Clicca **Genera**
11. **Copia il token** (viene mostrato solo una volta)

### Passo 4: Trova il tuo Company ID

Il Company ID lo trovi nella URL di Fatture in Cloud quando sei loggato. Guarda nella barra degli indirizzi del browser:

```
https://secure.fattureincloud.it/dashboard/XXXXXX
                                              ^^^^^^
                                          questo è il tuo Company ID
```

Oppure, dopo aver configurato il token, puoi usare il tool `list_companies` che te lo mostrerà.

### Passo 5: Configura le variabili ambiente

Su **Mac/Linux**, apri il terminale e scrivi:

```bash
export FIC_ACCESS_TOKEN="incolla-qui-il-tuo-token"
export FIC_COMPANY_ID="12345"
```

Per renderle permanenti, aggiungile al file `~/.zshrc` (Mac) o `~/.bashrc` (Linux):

```bash
echo 'export FIC_ACCESS_TOKEN="il-tuo-token"' >> ~/.zshrc
echo 'export FIC_COMPANY_ID="12345"' >> ~/.zshrc
source ~/.zshrc
```

Su **Windows** (PowerShell):

```powershell
$env:FIC_ACCESS_TOKEN = "il-tuo-token"
$env:FIC_COMPANY_ID = "12345"
```

### Passo 6: Connetti a Claude

#### Opzione A: Claude Code (terminale)

```bash
claude mcp add fatture-in-cloud \
  -e FIC_ACCESS_TOKEN="il-tuo-token" \
  -e FIC_COMPANY_ID="12345" \
  -- python3 /percorso/completo/fic-mcp/server.py
```

Sostituisci `/percorso/completo/` con il percorso dove hai scaricato il repository.

#### Opzione B: Claude Desktop (app)

1. Apri Claude Desktop
2. Vai su **Impostazioni > Sviluppatore > Modifica configurazione**
3. Si apre il file `claude_desktop_config.json`
4. Aggiungi questa sezione dentro `mcpServers`:

```json
{
  "mcpServers": {
    "fatture-in-cloud": {
      "command": "python3",
      "args": ["/percorso/completo/fic-mcp/server.py"],
      "env": {
        "FIC_ACCESS_TOKEN": "il-tuo-token",
        "FIC_COMPANY_ID": "12345"
      }
    }
  }
}
```

5. Salva e riavvia Claude Desktop

#### Opzione C: Cursor / Windsurf

Segui la documentazione del tuo editor per aggiungere server MCP. La configurazione è simile a Claude Desktop: servono il comando `python3`, il percorso al file `server.py`, e le due variabili ambiente.

### Passo 7: Verifica che funzioni

Apri Claude e prova a chiedere:

```
Mostrami le informazioni della mia azienda su Fatture in Cloud
```

Se tutto è configurato correttamente, Claude userà il tool `get_company_info` e ti mostrerà i dati della tua azienda.

## Cosa puoi fare (60 tool)

### Clienti e fornitori
- "Cerca il cliente Rossi"
- "Crea un nuovo cliente: Mario Bianchi, P.IVA 12345678901"
- "Modifica l'email del cliente 456"
- "Lista tutti i fornitori"

### Fatture e documenti
- "Mostrami le fatture di questo mese"
- "Crea una fattura per il cliente 123: Consulenza marketing, 1500 euro"
- "Quanto verrebbe il totale con IVA per 3 ore di consulenza a 80 euro?"
- "Trasforma il preventivo 789 in fattura"
- "Mostrami i preventivi in attesa"

### Fattura elettronica
- "Verifica l'XML della fattura 456 prima di inviarla"
- "Fai un test di invio SDI (dry run) sulla fattura 456"
- "Invia la fattura 456 allo SDI"
- "Perché la fattura 321 è stata rifiutata dallo SDI?"

### Prodotti
- "Lista i prodotti nel catalogo"
- "Crea un prodotto: Consulenza SEO, 150 euro all'ora"

### Contabilità
- "Mostrami la prima nota di marzo"
- "Quali sono i miei metodi di pagamento?"
- "Lista i corrispettivi"
- "Mostrami gli F24"

### Info di sistema
- "Quali tipi IVA ho configurati?"
- "Lista le valute disponibili"
- "Mostrami il profilo fiscale dell'azienda"

## Tabella completa dei tool

| Area | N. | Tool disponibili |
|------|----|-----------------|
| Account | 4 | `get_user_info`, `list_companies`, `get_company_info`, `get_company_plan_usage` |
| Clienti | 6 | `list_clients`, `get_client`, `create_client`, `modify_client`, `delete_client` |
| Fornitori | 4 | `list_suppliers`, `get_supplier`, `create_supplier`, `delete_supplier` |
| Prodotti | 4 | `list_products`, `get_product`, `create_product`, `delete_product` |
| Fatture | 9 | `list_issued_documents`, `get_issued_document`, `create_issued_document`, `modify_issued_document`, `delete_issued_document`, `get_issued_document_precreate_info`, `get_new_document_totals`, `transform_document` |
| E-fattura | 4 | `send_einvoice`, `verify_einvoice_xml`, `get_einvoice_xml`, `get_einvoice_rejection_reason` |
| Email | 3 | `get_document_email_data`, `send_document_email`, `list_emails` |
| Doc. ricevuti | 4 | `list_received_documents`, `get_received_document`, `create_received_document`, `delete_received_document` |
| Prima nota | 3 | `list_cashbook`, `create_cashbook_entry`, `delete_cashbook_entry` |
| Archivio | 4 | `list_archive`, `get_archive_document`, `create_archive_document`, `delete_archive_document` |
| F24 | 3 | `list_taxes`, `get_tax`, `delete_tax` |
| Corrispettivi | 2 | `list_receipts`, `get_receipt` |
| Webhooks | 3 | `list_webhooks`, `create_webhook`, `delete_webhook` |
| Info sistema | 8 | `list_vat_types`, `list_payment_methods`, `list_payment_accounts`, `list_product_categories`, `list_countries`, `list_currencies`, `list_languages`, `list_units_of_measure` |
| Impostazioni | 1 | `get_tax_profile` |

## Scope API necessari

Configura solo gli scope che ti servono (Principio del Minimo Privilegio):

| Cosa vuoi fare | Scope necessario |
|----------------|-----------------|
| Vedere i clienti | `entity.clients:r` |
| Creare/modificare clienti | `entity.clients:a` |
| Vedere le fatture | `issued_documents.invoices:r` |
| Creare/inviare fatture | `issued_documents.invoices:a` |
| Vedere i preventivi | `issued_documents.quotes:r` |
| Vedere i fornitori | `entity.suppliers:r` |
| Vedere i prodotti | `products:r` |
| Creare prodotti | `products:a` |
| Prima nota | `cashbook:r` (lettura) o `cashbook:a` (scrittura) |
| Documenti ricevuti | `received_documents:r` o `received_documents:a` |
| F24 | `taxes:r` o `taxes:a` |
| Impostazioni | `settings:r` |

## Risoluzione problemi

**"FIC_ACCESS_TOKEN non configurato"**
Le variabili ambiente non sono state impostate. Segui il Passo 5.

**Errore 401 (Unauthorized)**
Il token è scaduto, non valido o revocato. Genera un nuovo token dal Passo 3.

**Errore 403 (Forbidden)**
Il token non ha i permessi necessari. Verifica gli scope configurati.

**Errore 404 (Not Found)**
L'ID del documento, cliente o risorsa non esiste. Verifica l'ID.

**Errore 429 (Too Many Requests)**
Hai superato i limiti API. Aspetta qualche secondo e riprova.

**"FIC_COMPANY_ID non configurato"**
Chiedi a Claude "Mostrami le aziende collegate al mio account" per trovare il tuo Company ID, poi configuralo nel Passo 5.

## Avviso legale

Questo progetto utilizza le [API v2 di Fatture in Cloud](https://developers.fattureincloud.it/) nel rispetto delle [Condizioni Generali di Utilizzo delle API TeamSystem](https://developers.fattureincloud.it/docs/legal/terms/).

- Questo software **NON è affiliato** a TeamSystem S.p.A. o a Fatture in Cloud
- "Fatture in Cloud" è un marchio registrato di TeamSystem S.p.A.
- Ogni utente deve utilizzare il proprio account e il proprio Access Token
- L'utilizzo è riservato ad attività professionali e imprenditoriali
- Alcune funzionalità richiedono un piano a pagamento su Fatture in Cloud

Per i dettagli completi, consulta [LICENSE](LICENSE) e [LEGAL_NOTICE.md](LEGAL_NOTICE.md).
