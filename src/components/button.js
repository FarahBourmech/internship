import React from 'react';

const Button = ({ onClick, text }) => {
  return (
    <button
      onClick={onClick}
      className="w-full px-4 py-2 font-bold text-white bg-orange-500 rounded hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-400"
    >
      {text}
    </button>
  );
};

export default Button;
