import { useRef, useState } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  Stack,
  Alert,
} from '@mui/material';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import MicIcon from '@mui/icons-material/Mic';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import StopIcon from '@mui/icons-material/Stop';
import {
  identifyMonument,
  MonumentIdentificationResponse,
  askAssistant,
  AssistantResponse,
  voiceToText,
  textToVoice,
} from '../services/api';

export default function DemoPage() {
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [identifyResult, setIdentifyResult] = useState<MonumentIdentificationResponse | null>(null);
  const [identifyError, setIdentifyError] = useState<string | null>(null);
  const [shortDescription, setShortDescription] = useState<string | null>(null);

  const [question, setQuestion] = useState('');
  const [assistantAnswer, setAssistantAnswer] = useState<AssistantResponse | null>(null);
  const [assistantError, setAssistantError] = useState<string | null>(null);

  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  const [ttsAudioSrc, setTtsAudioSrc] = useState<string | null>(null);
  const [voiceError, setVoiceError] = useState<string | null>(null);

  // Handle file upload
  const onFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIdentifyError(null);
    setIdentifyResult(null);
    setShortDescription(null);
    const url = URL.createObjectURL(file);
    setImagePreview(url);
    try {
      const res = await identifyMonument(file);
      setIdentifyResult(res);
      // Try to fetch a short description using the assistant when a monument name is identified
      if (res?.identified_monument) {
        try {
          const desc = await askAssistant(
            `In 2-3 sentences, describe the monument ${res.identified_monument} including its historical significance and location.`
          );
          setShortDescription(desc.answer);
        } catch (err) {
          // Non-blocking: ignore description errors
        }
      }
    } catch (err: any) {
      setIdentifyError(err?.response?.data?.detail || 'Failed to identify monument');
    }
  };

  // Capture from camera
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const openCamera = () => {
    if (fileInputRef.current) {
      fileInputRef.current.accept = 'image/*';
      // hint mobile to use back camera
      // @ts-ignore
      fileInputRef.current.capture = 'environment';
      fileInputRef.current.click();
    }
  };

  const ask = async () => {
    setAssistantError(null);
    setAssistantAnswer(null);
    try {
      const res = await askAssistant(question);
      setAssistantAnswer(res);
    } catch (err: any) {
      setAssistantError(err?.response?.data?.detail || 'Failed to get assistant answer');
    }
  };

  // Voice recording
  const startRecording = async () => {
    setVoiceError(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const reader = new FileReader();
        reader.onloadend = async () => {
          const base64data = (reader.result as string).split(',')[1];
          try {
            const vtt = await voiceToText(base64data, 'en-US');
            setQuestion(vtt.text);
          } catch (err: any) {
            setVoiceError(err?.response?.data?.detail || 'Voice to text failed');
          }
        };
        reader.readAsDataURL(audioBlob);
      };
      recorder.start();
      setRecording(true);
    } catch (err: any) {
      setVoiceError('Microphone permission denied or unsupported');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  };

  const speakAnswer = async () => {
    if (!assistantAnswer?.answer) return;
    setVoiceError(null);
    try {
      const tts = await textToVoice(assistantAnswer.answer, 'en');
      const audioSrc = `data:audio/${tts.format};base64,${tts.audio_data}`;
      setTtsAudioSrc(audioSrc);
    } catch (err: any) {
      setVoiceError(err?.response?.data?.detail || 'Text to voice failed');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" fontWeight={700} sx={{ mb: 3 }}>
        Demo: Monument Identification & AI Assistant
      </Typography>
      <Grid container spacing={3}>
        {/* Left: Image identify */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Upload or Capture Photo</Typography>
            <Stack direction="row" spacing={2} sx={{ mb: 2 }}>
              <Button variant="outlined" startIcon={<UploadFileIcon />} onClick={() => fileInputRef.current?.click()}>
                Upload Photo
              </Button>
              <Button variant="contained" startIcon={<PhotoCameraIcon />} onClick={openCamera}>
                Use Camera
              </Button>
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={onFileChange}
              />
            </Stack>
            {imagePreview && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mb: 2 }}>
                <img src={imagePreview} alt="Preview" style={{ maxWidth: '100%', borderRadius: 8 }} />
              </Box>
            )}
            {identifyResult && (
              <Alert severity="success">
                Identified: <strong>{identifyResult.identified_monument}</strong> — Confidence: {(identifyResult.confidence * 100).toFixed(0)}%
              </Alert>
            )}
            {shortDescription && (
              <Paper variant="outlined" sx={{ p: 2, mt: 2 }}>
                <Typography variant="subtitle1" fontWeight={600}>About this monument</Typography>
                <Typography variant="body2" color="text.secondary">{shortDescription}</Typography>
              </Paper>
            )}
            {identifyError && <Alert severity="error">{identifyError}</Alert>}
          </Paper>
        </Grid>

        {/* Right: Assistant chat */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Ask Assistant</Typography>
            <Stack spacing={2}>
              <TextField
                label="Type your question"
                multiline
                minRows={3}
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="e.g., Tell me about the Pyramids of Giza"
              />
              <Stack direction="row" spacing={2}>
                <Button variant="contained" onClick={ask}>Ask</Button>
                {!recording ? (
                  <Button variant="outlined" startIcon={<MicIcon />} onClick={startRecording}>Speak Question</Button>
                ) : (
                  <Button variant="outlined" color="error" startIcon={<StopIcon />} onClick={stopRecording}>Stop</Button>
                )}
              </Stack>
              {assistantAnswer && (
                <Paper variant="outlined" sx={{ p: 2 }}>
                  <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>Assistant Answer</Typography>
                  <Typography>{assistantAnswer.answer}</Typography>
                  {assistantAnswer.related_monuments?.length > 0 && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        Related: {assistantAnswer.related_monuments.join(', ')}
                      </Typography>
                    </Box>
                  )}
                  <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
                    <Button variant="text" startIcon={<VolumeUpIcon />} onClick={speakAnswer}>Speak Answer</Button>
                    {ttsAudioSrc && (
                      <audio controls src={ttsAudioSrc} />
                    )}
                  </Stack>
                </Paper>
              )}
              {assistantError && <Alert severity="error">{assistantError}</Alert>}
              {voiceError && <Alert severity="error">{voiceError}</Alert>}
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}