import axios from 'axios';

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