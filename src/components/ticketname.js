import React, { useState } from 'react';

const TicketNameField = ({ onChange }) => {
  const [ticketName, setTicketName] = useState('');

  const handleChange = (e) => {
    setTicketName(e.target.value);
    onChange(e.target.value);
  };

  return (
    <input
      value={ticketName}
      onChange={handleChange}
      placeholder="Ticket name..."
      className="w-full px-4 py-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
    />
  );
};

export default TicketNameField;
