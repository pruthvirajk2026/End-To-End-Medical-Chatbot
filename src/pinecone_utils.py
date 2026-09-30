import os
from urllib.parse import urlsplit

import pinecone
from pinecone.core.client.configuration import Configuration


def get_pinecone_index_name():
    index_name = os.environ.get("PINECONE_INDEX", "").strip()
    if not index_name:
        raise RuntimeError("PINECONE_INDEX is not set.")
    return index_name


def initialize_pinecone(index_name):
    api_key = os.environ.get("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY is not set.")

    configured_host = os.environ.get("PINECONE_HOST", "").strip().strip("\"'")
    if not configured_host:
        raise RuntimeError("PINECONE_HOST is not set in the environment or .env file.")

    host_url = configured_host if "://" in configured_host else f"https://{configured_host}"
    parsed_host = urlsplit(host_url)
    if (
        parsed_host.scheme != "https"
        or not parsed_host.hostname
        or parsed_host.username
        or parsed_host.password
        or parsed_host.path not in ("", "/")
        or parsed_host.query
        or parsed_host.fragment
    ):
        raise ValueError(
            "PINECONE_HOST must be the HTTPS host shown for the Pinecone index, "
            "without a path, query, or fragment."
        )

    hostname_prefix = parsed_host.hostname.split(".", 1)[0].lower()
    normalized_index_name = index_name.lower()
    if not (
        hostname_prefix == normalized_index_name
        or hostname_prefix.startswith(f"{normalized_index_name}-")
    ):
        raise ValueError(
            f"PINECONE_HOST does not appear to belong to index {index_name!r}. "
            "Copy the Host from that exact index's details page."
        )

    pinecone.init(
        api_key=api_key,
        openapi_config=Configuration(host=f"https://{parsed_host.netloc}"),
    )
