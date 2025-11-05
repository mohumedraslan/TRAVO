import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;

export interface MonumentIdentificationResponse {
  identified_monument: string;
  confidence: number;
}

export interface AssistantResponse {
  answer: string;
  related_monuments: string[];
  confidence: number;
}

export async function identifyMonument(imageFile: File): Promise<MonumentIdentificationResponse> {
  const formData = new FormData();
  // The backend expects the field name 'image' for the UploadFile parameter
  formData.append('image', imageFile);
  const { data } = await api.post<MonumentIdentificationResponse>('/vision/identify', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function askAssistant(query: string, location?: string): Promise<AssistantResponse> {
  const payload = {
    query,
    location: location || null,
    query_type: 'text',
  };
  const { data } = await api.post<AssistantResponse>('/assistant/ask', payload);
  return data;
}

export interface VoiceToTextResponse {
  text: string;
  confidence: number;
}

export async function voiceToText(audioBase64: string, language: string = 'en-US'): Promise<VoiceToTextResponse> {
  const payload = { audio_data: audioBase64, language };
  const { data } = await api.post<VoiceToTextResponse>('/assistant/voice_to_text', payload);
  return data;
}

export interface TextToVoiceResponse {
  audio_data: string;
  format: string; // e.g. 'mp3'
}

export async function textToVoice(text: string, language: string = 'en', voice?: string): Promise<TextToVoiceResponse> {
  const payload: { text: string; language: string; voice?: string } = { text, language };
  if (voice) payload.voice = voice;
  const { data } = await api.post<TextToVoiceResponse>('/assistant/text_to_voice', payload);
  return data;
}