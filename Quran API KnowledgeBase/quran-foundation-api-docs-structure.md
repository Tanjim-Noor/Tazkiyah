# Quran Foundation API Documentation Site Structure

## Overview

The Quran Foundation API Documentation Portal at `https://api-docs.quran.foundation/` provides comprehensive API documentation for building Quran-related applications. The site is built using Docusaurus and follows a well-organized structure.

---

## Main Navigation Categories

The site has **5 main API documentation sections** plus supporting resources:

### 1. Content APIs (Latest: v4)
**Category URL:** `https://api-docs.quran.foundation/docs/category/content-apis`

Provides programmatic access to Quran core content. Uses OAuth2 Client Credentials flow with `content` scope.

### 2. Search APIs (Latest: v1.0)
**Category URL:** `https://api-docs.quran.foundation/docs/category/search-apis`

Search functionality for Quran content. Requires `search` scope.

### 3. User-related APIs (Latest: v1.0.0)
**Category URL:** `https://api-docs.quran.foundation/docs/category/user-related-apis`

User-specific data like bookmarks, notes, goals, streaks. Uses OAuth2 Authorization Code flow with PKCE.

### 4. OAuth2 APIs (Latest: v1.0.0)
**Category URL:** `https://api-docs.quran.foundation/docs/category/oauth2_apis`

Authentication and authorization endpoints.

### 5. JavaScript SDK
**URL:** `https://api-docs.quran.foundation/docs/sdk/javascript`

Official `@quranjs/api` SDK for Node.js and browsers.

---

## Complete URL Hierarchy

### Base URL Pattern
```
https://api-docs.quran.foundation/docs/{section}/{page}
```

### API Base URLs (for actual API calls)
- **Pre-Production:** `https://apis-prelive.quran.foundation`
- **Production:** `https://apis.quran.foundation`

### OAuth2 Base URLs
- **Pre-Production:** `https://prelive-oauth2.quran.foundation`
- **Production:** `https://oauth2.quran.foundation`

---

## Content APIs - Full Endpoint Documentation

**Introduction:** `/docs/content_apis_versioned/content-apis`

### Audio (15 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/chapter-reciter-audio-file` | `GET /chapter_recitations/:id/:chapter_number` | Get chapter's audio file of a reciter |
| `/docs/content_apis_versioned/chapter-reciter-audio-files` | `GET /chapter_recitations/:id` | List of all chapter audio files of a reciter |
| `/docs/content_apis_versioned/list-recitation` | `GET /recitations` | List recitations |
| `/docs/content_apis_versioned/list-chapter-recitation` | `GET /recitations/:recitation_id/by_chapter/:chapter_number` | Get Ayah recitations for specific Surah |
| `/docs/content_apis_versioned/list-juz-recitation` | `GET /recitations/:recitation_id/by_juz/:juz_number` | Get Ayah recitations for specific Juz |
| `/docs/content_apis_versioned/list-page-recitation` | `GET /recitations/:recitation_id/by_page/:page_number` | Get Ayah recitations for specific Page |
| `/docs/content_apis_versioned/list-hizb-recitation` | `GET /recitations/:recitation_id/by_hizb/:hizb_number` | Get Ayah recitations for specific Hizb |
| `/docs/content_apis_versioned/list-rub-el-hizb-recitation` | `GET /recitations/:recitation_id/by_rub_el_hizb/:rub_el_hizb_number` | Get Ayah recitations for specific Rub El Hizb |
| `/docs/content_apis_versioned/list-ayah-recitation` | `GET /recitations/:recitation_id/by_ayah/:ayah_key` | Get Ayah recitation for specific Ayah |
| `/docs/content_apis_versioned/list-manzil-recitation` | `GET /recitations/:recitation_id/by_manzil/:manzil_number` | Get Ayah recitations for specific Manzil |
| `/docs/content_apis_versioned/list-ruku-recitation` | `GET /recitations/:recitation_id/by_ruku/:ruku_number` | Get Ayah recitations for specific Ruku |
| + 4 more audio endpoints | | |

