import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [videoUrls, setVideoUrls] = useState(['']);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const apiUrl = 'http://localhost:5000/api/summarize';

  const handleChange = (index, value) => {
    const urls = [...videoUrls];
    urls[index] = value;
    setVideoUrls(urls);
  };

  const addUrlField = () => {
    setVideoUrls([...videoUrls, '']);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setSummary('');
    try {
      const response = await axios.post(apiUrl, { videoUrls });
      if (response.data.success) {
        setSummary(response.data.summary);
      } else {
        alert('Error: ' + response.data.error);
      }
    } catch (err) {
      alert('Request failed: ' + err.message);
    }
    setLoading(false);
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([summary], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `summary-${Date.now()}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-6">VidGist</h1>

      <div className="w-full max-w-xl bg-white shadow-md rounded-lg p-8">
        {videoUrls.map((url, idx) => (
          <input
            key={idx}
            type="text"
            placeholder="YouTube video URL"
            value={url}
            onChange={e => handleChange(idx, e.target.value)}
            className="w-full p-3 mb-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
          />
        ))}

        <div className="flex justify-between">
          <button
            onClick={addUrlField}
            className="bg-gray-200 px-4 py-2 rounded-lg hover:bg-gray-300"
          >+ Add Video</button>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Summarizing…' : 'Summarize'}
          </button>
        </div>
      </div>

      {summary && (
        <div className="w-full max-w-xl mt-8 bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Summary</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{summary}</p>

          <button
            onClick={handleDownload}
            className="mt-4 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
          >
            Download Summary
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
