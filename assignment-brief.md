# Assignment Brief (condensed)

Keep `assignment.md` as the official wording. This is the short version of what to build and submit.

## 1. What you are building

A web app for a UK energy utility team that buys electricity in the **day-ahead market**. They must decide, one day before delivery, how much extra power to procure beyond weather-dependent wind generation.

The app must do two things, for **national wind generation only** (no other fuels, no other data):

1. **Show the latest wind generation forecasts** available at decision time (i.e. the most recently published forecast available before the day-ahead gate, not a later revision).
2. **Quantify forecast accuracy** (actual vs forecast error) so the team can factor error into purchase decisions.

## 2. Data (Elexon, wind only)

- **Actuals** — `FUELHH` dataset: `https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream`
  - Only rows where `fuelType` = `WIND`.
  - `startTime` = target half-hour slot; `generation` = actual MW.
- **Forecasts** — `WINDFOR` dataset: `https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream`
  - `startTime` = target slot, `publishTime` = when the forecast was issued, `generation` = forecast MW.
  - Several forecasts exist per slot (different `publishTime`). Pick the latest one *published before* the decision deadline, otherwise the "accuracy" is fake.
- **Scope:** only data needed for purchase decisions made in **January 2026** (forecasts published in Jan 2026; some target slots fall on 1 Feb).

## 3. Tech constraints

- Frontend: **React**. Backend: **Python** (e.g. FastAPI).
- **Docker** (Dockerfile + docker-compose for local run).
- Deploy the sample app to **Vercel or Heroku** and link it.
- AI tools are allowed, but must be stated explicitly in the README.
- Timebox: **max 16 hours**.

## 4. Deliverables (all three are required)

| # | Deliverable | Key requirements |
|---|---|---|
| 1 | **Unlisted YouTube video, ≤ 10 min** | Part 1 (≤ 5 min): pitch the pilot to the client, impress them. Part 2 (≤ 5 min): technical walkthrough for a tech lead — architecture, design, analysis, codebase, key practices, knowledge transfer. **Evaluation starts here — do not submit without it.** |
| 2 | **Public GitHub repo, anonymous name** (e.g. random string like `kjhwr`) | README must contain: what every file/directory is, how to start the app (Docker), deployed app link. |
| 3 | **Submit form** | `https://forms.cloud.microsoft/r/FTX6K2bbnU` with all links. |

## 5. Submission checklist

- [ ] Forecast data chosen by `publishTime`, not "latest available now"
- [ ] Error metrics computed on the same half-hourly granularity and shown with the forecasts
- [ ] Dockerised app runs from a clean checkout, and deployed link works
- [ ] README complete, includes AI-tool disclosure
- [ ] Video recorded (≤ 10 min) and set to unlisted
- [ ] Repo is public under a non-identifying name
- [ ] Every submitted URL opened in **incognito** to confirm access works
- [ ] Form submitted before the link is shared anywhere else

## 6. What the client actually wants to see

- The forecast they would have used at decision time, with its publish time and how stale it is.
- A measured error (MAE / RMSE / bias, plus error by forecast horizon and by slot).
- A clear "how much to procure" framing that uses forecast ± quantified error, not just a pretty chart.
