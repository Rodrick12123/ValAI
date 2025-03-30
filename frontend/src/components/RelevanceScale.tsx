import React from 'react';
import { View, Text } from 'react-native';
import Svg, { Rect, Defs, LinearGradient, Stop } from 'react-native-svg';

type RelevanceScaleProps = {
  relevance: number;
  type: string;
};

const RelevanceScale: React.FC<RelevanceScaleProps> = ({ relevance, type}) => {
  const width = 100;
  const height = 20;
  const fillWidth = (relevance / 5) * width;

  return (
    <View style={{ alignItems: 'center', marginVertical: 10 }}>
      <Text style={{ fontSize: 10, marginBottom: 5 }}>{type} Relevance Scale</Text>
      <Svg width={width} height={height}>
        <Defs>
          <LinearGradient id="flameGradient" x1="0" y1="0" x2="1" y2="0">
            <Stop offset="0%" stopColor="#333" />
            <Stop offset="100%" stopColor={`rgb(${relevance * 51}, 0, 0)`} />
          </LinearGradient>
        </Defs>
        <Rect x="0" y="0" width={width} height={height} fill="#e0e0e0" />
        <Rect x="0" y="0" width={fillWidth} height={height} fill="url(#flameGradient)" />
      </Svg>
      
      <Text style={{ fontSize: 14, marginTop: 5 }}>Rank: {relevance}</Text>
    </View>
  );
};

export default RelevanceScale; 