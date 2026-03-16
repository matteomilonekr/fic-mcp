"""Fatture in Cloud MCP Server - Server MCP per le API v2 di Fatture in Cloud."""

import json
import os
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode

from fastmcp import FastMCP

mcp = FastMCP(
    name="Fatture in Cloud",
    instructions="""Server MCP per gestire Fatture in Cloud via API v2.
    Permette di creare, leggere, modificare ed eliminare fatture, clienti,
    fornitori, prodotti e molto altro direttamente da Claude o qualsiasi client MCP.

    Richiede: FIC_ACCESS_TOKEN e FIC_COMPANY_ID come variabili ambiente.
    Il token si ottiene da secure.fattureincloud.it > Impostazioni > Sviluppatori.""",
)

BASE_URL = "https://api-v2.fattureincloud.it"


def _get_token() -> str:
    token = os.environ.get("FIC_ACCESS_TOKEN", "")
    if not token:
        raise ValueError(
            "FIC_ACCESS_TOKEN non configurato. "
            "Imposta la variabile ambiente con il tuo token Fatture in Cloud."
        )
    return token


def _get_company_id() -> str:
    cid = os.environ.get("FIC_COMPANY_ID", "")
    if not cid:
        raise ValueError(
            "FIC_COMPANY_ID non configurato. "
            "Usa il tool list_companies per trovare l'ID, poi imposta FIC_COMPANY_ID."
        )
    return cid


def _api(method: str, path: str, data: dict = None, params: dict = None) -> dict:
    token = _get_token()
    url = f"{BASE_URL}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url += "?" + urlencode(clean)

    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, method=method.upper())
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")

    try:
        with urlopen(req) as resp:
            raw = resp.read().decode()
            return json.loads(raw) if raw else {}
    except HTTPError as e:
        error_body = e.read().decode()
        try:
            err = json.loads(error_body)
        except json.JSONDecodeError:
            err = {"raw_error": error_body}
        return {"error": True, "status_code": e.code, "detail": err}


# ============================================================
# USER & COMPANIES
# ============================================================


@mcp.tool(tags={"user", "account"})
def get_user_info() -> dict:
    """Ottieni le informazioni dell'utente autenticato (nome, email, ecc.)."""
    return _api("GET", "/user/info")


@mcp.tool(tags={"companies", "account"})
def list_companies() -> dict:
    """Lista tutte le aziende collegate all'account.
    Utile per trovare il company_id da usare nelle altre operazioni."""
    return _api("GET", "/user/companies")


@mcp.tool(tags={"companies"})
def get_company_info() -> dict:
    """Ottieni le informazioni dettagliate dell'azienda corrente (nome, P.IVA, indirizzo, piano, ecc.)."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/company/info")


@mcp.tool(tags={"companies"})
def get_company_plan_usage() -> dict:
    """Verifica l'utilizzo del piano corrente (limiti API, funzionalita disponibili)."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/company/plan_usage")


# ============================================================
# CLIENTS
# ============================================================


@mcp.tool(tags={"clients", "entities"})
def list_clients(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
) -> dict:
    """Lista i clienti dell'azienda con paginazione e ricerca.

    Args:
        page: Numero pagina (default: 1)
        per_page: Risultati per pagina (default: 50)
        q: Testo di ricerca (cerca in nome, email, P.IVA)
        sort: Campo di ordinamento (es. 'name', '-name' per decrescente)
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/entities/clients", params={
        "page": page, "per_page": per_page, "q": q, "sort": sort
    })


@mcp.tool(tags={"clients", "entities"})
def get_client(client_id: int) -> dict:
    """Ottieni il dettaglio completo di un cliente specifico.

    Args:
        client_id: ID univoco del cliente
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/entities/clients/{client_id}")


