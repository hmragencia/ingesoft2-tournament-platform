# v0 prompt used for the mockups

Tool: [v0 by Vercel](https://v0.app). Flow: start from a v0 template, attach the organization's reference image (`mockups/00-reference-dbs.jpg`) and send the prompt below.

```text
Use the attached image as the visual reference and adapt this template into the public website + installable PWA of "DBS Complejo Deportivo", a youth football (soccer) tournament organizer. Reuse the template's components where useful, but restyle everything to match the reference: dark navy header with the DBS logo, green primary buttons, the six coloured quick-access tiles, white rounded cards with soft shadows, and the dark footer.

CONTEXT (important for the data layer)
- This site is the PUBLIC face of an existing tournament-management platform (Next.js + Supabase/PostgreSQL) that already handles registration, fixtures, match scheduling, referees and results. This site does NOT manage the tournament: it only READS published data from public views (public_schedule, public_standings, public_top_scorers, public_best_defense, public_teams, public_clubs, public_venues) and adds its own features: fan accounts, team follows, news, sponsors, store and photo/video bookings.
- For this prototype use hard-coded mock data in /lib/mock-data.ts shaped like those views (typed with TypeScript) and read it only through /lib/data.ts, so it can be swapped for Supabase later. No backend and no real auth: fake the signed-in state.
- Never show personal data of players (most are minors): no ID numbers, birth dates, photos or contact data. A player appears only as name + team + goals.

GENERAL RULES
- All UI copy in English (production will be localized to Spanish later). Prices in Colombian pesos (COP).
- Mobile-first: every page must work at 360-390 px with a bottom navigation bar (Home, Schedule, Standings, My teams, More); desktop keeps the top navigation of the reference.
- Match status badges: "Scheduled", "To be scheduled" (no time or field yet), "Provisional" (result under review, yellow), "Final" (approved, green), "Postponed".
- Categories: U-8, U-10, U-12, U-14, U-16, U-18. Teams: Atlético DBS, Real Santander, CDP Elite, Talentos FC, Ciudadela FC, Bucaramanga City, Leones FC, DBS Academy (simple generated crests). Venue: DBS La Gloria (6 fields, cafeteria, parking, rest areas).
- Add a "Prototype screens" index at /screens that links every page below.

PAGES
1. / Home: recreate the reference. Hero "Where dreams begin" with CTAs "See my match" and "Sign in"; the six tiles (Schedule, Results, Standings, Clubs, Venues, News); Upcoming matches (day tabs + rows with time, category, field, crests and "Details"); Standings preview with category tabs; Latest news (3 cards); Our venues card; Categories strip; "Are you a player or family?" sign-in banner; sponsor logo strip; footer.
2. /schedule: matchday schedule and results. Tournament selector, category chips, group and matchday selectors. Match cards with time, field and teams; played matches show score and scorers; include one "Provisional" and one "To be scheduled" example. Dismissible "Install app" banner (dialog with iPhone steps).
3. /standings: group table (Pos, Team, P, W, D, L, GF, GA, GD, Pts) with a yellow dot on teams that have provisional results and a last row marked "Withdrawn". Tabs: Standings | Top scorers | Best defense.
4. /teams/[slug]: team profile with crest, club, category, group, current position, "Follow" button, upcoming matches and recent results, and a link to /clubs/[slug] (club page listing its teams by category).
5. /my-teams: signed-in fan home. One card per followed team with next match and last result, notification bell with a list, "Push notifications" toggle, manage follows.
6. /book-media: book a photo or video package for a scheduled match. Pick the match, choose a package (Photo pack COP 45,000 / Video highlights COP 80,000), order summary, "Pay securely" that simulates the payment-gateway redirect, then a "Payment approved" page.
7. /admin/public-site: organizer back-office (desktop) with a left sidebar: Public site, News, Gallery, Widgets, Sponsors, Store, Orders, Bookings, Pre-registrations. Branding form (logo, primary and secondary colors, custom domain) with a live phone preview; toggles for News, Gallery, Store, Bookings and Pre-registration; checklist of published tournaments.
8. /sponsor: sponsor dashboard (desktop). Date range, KPI cards (Impressions, Clicks, CTR), line chart over time, table by placement (Website banner, App banner, Matchday graphic), "Download report" button.
```