### Chapters (3 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-chapters` | `GET /chapters` | List Chapters |
| `/docs/content_apis_versioned/get-chapter` | `GET /chapters/:id` | Get Chapter |
| `/docs/content_apis_versioned/get-chapter-info` | `GET /chapters/:id/info` | Get Chapter Info |

### Verses (10 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/verses-by-chapter-number` | `GET /verses/by_chapter/:chapter_number` | By Chapter |
| `/docs/content_apis_versioned/verses-by-page-number` | `GET /verses/by_page/:page_number` | By Page |
| `/docs/content_apis_versioned/verses-by-juz-number` | `GET /verses/by_juz/:juz_number` | By Juz |
| `/docs/content_apis_versioned/verses-by-hizb-number` | `GET /verses/by_hizb/:hizb_number` | By Hizb |
| `/docs/content_apis_versioned/verses-by-rub-el-hizb-number` | `GET /verses/by_rub_el_hizb/:rub_el_hizb_number` | By Rub El Hizb |
| `/docs/content_apis_versioned/verses-by-manzil-number` | `GET /verses/by_manzil/:manzil_number` | By Manzil |
| `/docs/content_apis_versioned/verses-by-ruku-number` | `GET /verses/by_ruku/:ruku_number` | By Ruku |
| `/docs/content_apis_versioned/verses-by-verse-key` | `GET /verses/by_key/:verse_key` | By Verse Key |
| `/docs/content_apis_versioned/random-verse` | `GET /verses/random` | Get random ayah |
| + 1 more verse endpoint | | |

### Juz (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-juzs` | `GET /juzs` | List Juzs |
| `/docs/content_apis_versioned/get-juz` | `GET /juzs/:juz_number` | Get Juz |

### Quran (11 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/quran-verses-by-script` | `GET /quran/verses/:script` | Get Quran verses in a specific script |
| `/docs/content_apis_versioned/quran-verses-indopak` | `GET /quran/verses/indopak` | Get Indopak Script of ayah |
| `/docs/content_apis_versioned/quran-verses-uthmani` | `GET /quran/verses/uthmani` | Get Uthmani Script of ayah |
| `/docs/content_apis_versioned/quran-verses-uthmani-simple` | `GET /quran/verses/uthmani_simple` | Get Uthmani Simple script of ayah |
| `/docs/content_apis_versioned/quran-verses-uthmani-tajweed` | `GET /quran/verses/uthmani_tajweed` | Get Uthmani Tajweed script of ayah |
| `/docs/content_apis_versioned/quran-verses-imlaei` | `GET /quran/verses/imlaei` | Get Imlaei Script of ayah |
| `/docs/content_apis_versioned/quran-verses-imlaei-simple` | `GET /quran/verses/imlaei_simple` | Get Imlaei Simple script of ayah |
| `/docs/content_apis_versioned/quran-verses-code-v-1` | `GET /quran/verses/code_v1` | Get V1 Glyph codes of ayah |
| `/docs/content_apis_versioned/quran-verses-code-v-2` | `GET /quran/verses/code_v2` | Get V2 Glyph codes of ayah |
| + 2 more quran endpoints | | |

### Resources (9 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/recitation-info` | `GET /resources/recitations/:recitation_id/info` | Recitation Info |
| `/docs/content_apis_versioned/translation-info` | `GET /resources/translations/:translation_id/info` | Translation Info |
| `/docs/content_apis_versioned/tafsir-info` | `GET /resources/tafsirs/:tafsir_id/info` | Tafsir Info |
| `/docs/content_apis_versioned/recitations` | `GET /resources/recitations` | List Recitations |
| `/docs/content_apis_versioned/translations` | `GET /resources/translations` | List Translations |
| `/docs/content_apis_versioned/tafsirs` | `GET /resources/tafsirs` | List Tafsirs |
| `/docs/content_apis_versioned/languages` | `GET /resources/languages` | List Languages |
| `/docs/content_apis_versioned/chapter-reciters` | `GET /resources/chapter_reciters` | List Chapter Reciters |
| `/docs/content_apis_versioned/verse-media` | `GET /resources/verse_media` | Verse Media |

