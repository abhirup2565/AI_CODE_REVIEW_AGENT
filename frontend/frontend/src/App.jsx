import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Clock, Code, Github, Loader2, Search, FileCode, AlertTriangle } from 'lucide-react';

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [prNumber, setPrNumber] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [taskId, setTaskId] = useState('');
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('analyze');

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const analyzePR = async () => {
    if (!repoUrl || !prNumber) {
      setError('Repository URL and PR number are required');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze-pr`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          repo_url: repoUrl,
          pr_number: parseInt(prNumber),
          github_token: githubToken || undefined
        })
      });

      if (!response.ok) throw new Error('Failed to submit PR analysis');

      const data = await response.json();
      setTaskId(data.task_id);
      setActiveTab('status');
      pollStatus(data.task_id);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/status/${id}`);
        const data = await response.json();
        setStatus(data);

        if (data.state === 'SUCCESS') {
          clearInterval(interval);
          fetchResults(id);
        } else if (data.state === 'FAILURE') {
          clearInterval(interval);
          setLoading(false);
          setError('Analysis failed. Please try again.');
        }
      } catch (err) {
        clearInterval(interval);
        setError('Failed to fetch status');
        setLoading(false);
      }
    }, 2000);
  };

  const fetchResults = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/results/${id}`);
      const data = await response.json();
      setResults(data);
      setLoading(false);
      setActiveTab('results');
    } catch (err) {
      setError('Failed to fetch results');
      setLoading(false);
    }
  };

  const getStatusIcon = () => {
    if (!status) return <Clock className="w-5 h-5 text-gray-400" />;
    
    switch (status.state) {
      case 'PENDING':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'PROGRESS':
        return <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'SUCCESS':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'FAILURE':
        return <AlertCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusMessage = () => {
    if (!status) return 'Waiting to submit...';
    if (status.meta?.status) return status.meta.status;
    return status.state;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Code className="w-12 h-12 text-blue-500 mr-3" />
            <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              AI PR Review System
            </h1>
          </div>
          <p className="text-gray-400 text-lg">
            Automated code review powered by Google Gemini
          </p>
        </div>

        {/* Tabs */}
        <div className="flex justify-center mb-8 space-x-2">
          <button
            onClick={() => setActiveTab('analyze')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'analyze'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            <Github className="w-4 h-4 inline mr-2" />
            Analyze PR
          </button>
          <button
            onClick={() => setActiveTab('status')}
            disabled={!taskId}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'status'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            <Search className="w-4 h-4 inline mr-2" />
            Status
          </button>
          <button
            onClick={() => setActiveTab('results')}
            disabled={!results}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'results'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed'
            }`}
          >
            <FileCode className="w-4 h-4 inline mr-2" />
            Results
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-900/30 border border-red-500 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {/* Content */}
        <div className="bg-gray-800/50 backdrop-blur rounded-xl shadow-2xl p-8 border border-gray-700">
          {activeTab === 'analyze' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <Github className="w-6 h-6 mr-3 text-blue-500" />
                Submit Pull Request for Analysis
              </h2>
              
              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Repository URL *
                </label>
                <input
                  type="text"
                  value={repoUrl}
                  onChange={(e) => setRepoUrl(e.target.value)}
                  placeholder="https://github.com/owner/repo"
                  className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-100 placeholder-gray-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Pull Request Number *
                </label>
                <input
                  type="number"
                  value={prNumber}
                  onChange={(e) => setPrNumber(e.target.value)}
                  placeholder="123"
                  className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-100 placeholder-gray-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  GitHub Token (Optional)
                </label>
                <input
                  type="password"
                  value={githubToken}
                  onChange={(e) => setGithubToken(e.target.value)}
                  placeholder="ghp_xxxxxxxxxxxx"
                  className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-100 placeholder-gray-500"
                />
                <p className="text-sm text-gray-400 mt-2">
                  Required for private repositories
                </p>
              </div>

              <button
                onClick={analyzePR}
                disabled={loading}
                className="w-full px-6 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-semibold rounded-lg transition-all shadow-lg disabled:cursor-not-allowed flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Search className="w-5 h-5 mr-2" />
                    Start Analysis
                  </>
                )}
              </button>
            </div>
          )}

          {activeTab === 'status' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <Search className="w-6 h-6 mr-3 text-blue-500" />
                Analysis Status
              </h2>

              {taskId && (
                <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-gray-400">Task ID:</span>
                    <code className="px-3 py-1 bg-gray-800 rounded text-blue-400 font-mono text-sm">
                      {taskId}
                    </code>
                  </div>
                  
                  <div className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg">
                    {getStatusIcon()}
                    <div className="flex-1">
                      <p className="font-medium">{getStatusMessage()}</p>
                      <p className="text-sm text-gray-400 mt-1">
                        State: {status?.state || 'Initializing...'}
                      </p>
                    </div>
                  </div>

                  {loading && (
                    <div className="mt-4 flex items-center justify-center text-gray-400">
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      <span className="text-sm">Polling for updates...</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeTab === 'results' && results && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold mb-6 flex items-center">
                <FileCode className="w-6 h-6 mr-3 text-green-500" />
                Analysis Results
              </h2>

              <div className="bg-gradient-to-r from-green-900/20 to-blue-900/20 p-6 rounded-lg border border-green-700/30">
                <div className="flex items-center mb-4">
                  <CheckCircle className="w-6 h-6 text-green-500 mr-3" />
                  <h3 className="text-xl font-semibold">Analysis Complete</h3>
                </div>
                <p className="text-gray-300">
                  The AI has completed reviewing your pull request. Review the detailed findings below.
                </p>
              </div>

              <div className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                <h3 className="text-lg font-semibold mb-4 flex items-center">
                  <Code className="w-5 h-5 mr-2 text-blue-400" />
                  Detailed Results
                </h3>
                <pre className="bg-gray-950 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 border border-gray-800">
                  {JSON.stringify(results, null, 2)}
                </pre>
              </div>

              <button
                onClick={() => {
                  setRepoUrl('');
                  setPrNumber('');
                  setGithubToken('');
                  setTaskId('');
                  setStatus(null);
                  setResults(null);
                  setActiveTab('analyze');
                }}
                className="w-full px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-all"
              >
                Analyze Another PR
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Powered by FastAPI, Celery, and Google Gemini AI</p>
        </div>
      </div>
    </div>
  );
}

export default App;