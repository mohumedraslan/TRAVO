import React, { useEffect, useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';
import yaml from 'js-yaml';
import axios from 'axios';

interface ApiSpec {
  info: {
    title: string;
    description: string;
    version: string;
  };
  paths: Record<string, any>;
  components?: Record<string, any>;
}

export default function ApiDocsPage() {
  const [apiSpec, setApiSpec] = useState<ApiSpec | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchApiSpec = async () => {
      try {
        // Fetch the API spec from the backend
        const response = await axios.get('/api_spec.yaml', {
          baseURL: 'http://localhost:8000',
          responseType: 'text',
        });
        
        // Parse YAML to JavaScript object
        const parsedSpec = yaml.load(response.data) as ApiSpec;
        setApiSpec(parsedSpec);
      } catch (err) {
        console.error('Failed to load API spec:', err);
        setError('Failed to load API documentation. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchApiSpec();
  }, []);

  const renderEndpoints = () => {
    if (!apiSpec?.paths) return null;

    return Object.entries(apiSpec.paths).map(([path, methods]) => (
      <div key={path} className="mb-6 rounded-lg border border-zinc-200 bg-white p-4 shadow-sm dark:border-zinc-800 dark:bg-zinc-900">
        <h3 className="text-xl font-semibold text-blue-600 dark:text-blue-400">{path}</h3>
        
        {Object.entries(methods as Record<string, any>).map(([method, details]) => (
          <div key={`${path}-${method}`} className="mt-3">
            <div className="flex items-center gap-2">
              <span className={`rounded px-2 py-1 text-xs font-bold uppercase text-white ${
                method === 'get' ? 'bg-green-600' :
                method === 'post' ? 'bg-blue-600' :
                method === 'put' ? 'bg-orange-600' :
                method === 'delete' ? 'bg-red-600' : 'bg-gray-600'
              }`}>
                {method}
              </span>
              <span className="font-medium">{details.summary || 'No summary'}</span>
            </div>
            
            {details.description && (
              <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">{details.description}</p>
            )}
          </div>
        ))}
      </div>
    ));
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto max-w-4xl px-6 py-10">
        <h1 className="text-3xl font-bold">API Documentation</h1>
        
        {apiSpec && (
          <div className="mt-2">
            <p className="text-zinc-600 dark:text-zinc-400">
              {apiSpec.info.description}
            </p>
            <p className="mt-1 text-sm text-zinc-500 dark:text-zinc-500">
              Version: {apiSpec.info.version}
            </p>
          </div>
        )}

        {loading && (
          <div className="mt-8 flex justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
          </div>
        )}

        {error && (
          <div className="mt-6 rounded-lg border border-red-200 bg-red-50 p-4 text-red-700 dark:border-red-800 dark:bg-red-900/30 dark:text-red-400">
            {error}
          </div>
        )}

        {!loading && !error && apiSpec && (
          <div className="mt-8">
            <h2 className="mb-4 text-2xl font-semibold">Endpoints</h2>
            {renderEndpoints()}
          </div>
        )}
      </div>
    </div>
  );
}