import React from 'react';

const Table = ({ html }) => {
  return (
    <div
      className="mt-4"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
};

export default Table;