### Translations (8 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-surah-translations` | `GET /translations/:resource_id/by_chapter/:chapter_number` | Get translations for specific Surah |
| `/docs/content_apis_versioned/list-page-translations` | `GET /translations/:resource_id/by_page/:page_number` | Get translations for specific page |
| `/docs/content_apis_versioned/list-juz-translations` | `GET /translations/:resource_id/by_juz/:juz_number` | Get translations for specific Juz |
| `/docs/content_apis_versioned/list-hizb-translations` | `GET /translations/:resource_id/by_hizb/:hizb_number` | Get translations for specific Hizb |
| `/docs/content_apis_versioned/list-rub-el-hizb-translations` | `GET /translations/:resource_id/by_rub_el_hizb/:rub_el_hizb_number` | Get translations for specific Rub el Hizb |
| `/docs/content_apis_versioned/list-manzil-translations` | `GET /translations/:resource_id/by_manzil/:manzil_number` | Get translations for specific Manzil |
| `/docs/content_apis_versioned/list-ruku-translations` | `GET /translations/:resource_id/by_ruku/:ruku_number` | Get translations for specific Ruku |
| `/docs/content_apis_versioned/list-ayah-translations` | `GET /translations/:resource_id/by_ayah/:ayah_key` | Get translations for specific Ayah |

### Tafsirs (8 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-surah-tafsirs` | `GET /tafsirs/:resource_id/by_chapter/:chapter_number` | Get tafsirs for specific Surah |
| `/docs/content_apis_versioned/list-page-tafsirs` | `GET /tafsirs/:resource_id/by_page/:page_number` | Get tafsirs for specific page |
| `/docs/content_apis_versioned/list-juz-tafsirs` | `GET /tafsirs/:resource_id/by_juz/:juz_number` | Get tafsirs for specific Juz |
| `/docs/content_apis_versioned/list-hizb-tafsirs` | `GET /tafsirs/:resource_id/by_hizb/:hizb_number` | Get tafsirs for specific Hizb |
| `/docs/content_apis_versioned/list-rub-el-hizb-tafsirs` | `GET /tafsirs/:resource_id/by_rub_el_hizb/:rub_el_hizb_number` | Get tafsirs for specific Rub el Hizb |
| `/docs/content_apis_versioned/list-manzil-tafsirs` | `GET /tafsirs/:resource_id/by_manzil/:manzil_number` | Get tafsirs for specific Manzil |
| `/docs/content_apis_versioned/list-ruku-tafsirs` | `GET /tafsirs/:resource_id/by_ruku/:ruku_number` | Get tafsirs for specific Ruku |
| `/docs/content_apis_versioned/list-ayah-tafsirs` | `GET /tafsirs/:resource_id/by_ayah/:ayah_key` | Get tafsirs for specific Ayah |

### Hizb (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-hizbs` | `GET /hizbs` | List Hizbs |
| `/docs/content_apis_versioned/get-hizb` | `GET /hizbs/:hizb_number` | Get Hizb |

### Rub El Hizb (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-rub-el-hizbs` | `GET /rub_el_hizbs` | List Rubʿ al-Ḥizb |
| `/docs/content_apis_versioned/get-rub-el-hizb` | `GET /rub_el_hizbs/:rub_el_hizb_number` | Get Rubʿ al-Ḥizb |

### Ruku (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-rukus` | `GET /rukus` | List Rukus |
| `/docs/content_apis_versioned/get-ruku` | `GET /rukus/:ruku_number` | Get Ruku |

### Manzil (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/list-manzils` | `GET /manzils` | List Manzils |
| `/docs/content_apis_versioned/get-manzil` | `GET /manzils/:manzil_number` | Get Manzil |

### Foot Note (1 endpoint)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/content_apis_versioned/get-foot-note` | `GET /foot_notes/:id` | Get Foot Note |

---

## Search APIs - Full Endpoint Documentation

**Introduction:** `/docs/search_apis_versioned/quran-foundation-search-api`