@mcp.tool(tags={"clients", "entities"})
def create_client(
    name: str,
    email: Optional[str] = None,
    vat_number: Optional[str] = None,
    tax_code: Optional[str] = None,
    address_street: Optional[str] = None,
    address_city: Optional[str] = None,
    address_province: Optional[str] = None,
    address_postal_code: Optional[str] = None,
    country: Optional[str] = None,
    certified_email: Optional[str] = None,
    ei_code: Optional[str] = None,
) -> dict:
    """Crea un nuovo cliente nell'anagrafica.

    Args:
        name: Nome o ragione sociale del cliente
        email: Email del cliente
        vat_number: Partita IVA
        tax_code: Codice fiscale
        address_street: Indirizzo (via e numero)
        address_city: Citta
        address_province: Provincia (sigla, es. MI)
        address_postal_code: CAP
        country: Paese (es. Italia)
        certified_email: PEC
        ei_code: Codice destinatario SDI (7 caratteri)
    """
    cid = _get_company_id()
    client_data = {"name": name}
    if email:
        client_data["email"] = email
    if vat_number:
        client_data["vat_number"] = vat_number
    if tax_code:
        client_data["tax_code"] = tax_code
    if address_street:
        client_data["address_street"] = address_street
    if address_city:
        client_data["address_city"] = address_city
    if address_province:
        client_data["address_province"] = address_province
    if address_postal_code:
        client_data["address_postal_code"] = address_postal_code
    if country:
        client_data["country"] = country
    if certified_email:
        client_data["certified_email"] = certified_email
    if ei_code:
        client_data["ei_code"] = ei_code
    return _api("POST", f"/c/{cid}/entities/clients", {"data": client_data})


@mcp.tool(tags={"clients", "entities"})
def modify_client(client_id: int, data_json: str) -> dict:
    """Modifica un cliente esistente.

    Args:
        client_id: ID del cliente da modificare
        data_json: JSON con i campi da aggiornare (es. '{"name":"Nuovo Nome","email":"new@email.com"}')
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("PUT", f"/c/{cid}/entities/clients/{client_id}", {"data": body})


@mcp.tool(tags={"clients", "entities"})
def delete_client(client_id: int) -> dict:
    """Elimina un cliente dall'anagrafica.

    Args:
        client_id: ID del cliente da eliminare
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/entities/clients/{client_id}")
    return {"success": True, "message": f"Cliente {client_id} eliminato"}


# ============================================================
# SUPPLIERS
# ============================================================


@mcp.tool(tags={"suppliers", "entities"})
def list_suppliers(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
) -> dict:
    """Lista i fornitori dell'azienda.

    Args:
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/entities/suppliers", params={
        "page": page, "per_page": per_page, "q": q
    })


@mcp.tool(tags={"suppliers", "entities"})
def get_supplier(supplier_id: int) -> dict:
    """Ottieni il dettaglio di un fornitore.

    Args:
        supplier_id: ID del fornitore
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/entities/suppliers/{supplier_id}")


@mcp.tool(tags={"suppliers", "entities"})
def create_supplier(
    name: str,
    email: Optional[str] = None,
    vat_number: Optional[str] = None,
    tax_code: Optional[str] = None,
) -> dict:
    """Crea un nuovo fornitore.

    Args:
        name: Nome o ragione sociale
        email: Email
        vat_number: Partita IVA
        tax_code: Codice fiscale
    """
    cid = _get_company_id()
    supplier_data = {"name": name}
    if email:
        supplier_data["email"] = email
    if vat_number:
        supplier_data["vat_number"] = vat_number
    if tax_code:
        supplier_data["tax_code"] = tax_code
    return _api("POST", f"/c/{cid}/entities/suppliers", {"data": supplier_data})


@mcp.tool(tags={"suppliers", "entities"})
def delete_supplier(supplier_id: int) -> dict:
    """Elimina un fornitore.

    Args:
        supplier_id: ID del fornitore
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/entities/suppliers/{supplier_id}")
    return {"success": True, "message": f"Fornitore {supplier_id} eliminato"}


# ============================================================
# PRODUCTS
# ============================================================


@mcp.tool(tags={"products"})
def list_products(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
) -> dict:
    """Lista i prodotti/servizi del catalogo.

    Args:
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/products", params={
        "page": page, "per_page": per_page, "q": q
    })


@mcp.tool(tags={"products"})
def get_product(product_id: int) -> dict:
    """Ottieni il dettaglio di un prodotto/servizio.

    Args:
        product_id: ID del prodotto
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/products/{product_id}")


@mcp.tool(tags={"products"})
def create_product(
    name: str,
    code: Optional[str] = None,
    net_price: Optional[float] = None,
    net_cost: Optional[float] = None,
    measure: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """Crea un nuovo prodotto/servizio nel catalogo.

    Args:
        name: Nome del prodotto/servizio
        code: Codice prodotto
        net_price: Prezzo netto di vendita
        net_cost: Costo netto
        measure: Unita di misura (es. 'pz', 'ore', 'kg')
        description: Descrizione
    """
    cid = _get_company_id()
    product_data = {"name": name}
    if code:
        product_data["code"] = code
    if net_price is not None:
        product_data["net_price"] = net_price
    if net_cost is not None:
        product_data["net_cost"] = net_cost
    if measure:
        product_data["measure"] = measure
    if description:
        product_data["description"] = description
    return _api("POST", f"/c/{cid}/products", {"data": product_data})


@mcp.tool(tags={"products"})
def delete_product(product_id: int) -> dict:
    """Elimina un prodotto dal catalogo.

    Args:
        product_id: ID del prodotto
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/products/{product_id}")
    return {"success": True, "message": f"Prodotto {product_id} eliminato"}


