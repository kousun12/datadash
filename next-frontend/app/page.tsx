
'use client';
import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState('');
  
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      setInput('');
    }
  };

  return (
    <div className="min-h-screen font-[family-name:var(--font-geist-sans)] light">
      <main className="h-screen">
        <div className="w-96 fixed left-0 top-0 bottom-0 border-r border-gray-200 flex flex-col">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto p-4" style={{ height: 'calc(100vh - var(--input-height))' }}>
            <div className="flex flex-col justify-end min-h-full gap-4">
            {sampleMessages.map((message) => (
              <div
                key={message.id}
                className={`max-w-[85%] p-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-100 ml-auto'
                    : 'bg-gray-100'
                }`}
              >
                {message.content}
              </div>
            ))}
            </div>
          </div>
          
          <div className="p-4 border-t border-gray-200">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Explore the data..."
              className="w-full p-2 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={3}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
