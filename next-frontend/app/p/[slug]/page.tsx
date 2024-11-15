'use client';
import { use } from 'react';

export default function PlotPage({
  params
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = use(params);
  const baseUrl = process.env.NEXT_PUBLIC_DEFAULT_IFRAME_URL || 'http://localhost:3000';
  const iframeUrl = `${baseUrl}/p/${slug}`;

  return (
    <div className="min-h-screen">
      <iframe 
        src={iframeUrl}
        className="w-full h-screen border-0"
        allow="fullscreen"
      />
    </div>
  );
}
