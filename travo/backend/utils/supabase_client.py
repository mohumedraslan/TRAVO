import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Use environment variables or fallback to hardcoded keys (matching frontend for MVP)
# In production, these should strictly be env vars.
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://mvqljubjlufjyyktsljn.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA")

# If keys are still placeholders, try to read from config.py or similar if it exists, 
# or just let it fail if not provided. 
# For this user, I'll use the values I saw in their frontend config if I can access them,
# but I shouldn't hardcode them here if I can avoid it.
# However, the user's frontend `supabase.ts` has the keys.
# I will read them from there or ask the user.
# Wait, I can see `trovaMobile/src/config/supabase.ts` in the previous turn.
# I will use those keys if they are real, or just set up the structure.

# Actually, I'll check `config.py` in backend root first.
# But for now, I'll create the file with placeholders and comments.
# Wait, if I don't put real keys, the backend will fail to connect.
# I should try to get the keys from `trovaMobile/src/config/supabase.ts` since I have access to it.

url: str = SUPABASE_URL
key: str = SUPABASE_KEY

supabase: Client = create_client(url, key)
