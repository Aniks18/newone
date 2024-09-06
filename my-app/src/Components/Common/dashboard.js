import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './dashboard.css';
import LoadingAnimationWrapper from './LoadingAnimation';

const Dashboard = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState('');
  const [searchResult, setSearchResult] = useState('');
  const [processedData, setProcessedData] = useState(null);
  const [twitterData, setTwitterData] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [wordcloudImageUrl, setWordcloudImageUrl] = useState('');
  const [temporalImageUrl, setTemporalImageUrl] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearchQueryChange = (e) => setSearchQuery(e.target.value);
  const handleLocationChange = (e) => setLocation(e.target.value);

  const handleSearch = async () => {
    setLoading(true);
    setError(null);
    setProcessedData(null);
    setTwitterData(null);
    setImageUrl('');
    setWordcloudImageUrl('');
    setTemporalImageUrl('');

    try {
      const response = await axios.post('http://localhost:5000/search', {
        query: searchQuery,
        location: location,
      });

      setSearchResult(response.data.message);

      // Simulate a 12-second loading time
      setTimeout(() => {
        fetchProcessedData();
        fetchTwitterData();
        fetchImage();
        fetchWordcloudImage();
        fetchTemporalImage(); // Fetch temporal analysis image
        setLoading(false);
      }, 12000);
    } catch (error) {
      console.error('Error during search or processing:', error);
      setError('Failed to perform search. Please try again.');
      setLoading(false);
    }
  };

  const fetchProcessedData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/results', {
        responseType: 'json',
        timeout: 5000,
      });

      if (response.status === 200 && response.data) {
        setProcessedData(response.data);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Error fetching processed data:', error);
      setError(`Failed to fetch results. Error: ${error.message}`);
    }
  };

  const fetchTwitterData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/twitterresults', {
        responseType: 'json',
        timeout: 5000,
      });

      if (response.status === 200 && response.data) {
        setTwitterData(response.data);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Error fetching Twitter data:', error);
      setError(`Failed to fetch Twitter results. Error: ${error.message}`);
    }
  };

  const fetchImage = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/image', {
        responseType: 'blob',
        timeout: 5000,
      });

      if (response.status === 200) {
        const url = URL.createObjectURL(response.data);
        setImageUrl(url);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Error fetching image:', error);
      setError(`Failed to fetch image. Error: ${error.message}`);
    }
  };

  const fetchWordcloudImage = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/wordcloud', {
        responseType: 'blob',
        timeout: 5000,
      });

      if (response.status === 200) {
        const url = URL.createObjectURL(response.data);
        setWordcloudImageUrl(url);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Error fetching wordcloud image:', error);
      setError(`Failed to fetch wordcloud image. Error: ${error.message}`);
    }
  };

  const fetchTemporalImage = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/temporal', {
        responseType: 'blob',
        timeout: 5000,
      });

      if (response.status === 200) {
        const url = URL.createObjectURL(response.data);
        setTemporalImageUrl(url);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('Error fetching temporal image:', error);
      setError(`Failed to fetch temporal image. Error: ${error.message}`);
    }
  };

  useEffect(() => {
    const interval = setInterval(fetchProcessedData, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <LoadingAnimationWrapper show={loading} />
      
      <div className="header">
        <h1 className="dashboard-title">UDDHRTI AI DASHBOARD</h1>
        <div className="search-container">
          <input
            type="text"
            placeholder="Search Query..."
            value={searchQuery}
            onChange={handleSearchQueryChange}
            className="search-input"
          />
          <input
            type="text"
            placeholder="Location..."
            value={location}
            onChange={handleLocationChange}
            className="search-input"
          />
          <button onClick={handleSearch} className="search-button">Search</button>
        </div>
      </div>
      
      <div className="content">
        {error && (
          <div className="error-message" role="alert">
            <strong className="font-bold">Error!</strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {searchResult && (
          <div className="search-result">
            <div className="font-bold">Search Result:</div>
            <p>{searchResult}</p>
          </div>
        )}

        {processedData && (
          <div className="processed-data">
            <h2 className="data-title">News Data</h2>
            <pre className="data-content">
              {JSON.stringify(processedData, null, 2)}
            </pre>
          </div>
        )}

        {twitterData && (
          <div className="twitter-data">
            <h2 className="data-title">Twitter Data</h2>
            <pre className="data-content">
              {JSON.stringify(twitterData, null, 2)}
            </pre>
          </div>
        )}

        {imageUrl && (
          <div className="image-data">
            <h2 className="data-title">Analysis Image</h2>
            <img src={imageUrl} alt="Analysis" className="analysis-image" />
          </div>
        )}

        {wordcloudImageUrl && (
          <div className="image-data">
            <h2 className="data-title">Wordcloud Image</h2>
            <img src={wordcloudImageUrl} alt="Wordcloud" className="analysis-image" />
          </div>
        )}

        {temporalImageUrl && (
          <div className="image-data">
            <h2 className="data-title">Temporal Analysis Image</h2>
            <img src={temporalImageUrl} alt="Temporal Analysis" className="analysis-image" />
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
