import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, ActivityIndicator, TouchableOpacity, StyleSheet } from 'react-native';
import { getResults } from '../services/api';
import { BottomTabScreenProps } from '@react-navigation/bottom-tabs';

type RootTabParamList = {
  Account: undefined;
  "Add Analysis": undefined;
  Results: { submissionId?: number };
};

type ResultsHistoryScreenProps = BottomTabScreenProps<RootTabParamList, "Results">;

export default function ResultsHistoryScreen({ route }: ResultsHistoryScreenProps) {
  
  const submissionId = route?.params?.submissionId ?? null;

  if (!submissionId) {
    return <Text>No submission ID provided.</Text>;
  }
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedText, setSelectedText] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await getResults(submissionId);
        setResults(response);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching results:', error);
        setLoading(false);
      }
    };

    fetchResults();
  }, [submissionId]);

  if (loading) {
    return <ActivityIndicator size="large" color="#0000ff" />;
  }

  if (!results) {
    return <Text>No results found.</Text>;
  }

  const handleTextPress = (text: string) => {
    setSelectedText(text);
  };

  return (
    <ScrollView>
      <Text style={styles.header}>Revised Text:</Text>
      <View style={styles.textContainer}>
        {results.revised_text.split('. ').map((sentence: string, index: number) => (
          <TouchableOpacity key={index} onPress={() => handleTextPress(sentence)}>
            <Text style={styles.sentence}>{sentence}.</Text>
          </TouchableOpacity>
        ))}
      </View>
      {selectedText && (
        <View style={styles.analysisContainer}>
          <Text style={styles.analysisHeader}>Analysis for: "{selectedText}"</Text>
          <Text>Bias Score: {results.bias_score}</Text>
          {/* <Text>Truth Score: {results.truth_score}</Text> */}
          {/* Add more detailed analysis if available */}
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    margin: 10,
  },
  textContainer: {
    margin: 10,
  },
  sentence: {
    fontSize: 16,
    marginVertical: 5,
  },
  analysisContainer: {
    margin: 10,
    padding: 10,
    backgroundColor: '#f0f0f0',
    borderRadius: 5,
  },
  analysisHeader: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
});