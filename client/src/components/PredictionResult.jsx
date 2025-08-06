function PredictionResult({ result }) {
  return (
    <div className="mt-4 p-4 bg-green-100 border border-green-400 rounded">
      <h2 className="font-bold">Prediction:</h2>
      <p>{result}</p>
    </div>
  );
}

export default PredictionResult;
