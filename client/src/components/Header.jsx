import React from 'react';

const Header = () => {
  return (
    <header className="bg-white shadow-md p-4">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">
          🚨 Road Accident Alert System
        </h1>
        <nav>
          <ul className="flex space-x-6 text-sm text-gray-700">
            <li className="hover:text-blue-600 cursor-pointer">Home</li>
            <li className="hover:text-blue-600 cursor-pointer">Predict</li>
            <li className="hover:text-blue-600 cursor-pointer">About</li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
