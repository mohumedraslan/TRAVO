// This file contains global type declarations for the project

// Add TypeScript support for JSX
import React from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      // Define any custom JSX elements here
      [elemName: string]: any;
    }
  }
}

// Add any other global type declarations here
