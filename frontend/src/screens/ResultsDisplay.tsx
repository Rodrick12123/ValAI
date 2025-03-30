import React, { useState, useRef, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { BottomTabScreenProps } from '@react-navigation/bottom-tabs';
import { SafeAreaView } from 'react-native-safe-area-context';
import { styles } from '../styles/resultsDisplayStyles';
import Gauge from '../components/Gauge';
import AnalysisContainer from '../components/AnalysisContainer';

type RootTabParamList = {
  Account: undefined;
  "Add Analysis": undefined;
  ResultsDisplay: { results: any };
};

type ResultsDisplayScreenProps = BottomTabScreenProps<RootTabParamList, "ResultsDisplay">;

export default function ResultsDisplay({ route }: ResultsDisplayScreenProps) {
  const { results } = route.params;
  const [selectedContext, setSelectedContext] = useState<any>(null);
  const [analysisPosition, setAnalysisPosition] = useState<number | null>(null);

  // ScrollView ref to use scrollTo method
  const scrollViewRef = useRef<ScrollView | null>(null);

  // Ref for the analysis container
  const analysisContainerRef = useRef<View | null>(null);

  useEffect(() => {
    // Scroll to the analysis container when a context is selected
    if (selectedContext && analysisPosition !== null && scrollViewRef.current) {
      scrollViewRef.current.scrollTo({ y: analysisPosition, animated: true });
    }
  }, [selectedContext, analysisPosition]);

  const handleContextPress = (context: any) => {
    setSelectedContext(context);
  };

  const normalizeText = (text: string) =>
    // This is done properly in order to prevent quotation inconcistencies
    text.replace(/[“”]/g, '"').replace(/\s+/g, ' ')
        .replace(/['']/g, '"').replace(/\s+/g, ' ').trim();

  const renderTextWithContexts = () => {
    let fullText = normalizeText(results.fullText);
    let lastIndex = 0;
    const textElements = [];

    results["Context Contributions"].forEach((context: any, index: number) => {
      const normalizedContext = normalizeText(context.Context);
      const contextIndex = fullText.indexOf(normalizedContext, lastIndex);

      if (contextIndex === -1) return; // Skip if not found

      // Add normal text before the context
      if (contextIndex > lastIndex) {
        textElements.push(
          fullText.substring(lastIndex, contextIndex)
        );
      }

      // Add clickable context as an inline Text element
      textElements.push(
        <Text
          key={`context-${index}`}
          onPress={() => handleContextPress(context)}
          style={[
            styles.context,
            {
              backgroundColor: context["Truth Contribution"] && !context["Bias Contribution"] ? 'green' : 'red',
            },
          ]}
        >
          {fullText.substring(contextIndex, contextIndex + normalizedContext.length)}
        </Text>
      );

      lastIndex = contextIndex + normalizedContext.length;
    });

    // Add remaining normal text
    if (lastIndex < fullText.length) {
      textElements.push(fullText.substring(lastIndex));
    }

    return <Text style={styles.normalText}>{textElements}</Text>;
  };

  return (
    <SafeAreaView style={{ flex: 1 }}>
      <View style={styles.gaugeContainer}>
        <Gauge percentage={results["Overall Truth Percentage"]} label="Truth" />
        <Gauge percentage={results["Overall Bias Percentage"]} label="Bias" />
      </View>
      <ScrollView ref={scrollViewRef}>
        {/* Place uncertainty here */}
        <Text style={styles.header}>Full Text:</Text>
        <View style={styles.textContainer}>
          <ScrollView style={styles.fullTextScroll} nestedScrollEnabled={true}>
            {renderTextWithContexts()}
          </ScrollView>
        </View>

        {/* Analysis container */}
        {selectedContext && (
          <AnalysisContainer result={selectedContext} />
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
