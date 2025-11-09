-- Fix for user signup in Supabase
-- Run this in Supabase SQL Editor

-- 1. Create a function to handle user registration
CREATE OR REPLACE FUNCTION public.register_user(
  p_email TEXT,
  p_password TEXT,
  p_full_name TEXT DEFAULT NULL,
  p_username TEXT DEFAULT NULL
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_user_id UUID;
  v_result JSON;
BEGIN
  -- Create auth user
  INSERT INTO auth.users (
    instance_id,
    id,
    aud,
    role,
    email,
    encrypted_password,
    email_confirmed_at,
    raw_app_meta_data,
    raw_user_meta_data,
    created_at,
    updated_at,
    confirmation_token,
    email_change,
    email_change_token_new,
    recovery_token
  )
  VALUES (
    '00000000-0000-0000-0000-000000000000',
    gen_random_uuid(),
    'authenticated',
    'authenticated',
    p_email,
    crypt(p_password, gen_salt('bf')),
    NOW(),
    '{"provider":"email","providers":["email"]}',
    jsonb_build_object(
      'full_name', COALESCE(p_full_name, ''),
      'username', COALESCE(p_username, '')
    ),
    NOW(),
    NOW(),
    '',
    '',
    '',
    ''
  )
  RETURNING id INTO v_user_id;
  
  -- Create profile
  INSERT INTO public.profiles (id, username, full_name)
  VALUES (
    v_user_id,
    p_username,
    p_full_name
  );
  
  -- Return success
  v_result := json_build_object(
    'success', true,
    'user_id', v_user_id,
    'email', p_email
  );
  
  RETURN v_result;
  
EXCEPTION
  WHEN unique_violation THEN
    RETURN json_build_object(
      'success', false,
      'error', 'Email already exists'
    );
  WHEN OTHERS THEN
    RETURN json_build_object(
      'success', false,
      'error', SQLERRM
    );
END;
$$;

-- 2. Grant execute permission
GRANT EXECUTE ON FUNCTION public.register_user TO anon, authenticated;

-- 3. Test the function (optional)
-- SELECT public.register_user('test@example.com', 'password123', 'Test User', 'testuser');
