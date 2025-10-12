import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Clock, Code, Github, Loader2, Search, FileCode, Trash2, Eye, Sparkles, Zap, Shield, ArrowRight, LogOut } from 'lucide-react';

// Landing Page Component
function LandingPage({ onGetStarted }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-gray-100">
      {/* Navigation */}
      <nav className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Code className="w-8 h-8 text-blue-500" />
            <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
              AI PR Review
            </span>
          </div>
          <button
            onClick={onGetStarted}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all"
          >
            Sign In
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-20 text-center">
        <div className="max-w-4xl mx-auto">
          <div className="inline-block mb-6 px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full">
            <span className="text-blue-400 text-sm font-medium">✨ Powered by Google Gemini AI</span>
          </div>
          
          <h1 className="text-6xl font-bold mb-6 leading-tight">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
              AI-Powered Code Review
            </span>
            <br />
            <span className="text-white">In Seconds, Not Hours</span>
          </h1>
          
          <p className="text-xl text-gray-300 mb-12 max-w-2xl mx-auto">
            Automatically analyze GitHub Pull Requests with advanced AI. Get instant insights, 
            catch bugs, and improve code quality before merging.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={onGetStarted}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-semibold text-lg transition-all shadow-lg flex items-center justify-center"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button className="px-8 py-4 bg-gray-800 hover:bg-gray-700 rounded-lg font-semibold text-lg transition-all border border-gray-700">
              View Demo
            </button>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-16">
            Why Choose <span className="text-blue-400">AI PR Review?</span>
          </h2>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gray-800/50 backdrop-blur p-8 rounded-xl border border-gray-700 hover:border-blue-500/50 transition-all">
              <div className="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center mb-4">
                <Zap className="w-6 h-6 text-blue-500" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Lightning Fast</h3>
              <p className="text-gray-400">
                Get comprehensive code reviews in seconds. No more waiting hours for manual reviews.
              </p>
            </div>

            <div className="bg-gray-800/50 backdrop-blur p-8 rounded-xl border border-gray-700 hover:border-purple-500/50 transition-all">
              <div className="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center mb-4">
                <Sparkles className="w-6 h-6 text-purple-500" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-Powered Insights</h3>
              <p className="text-gray-400">
                Leverage Google Gemini's advanced AI to catch bugs, security issues, and code smells.
              </p>
            </div>

            <div className="bg-gray-800/50 backdrop-blur p-8 rounded-xl border border-gray-700 hover:border-green-500/50 transition-all">
              <div className="w-12 h-12 bg-green-500/10 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-green-500" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Secure & Private</h3>
              <p className="text-gray-400">
                Your code is analyzed securely. Optional GitHub token support for private repos.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="max-w-4xl mx-auto bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur p-12 rounded-2xl border border-blue-500/30 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Code Reviews?</h2>
          <p className="text-gray-300 mb-8 text-lg">
            Join developers who are saving hours every week with AI-powered code reviews.
          </p>
          <button
            onClick={onGetStarted}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-lg font-semibold text-lg transition-all shadow-lg"
          >
            Start Reviewing Now
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 border-t border-gray-800">
        <div className="text-center text-gray-500">
          <p>© 2024 AI PR Review. Powered by FastAPI, Celery & Google Gemini.</p>
        </div>
      </footer>
    </div>
  );
}

