
export default function Home() {
  const iframeUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000/p/agricultural-commodity-beginning-stocks-over-time';
  
  return (
    <div className="min-h-screen font-[family-name:var(--font-geist-sans)]">
      <main className="grid grid-cols-3 h-screen">
        {/* Left pane */}
        <div className="col-span-1 border-r border-gray-200 p-4">
          {/* Empty for now */}
        </div>
        
        {/* Right pane with iframe */}
        <div className="col-span-2">
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
