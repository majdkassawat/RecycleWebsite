// Vercel Serverless Function for Suggestions
// Uses Vercel KV (Redis) for persistent storage when available
// Falls back to in-memory storage for testing

const ADMIN_KEY = process.env.ADMIN_KEY || 'tadweer-admin-2025';
const KV_KEY = 'tadweer:suggestions';

// In-memory fallback (resets on cold start)
let memoryStore = [];

// Generate tracking ID
function generateTrackingId() {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    let id = 'TDW-';
    for (let i = 0; i < 6; i++) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return id;
}

// Generate UUID
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Storage abstraction
async function getStorage() {
    // Try Vercel KV if environment variables are set
    if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
        try {
            const { kv } = require('@vercel/kv');
            return {
                async get() {
                    return await kv.get(KV_KEY) || [];
                },
                async set(data) {
                    await kv.set(KV_KEY, data);
                },
                type: 'kv'
            };
        } catch (e) {
            console.log('KV not available, using memory');
        }
    }
    
    // Fallback to memory
    return {
        async get() {
            return memoryStore;
        },
        async set(data) {
            memoryStore = data;
        },
        type: 'memory'
    };
}

module.exports = async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(204).end();
    }

    const storage = await getStorage();

    try {
        // GET - List all suggestions or get by tracking_id
        if (req.method === 'GET') {
            const trackingId = req.query.tracking_id;
            const suggestions = await storage.get();
            
            if (trackingId) {
                const found = suggestions.find(s => s.tracking_id === trackingId.toUpperCase());
                if (found) {
                    // Return limited info for public tracking
                    return res.status(200).json([{
                        tracking_id: found.tracking_id,
                        category: found.category,
                        status: found.status,
                        created_at: found.created_at
                    }]);
                }
                return res.status(200).json([]);
            }

            // Check for admin auth for full list
            const authHeader = req.headers.authorization;
            
            if (authHeader !== `Bearer ${ADMIN_KEY}`) {
                return res.status(401).json({ error: 'Unauthorized' });
            }

            return res.status(200).json(suggestions);
        }

        // POST - Create new suggestion
        if (req.method === 'POST') {
            const body = req.body;
            
            // Validate
            if (!body.suggestion || body.suggestion.length < 10) {
                return res.status(400).json({ error: 'Suggestion too short' });
            }

            if (body.suggestion.length > 2000) {
                return res.status(400).json({ error: 'Suggestion too long' });
            }

            // Honeypot check
            if (body.website_url) {
                return res.status(400).json({ error: 'Invalid submission' });
            }

            const trackingId = generateTrackingId();
            const newSuggestion = {
                id: generateUUID(),
                tracking_id: trackingId,
                name: body.name || 'Anonymous',
                email: body.email || '',
                category: body.category || 'general',
                suggestion: body.suggestion,
                status: 'new',
                page_url: body.page_url || '',
                created_at: new Date().toISOString()
            };

            const suggestions = await storage.get();
            suggestions.unshift(newSuggestion);
            await storage.set(suggestions);

            return res.status(201).json({ 
                success: true, 
                tracking_id: trackingId,
                storage: storage.type
            });
        }

        // PATCH - Update suggestion status (admin only)
        if (req.method === 'PATCH') {
            const authHeader = req.headers.authorization;
            
            if (authHeader !== `Bearer ${ADMIN_KEY}`) {
                return res.status(401).json({ error: 'Unauthorized' });
            }

            const body = req.body;
            const { id, status } = body;

            if (!id || !status) {
                return res.status(400).json({ error: 'Missing id or status' });
            }

            const suggestions = await storage.get();
            const index = suggestions.findIndex(s => s.id === id);
            
            if (index === -1) {
                return res.status(404).json({ error: 'Suggestion not found' });
            }

            suggestions[index].status = status;
            suggestions[index].updated_at = new Date().toISOString();
            await storage.set(suggestions);

            return res.status(200).json({ success: true });
        }

        return res.status(405).json({ error: 'Method not allowed' });

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ error: 'Internal server error', details: error.message });
    }
};
