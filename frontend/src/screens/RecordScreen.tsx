import React from 'react';
import { StyleSheet, View, TouchableOpacity, Text } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import CameraView from '../components/CameraView';
import { RootStackParamList } from '../types/navigation';

type RecordScreenNavigationProp = NativeStackNavigationProp<RootStackParamList, 'Record'>;

const RecordScreen: React.FC = () => {
  const navigation = useNavigation<RecordScreenNavigationProp>();

  const handleVideoRecorded = (uri: string) => {
    navigation.navigate('Preview', { uri });
   };
  
  return (
    <View style={styles.container}>
      <StatusBar style="light" />
      
      <CameraView onVideoRecorded={handleVideoRecorded} />
      
      <TouchableOpacity 
        style={styles.backButton}
        onPress={() => navigation.goBack()}
      >
        <MaterialIcons name="arrow-back" size={24} color="white" />
      </TouchableOpacity>
      
      <View style={styles.instructions}>
        <Text style={styles.instructionText}>
          Record a video of someone speaking clearly
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  backButton: {
    position: 'absolute',
    top: 50,
    left: 20,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
  },
  instructions: {
    position: 'absolute',
    top: 50,
    left: 70,
    right: 20,
    padding: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: 10,
  },
  instructionText: {
    color: 'white',
    textAlign: 'center',
  },
});

export default RecordScreen;