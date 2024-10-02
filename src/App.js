import React, { useState, useEffect } from 'react';
import TicketNameField from './components/ticketname';
import TypeField from './components/typefield';
import JiraTableField from './components/jiratable';
import Button from './components/button';
import Table from './components/Table';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false); // Corrected loading state initialization
  const [ticketName, setTicketName] = useState('');
  const [type, setType] = useState('');
  const [jiraTable, setJiraTable] = useState('');
  const [tableHtml, setTableHtml] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    if (ticketName) { 
      setLoading(true);
      fetch(`/api/v1/greet/${encodeURIComponent(ticketName)}`) //GET THE API WHICH IT'S NAME IS TICKET NAME
        .then(res => res.json())
        .then(data => {
          setData(data);
          setLoading(false);
          let desc = data.description; 
          const array = desc.split("|"); //MAKE DESCRIPTION IN AN ARRAY
          const starWords = array.filter(item => item.startsWith('*') && item.endsWith('*'));
          const count = starWords.length; //COLUMN'S NUMBER
          
          
          let index;
          for(let i=0;i<array.length;i++)
          {
            if (array[i]===type)    //GET THE INDEX OF "TYPE"
              index=i;
          }
          

          let i=0;
          for(let j=1;j<count;j++){
            array[index+j]=arrayJiraTable[i]; //FILL IN THE NECESSARY FIELDS WITH JIRA CODE
            i++;
          if (i===count-1)
            break;
          
        }
        desc=array.join('|');
        data.description=desc;
        console.log(data)
        })
        .catch(err => {
          setError(err.message);
          setLoading(false);
        });
    }
  }, [ticketName]);

  /************************GET TYPE**************************************************/
  const handleTypeChange = (event) => {
    if (event && event.target) {
      setType(event.target.value);
    } else {
      console.error('Type is undefined');
    }
  };
  

  /***************************GET JIRA CODE *****************************************/
  const handleJiraTableChange = (event) => {
    if (event && event.target) {
      setJiraTable(event.target.value);
    } else {
      console.error('Jira Table is undefined');
    }
  };
  
  /***********************MAKE JIRA CODE IN AN ARRAY******************************************/
  let arrayJiraTable=jiraTable.split('|').filter(item => item.trim() !== "");
  



  const handleSubmit = () => {
    const isValidJiraSyntax = (value) => {
      const rows = value.trim().split('\n');
      return rows.every(row => row.startsWith('|') && row.endsWith('|'));
    };

    if (!jiraTable.trim()) {
      setErrorMessage('The input should not be empty.');
      setTableHtml('');
      return;
    }

    if (!isValidJiraSyntax(jiraTable)) {
      setErrorMessage('The table syntax is invalid. Each row should start and end with |.');
      setTableHtml('');
      return;
    }

    const rows = jiraTable.trim().split('\n');
    let hasValidData = false;

    rows.forEach((row) => {
      const cells = row.split('|').filter(cell => cell.trim() !== '');
      if (cells.length > 0) {
        hasValidData = true;
      }
    });

    if (!hasValidData) {
      setErrorMessage('The table format is invalid.');
      setTableHtml('');
      return;
    }
    setErrorMessage('');

/******************************RabbitMQ************************************** */
    
const payload = {
  ticketName,  // Use correct case
  type,
  jiraTable,   // Keep it consistent with Flask
};

// Make an API call to update the Jira ticket
fetch('/api/v1/greet/send', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload),
})
  .then((res) => res.json())
  .then((data) => {
    if (data.status === 'Message sent to queue') {  // Correct status check
      setErrorMessage('');
      console.log('Ticket updated successfully:', data);
    } else {
      setErrorMessage('Failed to update the ticket.');
    }
  })
  .catch((error) => {
    setErrorMessage('An error occurred while updating the ticket.');
    console.error('Error:', error);
  });
};
  

  return (
    <div className="flex items-center justify-center min-h-screen bg-orange-200">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <table>
          <tbody>
            <tr>
              <td>
                <TicketNameField onChange={setTicketName} />
              </td>
              <td>
                <TypeField onChange={handleTypeChange} value={type} />
              </td>
            </tr>
          </tbody>
        </table>

        <JiraTableField onChange={handleJiraTableChange} />
        <Button onClick={handleSubmit} text="Send" />
        {errorMessage && (
          <p className="text-red-500 mt-4">{errorMessage}</p>
        )}
        <Table html={tableHtml} />
      </div>
    </div>
  );
}

export default App;
