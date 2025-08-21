/** @type {import('next').NextConfig} */
const nextConfig = {
  // output: 'standalone', // Temporarily disabled for debugging
  experimental: {
    outputFileTracingRoot: process.cwd(),
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  },
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: process.env.BACKEND_URL + '/:path*',
  //     },
  //   ];
  // },
}

module.exports = nextConfig
