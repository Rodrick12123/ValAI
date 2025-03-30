import { StyleSheet } from 'react-native';

export const styles = StyleSheet.create({
  header: {
    fontSize: 18,
    fontWeight: 'bold',
    margin: 10,
  },
  gaugeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    marginBottom: 10
  },
  textContainer: {
    margin: 10,
    maxHeight: 300, // Limit the height of the text container
  },
  fullTextScroll: {
    maxHeight: 300, // Ensure the scrollable area is limited
  },
  context: {
    marginVertical: 5,
    padding: 5,
    borderRadius: 10,
  },
  normalText: {
    fontSize: 16,
    color: 'black',
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
  truthBiasContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  analysisDetail: {
    fontSize: 16,
    marginBottom: 5,
  },
  analysisReason: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 10,
  },
  toggleImproved: {
    fontSize: 14,
    color: '#007bff',
    textDecorationLine: 'underline',
    textAlign: 'center',
    marginVertical: 10,
  },
  improvedText: {
    fontSize: 16,
    color: '#333',
    marginVertical: 10,
    paddingHorizontal: 10,
    backgroundColor: '#e8f5e9',
    borderRadius: 5,
  },
  toggleSources: {
    fontSize: 14,
    color: '#007bff',
    textDecorationLine: 'underline',
    textAlign: 'center',
    marginVertical: 10,
  },
  sourcesContainer: {
    marginTop: 10,
  },
  sourceItem: {
    fontSize: 14,
    marginBottom: 5,
    color: '#333',
  },
});
