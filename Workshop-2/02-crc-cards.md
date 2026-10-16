# 2. CRC cards

One card per main class of the Public Module. Classes marked **read-only** come from the tournament-management platform through the `public_*` views; the Public Module never changes them. Classes marked **owned** are new in this module.

---

### PublicSite *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the organization's public brand: logo, primary and secondary colors, custom domain. | Organization |
| Decide which tournaments are published and which sections are on (news, gallery, store, bookings, pre-registration). | Tournament |
| Resolve the organization from the request host. | Organization |
| Provide the PWA manifest (name, icon, colors). | — |

### Tournament *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know its name, dates, status and whether it is public. | Organization |
| List its categories, groups and matchdays. | Category, Match |
| Refuse to expose any data when it is not public. | PublicSite |

### Team *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know its name, crest, club, category and group. | Club, Category |
| Give its upcoming matches and recent results. | Match |
| Give its current position in the group. | Standing |
| Report whether it has withdrawn. | Standing |

### Club *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know its name, slug and logo. | — |
| List all its teams in a tournament, grouped by category. | Team, Category |

### Match *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know home and away teams, date, time, field and matchday. | Team, Venue/Field |
| Expose its public status: to be scheduled, scheduled, provisional, final, postponed, walkover. | — |
| Give the score and the scorers (name and team only). | Goal |
| Tell whether it can still be booked for photo/video. | MediaBooking |

### Standing *(read-only, computed view)*

| Responsibilities | Collaborators |
|---|---|
| Give P, W, D, L, GF, GA, GD and points per team and group. | Team, Match |
| Order the table with the tie-break rules and send withdrawn teams to the bottom. | Team |
| Flag rows that include provisional results. | Match |

### FanAccount *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Register and authenticate a fan (e-mail or Google). | Auth provider |
| Follow and unfollow teams. | TeamFollow, Team |
| Keep push subscriptions and notification preferences. | PushSubscription |
| List the fan's own orders and bookings. | Order, MediaBooking |

### TeamFollow *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Link one fan with one team (no duplicates). | FanAccount, Team |
| Tell who must be notified when a team's schedule or result is published. | Notification |

### Notification *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Create one in-app notification per follower when a schedule is published or a result is approved. | TeamFollow, Match |
| Send it by Web Push to every active subscription and mark it as sent. | PushSubscription, Push service |
| Deactivate subscriptions that the push service rejects (410 Gone). | PushSubscription |
| Mark as read. | FanAccount |

### NewsPost *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold title, body, cover image, tag and status (draft or published). | Organization |
| Publish and unpublish; list newest first. | PublicSite |
| Optionally attach a matchday photo gallery. | GalleryPhoto |

### SponsorPlacement *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the creative, the target link, the slot (website banner, app banner, matchday graphic) and the start and end dates. | Sponsor |
| Tell whether it is active today. | — |
| Record anonymous impressions and clicks. | PlacementEvent |
| Summarize metrics by period for the sponsor's report. | Sponsor |

### Product *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold name, description, photo, price and active flag. | Organization |
| Manage its variants (size) and their stock. | ProductVariant |
| Refuse to sell more than the available stock. | OrderItem |

### Order *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Build the cart from items and compute the total. | OrderItem, ProductVariant |
| Start the checkout with the payment gateway. | Payment |
| Change status: pending → paid → ready for pickup → delivered (or cancelled). | Payment, Organizer |

### Payment *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Keep the gateway reference, amount and status of one charge. | Payment gateway |
| Apply the gateway webhook only once (idempotent by gateway reference). | Order, MediaBooking |
| Confirm the order or booking only when the payment is approved. | Order, MediaBooking |

### MediaBooking *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Book a photo or video package for a scheduled match. | Match, MediaPackage, FanAccount |
| Get paid through the gateway. | Payment |
| Receive the delivery link from the assigned photographer and notify the customer. | PhotographerAssignment, Notification |

### PreRegistration *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the club, contact person, categories of interest and target tournament. | Tournament |
| Be approved or rejected by the organizer, with a reason. | Organizer |
| On approval, hand the club over to the regular registration flow of the management platform. | Management platform |
