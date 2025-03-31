# Review Analysis Frontend

This is the frontend for the Sentiment & Aspect-Based Review Analysis Web App. It provides a user interface for analyzing product reviews, extracting key aspects, and detecting sentiment.

## Features

- Clean UI for inputting or uploading product reviews
- Text box for manual review input
- File upload option for bulk reviews (CSV format)
- Results section displaying:
  - Overall Sentiment (Positive, Neutral, Negative)
  - Key Aspects with detected sentiment
  - Summarized Review (AI-generated summary)
- Trend graph showing sentiment changes over time
- Table listing uploaded reviews with filter options

## Tech Stack

- React (Next.js)
- Tailwind CSS
- Chart.js for data visualization
- Axios for API requests

## Requirements

- Node.js 18+
- npm or yarn

## Setup

1. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

2. Create a `.env.local` file in the root directory with the following variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

- `app/` - Next.js app directory
  - `page.tsx` - Home page
  - `layout.tsx` - Root layout
  - `globals.css` - Global styles
  - `analyze/` - Review analysis page
    - `page.tsx` - Analysis input page
    - `results/` - Analysis results page
  - `dashboard/` - Dashboard page
  - `reviews/` - Reviews listing page

## Building for Production

```bash
npm run build
# or
yarn build
```

## Deployment

The frontend can be deployed to Vercel:

```bash
npm install -g vercel
vercel
```

## Backend Connection

This frontend connects to the Review Analysis API backend. Make sure the backend is running at the URL specified in your `.env.local` file.
