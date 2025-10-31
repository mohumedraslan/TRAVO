import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { askAssistant, voiceToText, textToVoice } from '@/src/api/assistantService';
import { Audio } from 'expo-av';
import * as FileSystem from 'react-native-fs';
import io from 'socket.io-client';
import { IconSymbol } from '@/components/ui/icon-symbol';

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  isAudio?: boolean;
  audioUri?: string;
}

interface SmartGuideChatProps {
  initialLocation?: string;
}

const SmartGuideChat: React.FC<SmartGuideChatProps> = ({ initialLocation }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const scrollViewRef = useRef<ScrollView>(null);
  const socketRef = useRef<any>(null);

  // Initialize socket connection
  useEffect(() => {
    // Connect to socket server
    socketRef.current = io('http://localhost:8000', {
      transports: ['websocket'],
    });

    socketRef.current.on('connect', () => {
      console.log('Connected to socket server');
    });

    socketRef.current.on('assistant_response', (data: any) => {
      addMessage({
        id: Date.now().toString(),
        text: data.answer,
        isUser: false,
        timestamp: new Date(),
      });
    });

    socketRef.current.on('disconnect', () => {
      console.log('Disconnected from socket server');
    });

    // Add welcome message
    if (initialLocation) {
      addMessage({
        id: '0',
        text: `Welcome to ${initialLocation}! How can I help you today?`,
        isUser: false,
        timestamp: new Date(),
      });
    } else {
      addMessage({
        id: '0',
        text: 'Hello! I\'m your TRAVO guide. How can I help you today?',
        isUser: false,
        timestamp: new Date(),
      });
    }

    // Cleanup on unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.disconnect();
      }
    };
  }, [initialLocation]);

  // Request audio recording permissions
  useEffect(() => {
    (async () => {
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== 'granted') {
        console.error('Audio recording permission not granted');
      }
    })();
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    setTimeout(() => {
      scrollViewRef.current?.scrollToEnd({ animated: true });
    }, 100);
  }, [messages]);

  // Add a new message to the chat
  const addMessage = (message: Message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  // Send text message
  const sendTextMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await askAssistant(inputText, 'TEXT', initialLocation);

      if (response.answer) {
        addMessage({
          id: Date.now().toString(),
          text: response.answer,
          isUser: false,
          timestamp: new Date(),
        });

        // Optional: Convert response to speech
        if (response.answer) {
          try {
            const speechResponse = await textToVoice(response.answer);

            const audioPath = `${FileSystem.CachesDirectoryPath}/response_${Date.now()}.mp3`;
            await FileSystem.writeFile(audioPath, Buffer.from(speechResponse).toString('base64'), 'base64');

            const { sound } = await Audio.Sound.createAsync({ uri: audioPath });
            setSound(sound);
            await sound.playAsync();
          } catch (error) {
            console.error('Error converting text to speech:', error);
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      addMessage({
        id: Date.now().toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Start recording audio
  const startRecording = async () => {
    try {
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );

      setRecording(recording);
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
    }
  };

  // Stop recording and send audio
  const stopRecording = async () => {
    if (!recording) return;

    setIsRecording(false);
    setIsLoading(true);

    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);

      if (!uri) {
        throw new Error('Recording URI is null');
      }

      // Add user audio message
      const userMessage: Message = {
        id: Date.now().toString(),
        text: '🎤 Audio message',
        isUser: true,
        timestamp: new Date(),
        isAudio: true,
        audioUri: uri,
      };

      addMessage(userMessage);

      // Convert audio to base64
      const base64Audio = await FileSystem.readFile(uri, 'base64');

      // Send to voice-to-text API
      const voiceToTextResponse = await voiceToText(base64Audio);

      if (voiceToTextResponse.text) {
        const transcribedText = voiceToTextResponse.text;

        // Update the user message with transcribed text
        setMessages((prevMessages) =>
          prevMessages.map((msg) =>
            msg.id === userMessage.id
              ? { ...msg, text: `🎤 "${transcribedText}"` }
              : msg
          )
        );

        // Send transcribed text to assistant
        const assistantResponse = await askAssistant(transcribedText, 'TEXT', initialLocation);

        if (assistantResponse.answer) {
          addMessage({
            id: Date.now().toString(),
            text: assistantResponse.answer,
            isUser: false,
            timestamp: new Date(),
          });

          // Convert response to speech
          try {
            const speechResponse = await textToVoice(assistantResponse.answer);

            const audioPath = `${FileSystem.CachesDirectoryPath}/response_${Date.now()}.mp3`;
            await FileSystem.writeFile(audioPath, Buffer.from(speechResponse).toString('base64'), 'base64');

            const { sound } = await Audio.Sound.createAsync({ uri: audioPath });
            setSound(sound);
            await sound.playAsync();
          } catch (error) {
            console.error('Error converting text to speech:', error);
          }
        }
      }
    } catch (error) {
      console.error('Error processing audio:', error);
      addMessage({
        id: Date.now().toString(),
        text: 'Sorry, I had trouble understanding that. Please try again.',
        isUser: false,
        timestamp: new Date(),
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Play audio message
  const playAudioMessage = async (uri: string) => {
    try {
      if (sound) {
        await sound.unloadAsync();
      }

      const { sound: newSound } = await Audio.Sound.createAsync({ uri });
      setSound(newSound);
      await newSound.playAsync();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  // Render message item
  const renderMessage = (message: Message) => {
    return (
      <View
        key={message.id}
        style={[
          styles.messageContainer,
          message.isUser ? styles.userMessage : styles.assistantMessage,
        ]}
      >
        {message.isAudio && message.audioUri ? (
          <TouchableOpacity
            style={styles.audioButton}
            onPress={() => playAudioMessage(message.audioUri!)}
          >
            <IconSymbol name="play.fill" size={16} color="white" />
            <Text style={styles.messageText}>{message.text}</Text>
          </TouchableOpacity>
        ) : (
          <Text style={styles.messageText}>{message.text}</Text>
        )}
        <Text style={styles.timestamp}>
          {message.timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </Text>
      </View>
    );
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      keyboardVerticalOffset={100}
    >
      <ScrollView
        ref={scrollViewRef}
        style={styles.messagesContainer}
        contentContainerStyle={styles.messagesContent}
      >
        {messages.map(renderMessage)}
        {isLoading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#2196F3" />
            <Text style={styles.loadingText}>Thinking...</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type your message..."
          placeholderTextColor="#999"
          returnKeyType="send"
          onSubmitEditing={sendTextMessage}
          editable={!isRecording}
        />
        <TouchableOpacity
          style={[styles.button, isRecording ? styles.recordingButton : null]}
          onPress={isRecording ? stopRecording : startRecording}
        >
          <IconSymbol
            name={isRecording ? "stop.fill" : "mic.fill"}
            size={20}
            color="white"
          />
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.button, { backgroundColor: '#2196F3' }]}
          onPress={sendTextMessage}
          disabled={!inputText.trim() || isLoading || isRecording}
        >
          <IconSymbol name="paperplane.fill" size={20} color="white" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    padding: 10,
    paddingBottom: 20,
  },
  messageContainer: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 16,
    marginVertical: 5,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
  },
  userMessage: {
    alignSelf: 'flex-end',
    backgroundColor: '#DCF8C6',
    borderBottomRightRadius: 4,
  },
  assistantMessage: {
    alignSelf: 'flex-start',
    backgroundColor: 'white',
    borderBottomLeftRadius: 4,
  },
  messageText: {
    fontSize: 16,
    color: '#333',
  },
  timestamp: {
    fontSize: 10,
    color: '#999',
    alignSelf: 'flex-end',
    marginTop: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#eee',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    backgroundColor: '#f0f0f0',
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
    fontSize: 16,
  },
  button: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: 5,
  },
  recordingButton: {
    backgroundColor: '#FF5252',
  },
  audioButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    backgroundColor: '#f0f0f0',
    padding: 10,
    borderRadius: 16,
    marginVertical: 5,
  },
  loadingText: {
    marginLeft: 5,
    color: '#666',
  },
});

export default SmartGuideChat;