### Search (1 endpoint)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/search_apis_versioned/search-controller-search` | `GET /search` | Search Quran content |

---

## User-related APIs - Full Endpoint Documentation

**Introduction:** `/docs/user_related_apis_versioned/user-related-apis`

### Collections (8 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/add-collection` | Add collection |
| + 7 more collection endpoints | |

### Bookmarks (6 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/add-user-bookmark` | Add user bookmark |
| + 5 more bookmark endpoints | |

### Preferences (3 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/add-or-update-preference` | Add or update preference |
| + 2 more preference endpoints | |

### Reading Sessions (2 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/add-or-update-user-reading-session` | Add or update user reading session |
| + 1 more reading session endpoint | |

### Goals (5 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/get-todays-goal-plan` | Get today's goal plan |
| + 4 more goal endpoints | |

### Streaks (2 endpoints)
| Page URL | Description |
|----------|-------------|
| `/docs/user_related_apis_versioned/get-streaks` | Get streaks |
| + 1 more streak endpoint | |

### Activity Days (3 endpoints)
| Page URL | Description |
|----------|-------------|
| Activity day endpoints | |

---

## OAuth2 APIs - Full Endpoint Documentation

**Introduction:** `/docs/oauth2_apis_versioned/oauth-2-apis`

### OAuth2 (3 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/oauth2_apis_versioned/oauth-2-token-exchange` | `POST /oauth2/token` | The OAuth 2.0 Token Endpoint |
| `/docs/oauth2_apis_versioned/introspect-o-auth-2-token` | `POST /oauth2/introspect` | Introspect OAuth2 Access and Refresh Tokens |
| `/docs/oauth2_apis_versioned/o-auth-2-authorize` | `GET /oauth2/auth` | OAuth 2.0 Authorize Endpoint |

### OIDC (2 endpoints)
| Page URL | Endpoint | Description |
|----------|----------|-------------|
| `/docs/oauth2_apis_versioned/get-oidc-user-info` | `GET /userinfo` | OpenID Connect Userinfo |
| `/docs/oauth2_apis_versioned/revoke-oidc-session` | `GET /oauth2/sessions/logout` | OpenID Connect Logout |

---

## JavaScript SDK Documentation

**Base URL:** `/docs/sdk`

### SDK Pages
| Page URL | Description |
|----------|-------------|
| `/docs/sdk` | Official SDKs overview |
| `/docs/sdk/javascript` | JavaScript SDK main page |
| `/docs/sdk/javascript/chapters` | Chapters API |
| `/docs/sdk/javascript/verses` | Verses API |
| `/docs/sdk/javascript/audio` | Audio API |
| `/docs/sdk/javascript/resources` | Resources API |
| `/docs/sdk/javascript/search` | Search API |
| `/docs/sdk/javascript/migration` | Migration Guide |

---

## Supporting Documentation Pages

### Getting Started
| Page URL | Description |
|----------|-------------|
| `/docs/quickstart` | 🚀 Quick Start Guide |
| `/docs/sdk` | Official SDKs |
| `/docs/updates` | 📢 Recent API Updates |

### Tutorials
| Page URL | Description |
|----------|-------------|
| `/docs/tutorials/oidc/getting-started-with-oauth2` | Using OAuth 2.0 to Access Quran.Foundation APIs |
| `/docs/tutorials/oidc/user-apis-quickstart` | User APIs Quick Start |
| `/docs/tutorials/oidc/openid-connect` | OpenID Connect |
| `/docs/tutorials/oidc/example-integration` | Web Integration Example |
| `/docs/category/mobile-apps` | Mobile Apps tutorials |

### Reference
| Page URL | Description |
|----------|-------------|
| `/docs/api/field-reference` | Field Reference (verse, word, translation, tafsir fields) |
| `/docs/user_related_apis_versioned/scopes` | OAuth2 Scopes |

### Legal
| Page URL | Description |
|----------|-------------|
| `/legal/developer-terms` | Developer Terms of Service |
| `/legal/developer-privacy` | Developer Privacy Policy Requirements |

