# 2. CRC cards

One card per main class of the Public Module. Classes marked **read-only** come from the tournament-management platform through the `public_*` views; the Public Module never changes them. Classes marked **owned** are new in this module.

---

### PublicSite *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the public-site settings of one organization: domain and brand overrides (logo, colors); when an override is empty, use the brand the organization already has in the management platform (BR-15). | Organization |
| Decide which tournaments are published and which sections are on (news, gallery, store, bookings, pre-registration). | Tournament |
| Resolve the organization from the request host. | Organization |
| Register its custom domain with the hosting platform and show the DNS records the organization must create. | Hosting platform (Cloudflare for SaaS) |
| Provide the organization's PWA manifest and icons (name, icon, colors). | — |

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
| Know home and away teams, date, time, field and matchday. | Team, Field, Matchday |
| Expose its public status: to be scheduled, scheduled, provisional, final, postponed, walkover. | — |
| Give the score and the scorers (name and team only). | Goal |
| Tell whether it can still be booked for photo/video: scheduled, not played and before the cut-off. | MediaBooking, MediaPackage |

### Matchday *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know its number, name and start and end dates. | Tournament, Category |
| List the matches played in it. | Match |
| Be the unit on which the capacity of a photo or video package is set. | MediaAvailability |

### Venue and Field *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know the venue's name and address, and the fields it has. | Tournament |
| Say where a match is played. They are never booked (BR-17). | Match |

### Document *(read-only)*

| Responsibilities | Collaborators |
|---|---|
| Know its title, type, publication date and file. | Tournament |
| Appear only when it is marked as public. | PublicSite |

### Standing *(read-only, computed view)*

| Responsibilities | Collaborators |
|---|---|
| Give P, W, D, L, GF, GA, GD and points per team and group. | Team, Match |
| Order the table with the tie-break rules and send withdrawn teams to the bottom. | Team |
| Flag rows that include provisional results. | Match |

### FanAccount *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Register and authenticate a fan (e-mail or Google), recording that the holder is an adult (BR-23). | Auth provider |
| Exist once per organization: the same person can have accounts in several organizations, and each one only sees its own data (BR-25). | Organization |
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

### Sponsor *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the allied brand's name, logo and contact, within one organization. | Organization |
| Link the brand to the account of its representative. | SponsorAccount |
| Give the metrics of its own placements. | SponsorPlacement |

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
| Hold the name, description, photo, price and active flag of a store item (merchandise such as a jersey). | Organization |
| Manage its variants. | ProductVariant |

### ProductVariant *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the size and stock of a store item (for example, a jersey in size M). It does not apply to photo or video packages. | Product |
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
| Keep the gateway reference, amount and status of one charge, tied to exactly one order or one booking. | Payment gateway, Order, MediaBooking |
| Apply the gateway webhook only once (idempotent by gateway reference). | Order, MediaBooking |
| Confirm the order or booking only when the payment is approved. | Order, MediaBooking |
| Charge with the organization's own merchant account and verify its webhook with that account's keys (BR-24). | PaymentAccount |

### PaymentAccount *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the organization's merchant account: provider, merchant id and public key; the secret key only as a reference to an encrypted vault. | Organization |
| Tell whether the account is active and whether it is in test or live mode. | — |
| Give the gateway adapter the keys to create checkouts and verify webhooks. | PaymentGateway |

### MediaPackage *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold a plan the organization offers: name, type (photo or video), price, booking cut-off and active flag. | Organization |
| Say on which matchdays it is offered and with what capacity. | MediaAvailability |

### MediaAvailability *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the capacity of one package on one matchday. | MediaPackage, Matchday |
| Tell how many slots are left. | MediaBooking |
| Refuse a booking when no slots are left. | MediaBooking |

### MediaBooking *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Book a photo or video package for a scheduled match, as an advance purchase. It does not book a field or a venue. | Match, MediaPackage, FanAccount |
| Store the price paid and take a slot of the matchday, releasing it if the booking expires unpaid. | MediaPackage, MediaAvailability |
| Get paid through the gateway. | Payment |
| Receive the delivery link from the assigned photographer and notify the customer. | PhotographerAssignment, Notification |

### PreRegistration *(owned)*

| Responsibilities | Collaborators |
|---|---|
| Hold the club, contact person, categories of interest and target tournament. | Tournament |
| Be approved or rejected by the organizer, with a reason. | OrganizerAccount |
| On approval, hand the club over to the regular registration flow of the management platform. | Management platform |
