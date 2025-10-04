import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class JSONStorage:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.ensure_data_dir()
        self.collections = {}
        self.load_all_collections()

    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def get_collection_path(self, collection_name: str) -> str:
        """Get file path for a collection"""
        return os.path.join(self.data_dir, f"{collection_name}.json")

    def load_collection(self, collection_name: str) -> List[Dict]:
        """Load a collection from JSON file"""
        file_path = self.get_collection_path(collection_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_collection(self, collection_name: str, data: List[Dict]) -> None:
        """Save a collection to JSON file"""
        file_path = self.get_collection_path(collection_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_all_collections(self):
        """Load all collections from data directory"""
        if os.path.exists(self.data_dir):
            for file_name in os.listdir(self.data_dir):
                if file_name.endswith('.json'):
                    collection_name = file_name[:-5]  # Remove .json extension
                    self.collections[collection_name] = self.load_collection(collection_name)

    def find_all(self, collection_name: str) -> List[Dict]:
        """Get all documents in a collection"""
        return self.collections.get(collection_name, [])

    def find_by_id(self, collection_name: str, doc_id: str) -> Optional[Dict]:
        """Find a document by ID"""
        collection = self.collections.get(collection_name, [])
        for doc in collection:
            if doc.get('id') == doc_id:
                return doc
        return None

    def find(self, collection_name: str, query: Dict) -> List[Dict]:
        """Find documents matching query"""
        collection = self.collections.get(collection_name, [])
        results = []
        for doc in collection:
            match = True
            for key, value in query.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                results.append(doc)
        return results

    def insert_one(self, collection_name: str, document: Dict) -> Dict:
        """Insert a document into a collection"""
        if collection_name not in self.collections:
            self.collections[collection_name] = []
        
        # Add metadata
        document['id'] = self.generate_id()
        document['createdAt'] = datetime.now().isoformat()
        
        self.collections[collection_name].append(document)
        self.save_collection(collection_name, self.collections[collection_name])
        return document

    def update_one(self, collection_name: str, doc_id: str, updates: Dict) -> Optional[Dict]:
        """Update a document by ID"""
        collection = self.collections.get(collection_name, [])
        for i, doc in enumerate(collection):
            if doc.get('id') == doc_id:
                # Update document
                collection[i] = {**doc, **updates}
                collection[i]['updatedAt'] = datetime.now().isoformat()
                self.save_collection(collection_name, collection)
                return collection[i]
        return None

    def delete_one(self, collection_name: str, doc_id: str) -> bool:
        """Delete a document by ID"""
        collection = self.collections.get(collection_name, [])
        for i, doc in enumerate(collection):
            if doc.get('id') == doc_id:
                del collection[i]
                self.save_collection(collection_name, collection)
                return True
        return False

    def delete_many(self, collection_name: str, query: Dict) -> int:
        """Delete multiple documents matching query"""
        collection = self.collections.get(collection_name, [])
        original_length = len(collection)
        self.collections[collection_name] = [doc for doc in collection if not all(
            doc.get(key) == value for key, value in query.items()
        )]
        deleted_count = original_length - len(self.collections[collection_name])
        if deleted_count > 0:
            self.save_collection(collection_name, self.collections[collection_name])
        return deleted_count

    def drop_collection(self, collection_name: str) -> None:
        """Drop a collection"""
        if collection_name in self.collections:
            del self.collections[collection_name]
            file_path = self.get_collection_path(collection_name)
            if os.path.exists(file_path):
                os.remove(file_path)

    def generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())

    def get_collection_stats(self, collection_name: str) -> Dict:
        """Get statistics for a collection"""
        collection = self.collections.get(collection_name, [])
        return {
            'count': len(collection),
            'size': len(json.dumps(collection).encode('utf-8'))
        }

    def backup(self, backup_dir: str) -> None:
        """Backup all collections to a directory"""
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        for collection_name, collection in self.collections.items():
            backup_path = os.path.join(backup_dir, f"{collection_name}.json")
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(collection, f, indent=2, ensure_ascii=False)

    def restore(self, backup_dir: str) -> None:
        """Restore all collections from a backup directory"""
        if not os.path.exists(backup_dir):
            raise FileNotFoundError(f"Backup directory not found: {backup_dir}")
        
        for file_name in os.listdir(backup_dir):
            if file_name.endswith('.json'):
                collection_name = file_name[:-5]
                backup_path = os.path.join(backup_dir, file_name)
                with open(backup_path, 'r', encoding='utf-8') as f:
                    collection = json.load(f)
                self.collections[collection_name] = collection
                self.save_collection(collection_name, collection)
