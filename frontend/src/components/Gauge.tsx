import React from 'react';
import { View, Text } from 'react-native';
import Svg, { Circle } from 'react-native-svg';

type GaugeProps = {
  percentage: number;
  label: 'Truth' | 'Bias';
};

const Gauge: React.FC<GaugeProps> = ({ percentage, label }) => {
  const radius = 45;
  const strokeWidth = 10;
  const center = radius + strokeWidth;
  const circumference = 2 * Math.PI * radius;
  const arcLength = (percentage / 100) * circumference;
  let translateX = -22;

  if(label == "Bias"){
    translateX = -22;
  }

  // Fixed color logic: Pure red/green scaling
  const getColor = () => {
    if (label === 'Truth') {
      return percentage >= 50 ? '#00FF00' : '#FF0000';
    } else {
      return percentage >= 50 ? '#FF0000' : '#00FF00';
    }
  };

  return (
    <View style={{ alignItems: 'center'}}>
      <Svg width={center * 2} height={center * 2} viewBox={`0 0 ${center * 2} ${center * 2}`}>
        {/* Background Circle */}
        <Circle cx={center} cy={center} r={radius} stroke="#e0e0e0" strokeWidth={strokeWidth} fill="none" />
        
        {/* Progress Arc */}
        <Circle
          cx={center}
          cy={center}
          r={radius}
          stroke={getColor()}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={`${arcLength}, ${circumference}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${center} ${center})`} // Start from top
        />
      </Svg>

      {/* Centered Label & Percentage */}
      <View style={{ position: 'absolute', top: '50%', left: '50%', transform: [{ translateX: translateX}, { translateY: -24 }], alignItems: 'center' }}>
        <Text style={{ fontSize: 18, fontWeight: 'bold', transform: [{ translateX: -4}, { translateY: 0 }]}}>{label}</Text>
        <Text style={{ fontSize: 16 }}>{percentage}%</Text>
      </View>
    </View>
  );
};

export default Gauge;
