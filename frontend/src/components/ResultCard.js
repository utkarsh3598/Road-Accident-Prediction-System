import React from 'react';

const ResultCard = ({ severity }) => {
  return (
    <div className="mt-6 p-4 bg-green-100 border-l-4 border-green-500 text-green-700 max-w-xl mx-auto">
      <p className="text-xl font-semibold">Predicted Severity:</p>
      <p className="text-2xl">{severity}</p>
    </div>
  );
};

export default ResultCard;
