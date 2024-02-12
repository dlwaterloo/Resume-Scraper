import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';

const containerStyle = {
  display: 'flex',
  justifyContent: 'space-around',
  alignItems: 'center',
  height: '100vh',
  padding: '0 50px',
};

const searchSectionStyle = {
  width: '40%',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  height: '60%',
};

const resultsSectionStyle = {
  width: '50%',
  borderLeft: '2px solid #ccc',
  paddingLeft: '20px',
};

const titleStyle = {
  textAlign: 'center',
  fontSize: '32px',
  fontWeight: 'bold',
  marginBottom: '20px',
  color: '#007bff',
};

const resultContainerStyle = {
  borderBottom: '1px solid #eee',
  paddingBottom: '10px',
  marginBottom: '10px',
};

const linkStyle = {
  color: '#007bff',
  textDecoration: 'none',
  fontWeight: 'bold',
};

const foundResumeStyle = {
  textAlign: 'center',
  fontSize: '20px',
  fontWeight: 'bold',
  marginTop: '30px',
};

const IndexPage = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (jobTitle, companyName) => {
    setLoading(true);
    setResults([]); // Clear existing results
    // ... Perform the search ...
    setLoading(false);
  };

  // Function to render the number of resumes found
  const renderResumeCount = () => {
    if (loading) return ''; // Do not show any message while loading
    return results.length > 0 ? `Found ${results.length} Resume${results.length > 1 ? 's' : ''}` : 'No Resumes Found';
  };

  return (
    <div style={containerStyle}>
      <div style={searchSectionStyle}>
        <h1 style={titleStyle}>Resume Search Engine</h1>
        <SearchForm onSearch={handleSearch} loading={loading} />
      </div>
      <div style={resultsSectionStyle}>
        <div style={foundResumeStyle}>{renderResumeCount()}</div>
        {results.map((result, index) => (
          <div key={index} style={resultContainerStyle}>
            <h3>{result.name}</h3>
            <a href={result.resume_link} style={linkStyle} target="_blank" rel="noopener noreferrer">Resume Link</a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default IndexPage;