# ============================================================
# ISSUED DOCUMENTS (fatture, preventivi, ordini, ecc.)
# ============================================================


@mcp.tool(tags={"invoices", "documents"})
def list_issued_documents(
    doc_type: str = "invoice",
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
    sort: Optional[str] = None,
) -> dict:
    """Lista i documenti emessi (fatture, preventivi, ordini, ecc.).

    Args:
        doc_type: Tipo documento. Valori: invoice, credit_note, quote, proforma, receipt, delivery_note, order, work_report, supplier_order, self_invoice
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
        sort: Ordinamento (es. 'date', '-date')
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents", params={
        "type": doc_type, "page": page, "per_page": per_page, "q": q, "sort": sort
    })


@mcp.tool(tags={"invoices", "documents"})
def get_issued_document(document_id: int) -> dict:
    """Ottieni il dettaglio completo di un documento emesso (fattura, preventivo, ecc.).

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/{document_id}")


@mcp.tool(tags={"invoices", "documents"})
def create_issued_document(data_json: str) -> dict:
    """Crea un nuovo documento emesso (fattura, preventivo, ordine, ecc.).

    Args:
        data_json: JSON completo del documento. Esempio minimo per fattura:
            {"type":"invoice","entity":{"name":"Mario Rossi","vat_number":"IT12345678901"},
             "items_list":[{"name":"Consulenza","net_price":500,"qty":1}]}
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/issued_documents", {"data": body})


@mcp.tool(tags={"invoices", "documents"})
def modify_issued_document(document_id: int, data_json: str) -> dict:
    """Modifica un documento emesso esistente.

    Args:
        document_id: ID del documento
        data_json: JSON con i campi da aggiornare
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("PUT", f"/c/{cid}/issued_documents/{document_id}", {"data": body})


@mcp.tool(tags={"invoices", "documents"})
def delete_issued_document(document_id: int) -> dict:
    """Elimina un documento emesso.

    Args:
        document_id: ID del documento da eliminare
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/issued_documents/{document_id}")
    return {"success": True, "message": f"Documento {document_id} eliminato"}


@mcp.tool(tags={"invoices", "email"})
def get_document_email_data(document_id: int) -> dict:
    """Ottieni i dati precompilati per inviare un documento via email.

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/{document_id}/email")


@mcp.tool(tags={"invoices", "email"})
def send_document_email(document_id: int, data_json: str) -> dict:
    """Invia un documento via email al destinatario.

    Args:
        document_id: ID del documento
        data_json: JSON con dati email. Esempio: {"recipient_email":"cliente@email.com","subject":"Fattura","body":"In allegato la fattura"}
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/issued_documents/{document_id}/email", {"data": body})


@mcp.tool(tags={"invoices", "einvoice"})
def send_einvoice(document_id: int, dry_run: bool = False) -> dict:
    """Invia una fattura elettronica allo SDI (Sistema di Interscambio).

    Args:
        document_id: ID della fattura da inviare
        dry_run: Se True, esegue solo una simulazione senza invio reale (utile per test)
    """
    cid = _get_company_id()
    body = {"data": {"send_options": {"dry_run": dry_run}}}
    return _api("POST", f"/c/{cid}/issued_documents/{document_id}/e_invoice/send", body)


@mcp.tool(tags={"invoices", "einvoice"})
def get_einvoice_xml(document_id: int) -> dict:
    """Ottieni l'XML della fattura elettronica per verifica.

    Args:
        document_id: ID della fattura
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/{document_id}/e_invoice/xml")


@mcp.tool(tags={"invoices", "einvoice"})
def verify_einvoice_xml(document_id: int) -> dict:
    """Verifica la correttezza dell'XML della fattura elettronica prima dell'invio.

    Args:
        document_id: ID della fattura
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/{document_id}/e_invoice/verify")


@mcp.tool(tags={"invoices", "einvoice"})
def get_einvoice_rejection_reason(document_id: int) -> dict:
    """Ottieni il motivo di rifiuto di una fattura elettronica respinta dallo SDI.

    Args:
        document_id: ID della fattura
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/{document_id}/e_invoice/rejection_reason")