// Login Page Component
function LoginPage({ onLogin, onBack }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    // Demo authentication - replace with real API call
    if (email && password.length >= 6) {
      const user = { email, name: email.split('@')[0] };
      onLogin(user);
    } else {
      setError('Invalid credentials. Password must be at least 6 characters.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Back Button */}
        <button
          onClick={onBack}
          className="mb-6 text-gray-400 hover:text-gray-300 flex items-center transition-colors"
        >
          <ArrowRight className="w-4 h-4 mr-2 rotate-180" />
          Back to Home
        </button>

        {/* Logo */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <Code className="w-12 h-12 text-blue-500" />
          </div>
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            AI PR Review
          </h1>
          <p className="text-gray-400 mt-2">
            {isSignUp ? 'Create your account' : 'Welcome back'}
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-gray-800/50 backdrop-blur rounded-xl shadow-2xl p-8 border border-gray-700">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-900/30 border border-red-500 rounded-lg flex items-start">
                <AlertCircle className="w-5 h-5 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-100 placeholder-gray-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-gray-100 placeholder-gray-500"
              />
            </div>

            <button
              type="submit"
              className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-lg transition-all shadow-lg"
            >
              {isSignUp ? 'Sign Up' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              onClick={() => setIsSignUp(!isSignUp)}
              className="text-blue-400 hover:text-blue-300 text-sm"
            >
              {isSignUp 
                ? 'Already have an account? Sign In' 
                : "Don't have an account? Sign Up"}
            </button>
          </div>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 p-4 bg-gray-800/30 rounded-lg border border-gray-700">
          <p className="text-gray-400 text-sm text-center">
            <strong className="text-gray-300">Demo:</strong> Use any email with password (6+ chars)
          </p>
        </div>
      </div>
    </div>
  );
}

// Main Dashboard Component
function Dashboard({ user, onLogout }) {
  const [repoUrl, setRepoUrl] = useState('');
  const [prNumber, setPrNumber] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [taskList, setTaskList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('analyze');
  const [selectedResult, setSelectedResult] = useState(null);
  const [showResultModal, setShowResultModal] = useState(false);

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    const savedTasks = JSON.parse(localStorage.getItem('prReviewTasks') || '[]');
    setTaskList(savedTasks);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      pollAllTasks();
    }, 5000);

    return () => clearInterval(interval);
  }, [taskList]);

  const saveTasksToLocalStorage = (tasks) => {
    localStorage.setItem('prReviewTasks', JSON.stringify(tasks));
    setTaskList(tasks);
  };

  const analyzePR = async () => {
    if (!repoUrl || !prNumber) {
      setError('Repository URL and PR number are required');
      return;
    }

    setLoading(true);
    setError('');

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
      
      const newTask = {
        id: data.task_id,
        repoUrl,
        prNumber,
        state: 'PENDING',
        meta: {},
        result: null,
        createdAt: new Date().toISOString()
      };

      const updatedTasks = [...taskList, newTask];
      saveTasksToLocalStorage(updatedTasks);
      
      setRepoUrl('');
      setPrNumber('');
      setGithubToken('');
      setActiveTab('status');
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const pollAllTasks = async () => {
    const incompleteTasks = taskList.filter(
      task => task.state !== 'SUCCESS' && task.state !== 'FAILURE'
    );

    for (const task of incompleteTasks) {
      try {
        const response = await fetch(`${API_BASE_URL}/status/${task.id}`);
        const data = await response.json();

        const updatedTasks = taskList.map(t => 
          t.id === task.id ? { ...t, state: data.state, meta: data.meta || {} } : t
        );
        saveTasksToLocalStorage(updatedTasks);
      } catch (err) {
        console.error(`Failed to fetch status for task ${task.id}`, err);
      }
    }
  };

  const fetchResult = async (taskId) => {
    try {
      const response = await fetch(`${API_BASE_URL}/results/${taskId}`);
      const data = await response.json();
      setSelectedResult(data);
      setShowResultModal(true);
    } catch (err) {
      setError('Failed to fetch results');
    }
  };

  const deleteTask = (taskId) => {
    const updatedTasks = taskList.filter(task => task.id !== taskId);
    saveTasksToLocalStorage(updatedTasks);
  };

  const getStatusIcon = (state) => {
    switch (state) {
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

  const getStatusMessage = (task) => {
    if (task.meta?.status) return task.meta.status;
    return task.state || 'Unknown';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header with Logout */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center">
            <Code className="w-10 h-10 text-blue-500 mr-3" />
            <div>
              <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
                AI PR Review System
              </h1>
              <p className="text-gray-400 text-sm">Welcome, {user.name}!</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-all flex items-center border border-gray-700"
          >
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </button>
        </div>

        <p className="text-center text-gray-400 text-lg mb-8">
          Automated code review powered by Google Gemini
        </p>

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
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'status'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            <Search className="w-4 h-4 inline mr-2" />
            Status ({taskList.length})
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 p-4 bg-red-900/30 border border-red-500 rounded-lg flex items-start">
            <AlertCircle className="w-5 h-5 text-red-500 mr-3 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-red-200">{error}</p>
            </div>
            <button onClick={() => setError('')} className="text-red-400 hover:text-red-300">
              ×
            </button>
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
                    Submitting...
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

              {taskList.length === 0 ? (
                <div className="text-center py-12">
                  <FileCode className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400 text-lg">No analysis tasks yet</p>
                  <p className="text-gray-500 mt-2">Submit a PR to get started</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {taskList.map((task) => (
                    <div key={task.id} className="bg-gray-900/50 p-6 rounded-lg border border-gray-700">
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex-1">
                          <div className="flex items-center mb-2">
                            <Github className="w-4 h-4 text-gray-400 mr-2" />
                            <span className="text-sm text-gray-300">PR #{task.prNumber}</span>
                          </div>
                          <code className="text-xs bg-gray-800 px-2 py-1 rounded text-blue-400 font-mono">
                            {task.id}
                          </code>
                        </div>
                        <button
                          onClick={() => deleteTask(task.id)}
                          className="text-red-400 hover:text-red-300 p-2 hover:bg-red-900/20 rounded transition-colors"
                          title="Delete task"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-4 bg-gray-800/50 rounded-lg mb-4">
                        {getStatusIcon(task.state)}
                        <div className="flex-1">
                          <p className="font-medium">{getStatusMessage(task)}</p>
                          <p className="text-sm text-gray-400 mt-1">
                            State: {task.state || 'Unknown'}
                          </p>
                        </div>
                      </div>

                      {task.state === 'SUCCESS' && (
                        <button
                          onClick={() => fetchResult(task.id)}
                          className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-all flex items-center justify-center"
                        >
                          <Eye className="w-4 h-4 mr-2" />
                          View Results
                        </button>
                      )}

                      {task.state === 'FAILURE' && (
                        <div className="p-3 bg-red-900/20 border border-red-700 rounded-lg text-red-300 text-sm">
                          Analysis failed. Please try again.
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Result Modal */}
        {showResultModal && selectedResult && (
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-gray-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden border border-gray-700">
              <div className="p-6 border-b border-gray-700 flex items-center justify-between">
                <h3 className="text-2xl font-semibold flex items-center">
                  <FileCode className="w-6 h-6 mr-3 text-green-500" />
                  Analysis Results
                </h3>
                <button
                  onClick={() => setShowResultModal(false)}
                  className="text-gray-400 hover:text-gray-300 text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="p-6 overflow-y-auto max-h-[calc(90vh-200px)]">
                <div className="bg-gradient-to-r from-green-900/20 to-blue-900/20 p-4 rounded-lg border border-green-700/30 mb-6">
                  <div className="flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-500 mr-3" />
                    <p className="text-gray-300">Analysis completed successfully</p>
                  </div>
                </div>

                <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                  <pre className="bg-gray-950 p-4 rounded-lg overflow-x-auto text-sm text-gray-300 border border-gray-800">
                    {JSON.stringify(selectedResult, null, 2)}
                  </pre>
                </div>
              </div>

              <div className="p-6 border-t border-gray-700">
                <button
                  onClick={() => setShowResultModal(false)}
                  className="w-full px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-all"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>Powered by FastAPI, Celery, and Google Gemini AI</p>
        </div>
      </div>
    </div>
  );
}

// Main App Component with Routing
function App() {
  const [currentPage, setCurrentPage] = useState('landing');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('prReviewUser');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
      setCurrentPage('dashboard');
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('prReviewUser', JSON.stringify(userData));
    setCurrentPage('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('prReviewUser');
    setCurrentPage('landing');
  };

  const handleGetStarted = () => {
    setCurrentPage('login');
  };

  const handleBackToLanding = () => {
    setCurrentPage('landing');
  };

  if (currentPage === 'landing') {
    return <LandingPage onGetStarted={handleGetStarted} />;
  }

  if (currentPage === 'login') {
    return <LoginPage onLogin={handleLogin} onBack={handleBackToLanding} />;
  }

  if (currentPage === 'dashboard' && user) {
    return <Dashboard user={user} onLogout={handleLogout} />;
  }

  return <LandingPage onGetStarted={handleGetStarted} />;
}

export default App;