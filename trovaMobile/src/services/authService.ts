import { supabase } from '../config/supabase';

export interface SignUpData {
  email: string;
  password: string;
  username: string;
  fullName: string;
}

export interface SignInData {
  email: string;
  password: string;
}

export const signUp = async (data: SignUpData) => {
  try {
    const { email, password, username, fullName } = data;
    
    const { user, error: signUpError } = await supabase.auth.signUp(
      {
        email,
        password,
      },
      {
        data: {
          username,
          full_name: fullName,
        },
      }
    );

    if (signUpError) throw signUpError;
    return { user, error: null };
  } catch (error: any) {
    console.error('Sign up error:', error);
    return { user: null, error: error.message };
  }
};

export const signIn = async (data: SignInData) => {
  try {
    const { email, password } = data;
    
    const { user, error: signInError } = await supabase.auth.signIn({
      email,
      password,
    });

    if (signInError) throw signInError;
    return { user, error: null };
  } catch (error: any) {
    console.error('Sign in error:', error);
    return { user: null, error: error.message };
  }
};

export const signOut = async () => {
  try {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    return { error: null };
  } catch (error: any) {
    console.error('Sign out error:', error);
    return { error: error.message };
  }
};

export const getCurrentUser = async () => {
  try {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    return { user, error: null };
  } catch (error: any) {
    console.error('Get current user error:', error);
    return { user: null, error: error.message };
  }
};

export const resetPassword = async (email: string) => {
  try {
    const { error } = await supabase.auth.api.resetPasswordForEmail(email);
    if (error) throw error;
    return { error: null };
  } catch (error: any) {
    console.error('Reset password error:', error);
    return { error: error.message };
  }
};
