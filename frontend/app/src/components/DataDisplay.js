import React from 'react';
import { useState, useEffect } from 'react';

const DataDisplay = ({ data }) => {
  const [currentPage, setCurrentPage] = useState(0);
  const dateFields = ['report_date', 'gap_start', 'gap_end','date_reported', 'date_occurred'];
  const pageSize = 50;

  // Reset current page when data changes
  useEffect(() => {
    setCurrentPage(0);
  }, [data]);

  // Function to format header names
  const formatHeader = (header) => {
    return header
      .replace(/_/g, ' ')
      .replace(/([a-z])([A-Z])/g, '$1 $2')
      .replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const formatDate = (dateString) => {
    const [year, month, day] = dateString.split('-');

    if (!dateString) {
      return ''
    }
    if (year && month && day) {
      return `${month}/${day}/${year}`
    }
    if (!year || !month || !day) {
      return dateString
    }
  };

  // Handle no data
  if (!data) {
    return (
      <div>
        <h2>Query Results</h2>
        <p>No data to display.</p>
      </div>
    );
  }

  // Handle error messages from the backend
  if (data.error) {
    return (
      <div>
        <h2>Query Results</h2>
        <p style={{ color: 'red' }}>Error: {data.error}</p>
      </div>
    );
  }

  // Check if data is an array and not empty
  if (Array.isArray(data) && data.length > 0) {
    const headers = Object.keys(data[0]);

    const startIndex = currentPage * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedData = data.slice(startIndex, endIndex);

    return (
      <div>
        <h2>Query Results</h2>
        <table>
          <thead>
            <tr>
              {headers.map((key, index) => (
                <th key={index}>{formatHeader(key)}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {headers.map((key, cellIndex) => (
                  <td key={cellIndex}>
                    {dateFields.includes(key) ? formatDate(row[key]) : row[key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        <div style={{ marginTop: '10px' }}>
          {currentPage > 0 && (
            <button onClick={() => setCurrentPage(currentPage - 1)}>Previous</button>
          )}
          {endIndex < data.length && (
            <button onClick={() => setCurrentPage(currentPage + 1)}>Next</button>
          )}
        </div>
        <br />
        {currentPage + 1} of {Math.ceil(data.length / pageSize)} Pages 
        <br />
        {pageSize * currentPage + 1} - {pageSize * currentPage + paginatedData.length} of {data.length} Results 
      </div>
    );
  }

  // Handle if data is empty
  if (Array.isArray(data) && data.length === 0) {
    return (
      <div>
        <h2>Query Results</h2>
        <p>No results found.</p>
      </div>
    );
  }
};


export default DataDisplay;
