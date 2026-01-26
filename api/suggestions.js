// Vercel Serverless Function for Suggestions
// Uses Vercel KV (Redis) for storage

const SUGGESTIONS_KEY = 'tadweer:suggestions';

export const config = {
  runtime: 'edge',
};

// Generate tracking ID
function generateTrackingId() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let id = 'TDW-';
  for (let i = 0; i < 6; i++) {
    id += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return id;
}

// Simple in-memory fallback (for when KV is not configured)
// In production, this will be replaced by Vercel KV
let memoryStore = [];

export default async function handler(request) {
  const url = new URL(request.url);
  const method = request.method;

  // CORS headers
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Handle preflight
  if (method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  try {
    // Try to use Vercel KV if available
    let kv = null;
    if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
      const { kv: kvClient } = await import('@vercel/kv');
      kv = kvClient;
    }

    // GET - List all suggestions or get by tracking_id
    if (method === 'GET') {
      const trackingId = url.searchParams.get('tracking_id');
      
      let suggestions = [];
      if (kv) {
        suggestions = await kv.get(SUGGESTIONS_KEY) || [];
      } else {
        suggestions = memoryStore;
      }

      if (trackingId) {
        const found = suggestions.find(s => s.tracking_id === trackingId.toUpperCase());
        if (found) {
          // Return limited info for public tracking
          return new Response(JSON.stringify([{
            tracking_id: found.tracking_id,
            category: found.category,
            status: found.status,
            created_at: found.created_at
          }]), {
            status: 200,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          });
        }
        return new Response(JSON.stringify([]), {
          status: 200,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Check for admin auth for full list
      const authHeader = request.headers.get('Authorization');
      const adminKey = process.env.ADMIN_KEY || 'tadweer-admin-2025';
      
      if (authHeader !== `Bearer ${adminKey}`) {
        return new Response(JSON.stringify({ error: 'Unauthorized' }), {
          status: 401,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      return new Response(JSON.stringify(suggestions), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // POST - Create new suggestion
    if (method === 'POST') {
      const body = await request.json();
      
      // Validate
      if (!body.suggestion || body.suggestion.length < 10) {
        return new Response(JSON.stringify({ error: 'Suggestion too short' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      if (body.suggestion.length > 2000) {
        return new Response(JSON.stringify({ error: 'Suggestion too long' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      // Honeypot check
      if (body.website_url) {
        return new Response(JSON.stringify({ error: 'Invalid submission' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      const trackingId = generateTrackingId();
      const newSuggestion = {
        id: crypto.randomUUID(),
        tracking_id: trackingId,
        name: body.name || 'Anonymous',
        email: body.email || '',
        category: body.category || 'general',
        suggestion: body.suggestion,
        status: 'new',
        page_url: body.page_url || '',
        created_at: new Date().toISOString()
      };

      // Save
      let suggestions = [];
      if (kv) {
        suggestions = await kv.get(SUGGESTIONS_KEY) || [];
        suggestions.unshift(newSuggestion);
        await kv.set(SUGGESTIONS_KEY, suggestions);
      } else {
        memoryStore.unshift(newSuggestion);
        suggestions = memoryStore;
      }

      return new Response(JSON.stringify({ 
        success: true, 
        tracking_id: trackingId 
      }), {
        status: 201,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    // PATCH - Update suggestion status (admin only)
    if (method === 'PATCH') {
      const authHeader = request.headers.get('Authorization');
      const adminKey = process.env.ADMIN_KEY || 'tadweer-admin-2025';
      
      if (authHeader !== `Bearer ${adminKey}`) {
        return new Response(JSON.stringify({ error: 'Unauthorized' }), {
          status: 401,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      const body = await request.json();
      const { id, status } = body;

      if (!id || !status) {
        return new Response(JSON.stringify({ error: 'Missing id or status' }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      let suggestions = [];
      if (kv) {
        suggestions = await kv.get(SUGGESTIONS_KEY) || [];
      } else {
        suggestions = memoryStore;
      }

      const index = suggestions.findIndex(s => s.id === id);
      if (index === -1) {
        return new Response(JSON.stringify({ error: 'Suggestion not found' }), {
          status: 404,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      suggestions[index].status = status;
      suggestions[index].updated_at = new Date().toISOString();

      if (kv) {
        await kv.set(SUGGESTIONS_KEY, suggestions);
      } else {
        memoryStore = suggestions;
      }

      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ error: 'Method not allowed' }), {
      status: 405,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('API Error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}
