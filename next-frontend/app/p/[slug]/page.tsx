'use client';
import {use, useState} from 'react';

const sampleMessages = [
  { id: 1, role: 'user', content: 'Can you analyze the agricultural data?' },
  { id: 2, role: 'assistant', content: 'I\'d be happy to help analyze the agricultural data. What specific aspects would you like to explore?' },
  { id: 3, role: 'user', content: 'Show me trends in corn stocks over time.' },
  { id: 4, role: 'assistant', content: 'I\'ve loaded the visualization showing corn stock trends. You can see there are significant seasonal variations, with peaks typically occurring after harvest seasons.' },
];

export default function PlotPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params);
  const baseUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000';
  const iframeUrl = `${baseUrl}/p/${slug}`;
  const [input, setInput] = useState('');

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sampleMessages.push({ id: sampleMessages.length + 1, role: 'user', content: input });
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
        <div className="fixed right-0 top-0 bottom-0 left-96 bg-white">
          <iframe
            src={iframeUrl}
            className="w-full h-full border-0"
            allow="fullscreen"
          />
        </div>
      </main>
    </div>
  );
}
