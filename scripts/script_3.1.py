"""
Gera embeddings dos produtos e indexa no AI Search com campo vector.
Requer: pip install --user sentence-transformers azure-search-documents azure-storage-blob
"""
import os
import csv
import time

from sentence_transformers import SentenceTransformer
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)
from azure.search.documents import SearchClient
from azure.storage.blob import BlobServiceClient

DIMENSION = 384
INDEX_NAME = "produtos-vector-index"


def main():
    endpoint = os.environ.get("SEARCH_ENDPOINT")
    storage = os.environ.get("STORAGE_ACCOUNT_NAME")

    if not endpoint or not storage:
        raise ValueError(
            "Defina as variáveis de ambiente SEARCH_ENDPOINT e STORAGE_ACCOUNT_NAME antes de executar."
        )

    credential = DefaultAzureCredential()
    print("→ Carregando modelo de embedding...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Baixar produtos do Blob Storage
    blob = BlobServiceClient(f"https://{storage}.blob.core.windows.net", credential=credential)
    blob_client = blob.get_blob_client(container="catalogo", blob="produtos.csv")
    csv_text = blob_client.download_blob().readall().decode("utf-8")
    rows = list(csv.DictReader(csv_text.splitlines()))

    if not rows:
        raise ValueError("O CSV de produtos está vazio ou não foi lido corretamente.")

    required_columns = {"id", "nome", "descricao", "categoria"}
    missing_columns = required_columns - set(rows[0].keys())
    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes no CSV: {sorted(missing_columns)}")

    print("rows:", len(rows))

    # Gerar embeddings de "nome + descricao"
    print(f"→ Gerando embeddings de {len(rows)} produtos...")
    textos = [f"{r['nome']}. {r['descricao']}" for r in rows]
    embeddings = model.encode(textos).tolist()
    print(f"✓ Embeddings gerados (dim={len(embeddings[0])})")

    # Definir índice com campo vector
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    index = SearchIndex(
        name=INDEX_NAME,
        fields=[
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="nome", type=SearchFieldDataType.String),
            SearchableField(name="descricao", type=SearchFieldDataType.String),
            SimpleField(name="categoria", type=SearchFieldDataType.String, filterable=True),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=DIMENSION,
                vector_search_profile_name="produtos-hnsw-profile",
            ),
        ],
        vector_search=VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="produtos-hnsw")],
            profiles=[
                VectorSearchProfile(
                    name="produtos-hnsw-profile",
                    algorithm_configuration_name="produtos-hnsw",
                )
            ],
        ),
    )

    try:
        index_client.delete_index(INDEX_NAME)
    except Exception:
        pass

    index_client.create_index(index)
    print(f"✓ Índice '{INDEX_NAME}' criado.")

    # Indexar documentos
    search_client = SearchClient(endpoint=endpoint, index_name=INDEX_NAME, credential=credential)
    docs = [
        {
            "id": r["id"],
            "nome": r["nome"],
            "descricao": r["descricao"],
            "categoria": r["categoria"],
            "content_vector": embeddings[i],
        }
        for i, r in enumerate(rows)
    ]

    upload_result = search_client.upload_documents(docs)
    for item in upload_result:
        if not item.get("succeeded", False):
            print("Falha no upload:", item)

    print(f"✓ Chamada de upload concluída para {len(docs)} documentos.")

    # Aguardar propagação no índice
    count = 0
    for _ in range(10):
        count = search_client.get_document_count()
        print("Documentos no índice:", count)
        if count > 0:
            break
        time.sleep(2)

    if count == 0:
        raise RuntimeError(
            "O índice continua vazio após o upload. Verifique autenticação, permissões e o conteúdo do CSV."
        )

    # Busca por vetor: gerar embedding da query e buscar nearest
    queries = [
        "preciso de uma cadeira boa para minha coluna",
        "algo para acompanhar séries",
        "presente para um amigo que ama café",
    ]

    for q in queries:
        q_vec = model.encode(q).tolist()
        print(f"\n=== Vector search: '{q}' ===")
        results = search_client.search(
            search_text=None,
            vector_queries=[{
                "kind": "vector",
                "vector": q_vec,
                "k": 3,
                "fields": "content_vector",
            }],
            select=["id", "nome", "descricao", "categoria"],
        )

        results_list = list(results)
        if not results_list:
            print("  Nenhum resultado encontrado.")
            continue

        for r in results_list:
            print(f"  [{r['@search.score']:.4f}] {r['nome']}")


if __name__ == "__main__":
    main()
