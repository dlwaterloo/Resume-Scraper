import React, { useState } from 'react';

const searchFormStyle = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '20px',
  gap: '10px',
};

const inputStyle = {
  width: '300px',
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid #ccc',
};

const buttonStyle = {
  padding: '10px 20px',
  borderRadius: '5px',
  border: 'none',
  backgroundColor: '#007bff',
  color: 'white',
  cursor: 'pointer',
};

const spinnerStyle = {
  marginLeft: '10px',
  border: '4px solid #f3f3f3',
  borderTop: '4px solid #3498db',
  borderRadius: '50%',
  width: '24px',
  height: '24px',
  animation: 'spin 2s linear infinite',
  alignSelf: 'center',
};

const buttonSpinnerContainerStyle = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const SearchForm = ({ onSearch, loading }) => {
  const [jobTitle, setJobTitle] = useState('');
  const [companyName, setCompanyName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(jobTitle, companyName);
  };

  return (
    <form onSubmit={handleSubmit} style={searchFormStyle}>
      <input 
        type="text" 
        value={jobTitle} 
        onChange={(e) => setJobTitle(e.target.value)} 
        placeholder="Job Title" 
        style={inputStyle} 
        disabled={loading}
      />
      <input 
        type="text" 
        value={companyName} 
        onChange={(e) => setCompanyName(e.target.value)} 
        placeholder="Company Name" 
        style={inputStyle}
        disabled={loading}
      />
      <div style={buttonSpinnerContainerStyle}>
        <button type="submit" style={buttonStyle} disabled={loading}>
          Search
        </button>
        {loading && <div style={spinnerStyle}></div>}
      </div>
    </form>
  );
};

export default SearchForm;


