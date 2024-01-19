import sqlalchemy
from llama_index import SQLDatabase, SimpleDirectoryReader, WikipediaReader, Document
from llama_index.indices.struct_store import (
    NLSQLTableQueryEngine,
    SQLTableRetrieverQueryEngine,
)