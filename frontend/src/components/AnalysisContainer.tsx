import React, { useState } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { styles } from '../styles/resultsDisplayStyles';
import RelevanceScale from './RelevanceScale';

type AnalysisContainerProps = {
    result: any;
};

const AnalysisContainer: React.FC<AnalysisContainerProps> = ({ result }) => {
    const [showSources, setShowSources] = useState<boolean>(false);
    const [showImproved, setShowImproved] = useState<boolean>(false);

    return (
        <View style={styles.analysisContainer}>
        <Text style={styles.analysisHeader}>Analysis for: "{result.Context}"</Text>
        <View style={styles.truthBiasContainer}>
            <Text style={styles.analysisDetail}>
                True: {result["Truth Contribution"] === true ? 'Yes' : result["Truth Contribution"] === false ? 'No' : 'Unknown'}
            </Text>
            <Text style={styles.analysisDetail}>Biased: {result["Bias Contribution"] === true ? 'Yes' : result["Bias Contribution"] === false ? 'No': 'Unkown'}</Text>
        </View>

        <RelevanceScale relevance={result["Truth Relevance Scale (1-5)"]} type='Truth' />
        <RelevanceScale relevance={result["Bias Relevance Scale (1-5)"]} type="Bias" />
        
        <Text style={{ fontSize: 16, textAlign: "center", fontWeight: 700}}>Reason Behind Evaluation:</Text>
        <Text style={styles.analysisReason}>{result["Reason"]}</Text>

        {result["Improved"] && (
            <TouchableOpacity onPress={() => setShowImproved(!showImproved)}>
            <Text style={styles.toggleImproved}>{showImproved ? 'Hide Improvement' : 'Show Improvement'}</Text>
            </TouchableOpacity>
        )}
        {showImproved && (
            <Text style={styles.improvedText}>{result["Improved"]}</Text>
        )}

        {result["TruthSources"] != "" &&(
            <TouchableOpacity onPress={() => setShowSources(!showSources)}>
                <Text style={styles.toggleSources}>{showSources ? 'Hide Sources' : 'Show Sources'}</Text>
            </TouchableOpacity>
        )}
        {showSources && result["TruthSources"] && (
            <View style={styles.sourcesContainer}>
            {result["TruthSources"].map((source: string, index: number) => (
                <Text key={index} style={styles.sourceItem}>{source}</Text>
            ))}
            </View>
        )}
        </View>
    );
};

export default AnalysisContainer; 