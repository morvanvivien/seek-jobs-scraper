# How to Scrape SEEK: Australia & New Zealand Job Postings (No Login)

> **Run it now, no code: [seek-jobs-scraper on the Apify Store](https://apify.com/bibian/seek-jobs-scraper)** &nbsp;|&nbsp; pay per result &nbsp;|&nbsp; no login, no CAPTCHA solving

SEEK is the largest job board in Australia and New Zealand. It has no public export and no official API for third parties, and it blocks plain HTTP requests, datacenter proxies and even a Chrome-impersonating TLS fingerprint on a residential proxy. This guide shows how to get SEEK postings as clean structured data anyway: title, company, salary, location and work type, straight from SEEK's own public search pages, with a real stealth browser behind a residential proxy doing the work for you.

Searches this page answers: SEEK scraper, SEEK job scraper, seek.com.au API, Australia jobs scraper, New Zealand jobs scraper.

## What you get from the SEEK scraper

- Every job posting matching your search, newest first: title, company, location, salary (when SEEK's advertiser discloses one) and employment type.
- Both SEEK sites in one Actor: `seek.com.au` (Australia) and `seek.co.nz` (New Zealand).
- Search by keyword, SEEK classification (e.g. "information-communication-technology") or location slug (e.g. "All-Sydney-NSW").
- "Only new results" mode for scheduled runs, so a daily run only returns, and charges, what is new.

Export the dataset as JSON, CSV or Excel, or read it through the Apify API. A real sample (five results from a live run, personal data removed) is in [`sample-output.json`](sample-output.json).

## Output fields

| Field | What it is |
|---|---|
| `id`, `url` | Stable SEEK job id and public link |
| `title`, `companyName` | Job title and advertiser as displayed |
| `locationLabel`, `city`, `region`, `postalCode`, `country` | Where the job is based |
| `remote` | `remote`, `hybrid`, `onsite` or `unknown` (SEEK's search card rarely states it) |
| `employmentType` | `full_time`, `part_time`, `contract`, `temporary` or `unknown` |
| `salaryMin`, `salaryMax`, `salaryCurrency`, `salaryPeriod` | Parsed from SEEK's own free-text salary label, `null` when SEEK shows no figure |
| `salaryLabel` | SEEK's raw salary text, always kept even when parsing fails |
| `datePosted` | ISO date the ad went live |
| `description` | SEEK's own short teaser (the full ad lives behind a page `robots.txt` disallows, see "Good to know") |
| `industry`, `subClassification` | SEEK's own category and sub-category |
| `bulletPoints` | The 1-3 short highlight lines SEEK shows on the search card |
| `source`, `sourceId`, `scrapedAt` | `seek.com.au`/`seek.co.nz`, SEEK's native job id, extraction timestamp |

## Use cases

- **Feed a job board or aggregator** with fresh Australian or New Zealand listings, deduplicated by SEEK's own job id.
- **Track a role or a market** (for example "software engineer" in Sydney) with "Only new results" switched on, so a scheduled run bills only the postings it hasn't delivered before.
- **Benchmark pay** for a role or region from the salary ranges SEEK's own advertisers disclose.
- **Monitor a classification** (for example "Information & Communication Technology") for volume and type mix over time.

## Input

| Field | What it does |
|---|---|
| `country` | `AU` searches seek.com.au, `NZ` searches seek.co.nz. |
| `keyword` | Job title or keyword, for example `software engineer`. Cannot be combined with `classification`. |
| `classification` | SEEK classification slug, exactly as it appears in a `seek.com.au/jobs-in-<slug>` URL. Cannot be combined with `keyword`. |
| `location` | SEEK location slug, exactly as it appears in a `.../in-<slug>` URL, for example `All-Sydney-NSW`. Empty searches the whole country. |
| `maxItems` | The run stops once this many postings are saved (default 50). |
| `onlyNew` | For scheduled runs: skip postings an earlier run of this same search already delivered. |

Example input:

```json
{
  "country": "AU",
  "keyword": "software engineer",
  "location": "All-Sydney-NSW",
  "maxItems": 50
}
```

## Four ways to use it

### 1. Apify console, no code

1. Open [the Actor page](https://apify.com/bibian/seek-jobs-scraper) and click **Try for free** (a free Apify account is enough).
2. Fill in the input form (country, keyword or classification, location) and click **Start**.
3. When the run finishes, open the **Output** tab, check the table, then **Export** as CSV, Excel or JSON.
4. For a daily alert, open **Schedules**, create a daily schedule and, optionally, add an integration that sends new results to Slack, e-mail or Google Sheets.

### 2. Apify API with JavaScript

```bash
npm install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
node examples/run.js
```

The complete file is [`examples/run.js`](examples/run.js) (ES module, Node 18 or later).

### 3. Apify API with Python

```bash
pip install apify-client
export APIFY_TOKEN="your token from Apify console, Settings, Integrations"
python examples/run.py
```

The complete file is [`examples/run.py`](examples/run.py). Never put your token in the code: read it from the `APIFY_TOKEN` environment variable as above.

### 4. REST API, one HTTP call

```bash
curl -X POST "https://api.apify.com/v2/acts/bibian~seek-jobs-scraper/run-sync-get-dataset-items?token=<YOUR_APIFY_TOKEN>" \
  -H "content-type: application/json" \
  -d '{"country": "AU", "keyword": "software engineer", "maxItems": 50}'
```

The response is the JSON array of postings, with the same fields as above.

## Pricing

Pay per result, shown on the [Store page](https://apify.com/bibian/seek-jobs-scraper) (the Store page is the reference; prices there may have changed since this guide was written). Apify's free plan includes monthly credits, enough to try it on a batch of results.

## Good to know

- **SEEK needs a real browser.** SEEK blocks a plain HTTP request, a datacenter proxy, and even a Chrome-impersonating TLS fingerprint on a residential proxy — only a real stealth browser (Camoufox) behind a residential proxy gets through. This Actor does that for you; you still call it like any other API.
- **One page per search, by design.** SEEK's own `robots.txt` disallows every query-string URL for a generic crawler, except two narrow exceptions this Actor doesn't rely on, and disallows the `/job/` job-detail path outright. So this Actor only ever fetches SEEK's plain, path-based search pages — which caps a single `keyword`/`classification`/`location` search at one page, up to 32 postings. Leaving `keyword`, `classification` and `location` all empty uses two built-in default categories instead of one, so the default run alone reaches 50. To go further, run the Actor again with a different `keyword`, `classification` or `location`.
- **`description` is SEEK's own teaser, not the full ad.** The full job description lives on the `/job/<id>` detail page, which (see above) this Actor never fetches, out of respect for `robots.txt`.
- **`experienceLevel` and `skills` are not on the search card**, only on the (disallowed) detail page, so they stay empty rather than being guessed.
- **Salary is best-effort.** SEEK's own salary label is free text ("$84,500 per year", "$30 - $40 per hour", or sometimes no figure at all); it's parsed whenever the unit is clear and left `null` otherwise (a missing number beats a wrong one). The raw text is always kept in `salaryLabel`.
- **No personal data.** SEEK's search cards never name an individual recruiter or carry a direct phone number or e-mail; the teaser and bullet points are still defensively scrubbed of any stray e-mail address before being saved.
- This is an unofficial tool, not affiliated with SEEK. Check the site's terms and the data protection rules that apply to your use.

## FAQ

**Does it need a browser or a proxy on my side?**
No. The Actor runs its own stealth browser and residential proxy internally; you call it like any other HTTP API.

**How do I get only New Zealand jobs?**
Set `country` to `NZ`.

**How do I get only new postings every day?**
Schedule the Actor daily and tick **Only new results** (`onlyNew`); each run then returns, and charges, only what the previous run of the same search did not already deliver.

**Can I get the data in Excel or Google Sheets?**
Yes. Export the dataset as CSV, Excel or JSON from the Apify console, or connect the Apify Google Sheets integration.

**Why do I only get up to 32 results for one keyword?**
That is SEEK's own `robots.txt` limit on a generic crawler for a single search (see "Good to know" above), not a bug. Run the Actor again with a different keyword, classification or location to get more.

## More job scrapers by the same author

- [Asia Pacific Jobs Scraper (SEEK + MyCareersFuture, one schema)](https://apify.com/bibian/asia-pacific-jobs-scraper)
- [North America Jobs Scraper (6 boards)](https://apify.com/bibian/north-america-jobs-scraper)
- [Europe Jobs Scraper (12 boards, 7 countries)](https://apify.com/bibian/europe-jobs-scraper)

## Try it

**[Open seek-jobs-scraper on the Apify Store](https://apify.com/bibian/seek-jobs-scraper)**

The code in `examples/` is released under the MIT license (see [LICENSE](LICENSE)). The data belongs to its original publishers.
