# Problem Statement

## 1. Title
SoundSphere — AI-Powered Music Streaming & Recommendation Platform

## 2. Domain
Entertainment / Media Streaming

## 3. Who is the user? (2-3 user types, with roles)
- **Listener (User)**: Browses songs, creates and manages playlists, plays tracks, views listening history, and receives personalized recommendations.
- **Admin**: Manages the song catalog (add/edit/remove songs and metadata), manages user accounts, and views platform-wide analytics (top songs, active users).

## 4. What problem are we solving? (3-5 sentences, real-life example)
Music listeners are overwhelmed by large catalogs and struggle to discover new songs that match their taste, often relying on generic top-charts instead of personalized suggestions. Existing simple playlist apps have no intelligence — they just store what a user manually adds, with no way to surface songs the user would actually like. For example, a user who mostly listens to high-energy dance tracks has no easy way to discover similar new songs without manually searching. SoundSphere solves this by combining a proper full-stack music platform (browse, play, playlist management) with a content-based recommendation engine that learns from song audio features to suggest music the user is genuinely likely to enjoy.

## 5. Proposed Solution (what the application will do, feature-wise)
- User authentication (signup/login) with JWT, role-based (Admin/User)
- Browse and search song catalog with metadata (title, artist, genre, audio features)
- Create, edit, and manage playlists (add/remove songs)
- Track listening history per user
- Admin dashboard to manage song catalog and view platform analytics
- Email notification on signup (3rd-party integration: transactional email service, e.g. SendGrid/SMTP)
- (Enhancement phase, Day 41–60): AI-based recommendation engine — content-based similarity (KNN/cosine similarity on audio features) plus mood-based clustering (K-Means), with an explainability layer and cold-start handling for new users

## 6. Core Entities / Database Tables (list all, minimum 5)
1. **Users** (id, name, email, password_hash, role, created_at)
2. **Songs** (id, title, artist, genre, duration, danceability, energy, valence, tempo, acousticness, cover_url)
3. **Playlists** (id, user_id [FK], name, created_at)
4. **PlaylistSongs** (id, playlist_id [FK], song_id [FK], added_at) — junction table (Many-to-Many between Playlists and Songs)
5. **ListeningHistory** (id, user_id [FK], song_id [FK], played_at)
6. **Recommendations** (id, user_id [FK], song_id [FK], score, reason, generated_at) — added in enhancement phase

## 7. User Roles & Permissions (minimum 2 distinct roles)
- **Admin**: Full CRUD on Songs table; view/manage all Users; view platform analytics; cannot access other users' private playlists.
- **User**: Read-only on Songs catalog; full CRUD on own Playlists; view own ListeningHistory and Recommendations; cannot access admin routes.

## 8. Success Criteria
- A user should be able to sign up, log in, and start playing a song in under 1 minute.
- A user should be able to create a playlist and add a song to it in under 30 seconds.
- (Enhancement) Given a song, the system should return at least 5 relevant recommendations in under 2 seconds.

## 9. Out of Scope (clearly list what you will NOT build, to avoid over-commitment)
- Actual licensed audio file streaming/hosting (will use preview clips or placeholder audio URLs, not full copyrighted tracks)
- Real payment/subscription billing (no real payment gateway integration beyond sandbox, if attempted)
- Social features like following other users, comments, or public profile pages
- Mobile app (web-only, responsive design instead)
- Real-time collaborative playlists (multiple users editing same playlist simultaneously)

## 10. Chosen Track: Python (FastAPI)