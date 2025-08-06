import { useState } from 'react';
import API from '../api';

function PredictionForm({ onResult }) {
  const [formData, setFormData] = useState({
    Day_of_Week: '',
    Age_band_of_driver: '',
    Light_conditions: '',
    Weather_conditions: '',
    Road_surface_type: '',
    Type_of_vehicle: ''
  });

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await API.post('/predict', formData);
      onResult(res.data.severity);
    } catch (err) {
      console.error(err);
      onResult('Error occurred');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {Object.keys(formData).map(key => (
        <div key={key}>
          <label>{key.replaceAll('_', ' ')}:</label>
          <input
            type="text"
            name={key}
            value={formData[key]}
            onChange={handleChange}
            required
            className="border p-2 w-full"
          />
        </div>
      ))}
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Predict</button>
    </form>
  );
}

export default PredictionForm;
