import axios from 'axios';
import { DocumentPickerAsset } from 'expo-document-picker';

const api = axios.create({
  baseURL: 'http://192.168.1.66:5000', 
});

export const submitText = async (userId: number, originalText: string) => {
  try {
    const response = await api.post('/submit', { user_id: userId, original_text: originalText });
    return response.data;
    
  } catch (error) {
    console.error('Error submitting text:', error);
    throw error;
  }
};

export const submitUploadedFile = async (userId: number, file: DocumentPickerAsset) => {
  try {
    const formData = new FormData();

    formData.append('user_id', userId.toString());
    formData.append('uploaded_file', {
      uri: file.uri,
      name: file.name || 'upload.txt',
      type: file.mimeType || 'text/plain',
    } as any);
    const response = await api.post('/submit/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log("submite")

    return response.data;
  } catch (error) {
    console.error('Error submitting file:', error);
    throw error;
  }
};

// might be redundant
export const submitTextDatabase = async (userId: number, originalText: string) => {
  try {
    const response = await api.post('/submitTextDatabase', { user_id: userId, original_text: originalText });
    return response.data;
    
  } catch (error) {
    console.error('Error submitting text:', error);
    throw error;
  }
};

export const getResults = async (submissionId: number) => {
  try {
    const response = await api.get(`/results/${submissionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching results:', error);
    throw error;
  }
};