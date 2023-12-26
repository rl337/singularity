
const http = require('http');
const express = require('express');
const path = require('path');
const { marked } = require('marked');

// Convert Markdown text to HTML
const markdownString = '# Hello World\nThis is a simple markdown example using **Marked**.';
const htmlContent = marked.parse(markdownString);

process.on('SIGINT', () => {
  console.log('Received SIGINT. Exiting now...');
  server.close(() => {
    // Optionally perform some cleanup
    process.exit(0);
  });
});

const app = express();

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'dist')));

const PORT = process.env.PORT || 80;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