@mcp.tool(tags={"invoices", "documents"})
def get_issued_document_precreate_info() -> dict:
    """Ottieni informazioni utili per la creazione di un documento (numerazione, default, ecc.)."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/info")


@mcp.tool(tags={"invoices", "totals"})
def get_new_document_totals(data_json: str) -> dict:
    """Calcola i totali di un nuovo documento prima di crearlo.

    Args:
        data_json: JSON con i dati del documento (items_list, entity, ecc.)
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/issued_documents/totals", {"data": body})


@mcp.tool(tags={"invoices", "transform"})
def transform_document(original_document_id: int, new_type: str) -> dict:
    """Trasforma un documento in un altro tipo (es. preventivo in fattura).

    Args:
        original_document_id: ID del documento originale
        new_type: Nuovo tipo (invoice, credit_note, quote, proforma, receipt, delivery_note, order)
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/issued_documents/transform", params={
        "original_document_id": original_document_id, "new_type": new_type
    })


# ============================================================
# RECEIVED DOCUMENTS
# ============================================================


@mcp.tool(tags={"received", "documents"})
def list_received_documents(
    doc_type: str = "expense",
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
) -> dict:
    """Lista i documenti ricevuti (spese, note di credito passive, ecc.).

    Args:
        doc_type: Tipo documento. Valori: expense, passive_credit_note, passive_delivery_note
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/received_documents", params={
        "type": doc_type, "page": page, "per_page": per_page, "q": q
    })


@mcp.tool(tags={"received", "documents"})
def get_received_document(document_id: int) -> dict:
    """Ottieni il dettaglio di un documento ricevuto.

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/received_documents/{document_id}")


@mcp.tool(tags={"received", "documents"})
def create_received_document(data_json: str) -> dict:
    """Registra un nuovo documento ricevuto (spesa).

    Args:
        data_json: JSON del documento ricevuto
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/received_documents", {"data": body})


@mcp.tool(tags={"received", "documents"})
def delete_received_document(document_id: int) -> dict:
    """Elimina un documento ricevuto.

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/received_documents/{document_id}")
    return {"success": True, "message": f"Documento ricevuto {document_id} eliminato"}


# ============================================================
# CASHBOOK (Prima Nota)
# ============================================================


@mcp.tool(tags={"cashbook", "accounting"})
def list_cashbook(
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    year: Optional[str] = None,
) -> dict:
    """Lista i movimenti di prima nota.

    Args:
        date_from: Data inizio filtro (formato YYYY-MM-DD)
        date_to: Data fine filtro (formato YYYY-MM-DD)
        year: Anno (es. '2026')
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/cashbook", params={
        "date_from": date_from, "date_to": date_to, "year": year
    })


@mcp.tool(tags={"cashbook", "accounting"})
def create_cashbook_entry(data_json: str) -> dict:
    """Crea un nuovo movimento di prima nota.

    Args:
        data_json: JSON del movimento
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/cashbook", {"data": body})


@mcp.tool(tags={"cashbook", "accounting"})
def delete_cashbook_entry(entry_id: int) -> dict:
    """Elimina un movimento di prima nota.

    Args:
        entry_id: ID del movimento
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/cashbook/{entry_id}")
    return {"success": True, "message": f"Movimento {entry_id} eliminato"}


# ============================================================
# ARCHIVE
# ============================================================


@mcp.tool(tags={"archive"})
def list_archive(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
) -> dict:
    """Lista i documenti dell'archivio.

    Args:
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/archive", params={
        "page": page, "per_page": per_page, "q": q
    })


@mcp.tool(tags={"archive"})
def get_archive_document(document_id: int) -> dict:
    """Ottieni un documento dall'archivio.

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/archive/{document_id}")


@mcp.tool(tags={"archive"})
def create_archive_document(data_json: str) -> dict:
    """Crea un nuovo documento nell'archivio.

    Args:
        data_json: JSON del documento
    """
    cid = _get_company_id()
    body = json.loads(data_json)
    return _api("POST", f"/c/{cid}/archive", {"data": body})


@mcp.tool(tags={"archive"})
def delete_archive_document(document_id: int) -> dict:
    """Elimina un documento dall'archivio.

    Args:
        document_id: ID del documento
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/archive/{document_id}")
    return {"success": True, "message": f"Documento archivio {document_id} eliminato"}


# ============================================================
# TAXES (F24)
# ============================================================


@mcp.tool(tags={"taxes", "f24"})
def list_taxes(year: Optional[str] = None) -> dict:
    """Lista i modelli F24.

    Args:
        year: Anno di riferimento (es. '2026')
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/taxes", params={"year": year})


