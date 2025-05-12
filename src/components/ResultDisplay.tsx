'use client';

import React from 'react';

// Using img tag instead of next/image to avoid the module not found error
// import Image from 'next/image';

interface ResultDisplayProps {
  result: {
    success: boolean;
    imageUrl: string;
    message: string;
    numberPlate: string | null;
  } | null;
}

export default function ResultDisplay({ result }: ResultDisplayProps) {
  if (!result) return null;

  return (
    <div className="w-full max-w-xl mx-auto bg-white rounded-lg shadow-md overflow-hidden mt-8">
      <div className="relative h-64 w-full">
        <img
          src={result.imageUrl}
          alt="Uploaded car image"
          className="object-contain w-full h-full"
        />
      </div>

      <div className="p-6">
        <div className="flex items-center">
          {result.numberPlate ? (
            <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold mr-2">
              Detected
            </div>
          ) : (
            <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-semibold mr-2">
              Not Detected
            </div>
          )}
          <p className="text-gray-700">{result.message}</p>
        </div>

        {result.numberPlate && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold text-gray-800">Number Plate:</h3>
            <div className="mt-2 bg-gray-200 p-4 rounded-lg flex items-center justify-center">
              <span className="text-2xl font-mono tracking-wider">{result.numberPlate}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 