from typing import Optional, List, Union

import firebase_admin
from firebase_admin import firestore
from firebase_admin.credentials import Certificate
from pydantic import BaseModel


class Firestore:
    def __init__(self, account_key_path: str = './accountKey.json'):
        """
        Constructor for the Firestore class.

        Args:
            account_key_path (str): Path to the Firebase service account key file. Default is './accountKey.json'.
        """
        self.__db_ref: Optional[firestore.client] = None
        self.__account_key_path: str = account_key_path

    def __connect(self):
        """
        Private method to connect to the Firestore database.
        """
        credentials = Certificate(self.__account_key_path)
        firebase_admin.initialize_app(credentials)
        self.__db_ref = firestore.client()

    # noinspection PyMethodMayBeStatic
    def __disconnect(self):
        """
        Private method to disconnect from the Firestore database.
        """
        # noinspection PyProtectedMember
        if firebase_admin._apps:
            firebase_admin.delete_app(firebase_admin.get_app())

    def __enter__(self) -> "Firestore":
        """
        Method called when entering a context block. Connects to the Firestore database.

        Returns:
            Firestore: The Firestore instance.
        """
        self.__connect()
        if self.__db_ref is None:
            raise Exception("Failed to connect to Firestore database.")
        return self

    def __del__(self):
        """
        Destructor method. Disconnects from the Firestore database.
        """
        self.__disconnect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Method called when exiting a context block. Disconnects from the Firestore database.
        """
        self.__disconnect()

    def add_document(self, document: BaseModel) -> BaseModel:
        """
        Add a document to the Firestore database.

        Args:
            document (BaseModel): A Pydantic BaseModel instance representing the document to be added.

        Returns:
            BaseModel: The same document with the Firestore document ID added.
        """
        collection = document.__class__.__name__
        print("Saving on collection {}".format(collection))
        doc = self.__db_ref.collection(collection).document()
        data = document.dict()
        del data['id']
        doc.set(data)
        document.id = doc.id
        return document

    def list_document(self, collection_name: str) -> List[dict]:
        """
        List all documents in a Firestore collection.

        Args:
            collection_name (str): The name of the Firestore collection.

        Returns:
            List[dict]: A list of dictionaries, each representing a document in the collection.
        """
        collection = self.__db_ref.collection(collection_name)
        documents_list = []
        for doc in collection.stream():
            data = doc.to_dict()
            data['id'] = doc.id
            documents_list.append(data)
        return documents_list

    def get_document(self, collection_name: str, document_id: str) -> Union[dict, None]:
        """
        Retrieve a single document from a Firestore collection by its ID.

        Args:
            collection_name (str): The name of the Firestore collection.
            document_id (str): The ID of the document to retrieve.

        Returns:
            Union[dict, None]: A dictionary representing the document if found, or None if not found.
        """
        doc_ref = self.__db_ref.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        else:
            return None

    def update_document(self, collection_name: str, document_id: str, data: dict) -> bool:
        """
        Update a document in a Firestore collection.

        Args:
            collection_name (str): The name of the Firestore collection.
            document_id (str): The ID of the document to update.
            data (dict): A dictionary containing the fields to update.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        doc_ref = self.__db_ref.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.update(data)
            return True
        else:
            return False

    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """
        Delete a document from a Firestore collection.

        Args:
            collection_name (str): The name of the Firestore collection.
            document_id (str): The ID of the document to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        doc_ref = self.__db_ref.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            return True
        else:
            return False