@mcp.tool(tags={"taxes", "f24"})
def get_tax(tax_id: int) -> dict:
    """Ottieni il dettaglio di un modello F24.

    Args:
        tax_id: ID del modello F24
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/taxes/{tax_id}")


@mcp.tool(tags={"taxes", "f24"})
def delete_tax(tax_id: int) -> dict:
    """Elimina un modello F24.

    Args:
        tax_id: ID del modello F24
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/taxes/{tax_id}")
    return {"success": True, "message": f"F24 {tax_id} eliminato"}


# ============================================================
# RECEIPTS (Corrispettivi)
# ============================================================


@mcp.tool(tags={"receipts"})
def list_receipts(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    q: Optional[str] = None,
) -> dict:
    """Lista i corrispettivi.

    Args:
        page: Numero pagina
        per_page: Risultati per pagina
        q: Testo di ricerca
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/receipts", params={
        "page": page, "per_page": per_page, "q": q
    })


@mcp.tool(tags={"receipts"})
def get_receipt(receipt_id: int) -> dict:
    """Ottieni il dettaglio di un corrispettivo.

    Args:
        receipt_id: ID del corrispettivo
    """
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/receipts/{receipt_id}")


# ============================================================
# WEBHOOKS
# ============================================================


@mcp.tool(tags={"webhooks", "automation"})
def list_webhooks() -> dict:
    """Lista tutte le sottoscrizioni webhook attive."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/subscriptions")


@mcp.tool(tags={"webhooks", "automation"})
def create_webhook(sink: str, event_type: str) -> dict:
    """Crea una nuova sottoscrizione webhook.

    Args:
        sink: URL endpoint che ricevera le notifiche
        event_type: Tipo di evento (es. 'issued_documents.invoices.create', 'entities.clients.update')
    """
    cid = _get_company_id()
    return _api("POST", f"/c/{cid}/subscriptions", {
        "data": {"sink": sink, "event_type": event_type}
    })


@mcp.tool(tags={"webhooks", "automation"})
def delete_webhook(subscription_id: int) -> dict:
    """Elimina una sottoscrizione webhook.

    Args:
        subscription_id: ID della sottoscrizione
    """
    cid = _get_company_id()
    _api("DELETE", f"/c/{cid}/subscriptions/{subscription_id}")
    return {"success": True, "message": f"Webhook {subscription_id} eliminato"}


# ============================================================
# INFO (dati di sistema)
# ============================================================


@mcp.tool(tags={"info", "system"})
def list_vat_types() -> dict:
    """Lista tutti i tipi IVA disponibili per l'azienda."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/info/vat_types")


@mcp.tool(tags={"info", "system"})
def list_payment_methods() -> dict:
    """Lista i metodi di pagamento configurati."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/info/payment_methods")


@mcp.tool(tags={"info", "system"})
def list_payment_accounts() -> dict:
    """Lista i conti di pagamento (banche, casse, ecc.)."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/info/payment_accounts")


@mcp.tool(tags={"info", "system"})
def list_product_categories() -> dict:
    """Lista le categorie prodotto disponibili."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/info/product_categories")


@mcp.tool(tags={"info", "system"})
def list_countries() -> dict:
    """Lista tutti i paesi disponibili."""
    return _api("GET", "/info/countries")


@mcp.tool(tags={"info", "system"})
def list_currencies() -> dict:
    """Lista tutte le valute disponibili."""
    return _api("GET", "/info/currencies")


@mcp.tool(tags={"info", "system"})
def list_languages() -> dict:
    """Lista le lingue disponibili per i documenti."""
    return _api("GET", "/info/languages")


@mcp.tool(tags={"info", "system"})
def list_units_of_measure() -> dict:
    """Lista le unita di misura disponibili."""
    return _api("GET", "/info/measures")


# ============================================================
# EMAILS
# ============================================================


@mcp.tool(tags={"emails"})
def list_emails() -> dict:
    """Lista tutte le email inviate tramite Fatture in Cloud."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/emails")


# ============================================================
# SETTINGS
# ============================================================


@mcp.tool(tags={"settings"})
def get_tax_profile() -> dict:
    """Ottieni il profilo fiscale dell'azienda (regime, tipo soggetto, ecc.)."""
    cid = _get_company_id()
    return _api("GET", f"/c/{cid}/settings/tax_profile")
