import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { NavigationContainer } from '@react-navigation/native';
import AccountScreen from '../screens/AccountScreen';
import AddAnalysisTaskScreen from '../screens/AddAnalysisTaskScreen';
import ResultsHistoryScreen from '../screens/ResultsHistoryScreen';
import ResultsDisplay from '../screens/ResultsDisplay';

type RootTabParamList = {
  Account: undefined;
  "Add Analysis": undefined;
  Results: { submissionId?: number }; 
};

type RootStackParamList = {
  MainTabs: undefined;
  ResultsDisplay: { results: any, fullText: string };
};

const Tab = createBottomTabNavigator<RootTabParamList>(); 
const Stack = createStackNavigator<RootStackParamList>();

// Bottom Tab Navigator (Main Screens)
function BottomTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Account" component={AccountScreen} />
      <Tab.Screen name="Add Analysis" component={AddAnalysisTaskScreen} />
      <Tab.Screen name="Results" component={ResultsHistoryScreen} />
    </Tab.Navigator>
  );
}

// Stack Navigator (Includes Bottom Tabs + ResultsDisplay)
export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="MainTabs" component={BottomTabs} options={{ headerShown: false }} />
        <Stack.Screen 
          name="ResultsDisplay" 
          component={ResultsDisplay} 
          options={{ headerShown: true, title: 'Results', headerBackTitle: 'Back' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
