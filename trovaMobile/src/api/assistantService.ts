import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface AskResponse {
  answer: string;
  confidence?: number;
}

export interface VoiceToTextResponse {
  text: string;
}

export const askAssistant = async (
  query: string,
  queryType: 'TEXT' | 'VOICE' = 'TEXT',
  location?: string
): Promise<AskResponse> => {
  try {
    const response = await axios.post(`${API_URL}/assistant/ask`, {
      query,
      query_type: queryType,
      location,
    });

    return response.data;
  } catch (error) {
    console.error('Error asking assistant:', error);
    throw error;
  }
};

export const voiceToText = async (audioData: string): Promise<VoiceToTextResponse> => {
  try {
    const response = await axios.post(`${API_URL}/assistant/voice_to_text`, {
      audio_data: audioData,
    });

    return response.data;
  } catch (error) {
    console.error('Error converting voice to text:', error);
    throw error;
  }
};

export const textToVoice = async (text: string): Promise<ArrayBuffer> => {
  try {
    const response = await axios.post(
      `${API_URL}/assistant/text_to_voice`,
      { text },
      { responseType: 'arraybuffer' }
    );

    return response.data;
  } catch (error) {
    console.error('Error converting text to voice:', error);
    throw error;
  }
};