import React, { useState } from 'react';
import { View, TextInput, Button, Text, ActivityIndicator } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { submitText, submitTextDatabase } from '../services/api';
import { NavigationProp } from "@react-navigation/native";

type AddAnalysisTaskScreenProps = {
  navigation: NavigationProp<any>;
};

export default function AddAnalysisTaskScreen({ navigation }: AddAnalysisTaskScreenProps) {
    const [text, setText] = useState('');
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const handleDocumentUpload = async () => {
        try {
        const result = await DocumentPicker.getDocumentAsync({
            type: 'text/*',
        });

        if (result.canceled || !result.assets || result.assets.length === 0) {
            console.log("User canceled document selection or no file selected.");
            return;
        }

        const file = result.assets[0]; // `assets` is an array
        

        if (file) {
            const fileContent = await fetch(file.uri).then((res) => res.text());
            setText(fileContent);
        }

        // if (result.type === 'success') {
        //     const fileContent = await fetch(result.uri).then(res => res.text());
        //     setText(fileContent);
        // }
        } catch (error) {
        console.error('Error uploading document:', error);
        }
    };

    const handleSubmit = async () => {
        setLoading(true);
        try {
          const response = await submitText(1, text);
          setMessage(response.message);
          setLoading(false);
          
          // Navigate using parent Stack Navigator
          navigation.getParent()?.navigate('ResultsDisplay', { results: response });
        } catch (error) {
          setMessage('Failed to submit text');
          setLoading(false);
        }
    };

    return (
        <View>
            <Button title="Upload Document" onPress={handleDocumentUpload} />
                <TextInput
                    placeholder="Enter text for analysis"
                    value={text}
                    onChangeText={setText}
                    multiline
                    style={{ height: 100, borderColor: 'gray', borderWidth: 1, margin: 10 }}
                />
            <Button title="Submit" onPress={handleSubmit} />
            {loading && <ActivityIndicator size="large" color="#0000ff" />}
            {message && <Text>{message}</Text>}
        </View>
    );
}