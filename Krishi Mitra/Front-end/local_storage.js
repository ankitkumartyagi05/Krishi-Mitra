// Frontend JSON Local Storage Utility
class LocalStorageDB {
    constructor(dbName = 'krishimitra_db') {
        this.dbName = dbName;
        this.initialize();
    }

    initialize() {
        if (!localStorage.getItem(this.dbName)) {
            localStorage.setItem(this.dbName, JSON.stringify({}));
        }
    }

    // Get the entire database
    getDB() {
        return JSON.parse(localStorage.getItem(this.dbName) || '{}');
    }

    // Save the entire database
    saveDB(db) {
        localStorage.setItem(this.dbName, JSON.stringify(db));
    }

    // Get a collection (table)
    getCollection(collectionName) {
        const db = this.getDB();
        return db[collectionName] || [];
    }

    // Save a collection
    saveCollection(collectionName, collection) {
        const db = this.getDB();
        db[collectionName] = collection;
        this.saveDB(db);
    }

    // Find all items in a collection
    findAll(collectionName) {
        return this.getCollection(collectionName);
    }

    // Find one item by id
    findById(collectionName, id) {
        const collection = this.getCollection(collectionName);
        return collection.find(item => item.id === id);
    }

    // Find items by query
    find(collectionName, query) {
        const collection = this.getCollection(collectionName);
        return collection.filter(item => {
            return Object.keys(query).every(key => item[key] === query[key]);
        });
    }

    // Insert a new item
    insert(collectionName, item) {
        const collection = this.getCollection(collectionName);
        item.id = this.generateId();
        item.createdAt = new Date().toISOString();
        collection.push(item);
        this.saveCollection(collectionName, collection);
        return item;
    }

    // Update an item
    update(collectionName, id, updates) {
        const collection = this.getCollection(collectionName);
        const index = collection.findIndex(item => item.id === id);
        if (index !== -1) {
            collection[index] = { ...collection[index], ...updates, updatedAt: new Date().toISOString() };
            this.saveCollection(collectionName, collection);
            return collection[index];
        }
        return null;
    }

    // Delete an item
    delete(collectionName, id) {
        const collection = this.getCollection(collectionName);
        const index = collection.findIndex(item => item.id === id);
        if (index !== -1) {
            collection.splice(index, 1);
            this.saveCollection(collectionName, collection);
            return true;
        }
        return false;
    }

    // Generate unique ID
    generateId() {
        return '_' + Math.random().toString(36).substr(2, 9);
    }

    // Clear entire database
    clear() {
        localStorage.removeItem(this.dbName);
        this.initialize();
    }

    // Drop a collection
    dropCollection(collectionName) {
        const db = this.getDB();
        delete db[collectionName];
        this.saveDB(db);
    }
}

// Create instance
const localStorageDB = new LocalStorageDB();

// Export for use in other modules
window.localStorageDB = localStorageDB;
