import React from 'react';

const TypeField = ({ onChange, value }) => {

  return (
    <input
      
      onChange={onChange}
      value={value}
      placeholder="Type..."
      className="w-full px-4 py-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
    />
  );
};

export default TypeField;
