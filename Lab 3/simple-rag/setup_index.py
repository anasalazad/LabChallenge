"""Optional helper (my addition): create the Pinecone index if it doesn't exist yet.

Same settings as section 5 of the sheet: dense, dimension 1024, cosine. (You can also click
"Create index" in the Pinecone console instead - that's what the sheet shows.)

    python setup_index.py
"""
import os
import time

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()
name = os.environ["PINECONE_INDEX"]
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

if pc.has_index(name):
    print(f"Index '{name}' already exists - nothing to do.")
else:
    print(f"Creating index '{name}' (dense, 1024 dims, cosine, AWS us-east-1 - the free Starter plan region)...")
    pc.create_index(name=name, dimension=1024, metric="cosine", vector_type="dense",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    while not pc.describe_index(name).status.ready:
        time.sleep(2)
    print("Ready.")
