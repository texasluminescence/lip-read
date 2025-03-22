import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { MaterialIcons } from '@expo/vector-icons';
import { RouteProp, useNavigation, useRoute } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import PlatformVideoPlayer from '../components/PlatformVideoPlayer';
import { RootStackParamList } from '../types/navigation';
import { uploadVideo } from '../services/api';

type PreviewScreenRouteProp = RouteProp<RootStackParamList, 'Preview'>;
type PreviewScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Preview'>;

const PreviewScreen: React.FC = () => {
  const navigation = useNavigation<PreviewScreenNavigationProp>();
  const route = useRoute<PreviewScreenRouteProp>();
  const { uri } = route.params;
  
  const [analyzing, setAnalyzing] = useState(false);
  const [transcript, setTranscript] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyzeVideo = async () => {
    setAnalyzing(true);
    setError(null);
    
    try {
      const result = await uploadVideo(uri);
      setTranscript(result);
    } catch (err) {
      console.error('Error analyzing video:', err);
      setError('Failed to analyze video. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleStartOver = () => {
    navigation.navigate('Home');
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <View style={styles.videoContainer}>
        <PlatformVideoPlayer uri={uri} />
      </View>
      
      <View style={styles.content}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <MaterialIcons name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        
        {transcript ? (
          <View style={styles.resultContainer}>
            <Text style={styles.resultTitle}>Transcript</Text>
            <ScrollView style={styles.transcriptContainer}>
              <Text style={styles.transcript}>{transcript}</Text>
            </ScrollView>
            <TouchableOpacity 
              style={[styles.button, styles.secondaryButton]}
              onPress={handleStartOver}
            >
              <MaterialIcons name="refresh" size={20} color="white" />
              <Text style={styles.buttonText}>Start Over</Text>
            </TouchableOpacity>
          </View>
        ) : (
          <View style={styles.actionContainer}>
            {analyzing ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#4285F4" />
                <Text style={styles.loadingText}>Analyzing video...</Text>
              </View>
            ) : (
              <>
                {error && <Text style={styles.errorText}>{error}</Text>}
                <TouchableOpacity 
                  style={[styles.button, styles.primaryButton]}
                  onPress={handleAnalyzeVideo}
                >
                  <MaterialIcons name="auto-awesome" size={20} color="white" />
                  <Text style={styles.buttonText}>Analyze Speech</Text>
                </TouchableOpacity>
              </>
            )}
          </View>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  videoContainer: {
    height: '50%',
    backgroundColor: 'black',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#eee',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  actionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 10,
    marginVertical: 10,
  },
  primaryButton: {
    backgroundColor: '#4285F4',
  },
  secondaryButton: {
    backgroundColor: '#34A853',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 8,
  },
  loadingContainer: {
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  errorText: {
    color: 'red',
    marginBottom: 16,
    textAlign: 'center',
  },
  resultContainer: {
    flex: 1,
  },
  resultTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#333',
  },
  transcriptContainer: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 16,
    marginBottom: 16,
  },
  transcript: {
    fontSize: 18,
    lineHeight: 26,
    color: '#333',
  },
});

export default PreviewScreen;