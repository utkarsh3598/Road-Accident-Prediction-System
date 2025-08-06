import React, { useState } from 'react';
import axios from 'axios';

const InputForm = ({ setPrediction }) => {
  const [formData, setFormData] = useState({
    day_of_week: '',
    age_band_of_driver: '',
    light_conditions: '',
    weather_conditions: '',
    road_surface_type: '',
    type_of_vehicle: '',
  });

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/predict", formData);
      setPrediction(res.data.severity);
    } catch (err) {
      alert("Prediction failed: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-md rounded p-6 max-w-xl mx-auto">
      {Object.keys(formData).map((key) => (
        <div key={key} className="mb-4">
          <label className="block font-semibold capitalize">{key.replace(/_/g, ' ')}:</label>
          <input
            type="text"
            name={key}
            value={formData[key]}
            onChange={handleChange}
            className="w-full border rounded p-2 mt-1"
            required
          />
        </div>
      ))}
      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Predict Severity
      </button>
    </form>
  );
};

export default InputForm;
