class MemoryApiClient {
    static async getHealth() {
        try {
            const res = await fetch('/api/v1/memory/health');
            const data = await res.json();
            return { ok: res.ok, ...data };
        } catch (err) {
            return { ok: false, status: 'error', message: err.message };
        }
    }

    static async getStatus() {
        try {
            const res = await fetch('/api/v1/memory/status');
            const data = await res.json();
            return { ok: res.ok, ...data };
        } catch (err) {
            return { ok: false, status: 'error', message: err.message };
        }
    }

    static async retrieveContext(collectionName, queryText, limit = 5) {
        try {
            const res = await fetch('/api/v1/memory/retrieve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    collection_name: collectionName,
                    query_text: queryText,
                    limit: limit
                })
            });
            const data = await res.json();
            return { ok: res.ok, ...data };
        } catch (err) {
            return { ok: false, status: 'error', message: err.message };
        }
    }

    static async storeMemory(memoryType, text, twinVersion, extraData = {}) {
        try {
            const res = await fetch('/api/v1/memory/store', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    memory_type: memoryType,
                    text: text,
                    twin_version: twinVersion,
                    extra_data: extraData
                })
            });
            const data = await res.json();
            return { ok: res.ok, ...data };
        } catch (err) {
            return { ok: false, status: 'error', message: err.message };
        }
    }
}
