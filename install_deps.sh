#!/bin/bash

# Install backend dependencies
echo "Installing backend dependencies..."
cd travo/backend
pip install -r requirements.txt
pip install supabase

# Install mobile app dependencies
echo "Installing mobile app dependencies..."
cd ../../trovaMobile
npm install @supabase/supabase-js @react-native-async-storage/async-storage react-native-url-polyfill @types/react-native-url-polyfill

# Install web dependencies
echo "Installing web dependencies..."
cd ../trovaweb
npm install @supabase/supabase-js

echo "All dependencies installed successfully!"

# Create .env file for mobile
cd ../trovaMobile
echo "NEXT_PUBLIC_SUPABASE_URL=https://mvqljubjlufjyyktsljn.supabase.co" > .env
echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA" >> .env

# Create .env file for web
cd ../trovaweb
echo "NEXT_PUBLIC_SUPABASE_URL=https://mvqljubjlufjyyktsljn.supabase.co" > .env.local
echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im12cWxqdWJqbHVmanl5a3RzbGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MTQwMjksImV4cCI6MjA3Nzk5MDAyOX0._6sCVs20oYzLUNfyYqlx54ZnuwoaamiCI_9SuSt1crA" >> .env.local

echo "Environment files created successfully!"
