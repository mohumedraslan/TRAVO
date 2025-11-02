import client from './client';

export interface AskResponse {
  answer: string;
  confidence?: number;
}

export interface VoiceToTextResponse {
  text: string;
}

export interface TextToVoiceResponse {
  audio_data: string; // base64
  format: 'mp3' | 'wav' | 'ogg' | string;
}

export const askAssistant = async (
  query: string,
  queryType: 'TEXT' | 'VOICE' = 'TEXT',
  location?: string
): Promise<AskResponse> => {
  const response = await client.post(`/assistant/ask`, {
    query,
    query_type: queryType,
    location,
  });
  return response.data;
};

export const voiceToText = async (audioData: string, language = 'en-US'): Promise<VoiceToTextResponse> => {
  const response = await client.post(`/assistant/voice_to_text`, {
    audio_data: audioData,
    language,
  });
  return response.data;
};

export const textToVoice = async (text: string, language = 'en'): Promise<TextToVoiceResponse> => {
  const response = await client.post(`/assistant/text_to_voice`, {
    text,
    language,
  });
  return response.data;
};