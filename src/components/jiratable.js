import React from 'react';

const JiraTableField = ({ onChange,value }) => {


  return (
    <textarea
      
      onChange={onChange}
      value={value}
      placeholder="Enter Jira table code..."
      className="w-full px-4 py-2 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
      rows="6"
    />
  );
};

export default JiraTableField;
