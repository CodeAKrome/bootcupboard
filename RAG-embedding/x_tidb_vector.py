import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.tidb import TiDB
from tidb_vector.integrations import TiDBVectorClient
from PIL import Image


TESTDB_NAME = "test"
PASS = os.getenv("TIDB_PASS")

# db = TiDB(password=PASS, database=TESTDB_NAME)
db = TiDB(password=PASS)
db.execute_query(f"DROP DATABASE IF EXISTS {TESTDB_NAME}")
db.execute_query(f"CREATE DATABASE IF NOT EXISTS {TESTDB_NAME}")
sql="""
CREATE TABLE vector_table_with_index (
    id INT PRIMARY KEY, doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
);
"""
# ---

import torch
from transformers import CLIPProcessor, CLIPModel

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def images_to_embeddings(images):
    # accept a list of images and return the image embeddings
    with torch.no_grad():
        inputs = processor(images=images, return_tensors="pt")
        image_features = model.get_image_features(**inputs)
        return image_features.cpu().detach().numpy()

def text_to_embedding(text):
    # accept a text and return the text embedding
    with torch.no_grad():
        inputs = processor(text=text, return_tensors="pt")
        text_features = model.get_text_features(**inputs)
        return text_features.cpu().detach().numpy()[0]


def load_images_from_files(image_paths):
    """Loads images from a list of file paths.

    Args:
        image_paths: A list of image file paths.

    Returns:
        A list of PIL Image objects.
    """
    images = []
    for path in image_paths:
        with open(path, 'rb') as f:
            image = Image.open(f)
            images.append(image)
    return images


def embed_images_from_files(image_paths):
    """Embeds images from a list of file paths.

    Args:
        image_paths: A list of image file paths.

    Returns:
        A numpy array of image embeddings.
    """
    images = load_images_from_files(image_paths)
    embeddings = images_to_embeddings(images)
    return embeddings


def read_png(file_path):
  """Reads a PNG image from the specified file path and returns a PIL.Image.Image object.

  Args:
    file_path: The path to the PNG image file.

  Returns:
    A PIL.Image.Image object representing the loaded image.
  """

  try:
    with open(file_path, 'rb') as f:
      img = Image.open(f)
      img.load()  # Load the image data to ensure it's ready for processing
      return img
  except FileNotFoundError:
    print(f"Error: File not found: {file_path}")
    return None
  except IOError:
    print(f"Error: Could not read image: {file_path}")
    return None


# ---

CONNECTION_STRING=f"mysql+pymysql://2s5azfALGtC83jk.root:{PASS}@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/test?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
TABLE_NAME = 'test'
#CONNECTION_STRING = 'mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_verify_cert=true&ssl_verify_identity=true'
tidb_vs = TiDBVectorClient(
    # the table which will store the vector data
    table_name=TABLE_NAME,
    # tidb connection string
    connection_string=CONNECTION_STRING,
    # the dimension of the vector, in this example, we use the ada model, which has 1536 dimensions
    vector_dimension=512,
    # if recreate the table if it already exists
    drop_existing_table=True,
)

ids = [
    "f8e7dee2-63b6-42f1-8b60-2d46710c1971",
    "8dde1fbc-2522-4ca2-aedf-5dcb2966d1c6",
    "e4991349-d00b-485c-a481-f61695f2b5ae",
]
documents = ["foo", "bar", "baz"]
embeddings = [
    text_to_embedding("foo"),
    text_to_embedding("bar"),
    text_to_embedding("baz"),
]
metadatas = [
    {"page": 1, "category": "P1"},
    {"page": 2, "category": "P1"},
    {"page": 3, "category": "P2"},
]

tidb_vs.insert(
    ids=ids,
    texts=documents,
    embeddings=embeddings,
    metadatas=metadatas,
)

tidb_vs.query(text_to_embedding("foo"), k=3)
# query with filter
tidb_vs.query(text_to_embedding("foo"), k=3, filter={"category": "P1"})
tidb_vs.delete(["f8e7dee2-63b6-42f1-8b60-2d46710c1971"])
# delete with filter
tidb_vs.delete(["f8e7dee2-63b6-42f1-8b60-2d46710c1971"], filter={"category": "P1"})

imageslist = ["llm.png", "txt.png"]
# import base64

# with open("llm.png", "rb") as image_file:
#     image_string = base64.b64encode(image_file.read())
    
# import io

# image = io.BytesIO(base64.b64decode(image_string))


# beddings = embed_images_from_files(imageslist)
#images = load_images_from_files(imageslist)

image = read_png("llm.png")
beddings = images_to_embeddings([image])


# ---


# import datasets

# imagenet_datasets = datasets.load_dataset('theodor1289/imagenet-1k_tiny', split='train')
# images = [i['image'] for i in imagenet_datasets]

# objects = []
# images_embedding = images_to_embeddings(images)


# ---


# importing modules 
# import urllib.request 
# from PIL import Image 
  
# urllib.request.urlretrieve( 
#   'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png', 
#    "gfg.png") 
  
# img = Image.open("gfg.png") 
# img.show()
