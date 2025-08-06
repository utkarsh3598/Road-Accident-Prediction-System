import React from 'react';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="p-4 max-w-3xl mx-auto">
        <PredictionForm />
      </main>
    </div>
  );
}

export default App;
