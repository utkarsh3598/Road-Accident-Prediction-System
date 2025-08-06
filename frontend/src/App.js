import React, { useState } from 'react';
import InputForm from './components/InputForm';
import ResultCard from './components/ResultCard';

function App() {
  const [prediction, setPrediction] = useState(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">🚨 Road Accident Severity Predictor</h1>
      <InputForm setPrediction={setPrediction} />
      {prediction && <ResultCard severity={prediction} />}
    </div>
  );
}

export default App;
