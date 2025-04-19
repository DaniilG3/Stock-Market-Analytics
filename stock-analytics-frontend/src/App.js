import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const App = () => {
  const [symbol, setSymbol] = useState('AAPL');
  const [summary, setSummary] = useState('');
  const [chartData, setChartData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const res = await axios.post('https://stock-market-analytics-production.up.railway.app/summary', {
        symbol,
        sma: 197.1,
        rsi: 72,
        percent_change: 1.8,
        trend: 'bullish',
      });
      setSummary(res.data.summary);
    } catch (err) {
      setSummary('Error fetching summary');
    }
    setLoading(false);
  };

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await axios.get(`https://stock-market-analytics-production.up.railway.app/chart/${symbol}`);
        setChartData(response.data);
      } catch (error) {
        console.error('Error fetching chart data', error);
      }
    };

    fetchChartData(); // ✅ trigger it
  }, [symbol]);

  return (
    <div style={{ padding: '40px', fontFamily: 'Arial' }}>
      <h2>📈 AI Stock Summary</h2>
      <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
        <option value="AAPL">AAPL</option>
        <option value="TSLA">TSLA</option>
        <option value="GOOG">GOOG</option>
        <option value="MSFT">MSFT</option>
        <option value="AMZN">AMZN</option>
      </select>
      <br /><br />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Generating...' : 'Get Summary'}
      </button>
      <br /><br />
      <div style={{ whiteSpace: 'pre-line', marginBottom: '40px' }}>{summary}</div>

      <h3>📊 {symbol} - Close Price vs SMA-5</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="close" stroke="#8884d8" name="Close" />
          <Line type="monotone" dataKey="sma_5" stroke="#82ca9d" name="SMA-5" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default App;