### Other
| Page URL | Description |
|----------|-------------|
| `/request-access` | Request API Access |

---

## URL Patterns

### Documentation Structure
```
/docs/category/{api-category}          # Category landing pages
/docs/{api}_versioned/{endpoint-name}  # Versioned API endpoint docs
/docs/sdk/{language}/{feature}         # SDK documentation
/docs/tutorials/{topic}/{subtopic}     # Tutorial pages
/docs/api/{reference-type}             # API reference pages
/legal/{document}                      # Legal documents
```

### API Categories Pattern
- `content_apis_versioned` - Content APIs (v4)
- `search_apis_versioned` - Search APIs (v1.0)
- `user_related_apis_versioned` - User-related APIs (v1.0.0)
- `oauth2_apis_versioned` - OAuth2 APIs (v1.0.0)

---

## OAuth2 Scopes Reference

### Content Scopes
- `content` - Read non user-related content

### Search Scopes
- `search` - Search indexed content

### User Data Scopes
- `bookmark`, `bookmark.read`, `bookmark.create`, `bookmark.delete`
- `collection`, `collection.read`, `collection.create`, `collection.update`, `collection.delete`
- `reading_session`, `reading_session.read`, `reading_session.create`, `reading_session.update`
- `preference`, `preference.read`, `preference.update`
- `activity_day`, `activity_day.read`, `activity_day.create`, `activity_day.estimate`, `activity_day.update`, `activity_day.delete`
- `goal`, `goal.read`, `goal.estimate`, `goal.create`, `goal.update`, `goal.delete`
- `streak`, `streak.read`, `streak.update`
- `user`, `user.profile.read`, `user.profile.update`, `user.rooms.read`, `user.search`, `user.follow`, `user.followers.read`, `user.following.read`
- `post`, `post.read`, `post.create`, `post.update`, `post.delete`, `post.save`, `post.like`, `post.report`, `post.log`, `post.export`
- `comment`, `comment.read`, `comment.create`, `comment.delete`, `comment.like`
- `room`, `room.read`, `room.create`, `room.update`, `room.admin`, `room.search`, `room.invite`, `room.join`, `room.leave`, `room.follow`, `room.unfollow`, `room.members.read`, `room.members.remove`, `room.posts.read`, `room.posts.update`
- `tag`, `tag.read`
- `note`, `note.read`, `note.create`, `note.update`, `note.delete`, `note.publish`

---

## API Endpoint Count Summary

| Category | Subcategory | Count |
|----------|-------------|-------|
| **Content APIs** | Audio | 15 |
| | Chapters | 3 |
| | Verses | 10 |
| | Juz | 2 |
| | Quran | 11 |
| | Resources | 9 |
| | Translations | 8 |
| | Tafsirs | 8 |
| | Hizb | 2 |
| | Rub El Hizb | 2 |
| | Ruku | 2 |
| | Manzil | 2 |
| | Foot Note | 1 |
| **Search APIs** | Search | 1 |
| **User APIs** | Collections | 8 |
| | Bookmarks | 6 |
| | Preferences | 3 |
| | Reading Sessions | 2 |
| | Goals | 5 |
| | Streaks | 2 |
| | Activity Days | 3 |
| **OAuth2 APIs** | OAuth2 | 3 |
| | OIDC | 2 |

**Total Documented Endpoints: ~100+**

---

## Authentication Requirements

### Content APIs
- OAuth2 Client Credentials flow
- Scope: `content`
- Headers: `x-auth-token`, `x-client-id`

### Search APIs
- OAuth2 Client Credentials flow
- Scope: `search`
- Headers: `x-auth-token`, `x-client-id`

### User APIs
- OAuth2 Authorization Code flow with PKCE
- Various user scopes
- Headers: `x-auth-token`, `x-client-id`

---

## External Resources

- **GitHub:** https://github.com/quran
- **NPM SDK:** https://www.npmjs.com/package/@quranjs/api
- **Discord:** https://discord.gg/SpEeJ5bWEQ
- **Donate:** https://donate.quran.foundation/
- **Contact:** developers@quran.com
